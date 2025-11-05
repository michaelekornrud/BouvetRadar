"""Service classes for SSB statistical classifications (NUTS and STYRK)."""

import io
from enum import IntEnum

import pandas as pd

from src.clients.ssb_client import SSBClient
from utils import get_logger
from exceptions import DataProcessingError, ParsingError

logger = get_logger(__name__)

class SSBLevel(IntEnum):
    """SSB hierarchy levels for both NUTS and STYRK classifications."""
    LEVEL_1 = 1
    LEVEL_2 = 2
    LEVEL_3 = 3
    LEVEL_4 = 4


class SSBService:
    """Base service class for SSB classification data operations."""

    def __init__(self, version: int):
        """Initialize service and load classification data.
        
        Args:
            version: SSB classification version identifier
            
        Raises:
            DataProcessingError: If data loading or processing fails
            ParsingError: If CSV data is malformed
        """
        self._version = version
        self._client = SSBClient()
        self._df: pd.DataFrame
        self._codes_dict: dict[str, str]
        self._load_data()

    def _load_data(self) -> None:
        """Load and process classification data from SSB API.
        
        Raises:
            DataProcessingError: If required columns are missing
            ParsingError: If CSV parsing fails
        """
        logger.info(
            "Loading SSB classification data from API",
            extra={"version": self._version}
        )

        # Fetch data via client
        response = self._client.get_classification_version(self._version)
        
        try:
            # Parse CSV
            csv_data = io.StringIO(response.text)
            self._df = pd.read_csv(csv_data, sep=";", encoding="utf-8")
            
        except (ValueError, pd.errors.ParserError) as e:
            logger.error(
                "Failed to parse SSB CSV data",
                extra={
                    "version": self._version,
                    "error": str(e)
                },
                exc_info=True
            )
            raise ParsingError(f"Failed to parse CSV data: {e}") from e
        
        # Validate required columns
        required_columns = {'code', 'parentCode', 'level', 'name'}
        missing_columns = required_columns - set(self._df.columns)
        
        if missing_columns:
            logger.error(
                "SSB CSV missing required columns",
                extra={
                    "version": self._version,
                    "missing_columns": list(missing_columns),
                    "found_columns": list(self._df.columns)
                }
            )
            raise DataProcessingError(
                f"CSV missing required columns: {', '.join(missing_columns)}"
            )
        
        # Keep only needed columns and create lookup dictionary
        self._df = self._df[list(required_columns)]
        self._codes_dict = dict(zip(self._df['code'], self._df['name']))

        logger.info(
            "SSB classification data loaded successfully",
            extra={
                "version": self._version,
                "total_codes": len(self._codes_dict),
                "columns": list(self._df.columns)
            }
        )

    def get_description(self, code: str) -> str | None:
        """Get description for a classification code.
        
        Args:
            code: Classification code
            
        Returns:
            Description or None if code not found
        """
        return self._codes_dict.get(code)

    def get_code_by_name(self, name: str, max_level: int | None = None) -> str | None:
        """Get code by name (case-insensitive search).
        
        Args:
            name: Name to search for
            max_level: Optional maximum level to filter by
            
        Returns:
            Matching code or None if not found
        """
        name_lower = name.lower()
        matches = self._df[self._df['name'].str.lower() == name_lower]
        
        if max_level is not None:
            matches = matches[matches['level'] <= max_level]
        
        return matches.iloc[0]['code'] if not matches.empty else None

    def get_by_level(self, level: int) -> list[dict[str, str]]:
        """Get all classification entries at a specific level.
        
        Args:
            level: Classification level (1-4)
            
        Returns:
            List of code/name dictionaries
        """
        filtered = self._df[self._df['level'] == level]
        
        # Vectorized operation - much faster than itertuples
        return [
            {"code": code, "name": name}
            for code, name in zip(filtered['code'], filtered['name'])
        ]

    def get_children(self, parent_code: str) -> list[dict[str, str]]:
        """Get all child codes for a given parent.
        
        Args:
            parent_code: Parent classification code
            
        Returns:
            List of child code/name dictionaries
        """
        children = self._df[self._df['parentCode'] == parent_code]
        
        return [
            {"code": code, "name": name}
            for code, name in zip(children['code'], children['name'])
        ]

    def search_by_name(self, query: str) -> list[dict[str, str | int | None]]:
        """Search codes by name (case-insensitive partial match).
        
        Args:
            query: Search query string
            
        Returns:
            List of matching entries with code, name, level, and parentCode
        """
        query_lower = query.lower()
        matches = self._df[
            self._df['name'].str.lower().str.contains(query_lower, na=False)
        ]
        
        return [
            {
                "code": row.code,
                "name": row.name,
                "level": row.level,
                "parentCode": row.parentCode if pd.notna(row.parentCode) else None
            }
            for row in matches.itertuples(index=False)
        ]

    def get_parent(self, code: str) -> dict[str, str] | None:
        """Get parent code and name for a given code.
        
        Args:
            code: Classification code
            
        Returns:
            Parent code/name dictionary or None if no parent
        """
        row = self._df[self._df['code'] == code]
        
        if row.empty:
            return None
        
        parent_code = row.iloc[0]['parentCode']
        
        if pd.isna(parent_code):
            return None
        
        parent_name = self.get_description(parent_code)
        
        return {"code": parent_code, "name": parent_name} if parent_name else None

    def get_all_codes(self) -> dict[str, str]:
        """Get all codes as a dictionary mapping code to name.
        
        Returns:
            Copy of internal codes dictionary
        """
        return self._codes_dict.copy()


class NUTSService:
    """Service for NUTS (Nomenclature of Territorial Units) operations."""

    # SSB classification version for NUTS codes
    NUTS_VERSION = "2482"

    def __init__(self):
        """Initialize NUTS service with current classification version."""
        self._ssb_service = SSBService(version=self.NUTS_VERSION)

    def get_municipalities(self, county_code: str) -> list[dict[str, str]]:
        """Get municipalities for a given county code (Level 3).
        
        Args:
            county_code: County code
            
        Returns:
            List of municipality code/name dictionaries
        """
        return self._ssb_service.get_children(county_code)

    def get_counties(self, region_code: str) -> list[dict[str, str]]:
        """Get counties for a given region code (Level 2).
        
        Args:
            region_code: Region code
            
        Returns:
            List of county code/name dictionaries
        """
        return self._ssb_service.get_children(region_code)

    def get_regions(self) -> list[dict[str, str]]:
        """Get all regions (Level 1).
        
        Returns:
            List of region code/name dictionaries
        """
        return self._ssb_service.get_by_level(SSBLevel.LEVEL_1)

    def get_hierarchical_structure_by_level(self, level: SSBLevel) -> list[dict]:
        """Get hierarchical NUTS structure up to specified level.
        
        Args:
            level: Maximum level to include in hierarchy
            
        Returns:
            Nested structure of regions/counties/municipalities
        """
        logger.debug(
            "Building NUTS hierarchical structure",
            extra={"max_level": level}
        )

        regions = self.get_regions()

        if level == SSBLevel.LEVEL_1:
            logger.debug(f"Returning {len(regions)} regions (level 1 only)")
            return regions

        # Build hierarchy by level
        for region in regions:
            counties = self.get_counties(region['code'])
            
            if level == SSBLevel.LEVEL_2:
                region['counties'] = counties
                continue
            
            # Process counties for level 3
            for county in counties:
                # Clean county name (remove Norwegian/Sami dual names)
                county['name'] = county['name'].split('/')[0].strip()
                county['municipalities'] = self.get_municipalities(county['code'])
            
            region['counties'] = counties

        logger.debug(
            "NUTS hierarchy built successfully",
            extra={
                "max_level": level,
                "regions": len(regions),
                "total_items": sum(
                    1 + len(r.get('counties', []))
                    for r in regions
                )
            }
        )

        return regions


class STYRKService:
    """Service for STYRK (Standard Classification of Occupations) operations."""

    # SSB classification version for STYRK codes
    STYRK_VERSION = "33"

    def __init__(self):
        """Initialize STYRK service with current classification version."""
        self._ssb_service = SSBService(version=self.STYRK_VERSION)

    def get_occupations(self, unit_code: str) -> list[dict[str, str]]:
        """Get specific occupations for a unit group code (Level 4).
        
        Args:
            unit_code: Unit group code
            
        Returns:
            List of occupation code/name dictionaries
        """
        return self._ssb_service.get_children(unit_code)

    def get_unit_groups(self, minor_code: str) -> list[dict[str, str]]:
        """Get unit groups for a minor group code (Level 3).
        
        Args:
            minor_code: Minor group code
            
        Returns:
            List of unit group code/name dictionaries
        """
        return self._ssb_service.get_children(minor_code)

    def get_minor_groups(self, major_code: str) -> list[dict[str, str]]:
        """Get minor groups for a major group code (Level 2).
        
        Args:
            major_code: Major group code
            
        Returns:
            List of minor group code/name dictionaries
        """
        return self._ssb_service.get_children(major_code)

    def get_major_groups(self) -> list[dict[str, str]]:
        """Get all major groups (Level 1).
        
        Returns:
            List of major group code/name dictionaries
        """
        return self._ssb_service.get_by_level(SSBLevel.LEVEL_1)

    def get_hierarchical_structure_by_level(self, level: SSBLevel) -> list[dict]:
        """Get hierarchical STYRK structure up to specified level.
        
        Args:
            level: Maximum level to include in hierarchy
            
        Returns:
            Nested structure of profession groups/subgroups/roles/titles
        """
        logger.debug(
            "Building STYRK hierarchical structure",
            extra={"max_level": level}
        )

        profession_groups = self.get_major_groups()

        if level == SSBLevel.LEVEL_1:
            logger.debug(f"Returning {len(profession_groups)} major groups (level 1 only)")
            return profession_groups

        # Build hierarchy by level
        for group in profession_groups:
            subgroups = self.get_minor_groups(group['code'])
            
            if level == SSBLevel.LEVEL_2:
                group['subgroups'] = subgroups
                continue

            # Process subgroups for level 3+
            for subgroup in subgroups:
                roles = self.get_unit_groups(subgroup['code'])
                
                if level == SSBLevel.LEVEL_3:
                    subgroup['roles'] = roles
                    continue

                # Process roles for level 4
                for role in roles:
                    role['titles'] = self.get_occupations(role['code'])
                
                subgroup['roles'] = roles
            
            group['subgroups'] = subgroups

        logger.debug(
            "STYRK hierarchy built successfully",
            extra={
                "max_level": level,
                "major_groups": len(profession_groups),
                "total_items": sum(
                    1 + len(g.get('subgroups', []))
                    for g in profession_groups
                )
            }
        )

        return profession_groups
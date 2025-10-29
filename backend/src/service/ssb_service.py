"""
NUTS Codes Service class
"""

import pandas as pd
from enum import Enum
import io
import json
from src.clients.ssb_client import SSBClient


class SSBLevel(Enum):
    """SSB hierarchy levels."""
    LEVEL1 = 1
    LEVEL2 = 2
    LEVEL3 = 3
    LEVEL4 = 4

class SSBService:
    """Service class for NUTS code operations."""

    def __init__(self, version : str | None = None):
          self._df: pd.DataFrame | None = None
          self._codes_dict: dict[str, str] | None = None
          self._version = version
          self._client = SSBClient()
          if version is not None:
            self._load_data()         


    def _load_data(self) -> None : 
        """Load data from API and process it."""
        try: 
            # Use client to fetch data
            response = self._client.get_version(self._version)

            # Process data
            file = io.StringIO(response.text)
            self._df = pd.read_csv(file, sep=";", encoding="utf-8")
            # Keep only needed columns
            self._df = self._df[['code', 'parentCode', 'level', 'name']]
            # Create lookup dictionary
            self._codes_dict = dict(zip(self._df['code'], self._df['name']))
        except Exception as e:
            raise Exception(f"Error loading NUTS data: {e}")
        
    def get_description(self, code: str) -> str | None: 
        """Get description for a code."""
        return self._codes_dict.get(code)
    
    def get_code_by_name(self, name: str, max_level: int | None = None) -> str | None:
        """Get code by name (case insensitive), optionally filtering by max level"""
        name_lower = name.lower()
        
        # Filter dataframe by name
        matches = self._df[self._df['name'].str.lower() == name_lower]
        
        # Further filter by max level if specified
        if max_level is not None:
            matches = matches[matches['level'] <= max_level]
        
        if not matches.empty:
            code = matches.iloc[0]['code']
            return code
        return None
    

    def get_by_level(self, level: str) -> list[dict[str, str]]:
        """Get all codes entries by level"""
        df_filtered = self._df[self._df['level'] == level]

        return [
            {"code" : row.code, "name": row.name} for row in df_filtered.itertuples()
            ]
        

    def get_children(self, parent_code: str) -> list[dict[str, str]]: 
        """Get all child codes for a given parent."""
        df_children = self._df[self._df['parentCode'] == parent_code]
        
        return [
            {"code": row.code, "name": row.name}
            for row in df_children.itertuples()
        ]


    def search_by_name(self, name: str) -> str | None: 
        """Search codes by name (case-insensitive)."""
        query_lower = name.lower()
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
            for row in matches.itertuples()
        ]
    

    def get_parent(self, code: str) -> dict[str, str] | None:
        """Get parent code for given code."""
        row = self._df[self._df['code'] == code]
        if row.empty:
            return None
        
        parent_code = row.iloc[0]['parentCode']
        if pd.isna(parent_code):
            return None
        
        parent_name = self.get_description(parent_code)
        return {"code": parent_code, "name": parent_name} if parent_name else None
    
    
    def get_all_codes(self) -> dict[str, str]:
        """Get all codes as dictionary."""
        return self._codes_dict.copy()

    # TODO: Implement export functionality if needed
    def export_to_json(self, output_path: str, format_type: str = "flat") -> None:
        ...


class NUTSService: 
    """Service class for NUTS code operations."""

    def __init__ (self):
        """Initialize NUTS service with SSBService instance."""
        self._ssb_service  = SSBService(version=2482)

    def get_municipalities(self, county_code: str) -> list[dict[str, str]]:
        """Get municipalities for a given county code."""
        return self._ssb_service.get_children(county_code)
    

    def get_counties(self, region_code: str) -> list[dict[str, str]]: 
        """Get counties for a given region code."""
        return self._ssb_service.get_children(region_code)
    
    
    def get_regions(self) -> list[dict[str, str]]:
        """Get all regions (level 1)."""
        return self._ssb_service.get_by_level(SSBLevel.LEVEL1.value) 
    

    def get_hierarchical_structure_by_level(self, level: SSBLevel) -> list[dict]:
        """Get hierarchical NUTS structure up to a specified level."""
        regions = self.get_regions()

        if level == SSBLevel.LEVEL1:
            return regions

        for region in regions:
            counties = self.get_counties(region['code'])
            if level == SSBLevel.LEVEL2:
                region['counties'] = counties

            for county in counties:
                county['name'] = county['name'].split('/')[0]
                municipalities = self.get_municipalities(county['code'])
                if level == SSBLevel.LEVEL3:
                    county['municipalities'] = municipalities
            
            region['counties'] = counties

        return regions

class STYRKService:
    """Service class for STYRK code operations.""" 
    def __init__(self):
        """Initialize STYRK service with SSBService instance."""
        self._ssb_service = SSBService(version=33)

    def get_occupations(self, unit_code: str):
        """Get specific occupations for a STYRK unit group code (Level 4)."""
        return self._ssb_service.get_children(unit_code)


    def get_unit_groups(self, minor_code: str):
        """Get unit groups for a STYRK minor group code (Level 3)."""
        return self._ssb_service.get_children(minor_code)


    def get_minor_groups(self, major_code: str):
        """Get minor groups for a STYRK major group code (Level 2)."""
        return self._ssb_service.get_children(major_code)

        
    def get_major_groups(self) -> list[dict[str,str]]:
        """Get all major groups - top level STYRK categories (Level 1)."""
        return self._ssb_service.get_by_level(SSBLevel.LEVEL1.value)
    

    def get_hierarchical_structure_by_level(self, level: SSBLevel) -> list[dict]:
        """Get hierarchical STYRK structure up to a specified level."""
        profession_groups = self.get_major_groups()

        if level == SSBLevel.LEVEL1:
            return profession_groups

        for group in profession_groups:
            subgroups = self.get_minor_groups(group['code'])
            if level == SSBLevel.LEVEL2:
                group['subgroups'] = subgroups
                continue

            for subgroup in subgroups:
                roles = self.get_unit_groups(subgroup['code'])
                if level == SSBLevel.LEVEL3:
                    subgroup['roles'] = roles
                    continue

                for role in roles:
                    role['titles'] = self.get_occupations(role['code'])
                subgroup['roles'] = roles
            group['subgroups'] = subgroups

        return profession_groups
    

if __name__ == "__main__":
    service = STYRKService()

    print(json.dumps(service.get_hierarchical_structure(), indent=2, ensure_ascii=False))

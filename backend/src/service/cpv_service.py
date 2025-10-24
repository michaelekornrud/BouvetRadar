"""
CPV (Common Procurement Vocabulary) Codes
Improved version with better organization and utility functions.
"""

from enum import Enum

# Main CPV codes dictionary
CPV_CODES: dict[int, str] = {
    # Software and Information Systems (48000000 series)
    48000000: "Programvare og informasjonssystemer",
    48100000: "Bransjespesifikk programvare",
    48151000: "Kontrollsystem, datamaskiner",
    48161000: "Administrativt bibliotekssystem",
    48200000: "Nettverks, internett og intranett programvare",
    48300000: "Programvare for dokumentopprettelse, tegning, bilde, tidsplanlegging og produktivitet",
    48322000: "Programvare for grafikk",
    48323000: "Programvare for datamaskinassistert fabrikkering",
    48324000: "Programvare for diagramfremstilling",
    48325000: "Programvare for formutvikling",
    48326000: "Programvare for kartlegging",
    48329000: "Bildebehandlings- og arkiveringssystem",
    48400000: "Programvare relatert til forretningsvirksomhet",
    48445000: "Programvare for håndtering av kundekontakter",
    48500000: "Kommunikasjons- og multimediaprogramvare",
    48600000: "Operativsystemer og programvare for databaser",
    48612000: "Databasestyringssystem",
    48613000: "Elektronisk datastyring",
    48700000: "Programvare verktøy",
    48800000: "Informasjonssystemer og servere",
    48810000: "Informasjonssystemer",
    48814000: "Medisinske informasjonssystemer",
    48900000: "Diverse programvarepakker og computersystemer",
    48910000: "Dataspill, programvare egnet for barn og skjermsparere",
    48911000: "Dataspill",
    48912000: "Programvare egnet for barn",
    48913000: "Skjermsparere",
    48930000: "Trenings- og underholdningsprogramvare",
    48931000: "Treningsprogramvare",
    48932000: "Underholdningsprogramvare",
    48940000: "Programvare til mønsterdesign og kalenderfunksjon",
    48941000: "Programvare til mønsterdesign",
    48942000: "Programvare til kalenderfunksjon",
    48950000: "Skipslokaliseringssystem og høyttaleranlegg",
    48960000: "Driver- og systemprogrampakke",
    48961000: "Ethernett-drivere",
    48962000: "Grafikkortdrivere",
    48970000: "Programvare for printing",
    48971000: "Programvare til oppsett av adressebøker",
    48972000: "Programvare for etikettproduksjon",
    48980000: "Programmeringsspråk og verktøy",
    48981000: "Programpakke for kompileringsverktøy",
    48982000: "Programvare for konfigurasjonshåndtering",
    48983000: "Programvare for programutvikling",
    48984000: "Programvareverktøy for grafisk brukergrensesnitt",
    48985000: "Programmeringsspråk",
    48986000: "Programvare til programtestning",
    48990000: "Programvarepakke for regneark og utvidet funksjonalitet",
    
    # Telecommunications Services (64000000 series)
    64000000: "Post- og telekommunikasjonstjenester",
    64200000: "Telekommunikasjonstjenester",
    64214400: "Utleie av fastlinjer",
    
    # Data Services (72000000 series)
    72000000: "Datatjenester: rådgivning, programvareutvikling, internett og systemstøtte",
    72100000: "Rådgivning vedrørende maskinvare",
    72200000: "Programmering av software og rådgivning",
    72212220: "Utviklingstjenester relatert til Programvare for internett og intranett",
    72212222: "Utviklingstjenester relatert til Programvare for webserver",
    72220000: "Systemtjenester og tekniske konsulenttjenester",
    72227000: "Konsulentvirksomhet i forbindelse med integrasjon av programvare",
    72230000: "Utvikling av kundespesifisert programvare",
    72240000: "Systemanalyse og programmering",
    72250000: "System- og støttetjenester",
    72300000: "Datatjenester",
    72310000: "Databehandling",
    72315200: "Drift av datanettverk",
    72320000: "Databasevirksomhet",
    72510000: "Datamaskinrelaterte driftstjenester",
    72514000: "Drift av dataanlegg",
    
    # Research and Development (73000000 series)
    73000000: "Forsknings- og utviklingsvirksomhet og tilhørende konsulenttjenester", # ADDED FOR MAIN CATEGORY
    73200000: "Konsulentvirksomhet i forbindelse med forskning og utvikling",
    73210000: "Konsulentvirksomhet i forbindelse med forskning",
    73220000: "Konsulentvirksomhet i forbindelse med utvikling",
    73300000: "Planleggingsarbeid og utførelse av forskning og utvikling",
    
    # Business Services (79000000 series)
    79000000: "Forretningstjenester: lov, reklame, rådgiving, ansettelse, trykking og sikkerhet", # ADDED FOR MAIN CATEGORY
    79311100: "Utforming av undersøkelse",
    79311200: "Utførelse av undersøkelse",
    79311300: "Analyse av undersøkelse",
    79315000: "Sosialforskning",
    79340000: "Reklame og markedsføringstjenester",
    79400000: "Bedriftsrådgivning og administrativ rådgivning og beslektede tjenester",
    79410000: "Bedriftsrådgivning og administrativ rådgivning",
    79411100: "Bedriftsutvikling og rådgivning",
    79412000: "Rådgivning i forbindelse med økonomisk forvaltning",
    79413000: "Rådgivning innen markedsføring",
    79415200: "Konsulentvirksomhet i forbindelse med design",
    79418000: "Rådgivning vedrørende innkjøp",
    79420000: "Ledelsesrelaterte tjenester",
    79421000: "Prosjektledelse, med unntak av bygge- og anleggsarbeid",
    79822500: "Grafisk design",
    79961100: "Reklamefotografering",
    
    # Education Services (80000000 series)
    80000000: "Tjenester i forbindelse med trening og utdannelse", # ADDED FOR MAIN CATEGORY
    80420000: "E-læringstjenester",
}

# Use Enum for main categories only
class CPVMainCategory(Enum):
    """Main CPV categories for high-level classification."""
    SOFTWARE_AND_INFORMATION_SYSTEMS = 48000000
    TELECOMMUNICATIONS_SERVICES = 64000000
    DATA_SERVICES = 72000000
    RESEARCH_AND_DEVELOPMENT = 73000000
    BUSINESS_SERVICES = 79000000
    EDUCATION_AND_EXERCISE = 80000000

# Automatically generate reverse lookup (no manual maintenance needed)
CPV_CODES_BY_NAME: dict[str, int] = {desc: code for code, desc in CPV_CODES.items()}

# Main category mappings
CPV_MAIN_CATEGORIES = {
    CPVMainCategory.SOFTWARE_AND_INFORMATION_SYSTEMS.name: CPVMainCategory.SOFTWARE_AND_INFORMATION_SYSTEMS.value,
    CPVMainCategory.TELECOMMUNICATIONS_SERVICES.name: CPVMainCategory.TELECOMMUNICATIONS_SERVICES.value,
    CPVMainCategory.DATA_SERVICES.name: CPVMainCategory.DATA_SERVICES.value,
    CPVMainCategory.RESEARCH_AND_DEVELOPMENT.name: CPVMainCategory.RESEARCH_AND_DEVELOPMENT.value,
    CPVMainCategory.BUSINESS_SERVICES.name: CPVMainCategory.BUSINESS_SERVICES.value,
    CPVMainCategory.EDUCATION_AND_EXERCISE.name: CPVMainCategory.EDUCATION_AND_EXERCISE.value,

}

class CPVService:
    """Service class for CPV code operations."""
    
    @staticmethod
    def get_description(code: int) -> str | None:
        """Get description for a CPV code."""
        return CPV_CODES.get(code)
    
    @staticmethod
    def get_code(description: str) -> int | None:
        """Get CPV code for a description."""
        return CPV_CODES_BY_NAME.get(description)
    
    @staticmethod
    def get_codes_by_category(category_code: int) -> dict[int, str]:
        """Get all codes that start with the same digits as category_code."""
        category_str = str(category_code)
        return {
            code: desc for code, desc in CPV_CODES.items()
            if str(code).startswith(category_str[:2])  # Match first 2 digits
        }
    
    @staticmethod
    def search_descriptions(query: str) -> dict[int, str]:
        """Search for CPV codes by description text."""
        query_lower = query.lower()
        return {
            code: desc for code, desc in CPV_CODES.items()
            if query_lower in desc.lower()
        }
    
    @staticmethod
    def get_all_codes() -> dict[int, str]:
        """Get all CPV codes."""
        return CPV_CODES.copy()
    
    @staticmethod
    def get_main_categories() -> list[tuple]:
        """Get main category codes and names."""
        return [(cat.value, cat.name) for cat in CPVMainCategory]
    
    @staticmethod
    def get_category_for_code(code: int) -> str:
        """Helper function to determine category name for a code."""
        if str(code).startswith('48'):
            return "Software and Information Systems"
        elif str(code).startswith('64'):
            return "Telecommunications Services"
        elif str(code).startswith('72'):
            return "Data Services"
        elif str(code).startswith('73'):
            return "Research and Development"
        elif str(code).startswith('79'):
            return "Business Services"
        elif str(code).startswith('80'):
            return "Education and Exercise"
        else:
            return "Other"


if __name__ == "__main__":
    # Example usage
    service = CPVService()
    
    print("=== CPV Service Examples ===")
    print(f"Description for code 48000000: {service.get_description(48000000)}")
    print(f"Code for 'Dataspill': {service.get_code('Dataspill')}")
    
    print("\n=== Software related codes ===")
    software_codes = service.get_codes_by_category(48000000)
    for code, desc in list(software_codes.items())[:5]:  # Show first 5
        print(f"{code}: {desc}")
    
    print("\n=== Search for 'programvare' ===")
    search_results = service.search_descriptions("programvare")
    for code, desc in list(search_results.items())[:3]:  # Show first 3
        print(f"{code}: {desc}")
    
    print("\n=== Main Categories ===")
    for code, name in service.get_main_categories():
        print(f"{code}: {name}")

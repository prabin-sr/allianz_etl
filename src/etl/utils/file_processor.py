import os
from pathlib import Path
from typing import List

BASE_DIR: Path = Path(__file__).parent.parent.parent.resolve()
MEDIA_DIR: Path = Path.joinpath(BASE_DIR, "media")

ZIP_FILE_NAME: str = "scraped_pages.zip"
EXCEL_FILE_NAME: str = "extracted_data_analytics.xlsx"
EXTRACTED_DATA_SHEET_NAME: str = "NHL Stats 1990-2011"
ANALYTICS_DATA_SHEET_NAME: str = "Winner and Loser per Year"
EXTRACTED_DATA_HEADERS: List[str] = [
    "Team Name",
    "Year",
    "Wins",
    "Losses",
    "OT Losses",
    "Win %",
    "Goals For (GF)",
    "Goals Against (GA)",
    "+ / -",
]
ANALYTICS_DATA_HEADERS: List[str] = [
    "Year",
    "Winner",
    "Winner Num. of Wins",
    "Loser",
    "Loser Num. of Wins",
]


def create_directory(dir_name: str | Path) -> None:
    os.makedirs(dir_name, exist_ok=True)

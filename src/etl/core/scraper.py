import asyncio
import random
import re
import string
import zipfile
from collections import defaultdict
from pathlib import Path
from typing import Dict, List
from urllib.parse import urljoin

import aiohttp
from bs4 import BeautifulSoup, element
from openpyxl import Workbook
from openpyxl.worksheet.worksheet import Worksheet

from etl.utils.constants import BASE_URL
from etl.utils.file_processor import (
    ANALYTICS_DATA_HEADERS,
    ANALYTICS_DATA_SHEET_NAME,
    EXCEL_FILE_NAME,
    EXTRACTED_DATA_HEADERS,
    EXTRACTED_DATA_SHEET_NAME,
    MEDIA_DIR,
    ZIP_FILE_NAME,
    create_directory,
)
from etl.utils.logger import LOGGER


class DataScraper:
    def __init__(self) -> None:
        self._base_url: str = BASE_URL
        self._media_dir: Path = MEDIA_DIR
        self._zip_file_name: str = ZIP_FILE_NAME
        self._excel_file_name: str = EXCEL_FILE_NAME
        self._extracted_data_headers: List[str] = EXTRACTED_DATA_HEADERS
        self._analytics_data_headers: List[str] = ANALYTICS_DATA_HEADERS
        self._extracted_data_sheet_name: str = EXTRACTED_DATA_SHEET_NAME
        self._analytics_data_sheet_name: str = ANALYTICS_DATA_SHEET_NAME

    async def fetch_all_pages(self, urls: List[str]) -> Dict[str, str]:
        async with aiohttp.ClientSession() as session:
            tasks = [session.get(url) for url in urls]
            responses = await asyncio.gather(*tasks)
            data: Dict[str, str] = {
                str(res.url): await res.text() for res in responses if res.status == 200
            }
            return data

    def extract_pagination_urls(self, html: str, base_url: str) -> List[str]:
        soup: BeautifulSoup = BeautifulSoup(html, "html.parser")
        pagination_links: element.ResultSet = soup.select("ul.pagination li a")
        urls: List[str] = [urljoin(base_url, a["href"]) for a in pagination_links]
        unique_urls: List[str] = list(set(urls))
        return unique_urls

    def extract_page_num(self, url: str) -> str:
        match = re.search(r"page_num=(\d+)", url)
        if match:
            page_num: str = match.group(1)
        else:
            page_num: str = "".join(
                random.choices(string.ascii_letters + string.digits, k=6)
            )
        return page_num

    def save_html_files_as_zip(
        self, page_responses: Dict[str, str], media_dir: Path, zip_file_name: str
    ) -> None:
        create_directory(media_dir)
        _zip_file_path: Path = Path.joinpath(media_dir, zip_file_name)

        with zipfile.ZipFile(_zip_file_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            for url, html in page_responses.items():
                page_num: str = self.extract_page_num(url)
                filename: str = f"{page_num}.html"
                zipf.writestr(filename, html)

    def parse_table_data_and_save(
        self,
        pagination_responses: Dict[str, str],
        media_dir: Path,
        excel_file_name: str,
    ) -> None:
        wb = Workbook()
        ws1: Worksheet = wb.active
        ws1.title = self._extracted_data_sheet_name
        ws2: Worksheet = wb.create_sheet(title=self._analytics_data_sheet_name)
        ws1.append(self._extracted_data_headers)
        ws2.append(self._analytics_data_headers)

        year_team_wins: Dict[List] = defaultdict(list)

        for html in pagination_responses.values():
            soup = BeautifulSoup(html, "html.parser")
            table_rows = soup.select("tr.team")

            for row in table_rows:
                team_name = row.select_one(".name").get_text(strip=True)
                year = int(row.select_one(".year").get_text(strip=True))
                wins = int(row.select_one(".wins").get_text(strip=True))
                losses = int(row.select_one(".losses").get_text(strip=True))
                ot_losses = row.select_one(".ot-losses").get_text(strip=True)
                win_pct = float(row.select_one(".pct").get_text(strip=True))
                goals_for = int(row.select_one(".gf").get_text(strip=True))
                goals_against = int(row.select_one(".ga").get_text(strip=True))
                diff = int(row.select_one(".diff").get_text(strip=True))

                ws1.append(
                    [
                        team_name,
                        year,
                        wins,
                        losses,
                        int(ot_losses) if ot_losses else 0,
                        win_pct,
                        goals_for,
                        goals_against,
                        diff,
                    ]
                )

                year_team_wins[year].append((team_name, wins))

        for year, teams in sorted(year_team_wins.items()):
            sorted_teams = sorted(teams, key=lambda x: x[1], reverse=True)
            winner_team, winner_wins = sorted_teams[0]
            loser_team, loser_wins = sorted_teams[-1]
            ws2.append([year, winner_team, winner_wins, loser_team, loser_wins])

        create_directory(media_dir)
        _excel_file_path: Path = Path.joinpath(media_dir, excel_file_name)
        wb.save(_excel_file_path)

    async def __call__(self) -> None:
        page_responses: Dict[str, str] = await self.fetch_all_pages(
            urls=[self._base_url]
        )

        start_page_html: str | None = page_responses.get(self._base_url, None)
        if not start_page_html:
            LOGGER.error("Extraction Interrupted...")
            raise SystemExit(f"Error happened while fetching URL {self._base_url}")

        pagination_urls: List[str] = self.extract_pagination_urls(
            start_page_html, self._base_url
        )

        pagination_responses: Dict[str, str] = await self.fetch_all_pages(
            urls=pagination_urls
        )

        sorted_pagination_responses: Dict[str, str] = dict(
            sorted(
                pagination_responses.items(),
                key=lambda item: int(re.search(r"page_num=(\d+)", item[0]).group(1)),
            )
        )

        # Assign to self._zip_task variable to handle the fire-and-forgot functionality in pytest
        self._zip_task = asyncio.create_task(
            asyncio.to_thread(
                self.save_html_files_as_zip,
                sorted_pagination_responses,
                self._media_dir,
                self._zip_file_name,
            )
        )

        self.parse_table_data_and_save(
            sorted_pagination_responses, self._media_dir, self._excel_file_name
        )

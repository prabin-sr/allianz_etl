import asyncio

from etl.core.scraper import DataScraper
from etl.utils.logger import LOGGER

if __name__ == "__main__":
    LOGGER.info("Extraction Started...")
    data_scraper = DataScraper()
    asyncio.run(data_scraper())
    LOGGER.info("Extraction Completed...")

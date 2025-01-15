import json
import pathlib
from typing import Dict, Optional

import requests
from pathlib import Path
import zipfile
from io import BytesIO

from bs4 import BeautifulSoup

from utils.logger import Logger
from utils.scraper.os_checker import OSChecker

logger = Logger().get_instance()


class ChromePageScraper:
    URL_LATEST = "https://googlechromelabs.github.io/chrome-for-testing/#stable"
    URL_ALL = "https://googlechromelabs.github.io/chrome-for-testing/latest-versions-per-milestone-with-downloads.json"

    _latest_cache = None
    _all_cache = None

    @staticmethod
    def __fetch(url: str) -> requests.Response:
        response = requests.get(url)
        response.raise_for_status()
        return response

    @classmethod
    def fetch_latest_page(cls) -> str:
        if cls._latest_cache is None:
            logger.info("Fetching the latest stable page.")
            cls._latest_cache = cls.__fetch(cls.URL_LATEST).text
        else:
            logger.info("Using cached latest stable page.")
        return cls._latest_cache

    @classmethod
    def fetch_all_versions_json(cls) -> Dict:
        if cls._all_cache is None:
            logger.info("Fetching all versions JSON data.")
            cls._all_cache = json.loads(cls.__fetch(cls.URL_ALL).text)
        else:
            logger.info("Using cached all versions JSON data.")
        return cls._all_cache

    @staticmethod
    def parse_latest() -> Dict[str, str]:
        drivers = {}
        page_content = ChromePageScraper.fetch_latest_page()

        soup = BeautifulSoup(page_content, "html.parser")
        element = soup.select_one(
            "section#stable.status-not-ok div.table-wrapper table tbody tr.status-ok"
        )

        if not element:
            raise ValueError("Element not found in the HTML.")

        code_elements = element.find_all("code")
        elements_list = [
            el.text.strip()
            for el in code_elements
            if el.text.strip() not in ["200", "chrome", "chromedriver"]
        ]

        for i in range(0, len(elements_list), 2):
            os_name, link = elements_list[i], elements_list[i + 1]
            drivers[os_name] = link

        return drivers

    def get_latest_driver(self, os_name: str):
        drivers = self.parse_latest()
        if os_name in drivers:
            logger.info(f"Latest driver for {os_name}: {drivers[os_name]}")
        else:
            logger.warning(f"No driver found for {os_name}.")

    @staticmethod
    def get_chromedriver(
        platform=None,
        version=None,
        milestone=None,
        d_dir: Optional[pathlib.Path] = None,
        is_extracted: bool = False,
    ) -> Optional[Path]:
        if version is None and milestone is None:
            raise ValueError("You must specify either version or milestone.")
        if platform is None:
            platform = OSChecker.check_os()

        download_dir = (
            d_dir or Path(__file__).resolve().parent.parent.parent / "resources"
        )
        parsed_data = ChromePageScraper.fetch_all_versions_json()
        milestones_data = parsed_data.get("milestones", {})

        for milestone_key, milestone_data in milestones_data.items():
            if (milestone is None or milestone_key == milestone) and (
                version is None or milestone_data["version"] == version
            ):
                chromedriver_info = next(
                    (
                        info
                        for info in milestone_data["downloads"].get(
                            "chromedriver", []
                        )
                        if platform is None or info["platform"] == platform
                    ),
                    None,
                )

                if chromedriver_info:
                    url = chromedriver_info["url"]
                    logger.info(f"Downloading Chromedriver from {url}.")
                    response = requests.get(url)
                    response.raise_for_status()

                    download_dir.mkdir(parents=True, exist_ok=True)
                    download_path = download_dir / "chromedriver.zip"

                    with open(download_path, "wb") as file:
                        file.write(response.content)
                        logger.info(f"Chromedriver downloaded to {download_dir}")

                    if is_extracted:
                        with zipfile.ZipFile(BytesIO(response.content)) as zip_ref:
                            zip_ref.extractall(download_dir)
                        logger.info(f"Chromedriver extracted to {download_dir}")

                    return download_path

        logger.warning("No suitable Chromedriver found.")
        return None


# if __name__ == "__main__":
#     ChromePageScraper.get_chromedriver(milestone="131")

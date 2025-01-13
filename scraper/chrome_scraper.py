import json
import pathlib
from typing import Dict, Optional

import requests
from pathlib import Path
import zipfile
from io import BytesIO

from bs4 import BeautifulSoup

from scraper.os_checker import OSChecker


class ChromePageScraper:
    URL_LATEST = (
        "https://googlechromelabs.github.io/chrome-for-testing/#stable"
    )
    URL_ALL = "https://googlechromelabs.github.io/chrome-for-testing/latest-versions-per-milestone-with-downloads.json"

    @staticmethod
    def __fetch(url: str) -> requests.Response:
        response = requests.get(url)
        response.raise_for_status()
        return response

    @staticmethod
    def parse_latest() -> Dict[str, str]:
        elements_list = []
        drivers = {}
        page = ChromePageScraper.__fetch(ChromePageScraper.URL_LATEST)

        soup = BeautifulSoup(page.text, "html.parser")
        element = soup.select_one(
            "section#stable.status-not-ok div.table-wrapper table tbody tr.status-ok"
        )

        if not element:
            raise Exception("Element not found in the HTML.")

        code_elements = element.find_all("code")

        for el in code_elements:
            text = el.text.strip()

            if text not in ["200", "chrome", "chromedriver"]:
                elements_list.append(text)

        for i in range(0, len(elements_list), 2):
            os = elements_list[i]
            link = elements_list[i + 1]
            drivers[os] = link

        return drivers

    def get_latest_driver(self, os_name: str):
        drivers = self.parse_latest()
        if os_name in drivers:
            print(drivers[os_name])

    @staticmethod
    def get_chromedriver(platform=None,
                         version=None,
                         milestone=None,
                         d_dir: Optional[pathlib.Path] = None,
                         is_extracted: bool = False
                         ):
        """
        :param platform: os_name and architecture
        :param version: your chrome browser version
        :param milestone: first 3 digits of a browser version: 129 or etc
        :param d_dir: Directory to save the chromedriver zip file
        :param is_extracted: extracts the chromedriver
        :return:
        """
        if version is None and milestone is None:
            raise ValueError(
                f"You must specify version or milestone: version {version},"
                f" milestone {milestone}"
            )
        if platform is None:
            platform = OSChecker.check_os()

        download_dir = d_dir or Path(__file__).resolve().parent.parent / "resources"

        # Parse the JSON data
        parsed_data = json.loads(
            ChromePageScraper.__fetch(ChromePageScraper.URL_ALL).text
        )
        milestones_data = parsed_data["milestones"]

        for milestone_key, milestone_data in milestones_data.items():
            if (milestone is None or milestone_key == milestone) and (
                    version is None or milestone_data["version"] == version
            ):
                if "chromedriver" in milestone_data["downloads"]:
                    for chromedriver_info in milestone_data["downloads"]["chromedriver"]:
                        if (
                                platform is None
                                or chromedriver_info["platform"] == platform
                        ):
                            url = chromedriver_info["url"]
                            response = requests.get(url)
                            response.raise_for_status()  # Check status

                            download_dir.mkdir(parents=True, exist_ok=True)
                            download_path = download_dir / "chromedriver.zip"

                            with open(download_path, "wb") as file:
                                file.write(response.content)
                                print(f"Chromedriver downloaded to {download_dir}")

                            if is_extracted:
                                with zipfile.ZipFile(BytesIO(response.content)) as zip_ref:
                                    zip_ref.extractall(download_dir)

                                print(f"Chromedriver extracted to {download_dir}")
                            return download_path

if __name__ == "__main__":
    ChromePageScraper.get_chromedriver(milestone="131")

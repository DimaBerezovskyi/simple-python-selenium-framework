import os
import shutil
import zipfile
import requests


class FileDownloader:
    def __init__(self, destination_folder="resources"):
        self.destination_folder = destination_folder

    def destination(self) -> str:
        return os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", self.destination_folder)
        )

    def create_destination_folder(self):
        path_to_file = self.destination()
        if not os.path.exists(path_to_file):
            try:
                os.makedirs(path_to_file)
            except OSError as e:
                raise RuntimeError(f"Failed to create destination folder: {path_to_file}: {e}")

    def download_file(self, download_url: str, destination_file: str):
        try:
            response = requests.get(download_url)
            response.raise_for_status()
        except requests.RequestException as e:
            raise RuntimeError(f"Failed to download file from {download_url}: {e}")

        with open(destination_file, "wb") as f:
            f.write(response.content)


class DriverManager:
    def __init__(self, destination_folder="resources"):
        self.destination_folder = destination_folder
        self.downloader = FileDownloader(self.destination_folder)
        self.os_checker = OSChecker()

    def extract_zip(self, zip_file: str, destination_folder: str):
        try:
            with zipfile.ZipFile(zip_file, "r") as zip_ref:
                zip_ref.extractall(destination_folder)
        except zipfile.BadZipFile as e:
            raise RuntimeError(f"Failed to unzip file {zip_file}: {e}")

    def rename_chromedriver(self, chromedriver_path: str):
        source_path = os.path.join(self.destination_folder, "chromedriver-mac-arm64", "chromedriver")
        try:
            os.rename(source_path, chromedriver_path)
        except (OSError, FileNotFoundError) as e:
            raise RuntimeError(f"Failed to move chromedriver from {source_path} to {chromedriver_path}: {e}")

    def download_and_extract_chromedriver(self, download_url: str):
        self.downloader.create_destination_folder()

        zip_file = os.path.join(self.destination_folder, "chromedriver.zip")
        chromedriver_path = os.path.join(self.destination_folder, "chromedriver")

        self.downloader.download_file(download_url, zip_file)
        self.extract_zip(zip_file, self.downloader.destination())
        self.rename_chromedriver(chromedriver_path)

        shutil.rmtree(os.path.join(self.destination_folder, "chromedriver-mac-arm64"), ignore_errors=True)
        os.remove(zip_file)

        self.os_checker.print_os_info()
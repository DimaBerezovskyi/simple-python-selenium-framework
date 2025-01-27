import argparse
import os
import sys
from pathlib import Path
from typing import Optional

from colorama import init
from pyfiglet import Figlet
import inquirer

from utils.scraper.chrome_scraper import ChromePageScraper

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.insert(0, project_root)


__version__ = "1.1.0"

TASKS = {
    "chromedriver": ["get_driver_by_milestone", "exit"],
    "firefox": ["download_geckodriver", "exit"],
}


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Driver Management Tool")

    # Adding subparsers for different drivers like chromedriver and geckodriver
    subparsers = parser.add_subparsers(dest='driver', help='Choose a driver to manage')

    # ChromeDriver specific subparser
    chromedriver_parser = subparsers.add_parser('chromedriver', help='Manage ChromeDriver')
    chromedriver_parser.add_argument(
        "-v", "--version", action="store_true", help="Show version and exit."
    )
    chromedriver_parser.add_argument(
        "-d", "--docs", action="store_true", help="Show documentation and exit."
    )
    chromedriver_parser.add_argument(
        "-milestone",
        "--milestone",
        type=str,
        required=True,  # Make milestone required
        help="Specify the milestone version (e.g., '131').",
    )

    return parser.parse_args()


def execute_task(task: str, milestone: str, version: Optional[str]) -> None:
    """Execute the selected task."""
    try:
        match task:
            case "get_driver_by_milestone":
                print(f"Downloading ChromeDriver for version {milestone}...")
                ChromePageScraper.get_chromedriver(milestone=milestone, version=version)
            case "TODO_download_geckodriver_TODO":
                print(f" Downloading GeckoDriver for version {milestone}...")
            case "exit":
                exit(0)
            case _:
                print(f"Task '{task}' is not supported.")
    except Exception as e:
        print(f"Error executing task '{task}': {e}")


def main() -> None:
    """Entry point for the Driver Management CLI."""
    init()
    f = Figlet(font="Slant")
    print(f.renderText("Driver Tool"))

    args = parse_args()

    # Show version or documentation if requested
    if args.version:
        print(f"Driver Tool version: {__version__}")
        return
    if args.docs:
        print("Documentation: This is a CLI tool to manage drivers like ChromeDriver and GeckoDriver.")
        return

    # Get available tasks based on the selected driver and milestone
    if args.driver == 'chromedriver' and args.milestone:
        available_tasks = TASKS.get("chromedriver", [])
        if not available_tasks:
            print(f"No tasks available for the selected milestone: {args.milestone}")
            return

        try:
            while True:
                answers = inquirer.prompt(
                    [
                        inquirer.List(
                            "task",
                            message=f"What task do you want to perform for ChromeDriver {args.milestone}?",
                            choices=available_tasks,
                        )
                    ]
                )
                task = answers["task"]
                execute_task(task, milestone=args.milestone, version=None)
        except KeyboardInterrupt:
            print("\nExiting...")
        except Exception as e:
            print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()

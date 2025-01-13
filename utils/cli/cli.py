import argparse
from pathlib import Path

from pyfiglet import Figlet
from rich.console import Console
from colorama import Fore, Style

from scraper.chrome_scraper import ChromePageScraper


def create_cli():
    # Initialize ArgumentParser
    parser = argparse.ArgumentParser(prog="sstf", description="SSTF Command Line Tool")

    # Add the 'get' subcommand
    subparsers = parser.add_subparsers(dest="command")

    # Add subcommand for 'get'
    get_parser = subparsers.add_parser("get", help="Download and manage Chromedriver")
    get_subparsers = get_parser.add_subparsers(dest="subcommand")

    # Add subcommand for 'chromedriver'
    chromedriver_parser = get_subparsers.add_parser("chromedriver",
                                                    help="Download chromedriver for a specified version and platform")
    chromedriver_parser.add_argument('--milestone', type=str,
                                     help=f"{Fore.CYAN}Chromium milestone version (e.g., 131).{Style.RESET_ALL}")
    chromedriver_parser.add_argument('--version', type=str,
                                     help=f"{Fore.CYAN}Chromium browser version.{Style.RESET_ALL}")
    chromedriver_parser.add_argument('--platform', type=str, choices=["windows", "mac", "linux"],
                                     help=f"{Fore.CYAN}Operating system platform.{Style.RESET_ALL}")
    chromedriver_parser.add_argument('--output-dir', type=str, default=None,
                                     help=f"{Fore.CYAN}Directory to save the downloaded Chromedriver.{Style.RESET_ALL}")
    chromedriver_parser.add_argument('--extract', action='store_true',
                                     help=f"{Fore.CYAN}Extract the Chromedriver after download.{Style.RESET_ALL}")

    # Parse arguments
    args = parser.parse_args()

    # Handle 'get chromedriver' logic
    if args.command == "get" and args.subcommand == "chromedriver":
        console = Console()

        # ASCII Art Header with Figlet (using Rich)
        fig = Figlet(font="slant")  # You can use different fonts like 'slant', 'block', etc.
        console.print(fig.renderText("Chromedriver Download"), style="bold green")

        # Run the actual logic for downloading chromedriver
        ChromePageScraper.get_chromedriver(
            platform=args.platform,
            version=args.version,
            milestone=args.milestone,
            d_dir=Path(args.output_dir) if args.output_dir else None,
            is_extracted=args.extract
        )


if __name__ == "__main__":
    create_cli()

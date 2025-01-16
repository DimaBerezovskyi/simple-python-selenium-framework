import argparse
from pathlib import Path

from utils.scraper.chrome_scraper import ChromePageScraper


def main():
    parser = argparse.ArgumentParser(prog="psaf", description="PSAF CLI Tool")

    # Subcommand for 'get' operations
    subparsers = parser.add_subparsers(dest="command")

    # Subcommand for 'get chromedriver'
    get_parser = subparsers.add_parser("get", help="Get a specific resource")
    get_subparsers = get_parser.add_subparsers(dest="resource")

    # Subcommand for 'chromedriver' under 'get'
    chromedriver_parser = get_subparsers.add_parser(
        "chromedriver", help="Download the ChromeDriver"
    )
    chromedriver_parser.add_argument(
        "--platform",
        type=str,
        help="Specify the platform (e.g., 'win32', 'linux64').",
    )
    chromedriver_parser.add_argument(
        "--version",
        type=str,
        help="Specify the version of ChromeDriver.",
    )
    chromedriver_parser.add_argument(
        "--milestone",
        type=str,
        help="Specify the milestone of ChromeDriver.",
    )
    chromedriver_parser.add_argument(
        "--output-dir",
        type=str,
        help="Directory to save the downloaded ChromeDriver.",
    )
    chromedriver_parser.add_argument(
        "--extract",
        action="store_true",
        help="Extract the downloaded ChromeDriver.",
    )

    args = parser.parse_args()

    if args.command == "get" and args.resource == "chromedriver":
        output_dir = Path(args.output_dir) if args.output_dir else None
        ChromePageScraper.get_chromedriver(
            platform=args.platform,
            version=args.version,
            milestone=args.milestone,
            d_dir=output_dir,
            is_extracted=args.extract,
        )


if __name__ == "__main__":
    main()
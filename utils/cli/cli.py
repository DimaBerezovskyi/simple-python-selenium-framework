@click.command()
@click.option("--platform", default=None, help="OS and architecture (e.g., 'win64', 'mac64')")
@click.option("--version", default=None, help="The version of Chrome (e.g., '89.0.4389.82')")
@click.option("--milestone", default=None, help="Milestone version (e.g., '129')")
@click.option("--dir", default=None, type=pathlib.Path, help="Directory to save the chromedriver")
@click.option("--extract", is_flag=True, help="Extract the chromedriver after downloading")
def cli(platform, version, milestone, dir, extract):
    """
    CLI command to fetch the latest Chrome driver
    """
    print(f"Fetching ChromeDriver for platform: {platform}, version: {version}, milestone: {milestone}")
    ChromePageScraper.get_chromedriver(platform=platform, version=version, milestone=milestone, d_dir=dir, is_extracted=extract)

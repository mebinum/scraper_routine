import zipfile
from typing import List
import tempfile
import requests
from splinter import Browser
from scraper.logger import log, Logger
from scraper.data_loader import DataLoader
from scraper.utils import extract_zip, sanitize_url


DOWNLOAD_URI = "https://www.stats.govt.nz/large-datasets/csv-files-for-download"
DOWNLOAD_LINKS_XPATH = "//h2[contains(text(), 'Business')]/following-sibling::ul/descendant::h3/child::a"
TEMP_PATH = ".local/temp"

def scrape_csv_files(pageURL: str, xpath_selector: str) -> List[str]:
    print("Getting csv list...")
    firstBrowser = "phantomjs"
    secondBrowser = "chrome"
    try:
        browser = Browser(firstBrowser)
    except Exception:
        Logger.warning(
            "\nYou have not properly installed or configured PhantomJS!\nYou will see an automated browser popping up and crawling,\nwhich you will not see if you have properly installed or configured PhantomJS.\nDo not close that automated browser...\n"
        )

        try:
            input("Press any key to continue...\n")
        except:
            pass

        try:
            browser = Browser(secondBrowser)
            log("Using Chrome Web Driver...\n")

        except:
            browser = Browser()
            log("Using Firefox Web Driver...\n")

    # browser.driver.maximize_window()
    browser.visit(pageURL)

    #
    csv_files = [element["href"] for element in browser.find_by_xpath(xpath_selector)]
    log(f"csv_files {csv_files}")
    return csv_files


def download_csv_files(urls: List[str]) -> dict[str, str]:
    """
    Download the CSV files from the given URLs and return a list of file paths.
    """
    downloaded_files = {}

    for url in urls:
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix= ".csv" if url.endswith(".csv") else ".zip") as temp_file:
                response = requests.get(url)
                # Check if the request was successful
                if response.status_code == 200:
                    temp_file.write(response.content)
                    downloaded_files[url] = temp_file.name
                    log(
                        f"\nDownloaded file from URL: {url}.\nSaved to file: {temp_file.name}"
                    )
                else:
                    log(
                    f"Failed to download CSV file from URL: {url}. Status code: {response.status_code}"
                )
        except requests.exceptions.RequestException as e:
            Logger.error(f"Failed to download CSV file from URL: {url}. Error: {e}")
            Logger.exception(e)

    return downloaded_files


def extract_csv_files(file_paths: dict[str, str]) -> dict[str, List[str]]:
    """
    Extract the individual CSV files from any zip files in the given file paths and return a list of CSV file paths.
    """
    csv_file_paths = {}

    for [url, file_path] in file_paths.items():
        csv_file_paths[url] = []
        if file_path.endswith(".zip"):
            try:
                # Extract the zip file
                log(f"Found zip {file_path}\nExtracting Zip...")
                extracted_files = extract_zip(file_path, TEMP_PATH)
                log(f"📦 Extracted files from {file_path}\nFiles {extracted_files}")
                # Get the path of the extracted CSV files and add them to the list
                extracted_csv_paths = [
                    file for file in extracted_files if file.endswith(".csv")
                ]
                csv_file_paths[url].extend(extracted_csv_paths)
            except zipfile.BadZipFile:
                Logger.error(
                    f"❌ Failed to extract CSV files from zip: {file_path}. The file is not a valid zip file."
                )
        elif file_path.endswith(".csv"):
            csv_file_paths[url].append(file_path)
        else:
            log(f"Skipping file with unsupported format: {file_path}")

    return csv_file_paths


def load_database_with_csvs(csv_file_paths :dict[str, List[str]]):
    for [url, filepath] in csv_file_paths.items():
        load_data_into_db(url, filepath)

def load_data_into_db(url, filepath):
    table_name = sanitize_url(url) if url.endswith(".csv") else None
    for path in filepath:
        try:
            log(f"\nLoading data from {path} downloaded from {url}")
            loader = DataLoader(path, table_name)
            log(f"loader {loader}")
            log(f"Creating table {loader.table_name}")
            loader.create_table()
            if(loader.verify_data_loaded()):
                log("✅ Table created and data loaded")
            else:
                log("✅ Table was created but data did not load")
        except Exception as e:
            Logger.error(
                    f"❌ Failed to load database with CSV file: {filepath}. Error: {e}"
                )
            Logger.exception(e)


async def task(name, work_queue):
    while not work_queue.empty():
        [url, filepath] = await work_queue.get()
        print(f"Task {name} running")
        await load_data_into_db(url, filepath)


def main() -> None:
    # Scrape CSV files
    urls = scrape_csv_files(DOWNLOAD_URI, DOWNLOAD_LINKS_XPATH)

    log(f"found {len(urls)} to download")

    # Download CSV files
    log(f"Downloading files from url {urls}")
    file_paths = download_csv_files(urls)

    # Extract CSV files
    log("Extracting all csv files")
    csv_file_paths = extract_csv_files(file_paths)

    # log(f"All extracted csvs {csv_file_paths}")
    load_database_with_csvs(csv_file_paths)


if __name__ == "__main__":
    main()

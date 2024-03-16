from scraper.utils import sanitize_url
from .dummy_data import all_csvs
import pytest

from scraper.data_loader import DataLoader


@pytest.fixture
def setup_data():
    data = {'https://www.stats.govt.nz/assets/Uploads/Annual-enterprise-survey/Annual-enterprise-survey-2021-financial-year-provisional/Download-data/annual-enterprise-survey-2021-financial-year-provisional-csv.csv': ['/var/folders/26/y8r3bfj14b11gw9t18dgmd340000gp/T/tmpgoz1cmfy.csv']}
    return data


def test_scrap_url(setup_data):

    for [url, filepath] in setup_data.items():
        for path in filepath:
            try:
                print(f"Loader for {path}")
                loader = DataLoader(path)
                # Get the data types of each column
                print(loader)
                print("Loader columns")
                print(loader.columns)
                # assert loader.table_name == "tmpgoz1cmfy"
                # # Print column names, data types, and content
                # for column in df.columns:
                #     print(f"Column Name: {column}")
                #     print(f"Data Type: {df[column].dtype}")
                #     # print(f"Content:")
                #     # print(df[column])
                #     print("\n")

            except Exception as e:
                print(f"error {e}")

def test_sanitize_url():
    url = "'https://www.stats.govt.nz/assets/Uploads/Annual-enterprise-survey/Annual-enterprise-survey-2021-financial-year-provisional/Download-data/annual-enterprise-survey-2021-financial-year-provisional-csv.csv"

    assert (
        sanitize_url(url)
        == "annual-enterprise-survey-2021-financial-year-provisional-csv"
    )

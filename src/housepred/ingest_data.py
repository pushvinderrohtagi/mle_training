import argparse
import logging
import os
import pandas as pd
import tarfile
from six.moves import urllib

HOUSING_URL = (
    "https://raw.githubusercontent.com/ageron/handson-ml/master/datasets/housing/housing.tgz"
)
HOUSING_PATH = os.path.join("data", "raw")


def fetch_housing_data(housing_url=HOUSING_URL, housing_path=HOUSING_PATH):
    """Fetch housing data from url and save to path.

    Parameters
    ----------
    housing_url : str
        Url to fetch data from.
    housing_path : str
        Path to save data to.
    """
    os.makedirs(housing_path, exist_ok=True)
    tgz_path = os.path.join(housing_path, "housing.tgz")
    urllib.request.urlretrieve(housing_url, tgz_path)
    housing_tgz = tarfile.open(tgz_path)
    housing_tgz.extractall(path=housing_path)
    housing_tgz.close()


def load_housing_data(housing_path=HOUSING_PATH):
    """Load housing data from csv file.

    Parameters
    ----------
    housing_path : str
        Path to csv file.

    Returns
    -------
    pd.DataFrame
        Dataframe containing data.
    """
    csv_path = os.path.join(housing_path, "housing.csv")
    return pd.read_csv(csv_path)


def ingest_data_main(output_dir):
    """Main function for data ingestion that takes output directory and saves data to it.

    Parameters
    ----------
    output_dir : str
        Output directory.
    """
    fetch_housing_data(HOUSING_URL, HOUSING_PATH)
    housing = load_housing_data(HOUSING_PATH)
    housing.to_csv(os.path.join(output_dir, "housing_new.csv"), index=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Data ingestion script.")
    parser.add_argument("--output_dir", type=str, help="Output directory.")
    args = parser.parse_args()
    log_dir = "/home/pushvinder/mle_training/logs/"
    logging.basicConfig(
        filename=os.path.join(log_dir, "ingest_data.log"),
        level=logging.INFO,
        format="%(levelname)s:%(message)s",
    )
    logging.info("Started data ingestion.")
    ingest_data_main(args.output_dir)
    logging.info("Finished data ingestion.")

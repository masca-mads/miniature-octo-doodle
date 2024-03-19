"""
Step 1: Read in our data
"""
import pandas as pd


def read_file(file: str) -> pd.DataFrame:
    """
    This functions takes in a string that contains information
    Regarding the location for a strava.csv file
    """

    df = pd.read_csv(file)
    print(f"Loaded {len(df)} rows of data")
    return df


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=str, help="File location for strava.csv data")
    args = parser.parse_args()

    print("Loading data ....")
    data = read_file(args.file)

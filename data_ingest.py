import pandas as pd


def read_file(file:str) -> pd.DataFrame:
    """
    This functions takes in a string that contains information
    Regarding the location for a strava.csv file
    """

    df = pd.read_csv(file)
    return df


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('file',
                        type=str,
                        help='File location for strava.csv data')
    print('Loading data ....')
    parser.add_argument('output',
                        help='resultant Pandas dataframe after reading in file')

"""
Step 2: Clean our dataframe and add some features
"""
import pandas as pd
import numpy as np

def data_cleaning(df: pd.DataFrame) -> pd.DataFrame:
    """
    Reads in our strava dataset and makes it easier to work with
    - Changes column names to be more programming friendly
    - Adds in metrics that convert some base units to Imperial units
        - distance (m) -> dist_mi (miles)
        - enhanced_altitude (m) -> alt (ft)
        - enhanced_speed (m/s) -> speed_mph (mph)
        - position_* (semicircle) -> lat, lon
    """

    df_clean = df.rename(
        columns={
            "Air Power": "aPower",
            "Cadence": "rCadence",
            "Form Power": "fPower",
            "Ground Time": "GCT",
            "Leg Spring Stiffness": "LSS",
            "Vertical Oscillation": "VO",
        }
    )

    df_clean["dist_mi"] = df_clean["distance"] / 1609.344  # meters -> miles
    df_clean["alt"] = df_clean["enhanced_altitude"] * 3.28084  # meters -> ft
    df_clean["speed_mph"] = df_clean["enhanced_speed"]  # m/s -> mph
    df_clean["lat"] = df_clean["position_lat"] * (
        180.0 / 2.0**31.0
    )  # semicircle -> latitude
    df_clean["lon"] = df_clean["position_long"] * (
        180.0 / 2.0**31.0
    )  # semicircle -> longitude
    df_clean["timestamp"] = pd.to_datetime(
        df_clean.timestamp, utc=False
    )  # Format datetime
    df_clean["fit_name"] = df_clean["datafile"].str.extract(
        r"\/(.*.fit)"
    )  # Store fit file name
    df_clean["activity_date"] = df_clean["timestamp"].apply(
        lambda x: x.date()  # Store the activity date
    )

    return df_clean

def activity_summary(df:pd.DataFrame) -> pd.DataFrame:
    """
    Generate a quick summary of all activities
    """

    summary = df.groupby('fit_name').agg({
        'speed_mph': np.mean,
        'dist_mi': np.max,
        'heart_rate': np.mean,
        'Power': np.mean,
        'cadence': np.mean
    })

    return summary


if __name__ == "__main__":
    import argparse
    import pickle

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "strava_file", help="String file location of all strava activities"
    )
    parser.add_argument("-o", "--output", help="Output path to save file")
    args = parser.parse_args()

    # Run arguments
    print("Loading in data ...")
    df_strava = pd.read_csv(args.strava_file)
    print("... cleaning data...")
    df_strava = data_cleaning(df_strava)
    df_summary = activity_summary(df_strava)
    print("\n")
    print(
        df_strava[
            ["activity_date", "fit_name", "timestamp", "dist_mi", "speed_mph"]
        ].sample(5)
    )

    # If user specified an output
    if args.output:
        # Saving output
        print("... and saving the output")
        with open(args.output, "wb+") as out:
            pickle.dump(df_strava, out)
    else:
        print("... no save file locatio specified.")
        print('To specify a save location, use the "-o" flag')

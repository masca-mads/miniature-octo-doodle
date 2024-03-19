import pandas as pd


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

    df_clean = df.rename(columns={'Air Power': 'aPower',
                                  'Cadence': 'rCadence',
                                  'Form Power': 'fPower',
                                  'Ground Time': 'GCT',
                                  'Leg Spring Stiffness': 'LSS',
                                  'Vertical Oscillation': 'VO'
                                  })
    
    df_clean['dist_mi'] = df_clean['distance'] / 1609.344                   # meters -> miles
    df_clean['alt'] = df_clean['enhanced_altitude'] * 3.28084               # meters -> ft
    df_clean['speed_mph'] = df_clean['enhanced_speed']                      # m/s -> mph
    df_clean['lat'] = df_clean['position_lat'] * (180.0 / 2.0 ** 31.0)      # semicircle -> latitude
    df_clean['lon'] = df_clean['position_long'] * (180.0 / 2.0 ** 31.0)      # semicircle -> longitude
    df_clean['timestamp'] = pd.to_datetime(df_clean.timestamp, utc=False)   # Format datetime
    df_clean['fit_name'] = df_clean['datafile'].str.extract('\/(.*.fit)')   # Store fit file name
    df_clean['activity_date'] = df_clean['timestamp'].apply(
        lambda x: x.date()                                                  # Store the activity date
    )

    return df_clean


if __name__ == '__main__':
    import argparse
    import pickle
    import pandas as pd
    
    parser = argparse.ArgumentParser()
    parser.add_argument('strava_file', help='String file location of all strava activities')
    parser.add_argument('-o', '--output', help='Output path to save file')
    args = parser.parse_args()

    # Run arguments
    print('Loading in data ...')
    df = pd.read_csv(args.strava_file)
    print('... cleaning data...')
    df = data_cleaning(df)
    print('\n')
    print(df[['activity_date', 'fit_name', 'timestamp', 'dist_mi', 'speed_mph']].sample(5))

    # If user specified an output
    if args.output:
        # Saving output
        print('... and saving the output')
        with open(args.output, 'wb+') as out:
            pickle.dump(df, out)
    else:
        print('... no save file locatio specified.')
        print('To specify a save location, use the "-o" flag')


"""
Step 3: Create some visualizations
- This is a basic plot to break up run and ride data visually
"""

import altair as alt
import pandas as pd


def hr_by_activity(df: pd.DataFrame, save_location: str = "output/summary.png"):
    """
    Takes in a summary dataframe of the Strava activities
    Generates a plot that is saved to the specified location
    """

    # We'll be using the Altair library for this exercise
    hr_scatter = (
        alt.Chart(df)
        .mark_point()
        .encode(
            x=alt.X("dist_mi:Q", title="DISTANCE (miles)"),
            y=alt.Y("speed_mph", title="SPEED (mph)"),
            color=alt.Color(
                "heart_rate",
                bin=True,
                title="HR - BINNED",
                scale=alt.Scale(scheme="orangered"),
            ),
        )
    )

    # Assumption - not running faster than 8 mph or 8 miles
    # Creating a bounding box
    run_ride_dissection = pd.DataFrame(
        {"mph_limit": [0, 8], "dist_limit": [0, 8], "activity_cat": ["run", "ride"]}
    )

    run_box = (
        alt.Chart(run_ride_dissection)
        .mark_rect()
        .encode(
            x="min(dist_limit)",
            x2="max(dist_limit)",
            y="min(mph_limit)",
            y2="max(mph_limit)",
            opacity=alt.value(0.2),
        )
    )

    text = (
        alt.Chart(run_ride_dissection)
        .mark_text(align="left", baseline="middle", dx=2, dy=5, size=11)
        .encode(x="dist_limit", text="activity_cat")
    )

    chart = hr_scatter + run_box + text
    chart.save(save_location)
    return chart


if __name__ == "__main__":
    from feature_addition import activity_summary, data_cleaning
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--pickle", help="Location for pickle file")

    parser.add_argument(
        "-n", "--new_file", help="Instead of loading saved data, load new strava CSV"
    )

    parser.add_argument("-o", "--output", help="Location to save output chart")
    args = parser.parse_args()

    # Run arguments
    # 1. First we load in the datafile
    if args.pickle:
        print("Loading data from saved file")
        strava = pd.read_pickle(args.pickle)
    # 2. Or we load a new file
    elif args.new_file:
        print("Reloading Strava data")
        activities = pd.read_csv(args.new_file)
        strava = data_cleaning(activities)
    else:
        print("No data provided... exiting")

    # 3. Then we summarize and plot
    summary_df = activity_summary(strava)
    print("Saving chart")
    hr_by_activity(summary_df, args.output)

import pandas as pd

def participating_nation_overtime(df , col_name):
    df = pd.DataFrame(df.drop_duplicates(['Year' ,col_name])['Year']
                      .value_counts()
                      .reset_index()
                      .sort_values('Year')
                      )
    return df

def leaderboard(
    df,
    entity="athlete",
    year="Overall",
    sport="Overall",
    top_n=20
):
    # only medal-winning rows
    medal_df = df.dropna(subset=["Medal"])

    # normalize inputs
    entity = entity.lower()
    year = str(year).lower()
    sport = str(sport).lower()

    # filter by year
    if year != "overall":
        medal_df = medal_df[medal_df["Year"] == int(year)]

    # filter by sport
    if sport != "overall":
        medal_df = medal_df[medal_df["Sport"].str.lower() == sport]

    # choose grouping column
    if entity == "athlete":
        group_col = "Name"
        extra_cols = ["Sport", "NOC"]

        # 🔥 DEDUPLICATE medals per athlete
        medal_df = medal_df.drop_duplicates(
            subset=["Name", "Year", "Sport", "Event", "Medal"]
        )

    elif entity == "country":
        group_col = "region" if "region" in medal_df.columns else "NOC"
        extra_cols = []

        # 🔥 DEDUPLICATE medals per country
        medal_df = medal_df.drop_duplicates(
            subset=[group_col, "Year", "Sport", "Event", "Medal"]
        )

    else:
        raise ValueError("entity must be 'athlete' or 'country'")

    # aggregate medals
    result = (
        medal_df
        .groupby(group_col)
        .size()
        .reset_index(name="Medals")
        .sort_values("Medals", ascending=False)
        .head(top_n)
        .reset_index(drop=True)
    )

    # attach extra columns for athletes
    if extra_cols:
        result = result.merge(
            medal_df[[group_col] + extra_cols].drop_duplicates(group_col),
            on=group_col,
            how="left"
        )

    # ranking
    result.index = result.index + 1
    result.index.name = "Rank"

    return result


    
    
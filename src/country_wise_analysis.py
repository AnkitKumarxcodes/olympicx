import pandas as pd


def country_successful_sport(df , country):
    temp_df = df.dropna(subset = ['Medal'])
    temp_df = temp_df.drop_duplicates(subset = ["Team" , "NOC" , "Year" , "City" , "Sport" , "Event" , "Medal" , "Games"])
    new_df = temp_df[temp_df['region'] == country]
    return new_df

def year_wise_medals(df , country):
    new_df = country_successful_sport(df , country)
    new_df = new_df.groupby(['Year']).count()['Medal'].reset_index()
    new_df.rename(columns={'Year':'Edition'} , inplace=True)
    return new_df

def top_10_athlete(df , country):
    medal_tally = df.dropna(subset = ["Medal"])
    medal_tally = medal_tally[medal_tally['region'] == country]

    result =  medal_tally['Name'].value_counts().reset_index().head(10).merge(df ).drop_duplicates('Name')[['Name' , 'count'  , 'Sport']].reset_index(drop = True)
    result.index = result.index +1
    return result
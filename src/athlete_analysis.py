import pandas as pd

def age_distribution(df ):
    athlete_df = df.drop_duplicates(subset = ['Name' , 'region'])
    x1 = athlete_df['Age'].dropna()

    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()
    return x1 , x2 ,x3 ,x4 

def sports_distribution(df , core_sports , medal_type = "Gold"):
    athlete_df = df.drop_duplicates(subset = ['Name' , 'region'])
    x = []
    name =[]
    if core_sports == []:
        olympic_sports = df['Sport'].value_counts()
        core_sports = olympic_sports[olympic_sports >= 60].index.tolist() 
    for sport in core_sports:
        temp_df = athlete_df[athlete_df['Sport']==sport]
        if medal_type == "ALL":
            ages = temp_df[temp_df['Medal'].notna()]['Age'].dropna()
        else:
            ages = temp_df[temp_df['Medal'] == medal_type]['Age'].dropna()

        if not ages.empty:
            x.append(ages)
            name.append(sport)
    
    return x , name

def height_weight_df(df , sport):
    athlete_df = df.drop_duplicates(subset = ['Name' , 'region'])
    athlete_df['Medal'].fillna('No Medal' , inplace = True)
    if sport != 'overall':
        athlete_df = athlete_df[athlete_df['Sport'] == sport]
    return athlete_df

def men_vs_women(df):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()

    final = men.merge(women, on='Year', how='left')
    final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)

    final.fillna(0, inplace=True)

    return final
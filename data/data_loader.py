import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).parent 

def load_data():
    df = pd.read_csv(DATA_DIR / "athlete_events.csv")
    region_df = pd.read_csv(DATA_DIR / "noc_regions.csv")
    return df, region_df

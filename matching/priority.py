import pandas as pd
from .scoring import compute_simple_score

def build_compatibility_matrix(adopters_df, dogs_df):
    available_dogs = dogs_df[dogs_df["Status"].str.lower() == "available"]

    rows = []

    for _, adopter in adopters_df.iterrows():
        for _, dog in available_dogs.iterrows():
            score = compute_simple_score(adopter, dog)

            rows.append({
                "Adopter_Name": adopter["Adopter's Name"],
                "Dog_Name": dog["Name"],
                "Score": score,
                "Application_Date": adopter.get("App Submitted Date")
            })

    df = pd.DataFrame(rows)
    df["Application_Date"] = pd.to_datetime(df["Application_Date"], errors="coerce")
    return df

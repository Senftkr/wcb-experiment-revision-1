# updated to force redeploy
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


def build_priority_table(compat_df, min_score=0):
    # Filter by minimum score
    filtered = compat_df[compat_df["Score"] >= min_score].copy()

    # Sort by dog, then score (desc), then application date (asc)
    filtered = filtered.sort_values(
        by=["Dog_Name", "Score", "Application_Date"],
        ascending=[True, False, True]
    )

    # Assign rank numbers
    filtered["Rank"] = filtered.groupby("Dog_Name").cumcount() + 1

    # Convert rank → FIL / NIL / TIL
    def label_rank(r):
        if r == 1:
            return "FIL"
        if r == 2:
            return "NIL"
        if r == 3:
            return "TIL"
        return ""

    filtered["Line_Status"] = filtered["Rank"].apply(label_rank)

    return filtered

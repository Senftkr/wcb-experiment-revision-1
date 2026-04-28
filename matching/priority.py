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
                "Application_Date": adopter["App Submitted Date"]
            })

    df = pd.DataFrame(rows)
    df["Application_Date"] = pd.to_datetime(df["Application_Date"], errors="coerce")
    return df


def build_priority_table(compat_df, min_score=60):
    df = compat_df[compat_df["Score"] >= min_score].copy()

    df = df.sort_values(
        by=["Dog_Name", "Score", "Application_Date"],
        ascending=[True, False, True]
    )

    results = []

    for dog, group in df.groupby("Dog_Name"):
        group = group.reset_index(drop=True)

        fil = group.iloc[0] if len(group) > 0 else None
        nil = group.iloc[1] if len(group) > 1 else None
        til = group.iloc[2] if len(group) > 2 else None

        results.append({
            "Dog_Name": dog,

            "FIL_Adopter": fil["Adopter_Name"] if fil is not None else None,
            "FIL_Date": fil["Application_Date"] if fil is not None else None,
            "FIL_Score": fil["Score"] if fil is not None else None,

            "NIL_Adopter": nil["Adopter_Name"] if nil is not None else None,
            "NIL_Date": nil["Application_Date"] if nil is not None else None,
            "NIL_Score": nil["Score"] if nil is not None else None,

            "TIL_Adopter": til["Adopter_Name"] if til is not None else None,
            "TIL_Date": til["Application_Date"] if til is not None else None,
            "TIL_Score": til["Score"] if til is not None else None,
        })

    return pd.DataFrame(results)

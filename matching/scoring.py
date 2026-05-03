import pandas as pd
import numpy as np

def compute_simple_score(adopter, dog):
    score = 0

    prefs = str(adopter.get("Who/what kind of dogs do they want?", "")).lower()
    notes = str(adopter.get("Call Notes / Placement Decision (Completed on Call)", "")).lower()
    kids = str(adopter.get("Have kids? (incl. age)", "")).lower()
    dogs_owned = str(adopter.get("Have dogs? (inc. Breed, Age, Gender)", "")).lower()
    cats_owned = str(adopter.get("Have cats?", "")).lower()

    good_kids = str(dog.get("Good with Kids", "")).lower()
    good_dogs = str(dog.get("Good with Dogs", "")).lower()
    good_cats = str(dog.get("Good with Cats", "")).lower()
    breed = str(dog.get("Breed", "")).lower()
    tail = str(dog.get("Tail", "")).lower()
    age = dog.get("Age", None)

    # Kids
    kids_clean = kids.replace("none", "").replace("n/a", "").strip()

        if "yes" in good_kids:
         score += 20
        elif "no" in good_kids:
         score -= 30
    else:
        if "no" in good_kids:
         score += 10

    # Dogs
    if dogs_owned.strip() != "" and "no" not in dogs_owned:
        if "yes" in good_dogs or "slow intro" in good_dogs:
         score += 20
        elif "no" in good_dogs:
         score -= 25
    else:
        if "only" in str(dog.get("Special Needs", "")).lower():
         score += 15

    # Cats
    if "yes" in cats_owned:
        if "yes" in good_cats:
         score += 20
        elif "no" in good_cats:
         score -= 30

    # Breed preferences
    if "no mix" in prefs or "no mix" in notes:
        if "mix" in breed:
         score -= 30

    if "puppy" in prefs or "puppy" in notes:
        if age is not None and age <= 1.5:
         score += 20

    if "under 5" in prefs:
        if age is not None and age <= 5:
         score += 15

    if "male" in prefs:
        if str(dog.get("Sex", "")).lower() == "male":
         score += 10

    if "female" in prefs:
        if str(dog.get("Sex", "")).lower() == "female":
         score += 10

    if "dock" in prefs:
        if "dock" in tail:
         score += 10

    # Special needs
    special = str(dog.get("Special Needs", "")).lower()
    if special not in ["", "none", "nan"]:
        if "boxer exp" in prefs or "boxer exp" in notes:
         score += 10
        else:
         score -= 10

    return max(0, min(100, score))

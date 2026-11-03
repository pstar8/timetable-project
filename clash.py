import pandas as pd
from itertools import combinations

def load_timetable(file):
    name = getattr(file, "name", str(file)).lower()
    if name.endswith((".xlsx", ".xls")):
        df = pd.read_excel(file)
    else:
        df = pd.read_csv(file)
        df.columns = df.columns.str.strip().str.lower()
        for col in ["course", "day", "hall"]:
            df[col] = df[col].astype(str).str.strip()
        df["start"] = pd.to_datetime(df["start"].astype(str).str.strip().str[:5], format="%H:%M").dt.time
        df["end"] = pd.to_datetime(df["end"].astype(str).str.strip().str[:5], format="%H:%M").dt.time
    return df 

def find_clashes(df):
    clashes = []
    for (hall, day), group in df.groupby(["hall", "day"]):
        rows = group.to_dict("records")
        combinations(rows, 2)
        for a, b in combinations(rows, 2):
            if a["start"] < b["end"] and b["start"] < a["end"]:
                overlap_start = max(a["start"], b["start"])
                overlap_end = min((a["end"], b["end"]))
                clashes.append({
                    "course_a": a["course"],
                    "course_b": b["course"],
                    "hall": hall,
                    "day": day,
                    "overlap_start": overlap_start,
                    "overlap_end": overlap_end
                })
    return clashes

if __name__ == "__main__":
    df = load_timetable("data/sample_timetable.csv")
    for c in find_clashes(df):
        print(c)
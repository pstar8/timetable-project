import streamlit as st
import pandas as pd
from clash import load_timetable, find_clashes

st.title("Timetable Clash Checker")
st.write("Upload a timetable to find hall and time clashes.")

uploaded = st.file_uploader("Upload timetable (CSV)", type=["csv"])

if uploaded is not None:
    df = load_timetable(uploaded)
    clashes = find_clashes(df)

    if not clashes:
        st.success("No clashes found.")
    else:
        st.error(f"{len(clashes)} clash(es) found")
        df = pd.DataFrame(clashes)
        df["overlap_start"] = df["overlap_start"].apply(lambda t: t.strftime("%H:%M"))
        df["overlap_end"] = df["overlap_end"].apply(lambda t: t.strftime("%H:%M"))
        

        # TODO turn `clashes` into a DataFrame, make the two time
        # columns readable (e.g. "09:00"), and show it with st.dataframe
        # Times are datetime.time objects. .apply(lambda t: t.strftime("%H:%M")) on a column turns them into clean text
        # Also worth showing: a line per clash like “ECN 201 vs CSC 201, LT1, Monday, 09:00 to 11:00”. Try it with st.write in a loop if the table feels dull.
import streamlit as st
import pandas as pd
import numpy as np

DATE_COLUMN = "date/time"
DATA_URL = (
    "https://s3-us-west-2.amazonaws.com/"
    "streamlit-demo-data/uber-raw-data-sep14.csv.gz"
)


@st.cache
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis="columns", inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])

    return data


st.title("Uber Pickups in NYC")
data_load_state = st.text("Loading data...")
data = load_data(10000)
data_load_state.text("Done! (using st.cache)")

st.subheader("Raw Data")
st.write(data)

st.subheader("Number of pickups by hour")
hist_values = np.histogram(data[DATE_COLUMN].dt.hour, bins=24, range=(0, 24))[0]
st.bar_chart(hist_values)

# Streamlit has magic to interpret markdown, data, and charts if it's on a
# line of it's own. Can be disabled. 
# See: https://docs.streamlit.io/library/api-reference/write-magic/magic
"Uncheck this to filter on pickup times"

if st.checkbox("Show all pickups"):
    st.subheader("Map of all pickups")
    # Note to self: this funciton expects columns with names "lat" and "lon". To
    # customize this function, including which columns it uses see
    # https://docs.streamlit.io/library/api-reference/charts/st.pydeck_chart
    st.map(data)
else:
    hour_to_filter = st.slider("hour", 0, 23, 17)  # min: 0h, max: 23h, default: 17h
    filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]
    st.subheader(f"Map of all pickups at {hour_to_filter}:00")
    st.map(filtered_data)


st.columns()
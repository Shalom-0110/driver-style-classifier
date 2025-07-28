import streamlit as st
import fastf1 as ff1
from fastf1 import plotting
import joblib
import plotly.express as px
from utils.features import extract_features

model = joblib.load("kmeans.pkl")

st.set_page_config(page_title="Driver Style Classifier", layout="wide")

st.title("🏎️ Driver Style Classifier")
st.markdown("Analyze and classify F1 driver styles based on telemetry data.")

st.sidebar.header("Session Selection")
season = st.sidebar.selectbox("Season", list(reversed(range(2018, 2025))))
event = st.sidebar.selectbox("Event", ["Monza", "Silverstone", "Spa", "Bahrain"])
session = st.sidebar.selectbox("Session Type", ["Race", "Qualifying"])

if "session_loaded" not in st.session_state:
    st.session_state.session_loaded = False

if st.sidebar.button("Analyze Session"):
    with st.spinner("Loading session data..."):
        ff1.Cache.enable_cache(".cache")
        session_data = ff1.get_session(season, event, session)
        session_data.load()
        st.session_state.session_data = session_data
        st.session_state.session_loaded = True
        st.success(f"Loaded {event} {session} from {season}!")


if st.session_state.session_loaded:
    session_data = st.session_state.session_data
    drivers = session_data.drivers
    driver_names = []
    for d in drivers:
        info = session_data.get_driver(d)
        full_name = info.get("FullName") or info.get("Surname") or d
        driver_names.append(full_name)

    selected_driver = st.selectbox("Select a driver", driver_names)
    driver_id = drivers[driver_names.index(selected_driver)]

    try:
        lap = session_data.laps.pick_drivers(driver_id).pick_fastest()
        tel = lap.get_car_data().add_distance()

        X = extract_features(lap)
        style_index = model.predict(X)[0]
        style_labels = {
            0: "Aggressive Cornering",
            1: "Smooth & Consistent",
            2: "Late Braking",
            3: "Balanced",
        }
        label = style_labels.get(style_index, f"Style {style_index}")

        st.subheader("🧠 Driver Style Classification")
        st.markdown(f"**{selected_driver}** was classified as driving in **{label}**")


        fig = px.line(tel, x="Distance", y="Speed",
                      title="Speed vs Distance",
                      labels={"Speed": "Speed (km/h)", "Distance": "Track Distance (m)"})
        fig.update_traces(line=dict(color="cyan"))
        fig.update_layout(template="plotly_dark")

        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"Could not load data for {selected_driver}: {e}")

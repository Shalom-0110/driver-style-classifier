# 🏎️ Driver Style Classifier

Hi! This is a simple little Streamlit app I built to classify F1 driver styles based on telemetry data. It uses FastF1 to fetch race data, extracts key features, and then uses a KMeans model to guess what kind of driving style a driver has like smooth, aggressive, or late braking.

### What it does:
- Lets you pick a season, track, session, and driver
- Finds their fastest lap
- Analyzes their telemetry
- Classifies their style (and shows a pretty graph too)

### Tech used:
Streamlit, FastF1, Plotly, scikit-learn, and Python of course 

### What’s coming next:
- Throttle vs Distance
- Brake heatmap
- Compare two drivers side-by-side


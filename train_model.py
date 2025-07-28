import fastf1 as ff1
from sklearn.cluster import KMeans
import pickle
import numpy as np

ff1.Cache.enable_cache(".cache")

drivers = ["VER", "HAM", "LEC", "NOR"]
sessions = [("Monza", "Race", 2023), ("Silverstone", "Race", 2023)]

X = []

for gp, sess_type, year in sessions:
    session = ff1.get_session(year, gp, sess_type)
    session.load()

    for drv in drivers:
        laps = session.laps.pick_driver(drv)
        if not laps.empty:
            lap = laps.pick_fastest()
            tel = lap.get_car_data().add_distance()
            df = tel

            throttle_var = df['Throttle'].var()
            brake_spikes = (df['Brake'] > df['Brake'].mean() + 2 * df['Brake'].std()).sum()
            avg_speed = df['Speed'].mean()

            X.append([throttle_var, brake_spikes, avg_speed])

X = np.array(X)

model = KMeans(n_clusters=3, random_state=42)
model.fit(X)


with open("kmeans.pkl", "wb") as f:
    pickle.dump(model, f)

print("Model trained and saved as kmeans.pkl")

import pandas as pd

def extract_features(lap):
    tel = lap.get_car_data().add_distance()
    
    avg_speed = tel['Speed'].mean()
    max_throttle = tel['Throttle'].max()
    max_brake = tel['Brake'].max()

    return [[avg_speed, max_throttle, max_brake]]

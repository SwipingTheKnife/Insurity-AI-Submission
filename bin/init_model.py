#This file is being used to create the model using training data
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.tree import DecisionTreeRegressor
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder
from sklearn.model_selection import train_test_split
import joblib


data = pd.read_csv("../data/trainingData.csv")

X = data.drop(columns=['trip_id', 'driver_id', 'start_time', 'end_time', 'claim'])
y = data['claim']

categorical_features = ['weather', 'time_of_day']
numerical_features = [col for col in X.columns if col not in categorical_features]

preprocessor = ColumnTransformer(
    transformers=[
        ('num', 'passthrough', numerical_features),
        ('cat', OneHotEncoder(), categorical_features)
    ]
)

tree = DecisionTreeRegressor(max_depth=5, random_state=42)
pipeline = Pipeline([
    ('preprocessor', preprocessor),
    ('tree', tree)
])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

pipeline.fit(X_train, y_train)

scaler = MinMaxScaler(feature_range=(0, 100))
y_train_pred = pipeline.predict(X_train).reshape(-1, 1)
scaler.fit(y_train_pred)

joblib.dump(pipeline, 'discount_tree_pipeline.pkl')
joblib.dump(scaler, 'discount_scaler.pkl')

new_trip = pd.DataFrame({
    'start_lat': [40.73],
    'start_lon': [-74.15],
    'end_lat': [40.77],
    'end_lon': [-73.96],
    'distance_miles': [70.9],
    'duration': [31],
    'avg_speed': [57.0],
    'max_speed': [60.5],
    'hard_brakes': [3],
    'time_of_day': ['morning'],
    'weather': ['snow']
})

raw_pred = pipeline.predict(new_trip).reshape(-1, 1)
normalized_pred = scaler.transform(raw_pred)

discount_min = 5
discount_max = 20
discount = discount_min + (normalized_pred / 100) * (discount_max - discount_min)

print(f"Predicted discount: {discount[0][0]:.2f}%")
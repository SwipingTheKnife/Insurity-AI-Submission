#This file is being used to create the model using training data
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, roc_auc_score
from sklearn.pipeline import Pipeline
from sklearn.tree import DecisionTreeRegressor, DecisionTreeClassifier
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder
from sklearn.model_selection import train_test_split
import joblib
from discount_model import DiscountModel


data = pd.read_csv("../data/trainingData.csv")

X = data.drop(columns=['trip_id', 'driver_id', 'start_time', 'end_time', 'claim'])
y = data['claim']

print(y.value_counts())

categorical_features = ['weather', 'time_of_day']
numerical_features = [col for col in X.columns if col not in categorical_features]

preprocessor = ColumnTransformer(
    transformers=[
        ('num', 'passthrough', numerical_features),
        ('cat', OneHotEncoder(), categorical_features)
    ]
)


tree = RandomForestClassifier(
    n_estimators=200,        # more trees → smoother probabilities
    max_depth=None,          # let each tree grow fully
    min_samples_leaf=20,     # avoid overfitting tiny leaves
    random_state=42
)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

pipeline = Pipeline([
    ('preprocessor', preprocessor),
    ('tree', tree),
])

pipeline.fit(X_train, y_train)

y_train_proba = pipeline.predict_proba(X_train)[:, 1]


discount_model = DiscountModel(pipeline)

discount_model.save('discount_model.pkl')

#Evaluation of model
y_test_pred = pipeline.predict(X_test)
y_test_proba = pipeline.predict_proba(X_test)[:, 1]

acc = accuracy_score(y_test, y_test_pred)
roc = roc_auc_score(y_test, y_test_proba)

print(f"Test Accuracy: {acc:.3f}")
print(f"Test ROC-AUC: {roc:.3f}")


new_trip = pd.DataFrame({
    'start_lat': [40.73],
    'start_lon': [-74.15],
    'end_lat': [40.77],
    'end_lon': [-73.96],
    'distance_miles': [70.9],
    'duration': [31],
    'avg_speed': [65],
    'max_speed': [80],
    'hard_brakes': [10],
    'time_of_day': ['morning'],
    'weather': ['snow']
})

pred_discount = discount_model.predict_discount(new_trip)
print(f"Predicted discount: {pred_discount[0][0]:.2f}%")
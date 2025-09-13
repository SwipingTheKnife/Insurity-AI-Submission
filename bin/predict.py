# predict.py
# This script loads the trained discount model and predicts discounts for new trips
from discount_model import DiscountModel
import pandas as pd
import joblib

# ----------------------------
# Step 1: Load trained model
# ----------------------------
discount_model = DiscountModel.load("discount_model.pkl")


# ----------------------------
# Step 2: Load new data (CSV of trips without 'claim')
# ----------------------------
# Example: a file "new_trips.csv"
data = pd.read_csv("../data/Testdata.csv")

# ----------------------------
# Step 3: Predict discounts
# ----------------------------
pred_discounts = discount_model.predict_discount(data)

# Flatten results into a 1D list
pred_discounts = pred_discounts.flatten()

# ----------------------------
# Step 4: Add results to DataFrame
# ----------------------------
data["predicted_discount"] = [f"{d:.2f}%" for d in pred_discounts]
print(data[["predicted_discount"]])

with open("my_file.txt", "w") as f:
    f.write("\n".join(data["predicted_discount"].astype(str)))
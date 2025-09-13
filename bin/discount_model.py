import joblib


class DiscountModel:
    def __init__(self, pipeline, discount_min=0, discount_max=20):
        self.pipeline = pipeline
        self.discount_min = discount_min
        self.discount_max = discount_max

    def predict_discount(self, trip_df):
        raw_proba = self.pipeline.predict_proba(trip_df)[:, 1]  # 0 to 1
        discount = self.discount_min + raw_proba * (self.discount_max - self.discount_min)
        print(discount)
        discount = discount.reshape(-1, 1)
        return discount

    def save(self, filename):
        joblib.dump(self, filename)

    @staticmethod
    def load(filename):
        return joblib.load(filename)
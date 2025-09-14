import json
import os
from typing import List

import jwt
import pandas as pd
from fastapi import APIRouter, Request, Cookie, Depends, HTTPException, UploadFile, File
from jose import JWTError
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates

from models.discount_model import DiscountModel
from src.models.user_model import User
from src.models.trips_model import Trips, Base
from src.db_conn import engine, get_db

router = APIRouter()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "../templates"))

Base.metadata.create_all(bind=engine)

SECRET_KEY = "secret"
ALGORITHM = "HS256"

def get_current_user(
    access_token: str = Cookie(None),  # 👈 pulls the cookie back
    db: Session = Depends(get_db)
):
    if not access_token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    try:
        payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(User).filter(User.user_id == int(user_id)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


@router.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    trips = db.query(Trips).filter(Trips.driver_id == current_user.user_id).all()

    if trips:
        trip_data = pd.DataFrame([{
            "start_lat": t.start_lat,
            "start_lon": t.start_lon,
            "end_lat": t.end_lat,
            "end_lon": t.end_lon,
            "distance_miles": t.distance_miles,
            "duration": t.duration,
            "avg_speed": t.avg_speed,
            "max_speed": t.max_speed,
            "hard_brakes": t.hard_brakes,
            "time_of_day": t.time_of_day,
            "weather": t.weather
        } for t in trips])

        discount_model = DiscountModel.load(BASE_DIR + "/../../models/discount_model.pkl")

        trip_data["predicted_discount"] = discount_model.predict_discount(trip_data).flatten()


        trip_data["driving_score"] = (trip_data["predicted_discount"]) * 5

        avg_driving_score = trip_data["driving_score"].mean()
        avg_discount = trip_data["predicted_discount"].mean()
    else:
        avg_driving_score = 0
        avg_discount = 0

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "user": current_user,
            "trips": trips,
            "avg_driving_score": round(avg_driving_score, 1),
            "avg_discount": round(avg_discount, 1)
        }
    )


class TripInput(BaseModel):
    start_time: str
    end_time: str
    start_lat: float
    start_lon: float
    end_lat: float
    end_lon: float
    distance_miles: float
    duration: float
    avg_speed: float
    max_speed: float
    hard_brakes: int
    time_of_day: str
    weather: str

@router.post("/upload_trips")
async def upload_trips(trips_list: List[TripInput],
                       current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not trips_list:
        raise HTTPException(status_code=400, detail="Empty JSON list")

    # Insert into database
    for trip_input in trips_list:
        trip_data = trip_input.dict()
        trip_data["driver_id"] = int(current_user.user_id)
        trip = Trips(**trip_data)
        db.add(trip)

    db.commit()

    all_trips = db.query(Trips).filter(Trips.driver_id == current_user.user_id).all()

    all_trip_df = pd.DataFrame([{
        "start_lat": t.start_lat,
        "start_lon": t.start_lon,
        "end_lat": t.end_lat,
        "end_lon": t.end_lon,
        "distance_miles": t.distance_miles,
        "duration": t.duration,
        "avg_speed": t.avg_speed,
        "max_speed": t.max_speed,
        "hard_brakes": t.hard_brakes,
        "time_of_day": t.time_of_day,
        "weather": t.weather
    } for t in all_trips])



    # Predict discount
    discount_model = DiscountModel.load("models/discount_model.pkl")
    discounts = discount_model.predict_discount(all_trip_df).flatten()
    avg_discount = float(discounts.mean())

    avg_driving_score = (
            (avg_discount - discount_model.discount_min) /
            (discount_model.discount_max - discount_model.discount_min) * 100
    )

    return {"avg_discount": avg_discount,
            "avg_driving_score": avg_driving_score,
            "new_trips": [
                {
                    "distance_miles": trip.distance_miles,
                    "duration": trip.duration,
                    "weather": trip.weather
                }
                for trip in trips_list
            ],
            }
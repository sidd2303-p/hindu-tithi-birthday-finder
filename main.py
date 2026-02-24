from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

TITHI_NAMES = [
    "Pratipada", "Dwitiya", "Tritiya", "Chaturthi", "Panchami",
    "Shashthi", "Saptami", "Ashtami", "Navami", "Dashami",
    "Ekadashi", "Dwadashi", "Trayodashi", "Chaturdashi", "Purnima",
    "Pratipada", "Dwitiya", "Tritiya", "Chaturthi", "Panchami",
    "Shashthi", "Saptami", "Ashtami", "Navami", "Dashami",
    "Ekadashi", "Dwadashi", "Trayodashi", "Chaturdashi", "Amavasya"
]

def approx_tithi(date):
    """
    Approximate lunar tithi calculation.
    Accuracy: demo / festival-level (resume acceptable)
    """
    known_new_moon = datetime(2023, 1, 21)  # reference Amavasya
    days_diff = (date - known_new_moon).days
    tithi_index = days_diff % 30
    return TITHI_NAMES[tithi_index], tithi_index

@app.post("/get-hindu-birthday")
def hindu_birthday(
    dob: str = Form(...),
    target_year: int = Form(...)
):
    birth_date = datetime.strptime(dob, "%Y-%m-%d")
    tithi_name, tithi_index = approx_tithi(birth_date)

    # search in selected year
    check_date = datetime(target_year, 1, 1)

    for _ in range(370):
        _, idx = approx_tithi(check_date)
        if idx == tithi_index:
            return {
                "janma_tithi": tithi_name,
                "hindu_birthday_year": target_year,
                "hindu_birthday_date": check_date.strftime("%d %B %Y")
            }
        check_date += timedelta(days=1)

    return {"error": "Tithi not found"}
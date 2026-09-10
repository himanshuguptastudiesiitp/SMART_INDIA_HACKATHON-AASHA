from fastapi import FastAPI
import requests
from datetime import datetime , timedelta
from apscheduler.schedulers.background import BackgroundScheduler

from database import engine, Base, SessionLocal
import models

app = FastAPI()

Base.metadata.create_all(bind=engine)

def calculate_risk(rainfall,soil_moisture):
    if rainfall > 5 and soil_moisture > 0.35:
        return "High"
    elif rainfall >2 or soil_moisture > 0.35:
        return "Moderate"
    else:
        return "Low"

def calculate_combined_risk(
        rainfall,
        soil_moisture,
        last_6_hours_rainfall,
        last_12_hours_rainfall,
        last_3_days_rainfall,
        last_5_days_rainfall,
        last_12_days_rainfall,
        rainfall_trend

):
    score=0

    # current rainfall =0
    if rainfall > 5:
        score += 15

    elif rainfall> 2:
        score +=8

    # soil moisture
    if soil_moisture > 0.35:
        score+=20
    elif soil_moisture > 0.25:
        score+=10

    # short-term rainfall
    if last_6_hours_rainfall > 10:
        score+=20
    elif last_6_hours_rainfall > 5:
        score+=10

    #12- hours rainfall
    if last_12_hours_rainfall > 20:
        score +=10
    elif last_12_hours_rainfall > 10:
        score +=5
    # 3 days accumulated rainfall
    if last_3_days_rainfall > 100:
        score +=10
    elif last_3_days_rainfall> 50:
        score +=5

    # 5 days accumulated rainfall

    if last_5_days_rainfall > 150:
        score +=5
    # 12 days accumulated rainfall
    if last_12_days_rainfall > 250:
        score+=5

    # rainfall trend
    if rainfall_trend == "Increasing":
        score+=10
    # risk classification 
    
    if score >=70:
        risk = "High"
    elif score >= 40 :
        risk = "Moderate"
    else:
        risk = "Low"

    return risk, score

def generate_alert(risk,risk_score):
    if risk =="High":
        return "ALERT: High landslide risk detected. Immediate action required ."
    elif risk=="Moderate":
        return "WARNING:  Moderate landslide risk detected. Continue monitoring."
    else:
        return "No immediate landslide risk detected."
    
def refresh_weather_data():

    latitude =26.0
    longitude= 85.0 
    url="https://api.open-meteo.com/v1/forecast"

    params={
        "latitude":latitude,
        "longitude":longitude,
        "hourly":"precipitation,soil_moisture_0_to_1cm",
        "forecast_days":12,
        "timezone":"Asia/Kolkata"
    }
    response = requests.get(url,params=params)
    data=response.json()

    db=SessionLocal()

    try:
        rainfall_values = data["hourly"]["precipitation"]
        soil_moisture_values=data["hourly"]["soil_moisture_0_to_1cm"]
        time_values=data["hourly"]["time"]

        for current_index,(time, rainfall, soil_moisture) in enumerate(
            zip(time_values, rainfall_values, soil_moisture_values

            )
        ):

        
        
            rainfall_record=models.Rainfall()


            rainfall_record.latitude=data["latitude"]
            rainfall_record.longitude=data["longitude"]

            
            rainfall_record.timestamp=datetime.fromisoformat(time)
            rainfall_record.precipitation = rainfall
            rainfall_record.unit=data["hourly_units"]["precipitation"]

            # last 6 hours rainfall
            last_6_hours_rainfall = sum(
                rainfall_values[max(0,current_index -5):current_index +1]
            )

            # previou 6 hours rainfall
            previous_6_hours_rainfall = sum(
                rainfall_values[max(0,current_index -11):current_index -5]
            )

            #last 12 hours rainfall
            last_12_hours_rainfall = sum(rainfall_values[
                max(0,current_index -11):current_index +1
            ])
            # last 3 days rainfall
            last_3_days_rainfall = sum(
                rainfall_values[max(0,current_index - 71):current_index +1]
            )

            # last 5 days rainfall
            last_5_days_rainfall = sum(
                rainfall_values[max(0,current_index -119):current_index +1]
            )
            # last 12 days rainfall
            last_12_days_rainfall=sum(
                rainfall_values[max(0,current_index - 287):current_index + 1]
            )

            # rainfall trend 
            if last_6_hours_rainfall > previous_6_hours_rainfall:
                rainfall_trend = "Increasing"
            elif last_6_hours_rainfall < previous_6_hours_rainfall:
                rainfall_trend = "Decreasing"
            else:
                rainfall_trend = "Stable"

            soil_moisture = soil_moisture if soil_moisture is not None else 0 


            risk,score= calculate_combined_risk(
                rainfall,
                soil_moisture,
                last_6_hours_rainfall,
                last_12_hours_rainfall,
                last_3_days_rainfall,
                last_5_days_rainfall,
                last_12_days_rainfall,
                rainfall_trend
            )

            rainfall_record.risk_level=risk
            rainfall_record.risk_score=score
            soil_data=models.SoilMoisture()

            soil_data.latitude=data["latitude"]
            soil_data.longitude=data["longitude"]
            soil_data.timestamp=datetime.fromisoformat(time)
            soil_data.moisture=soil_moisture
            soil_data.unit=data["hourly_units"]["soil_moisture_0_to_1cm"]

            existing_record =db.query(models.Rainfall).filter_by(
                latitude=data["latitude"],
                longitude=data["longitude"],
                timestamp=datetime.fromisoformat(time)
            ).first()

            if existing_record:
                continue

            db.add(rainfall_record)
            db.add(soil_data)



        db.commit()

        print("Weather data refreshed and saved to database.")

    finally:
        db.close()


scheduler=BackgroundScheduler()

scheduler.add_job(
    refresh_weather_data,
    "interval",
    hours=1
)

scheduler.start()



def calculate_risk_score(rainfall,soil_moisture):
    rainfall_score=min(rainfall*10,50)
    soil_score = min(soil_moisture*100,50)

    return rainfall_score+soil_score
    
    

@app.get("/test-risk")

def test_risk():
    rainfall = 6
    soil_moisture= 0.40
    last_6_hours_rainfall=12
    rainfall_trend="Increasing"

    risk,score = calculate_combined_risk(
        rainfall,
        soil_moisture,
        0,
        0,
        0,
        0,
        0,
        rainfall_trend
    )

    alert=generate_alert(risk,score)

    return{
        "rainfall":rainfall,
        "soil_moisture":soil_moisture,
        "last_6_hours_rainfall":last_6_hours_rainfall,
        "rainfall_trend":rainfall_trend,
        "risk":risk,
        "risk_score":score,
        "alert":alert
    }

@app.get("/")
def home():
    return{"message":"sih26001 backend is running. "}

@app.get("/rainfall")
def  get_rainfall(latitude:float,longitude:float):
    db=SessionLocal()

    try:
        url = "https://api.open-meteo.com/v1/forecast"

        params= {
            "latitude":latitude,
            "longitude": longitude,
            "hourly":"precipitation,soil_moisture_0_to_1cm",
            "forecast_days":1,
            "timezone":"Asia/Kolkata"
        }

        response = requests.get(url, params=params)
        data= response.json()

        rainfall_values= data["hourly"]["precipitation"]
        soil_moisture_values=data["hourly"]["soil_moisture_0_to_1cm"]
        time_values=data["hourly"]["time"]

        hourly_rainfall=data["hourly"]["precipitation"]
        hourly_soil_moisture=data["hourly"]["soil_moisture_0_to_1cm"]

        combined_risks=[]
        combined_scores=[]


        for time,rainfall, soil_moisture in zip(
            time_values,
            rainfall_values,
            soil_moisture_values
        ):

            rainfall_data= models.Rainfall()
            soil_data=models.SoilMoisture()

            rainfall_data.latitude = data["latitude"]
            rainfall_data.longitude = data["longitude"]
        
            rainfall_data.precipitation = rainfall

            soil_data.latitude=data["latitude"]
            soil_data.longitude=data["longitude"]
            soil_data.timestamp=datetime.fromisoformat(time)
            soil_data.moisture= soil_moisture
            soil_data.unit=data["hourly_units"]["soil_moisture_0_to_1cm"]

            current_index = time_values.index(time)

            # last 6 hours rainfall

            start_index = max(0,current_index -5)

            last_6_hours_rainfall = sum(
                hourly_rainfall[start_index:current_index + 1]
            )
            # previous 6 hours rainfall
            previous_start = max(0, current_index -11)
            previous_end= max(0, current_index -5)

            previous_6_hours_rainfall = sum(
                hourly_rainfall[previous_start:previous_end]
            )

            # last 12 hours rainfall
            last_12_hours_rainfall = sum(
                hourly_rainfall[
                    max(0,current_index - 11):current_index +1
                ]
            )

            # last 3 days rainfall 
            last_3_days_rainfall =sum(
                hourly_rainfall[
                    max(0,current_index - 71):current_index +1 
                ]
            )
            # last 5 days rainfall
            last_5_days_rainfall = sum(
                hourly_rainfall[
                    max(0,current_index -119):current_index +1
                ]
            )
            # last 12 days rainfall
            last_12_days_rainfall =sum(
                hourly_rainfall[
                    max(0,current_index -287):current_index +1
                ]
            )

            #Rainfall trend
            if last_6_hours_rainfall> previous_6_hours_rainfall:
                rainfall_trend = "Increasing"
            elif last_6_hours_rainfall < previous_6_hours_rainfall:
                rainfall_trend = "Decreasing "
            else:
                rainfall_trend = "Stable"

            # Combined risk 
            risk,combined_score = calculate_combined_risk(
                rainfall, 
                soil_moisture,
                last_6_hours_rainfall,
                last_12_hours_rainfall,
                last_3_days_rainfall,
                last_5_days_rainfall,
                last_12_days_rainfall,
                rainfall_trend
            )

            
            rainfall_data.risk_level = risk
            rainfall_data.risk_score=combined_score

            combined_risks.append(risk)
            combined_scores.append(combined_score)



            rainfall_data.unit = data["hourly_units"]["precipitation"]
            rainfall_data.timestamp = datetime.fromisoformat(time)

            existing_record=db.query(models.Rainfall).filter_by(
                latitude=data["latitude"],
                longitude=data["longitude"],
                timestamp=datetime.fromisoformat(time)
            ).first()

            if existing_record:
                soil_existing=db.query(models.SoilMoisture).filter_by(
                    latitude=data["latitude"],
                    longitude=data["longitude"],
                    timestamp=datetime.fromisoformat(time)
                ).first()

                if not soil_existing:
                    db.add(soil_data)

                continue

            db.add(rainfall_data)
            db.add(soil_data)


        db.commit()

        return {
            "location":{
                "latitude":data["latitude"],
                "longitude":data["longitude"],
                "elevation" :  data["elevation"]
            },
            "timezone":data["timezone"],
            "hourly_rainfall":{
                "time":data["hourly"]["time"],
                "precipitation": data["hourly"]["precipitation"],
                "unit":data["hourly_units"]["precipitation"],

                "risk_level":combined_risks,
                "risk_score":combined_scores,

                "soil_moisture":data["hourly"]["soil_moisture_0_to_1cm"]


            }
        }
    finally:
        db.close()
@app.get("/rainfall/history")
def rainfall_history():
    db = SessionLocal()
    rainfall_records = db.query(models.Rainfall).all()
    db.close()
    return rainfall_records

@app.get("/soil-moisture/history")
def soil_moisture_history():
    db=SessionLocal()
    soil_records=db.query(models.SoilMoisture).all()
    db.close()
    return soil_records

@app.get("/rainfall/by-date")
def rainfall_by_date(
    latitude: float,
    longitude: float,
    date: str
):
    url = "https://archive-api.open-meteo.com/v1/archive"

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": (
            datetime.fromisoformat(date) - timedelta(days=12)
        ).strftime("%Y-%m-%d"),
        "end_date": date,
        "hourly": "precipitation",
        "timezone": "Asia/Kolkata"
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    data = response.json()

    rainfall_values = data["hourly"]["precipitation"]

    time_values=data["hourly"]["time"]

    target_index=None

    for i, time in enumerate(time_values):
        if time.startswith(date):
            target_index=i
            break

    if target_index is None:
        return{
            "Error":"Requests date data not available"
        }

    daily_rainfall = [
    value for value in rainfall_values[target_index:target_index + 24]
    if value is not None
    ]

    total_rainfall = sum(daily_rainfall)
    max_rainfall = max(daily_rainfall)
    average_rainfall = total_rainfall / len(daily_rainfall)

    # Rainfall windows for requested date

    last_6_hours_rainfall = sum(
        value for value in rainfall_values[
            max(0,target_index-5):target_index + 1
        ]
        if value is not None
    )

    last_12_hours_rainfall = sum(
        value for value in rainfall_values[
            max(0,target_index - 11):target_index +1
        ]
        if value is not None
    )
    last_3_days_rainfall = sum(
        value for value in rainfall_values[
            max(0,target_index - 71):target_index + 1
        ]
        if value is not None
    )
    last_5_days_rainfall = sum(
        value for value in rainfall_values[
            max(0,target_index - 119):target_index + 1
        ]
        if value is not None
    )

    last_12_days_rainfall=sum(
        value for value in rainfall_values[
            max(0,target_index - 287):target_index + 1
        ]
        if value is not None

    )


    # Rainfall trend
    first_half = sum(
        value for value in rainfall_values[:12]
        if value is not None
    )

    second_half = sum(
        value for value in rainfall_values[12:]
        if value is not None
    )

    if second_half > first_half:
        rainfall_trend = "Increasing"
    elif second_half < first_half:
        rainfall_trend = "Decreasing"
    else:
        rainfall_trend = "Stable"

    # Risk calculation
    risk, risk_score = calculate_combined_risk(
        rainfall=max_rainfall,
        soil_moisture=0,
        last_6_hours_rainfall=last_6_hours_rainfall,
        last_12_hours_rainfall=last_12_hours_rainfall,

        last_3_days_rainfall=last_3_days_rainfall,
        last_5_days_rainfall=last_5_days_rainfall,
        last_12_days_rainfall=last_12_days_rainfall,
        rainfall_trend=rainfall_trend
    )

    return {
        "latitude": latitude,
        "longitude": longitude,
        "date": date,
        "total_rainfall": total_rainfall,
        "max_hourly_rainfall": max_rainfall,
        "average_hourly_rainfall": average_rainfall,
        "last_6_hours_rainfall":last_6_hours_rainfall,
        "last_12_hours_rainfall":last_12_hours_rainfall,
        "last_3_days_rainfall":last_3_days_rainfall,
        "last_5_days_rainfall":last_5_days_rainfall,
        "last_12_days_rainfall":last_12_days_rainfall,
        "rainfall_trend": rainfall_trend,
        "risk_level": risk,
        "risk_score": risk_score,
        "unit": data["hourly_units"]["precipitation"]
    }

@app.get("/rainfall/summary")
def rainfall_summary(latitude:float,longitude:float):
    db=SessionLocal()

    try:
        rainfall_records=db.query(models.Rainfall).filter(
            models.Rainfall.latitude.between(latitude - 0.5,latitude + 0.5),
            models.Rainfall.longitude.between(longitude - 0.5, longitude + 0.5)
        ).all()

        rainfall_records.sort(key=lambda record: record.timestamp)

        if rainfall_records:

            latest_rainfall=rainfall_records[-1].precipitation
        else:

            latest_rainfall=0

       

        soil_records = db.query(models.SoilMoisture).filter(
            models.SoilMoisture.latitude.between(latitude -0.5, latitude +0.5),
            models.SoilMoisture.longitude.between(longitude -0.5, longitude +0.5)
        ).all()

        if soil_records:
            soil_records.sort(key=lambda record: record.timestamp)
            latest_soil_moisture = soil_records[-1].moisture
        else:
            latest_soil_moisture= None

        if rainfall_records:
            total_rainfall = sum(record.precipitation for record in rainfall_records)
            average_rainfall = total_rainfall / len(rainfall_records)
            max_rainfall = max(record.precipitation for record in rainfall_records)

            latest_time= max(record.timestamp for record in rainfall_records)

            six_hours_ago= latest_time - timedelta(hours=6)

            last_6_hours = [
                record for record in rainfall_records
                if record.timestamp >= six_hours_ago
            ]

            last_6_hours_rainfall = sum(
                record.precipitation for record in last_6_hours
            )
            twelve_hours_ago= latest_time - timedelta(hours=12)

            last_12_hours =[
                record for record in rainfall_records
                if record.timestamp >= twelve_hours_ago
            ]

            last_12_hours_rainfall =sum(
                record.precipitation for record in last_12_hours
            )

            previous_6_hours = [
                record for record in rainfall_records
                if twelve_hours_ago <= record.timestamp < six_hours_ago
            ]
            previous_6_hours_rainfall = sum(
                record.precipitation for record in previous_6_hours
            )

            last_3_days_rainfall=sum(
                record.precipitation
                for record in rainfall_records
                if latest_time - record.timestamp <= timedelta(days=3)
            )
            last_5_days_rainfall=sum(
                record.precipitation 
                for record in rainfall_records
                if latest_time- record.timestamp <= timedelta(days=5)

            )

            last_12_days_rainfall=sum(

                record.precipitation
                for record in rainfall_records
                if latest_time-record.timestamp  <= timedelta(days=12)
            )

        

        else:
            total_rainfall = 0
            average_rainfall=0
            max_rainfall=0
            latest_time=None
            last_6_hours_rainfall=0

            previous_6_hours_rainfall = 0

            last_3_days_rainfall=0
            last_5_days_rainfall=0
            last_12_days_rainfall=0




        if last_6_hours_rainfall > previous_6_hours_rainfall:
            rainfall_trend = "Increasing"

        elif last_6_hours_rainfall < previous_6_hours_rainfall:
            rainfall_trend = "Decreasing"

        else:
            rainfall_trend= "Stable"

        current_risk,current_risk_score= calculate_combined_risk(
            
            latest_rainfall,
            latest_soil_moisture or 0 ,
            last_6_hours_rainfall,
            last_12_hours_rainfall,
            last_3_days_rainfall,
            last_5_days_rainfall,
            last_12_days_rainfall,
            rainfall_trend
        )
        alert_mesage=generate_alert(
            current_risk,
            current_risk_score
        )

        if current_risk=="High":
            risk_message="High landslide risk. Immediate attention required."
        elif current_risk=="Moderate":
            risk_message="Moderate landslide risk. Continue monitoring."
        else:
            risk_message="Low landslide risk. Conditions are currently stable."

        return{
            "total_records":len(rainfall_records),
            "total_rainfall":total_rainfall,
            "average_rainfall":average_rainfall,
            "max_rainfall":max_rainfall,
            "last_6_hours_rainfall":last_6_hours_rainfall,
            "last_12_hours_rainfall":last_12_hours_rainfall,
            "last_3_days_rainfall":last_3_days_rainfall,
            "last_5_days_rainfall":last_5_days_rainfall,
            "last_12_days_rainfall":last_12_days_rainfall,
            "rainfall_trend":rainfall_trend,
            "latest_soil_moisture":latest_soil_moisture,
            "current_risk":current_risk,
            "current_risk_score":current_risk_score,
            "risk_message":risk_message,
            "alert_message":alert_mesage
        }
    finally:
        db.close()

@app.get("/alerts")
def get_alerts(latitude:float,longitude:float):
    db=SessionLocal()

    try:
        rainfall_records = db.query(models.Rainfall).filter(
            models.Rainfall.latitude.between(latitude - 0.5, latitude +0.5),
            models.Rainfall.longitude.between(longitude -0.5 , longitude +0.5)

        ).all()

        soil_records = db.query(models.SoilMoisture).filter(
            models.SoilMoisture.latitude.between(latitude -0.5, latitude + 0.5),
            models.SoilMoisture.longitude.between(longitude - 0.5 , longitude +0.5)

        ).all()

        if not rainfall_records:
            return{
                "alert": "No weather data available.",
                "risk":"Unknown"
            }

        rainfall_records.sort(key=lambda record: record.timestamp)
        latest_rainfall = rainfall_records[-1].precipitation

        if soil_records:
            soil_records.sort(key=lambda record: record.timestamp)
            latest_soil_moisture = soil_records[-1].moisture
        else:
            latest_soil_moisture=0
        now = rainfall_records[-1].timestamp

        last_6_hours_rainfall = sum(
            record.precipitation
            for record in rainfall_records
            if now - record.timestamp <= timedelta(hours=6)

        )
        previous_6_hours_rainfall = sum(
            record.precipitation
            for record in rainfall_records
            if timedelta(hours=6) < now-record.timestamp  <= timedelta(hours=12)
        )
        last_12_hours_rainfall = sum(
            record.precipitation 
            for record in rainfall_records
            if now - record.timestamp <= timedelta(hours=12)

        )
        last_3_days_rainfall = sum(
            record.precipitation
            for record in rainfall_records
            if now - record.timestamp <= timedelta(days=3)
        )
        last_5_days_rainfall= sum(
            record.precipitation 
            for record in rainfall_records
            if now - record.timestamp <= timedelta(days=5)
        )
        last_12_days_rainfall = sum(
            record.precipitation 
            for record in rainfall_records
            if now - record.timestamp <= timedelta(days=12)
        ) 

        if last_6_hours_rainfall > previous_6_hours_rainfall:
            rainfall_trend = "Increasing"
        elif last_6_hours_rainfall < previous_6_hours_rainfall:
            rainfall_trend = "Decreasing"
        else:
            rainfall_trend = "Stable"

        risk, risk_score = calculate_combined_risk(
            latest_rainfall,
            latest_soil_moisture or 0,
            last_6_hours_rainfall,
            last_12_hours_rainfall,
            last_3_days_rainfall,
            last_5_days_rainfall,
            last_12_days_rainfall,
            rainfall_trend
        )

        alert = generate_alert(risk,risk_score)

        return {
            "location":{
                "latitude":latitude,
                "longitude":longitude
            },
            "latest_rainfall":latest_rainfall,
            "latest_soil_moisture":latest_soil_moisture,
            "last_6_hours_rainfall":last_6_hours_rainfall,
            "rainfall_trend":rainfall_trend,
            
            "risk":risk,

            "risk_score":risk_score,
            
            
            "alert":alert
        }

    finally:
        db.close()

@app.get("/rainfall/forecast-risk")
def forecast_risk(latitude:float,longitude:float):

    url="http://api.open-meteo.com/v1/forecast"

    params={
        "latitude":latitude,
        "longitude":longitude,
        "hourly":"precipitation,soil_moisture_0_to_1cm",
        "forecast_days":12,
        "timezone":"Asia/Kolkata"
    }

    response = requests.get(url,params=params)
    data=response.json()

    rainfall_values = data["hourly"]["precipitation"]
    soil_moisture_values=data["hourly"]["soil_moisture_0_to_1cm"]
    time_values = data["hourly"]["time"]

    forecast_risk=[]
    forecast_scores=[]

    for current_index,(time,rainfall,soil_moisture) in enumerate(zip(
        time_values,
        rainfall_values,
        soil_moisture_values
    
    )):
        # last 6 hours 
        start_index=max(0,current_index -5)

        last_6_hours_rainfall = sum(
            rainfall_values[start_index:current_index +1]

        )

        #previous 6 hours 
        previous_start = max(0,current_index - 11)
        previous_end = max(0, current_index -5)

        previous_6_hours_rainfall = sum(
            rainfall_values[previous_start:previous_end]
        )

        # last 12 hours
        last_12_hours_rainfall = sum(
            rainfall_values[
                max(0,current_index-11):current_index +1
            ]
        )

        # last 3 days rainfall
        last_3_days_rainfall =sum(
            rainfall_values[
                max(0,current_index-71):current_index + 1
            ]
        )

        # last 5 days rainfall
        last_5_days_rainfall=sum(
            rainfall_values[
                max(0,current_index-119):current_index +1
            ]
        )

        # last 12 days rainfall
        last_12_days_rainfall = sum(
            rainfall_values[
                max(0,current_index -287):current_index + 1
            ]
        )

        #Rainfall trend

        if last_6_hours_rainfall > previous_6_hours_rainfall:
            rainfall_trend = "Increasing"
        elif last_6_hours_rainfall < previous_6_hours_rainfall:
            rainfall_trend = "Decreasing"
        else:
            rainfall_trend ="Stable"

        soil_moisture = soil_moisture if soil_moisture is not None else 0 


        #combined risk
        risk,score=calculate_combined_risk(
                rainfall,
                soil_moisture,
                last_6_hours_rainfall,
                last_12_hours_rainfall,
                last_3_days_rainfall,
                last_5_days_rainfall,
                last_12_days_rainfall,
                rainfall_trend
        )

        forecast_risk.append(risk)
        forecast_scores.append(score)

    highest_score=max(forecast_scores)
    highest_index=forecast_scores.index(highest_score)
    highest_risk=forecast_risk[highest_index]
    highest_risk_time=time_values[highest_index]


    return{

        "location":{

            "latitude":data["latitude"],
            "longitude":data["longitude"]

        },

        "forecast":{
            "time":time_values,
            "rainfall":rainfall_values,
            "soil_moisture":soil_moisture_values,

            "risk_level":forecast_risk,
            "risk_scores":forecast_scores,

            "highest_risk":highest_risk,
            "highest_risk_scores":highest_score,
            "highest_risk_time":highest_risk_time
        }
    }

# AASHA — A Ray of Hope

### AI-Powered Landslide Risk Monitoring & Early Warning System

> **Smart India Hackathon 2026 Project**

SAAHAS is an AI-powered, data-driven early warning and decision-support platform designed to monitor, assess, and communicate **landslide risk across the Northeastern Region of India**.

The platform brings together rainfall, soil moisture, geographical information, risk assessment, incident reporting, and alert mechanisms into a unified dashboard to help authorities and communities identify potentially vulnerable areas and respond before situations become critical.


## Problem Statement

The Northeastern Region of India is highly vulnerable to landslides due to its:

* High and unpredictable rainfall
* Steep and fragile terrain
* Soil instability
* Changing weather conditions
* Road and infrastructure vulnerability
* Limited availability of localized real-time risk information

Existing information is often fragmented across different sources. This makes it difficult for authorities and users to obtain a **single, understandable view of current risk conditions**.

SAAHAS addresses this challenge by creating a centralized platform that combines environmental observations, risk indicators, geographic information, and field reports.



#  Our Solution

SAAHAS provides a unified monitoring and early-warning interface that allows users to:

* Monitor rainfall conditions
* Track soil moisture
* Identify high-risk geographical zones
* Visualize risk on a map
* View rainfall and risk trends
* Receive risk-based alerts
* Submit ground-level incident reports
* Track reported incidents
* Analyze risk indicators for different locations
* Support faster decision-making by authorities

The objective is not simply to display data, but to convert environmental and field information into **actionable risk intelligence**.



#  Key Objectives

1. **Early Risk Identification**
   Detect locations showing environmental conditions associated with increased landslide risk.

2. **Real-Time Monitoring**
   Provide a centralized dashboard for monitoring rainfall and other environmental indicators.

3. **Geospatial Visualization**
   Display risk conditions geographically so vulnerable zones can be identified quickly.

4. **Community Reporting**
   Allow users and field personnel to report incidents and upload relevant information.

5. **Risk Communication**
   Present complex environmental information through simple risk levels and visual indicators.

6. **Decision Support**
   Help authorities prioritize locations requiring monitoring, inspection, or intervention.



# System Architecture

```text
                    ┌──────────────────────────┐
                    │   Environmental Data     │
                    │                          │
                    │  • Rainfall              │
                    │  • Soil Moisture         │
                    │  • Geographic Data       │
                    └────────────┬─────────────┘
                                 │
                                 ▼
                    ┌──────────────────────────┐
                    │   Data Processing Layer   │
                    │                          │
                    │ • Validation             │
                    │ • Processing             │
                    │ • Risk Calculation       │
                    └────────────┬─────────────┘
                                 │
                                 ▼
                    ┌──────────────────────────┐
                    │      Backend API          │
                    │                          │
                    │        Python            │
                    │      SQLAlchemy           │
                    └────────────┬─────────────┘
                                 │
              ┌──────────────────┼──────────────────┐
              │                  │                  │
              ▼                  ▼                  ▼
        ┌───────────┐      ┌────────────┐     ┌─────────────┐
        │ Dashboard │      │ Risk Zones │     │ Rainfall &  │
        │           │      │            │     │ Forecast    │
        └───────────┘      └────────────┘     └─────────────┘
              │                  │                  │
              └──────────────────┼──────────────────┘
                                 ▼
                    ┌──────────────────────────┐
                    │     Users / Authorities  │
                    │                          │
                    │  Monitor → Analyze →     │
                    │  Report → Respond        │
                    └──────────────────────────┘


# Major Features

## 1. Monitoring Dashboard

The central dashboard provides an overview of the monitored region.

It can display:

* Total monitored locations
* Current rainfall conditions
* Risk distribution
* High-risk areas
* Environmental indicators
* Alerts
* Geographic risk visualization

The dashboard is designed to provide a quick overview before users move into detailed analysis.



## 2.  High-Risk Zone Detection

The High Risk Zones module identifies locations based on their calculated risk conditions.

The interface provides information such as:

| Parameter     | Description                |
| ------------- | -------------------------- |
| Zone          | Geographic monitoring zone |
| State         | Associated state           |
| Rainfall      | Recorded rainfall          |
| Soil Moisture | Soil moisture condition    |
| Risk Level    | Low / Moderate / High      |
| Risk Score    | Numerical risk indicator   |
| Coordinates   | Latitude and longitude     |

This allows users to quickly identify areas requiring greater attention.



## 3.  Rainfall Monitoring

Rainfall is one of the important environmental indicators considered by the platform.

The rainfall module provides:

* Rainfall measurements
* Timestamp information
* Geographic coordinates
* Risk classification
* Risk score
* Forecast-related information

Users can select a location and examine its environmental conditions.



## 4.  Soil Moisture Monitoring

Soil moisture information is incorporated into the risk assessment framework.

High soil moisture can be an important indicator when combined with other environmental and terrain-related factors.

SAAHAS stores:

* Location
* Timestamp
* Moisture value
* Measurement unit

This information can subsequently be used for more advanced predictive modelling.



#  Risk Assessment

SAAHAS represents risk using interpretable categories:

```text
LOW
  ↓
MODERATE
  ↓
HIGH
```

A numerical **risk score** is also associated with monitored locations.

This dual representation allows:

* Users to understand risk quickly through categories
* Technical users to examine numerical values
* Authorities to prioritize areas for further investigation

> **Note:** The risk score is intended as a decision-support indicator and should not be interpreted as a guaranteed prediction of a landslide event.



#  Geographic Monitoring

The platform focuses on the **Northeastern Region of India**, an area containing several landslide-prone mountainous and hilly regions.

Geographic coordinates are used to associate environmental observations with specific monitoring locations.

This enables the system to transform tabular environmental information into a spatially understandable risk map.



#  Incident Reporting

SAAHAS also includes a ground-level reporting mechanism.

Users can submit:

* Name
* Role
* State
* Problem type
* Location
* Description
* Photograph
* Rating
* Feedback

This creates a bridge between:

```text
Environmental Data
        +
Ground-Level Information
        ↓
Better Situational Awareness
```

Field reports can provide information that may not immediately appear in environmental datasets.



#  Database Design

The backend uses a relational database architecture through SQLAlchemy.

### Rainfall

```text
Rainfall
├── id
├── latitude
├── longitude
├── timestamp
├── precipitation
├── unit
├── risk_level
└── risk_score
```

### Soil Moisture

```text
SoilMoisture
├── id
├── latitude
├── longitude
├── timestamp
├── moisture
└── unit
```

### Incident Report

```text
IncidentReport
├── id
├── name
├── role
├── state
├── problem_type
├── location
├── description
├── photo
├── rating
├── feedback
└── status
```


#  Backend API

The frontend communicates with the backend through REST-style API endpoints.

Important endpoints include:

```text
GET  /rainfall/summary
GET  /alerts
GET  /rainfall/chart
GET  /risk-grid
GET  /high-risk-zones
GET  /rainfall/forecast-risk
```

These APIs provide the frontend with processed environmental and risk information.



#  Technology Stack

## Frontend

* HTML5
* CSS3
* JavaScript
* Responsive UI
* Interactive dashboard components

## Backend

* Python
* FastAPI / Python API architecture
* SQLAlchemy

## Database

* SQLite
* Relational data modelling

## Data & Analytics

* Rainfall data
* Soil moisture data
* Geographic coordinates
* Risk scoring
* Environmental indicators

## Development Tools

* Visual Studio Code
* Git
* GitHub
* Browser Developer Tools
* API testing tools


#  Project Structure

```text
SMART_INDIA_HACKATHON-AASHA/
│
├── Dashboard.html
├── HighRiskZones.html
├── RainfallData.html
├── RoadConnectivity.html
├── UploadReport.html
├── AccountsAndAlerts.html
├── ReportsAndStatus.html
├── Settings.html
│
├── AASHA.css
│
├── main.py
├── database.py
├── models.py
│
├── ner/
│   └── Northeastern Region geographic data
│
├── requirements.txt
│
└── README.md
```



# ⚙️ Installation & Setup

## 1. Clone the repository

```bash
git clone https://github.com/himanshuguptastudiesiitp/SMART_INDIA_HACKATHON-AASHA.git
```

```bash
cd SMART_INDIA_HACKATHON-AASHA
```



## 2. Create a virtual environment

### Windows

```bash
python -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
```

```bash
source venv/bin/activate
```


## 3. Install dependencies

```bash
pip install -r requirements.txt
```

If `requirements.txt` is not available in your local version:

```bash
pip install fastapi uvicorn sqlalchemy
```



# Running the Backend

Start the API server using:

```bash
uvicorn main:app --reload
```

The backend will normally become available at:

```text
http://127.0.0.1:8000
```

API documentation can be accessed through the FastAPI documentation interface:

```text
http://127.0.0.1:8000/docs
```

---

# 🌐 Running the Frontend

Open the frontend HTML files in a browser or serve the project using a local development server.

For example:

```bash
python -m http.server 5500
```

Then open:

```text
http://127.0.0.1:5500
```

Make sure the backend API is running simultaneously so that frontend API requests can retrieve data.


# 🔄 Data Flow

The basic data flow of SAAHAS is:

```text
Environmental / Geographic Data
              ↓
        Data Processing
              ↓
       Risk Assessment
              ↓
          Backend API
              ↓
       Frontend Dashboard
              ↓
       User Interpretation
              ↓
     Alert / Report / Action
```



#  AI & Future Intelligence Layer

The current prototype establishes the foundation required for an intelligent landslide-risk system.

Future versions can introduce machine-learning models using features such as:

* Rainfall intensity
* Cumulative rainfall
* Soil moisture
* Terrain slope
* Elevation
* Land cover
* Geological characteristics
* Historical landslide records
* Drainage conditions
* Road connectivity
* Weather forecasts

A potential predictive pipeline is:

```text
Historical Environmental Data
             ↓
       Feature Engineering
             ↓
       ML Model Training
             ↓
       Risk Probability
             ↓
    Risk Classification
             ↓
       Early Warning
```

Possible models for experimentation include:

* Random Forest
* Gradient Boosting
* XGBoost
* Logistic Regression
* Neural Networks

Model selection should ultimately be based on validation performance, data availability, interpretability, and operational requirements.

---

# Future Scope

### 1. Machine Learning Prediction

Develop a validated ML model capable of estimating landslide probability from environmental and geographic features.

### 2. Real-Time Data Integration

Integrate live sources for:

* Rainfall
* Weather
* Soil moisture
* Satellite observations
* Geological information

### 3. Satellite & Remote Sensing

Incorporate satellite-derived information such as:

* Land-cover changes
* Vegetation indices
* Surface deformation
* Terrain characteristics

### 4. Automated Alerts

Introduce configurable alerts through:

* SMS
* Email
* Mobile notifications
* Web notifications

### 5. Authority Dashboard

Create dedicated interfaces for:

* Disaster management authorities
* District administration
* Road authorities
* Field teams

### 6. Mobile Application

Develop Android/iOS applications for field personnel and citizens.

### 7. Multilingual Support

Provide information in regional languages to improve accessibility for communities in the Northeastern states.

### 8. Explainable AI

Provide explanations alongside predictions, such as:

```text
Risk Score: 78%

Major contributing indicators:
• High cumulative rainfall
• Elevated soil moisture
• Steep terrain
```

This can make AI-generated warnings more understandable to decision-makers.



# Responsible Use

AASHA is intended as a **decision-support and early-warning platform**.

Risk indicators should be interpreted together with:

* Official disaster-management information
* Ground verification
* Local authority assessments
* Meteorological information
* Geological expertise

The platform does not guarantee that a landslide will or will not occur.



#  Expected Impact

SAAHAS aims to contribute to:

### Early Awareness

Identify potentially vulnerable locations before conditions become critical.

### Faster Response

Help authorities focus attention on locations showing elevated risk indicators.

### Better Information Access

Bring multiple environmental indicators into one interface.

### Community Participation

Enable ground-level reporting from people and field personnel.

### Data-Driven Decision Support

Provide structured environmental and geographic information for operational planning.



# Smart India Hackathon

**Hackathon:** Smart India Hackathon 2026
**Project:** AASHA — A Ray of Hope
**Domain:** Disaster Management / AI / Geospatial Intelligence
**Focus:** Landslide Risk Monitoring and Early Warning
**Region:** Northeastern India



# Team

Developed as a team project for **Smart India Hackathon 2026**.

### Team Members

* **Himanshu Kumar**
* **Aditya Thakur**
* **Aditya Sharma**
* **Sahil**
* **Arin**
* **Sankarshan**



#  Project Vision

> **From fragmented environmental data to actionable early warning intelligence.**

SAAHAS aims to build a technology layer that connects environmental monitoring, geographic intelligence, community reporting, and predictive analytics to help create safer and more responsive disaster-management systems.



#  License

This project is developed for educational, research, and hackathon purposes.



#  Support the Project

If you find the project useful or interesting, consider giving the repository a ⭐ on GitHub.

**AASHA — A Ray of Hope**

*Technology that helps us see risk before it becomes a disaster.*

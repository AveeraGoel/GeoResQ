# 🌍 GeoResQ

## Disaster Risk Intelligence & Multi-Hazard Mapping

GeoResQ is a satellite-based disaster risk intelligence platform designed to analyze and visualize disaster risk using Earth observation and geospatial datasets.

### 🚨 Problem Domain

Disaster Risk Analysis

GeoResQ combines:

- Sentinel-1 SAR
- Sentinel-2
- SRTM DEM
- CHIRPS rainfall
- MERIT Hydro
- Dynamic World
- GHSL population

### 🛰️ GeoResQ Pipeline

Satellite Data  
↓  
Image Processing  
↓  
Geospatial Analysis  
↓  
Hazard & Exposure Indicators  
↓  
Multi-Hazard Risk Model  
↓  
Interactive Risk Map  
↓  
Decision Support

### 🌊 Flood Analysis

Sentinel-1 SAR is used to identify changes in surface backscatter and detect potential flood-affected areas.

### ⛰️ Landslide Analysis

Landslide susceptibility is modeled using:

- Slope
- Rainfall
- NDVI
- Elevation

### 🏙️ Exposure Analysis

Exposure combines:

- Built-up areas
- Population

### ⚠️ Multi-Hazard Risk

GeoResQ calculates:

Risk = 40% Flood Hazard + 30% Landslide Hazard + 30% Exposure

Areas with a risk score ≥ 0.40 are classified as elevated-risk zones.

### 🎛️ Interactive Dashboard

The dashboard provides:

- Interactive satellite-based map
- Hazard layer control
- Flood detection
- Flood hazard
- Landslide hazard
- Exposure
- Multi-hazard risk
- Elevated-risk zones
- Affected settlements
- Interactive risk assessment key
- Decision-support indicators

### 🛠️ Technology

- Python
- Streamlit
- Google Earth Engine
- Folium
- Pandas
- Geospatial analysis

### 👥 Project

GeoResQ — Disaster Risk Intelligence Prototype

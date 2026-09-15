# Welcome to My Dark Sky
***

## Task
The Dark Sky weather app was discontinued after Apple's acquisition. The challenge is to rebuild its core experience — current conditions, multi-day forecast, and location search — as a small, well-structured web app, using a free public weather API (OpenWeather) in place of Dark Sky's original proprietary forecasting engine, while keeping API usage efficient through caching.
## Description
This project recreates a simplified version of Dark Sky using Flask and the OpenWeather API. It supports two ways of choosing a location — automatic geolocation via the browser, or a text search with live suggestions — and shows today's weather plus a 5-day forecast that the user can step through day by day. To avoid hitting the OpenWeather API on every request, responses are cached in a SQLite database for 5 minutes per location. The interface is built with a custom dark, atmospheric design (Flask + Tailwind) rather than a generic template.
## Installation

```bash
git clone https://github.com/mehin2m/dark-sky-remake.git
cd dark-sky-remake
pip install -r requirements.txt
cp .env.example .env
```

Then open `.env` and set `OPENWEATHER_API_KEY` to a free key from [openweathermap.org/api](https://openweathermap.org/api).

## Usage

```bash
python app.py
```

Then open `http://localhost:5000` (or the `PORT` you set) in your browser. Search for a city or use the "Current location" button, then click a day in the forecast list to see its details.
```

### The Core Team
no team 

<span><i>Made at <a href='https://qwasar.io'>Qwasar SV -- Software Engineering School</a></i></span>
<span><img alt='Qwasar SV -- Software Engineering School's Logo' src='https://storage.googleapis.com/qwasar-public/qwasar-logo_50x50.png' width='20px' /></span>

"""TRIPSA — live weather per city via the free Open-Meteo API (no key needed)."""
import requests
import streamlit as st

# WMO weather interpretation codes -> (icon, English label)
WMO = {
    0: ("☀️", "Clear sky"), 1: ("🌤️", "Mainly clear"), 2: ("⛅", "Partly cloudy"),
    3: ("☁️", "Overcast"), 45: ("🌫️", "Fog"), 48: ("🌫️", "Rime fog"),
    51: ("🌦️", "Light drizzle"), 53: ("🌦️", "Drizzle"), 55: ("🌧️", "Dense drizzle"),
    61: ("🌦️", "Light rain"), 63: ("🌧️", "Rain"), 65: ("🌧️", "Heavy rain"),
    71: ("🌨️", "Light snow"), 73: ("🌨️", "Snow"), 75: ("❄️", "Heavy snow"),
    80: ("🌦️", "Rain showers"), 81: ("🌧️", "Rain showers"), 82: ("⛈️", "Violent showers"),
    95: ("⛈️", "Thunderstorm"), 96: ("⛈️", "Thunderstorm + hail"), 99: ("⛈️", "Thunderstorm + hail"),
}


@st.cache_data(ttl=1800, show_spinner=False)
def get_weather(lat, lng):
    """Return current weather dict for coordinates, or None on failure."""
    try:
        r = requests.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": lat, "longitude": lng, "current_weather": "true",
                "hourly": "relativehumidity_2m", "timezone": "auto",
            },
            timeout=10,
        )
        j = r.json()
        cw = j.get("current_weather", {})
        code = cw.get("weathercode", 0)
        icon, label = WMO.get(code, ("🌡️", "—"))
        return {
            "temp": round(cw.get("temperature", 0)),
            "wind": round(cw.get("windspeed", 0)),
            "icon": icon,
            "label": label,
        }
    except Exception:
        return None


def weather_badge(lat, lng):
    """Compact HTML badge for a city, e.g. '☀️ 32°C · Clear'."""
    w = get_weather(lat, lng)
    if not w:
        return ""
    return f"{w['icon']} {w['temp']}°C · {w['label']} · 💨{w['wind']}km/h"

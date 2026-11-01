#!/usr/bin/env python3
"""
FastMCP Server for Singapore NEA Real-Time Weather & Hydroplaning Collision Risk Engine
Compatible with Antigravity IDE (Gemini 3.8 Flash)
Data Endpoints (NEA / data.gov.sg v2):
  - Live 5-minute station rainfall: https://api-open.data.gov.sg/v2/real-time/api/rainfall
  - Live wind speed: https://api-open.data.gov.sg/v2/real-time/api/wind-speed
  - Live 2-hour town nowcast: https://api-open.data.gov.sg/v2/real-time/api/two-hr-forecast
  - Live 24-hour weather outlook: https://api-open.data.gov.sg/v2/real-time/api/twenty-four-hr-forecast
"""

import json
import math
import urllib.request
from typing import Dict, Any, List, Optional

try:
    from mcp.server.fastmcp import FastMCP
    mcp = FastMCP("sg-nea-weather-mcp")
except ImportError:
    class DummyMCP:
        def __init__(self, name): self.name = name
        def tool(self):
            def dec(fn): return fn
            return dec
        def run(self): print("FastMCP not installed. Run: pip install mcp httpx")
    mcp = DummyMCP("sg-nea-weather-mcp")

# Known Centroids for Major Singapore Postal Districts / Corridors
CORRIDOR_CENTROIDS = {
    "82": {"name": "Punggol / TPE Merge", "lat": 1.3912, "lng": 103.9056},
    "73": {"name": "Woodlands / BKE Causeway", "lat": 1.4310, "lng": 103.7745},
    "64": {"name": "Jurong West / Tuas PIE", "lat": 1.3340, "lng": 103.6920},
    "56": {"name": "Bishan / Braddell CTE", "lat": 1.3418, "lng": 103.8569},
    "17": {"name": "Clarke Quay / Downtown Nightlife", "lat": 1.2905, "lng": 103.8458},
    "38": {"name": "Geylang / Kallang Arterial", "lat": 1.3140, "lng": 103.8835},
    "52": {"name": "Tampines Regional Centre", "lat": 1.3645, "lng": 103.9480},
    "31": {"name": "Toa Payoh Central", "lat": 1.3343, "lng": 103.8510},
    "23": {"name": "Orchard / Tanglin Belt", "lat": 1.3048, "lng": 103.8318},
    "26": {"name": "Bukit Timah / Dunearn Corridor", "lat": 1.3250, "lng": 103.8050},
    "12": {"name": "Clementi / AYE Logistics Axis", "lat": 1.3145, "lng": 103.7652},
    "05": {"name": "Chinatown / New Bridge Road", "lat": 1.2847, "lng": 103.8427},
    "46": {"name": "Bedok Central / New Upper Changi", "lat": 1.3236, "lng": 103.9312}
}


def _http_get(url: str, timeout: int = 8) -> Dict[str, Any]:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


@mcp.tool()
def get_live_station_rainfall(postal_code_or_subzone: Optional[str] = None) -> Dict[str, Any]:
    """
    Fetch live 5-minute rainfall readings across Singapore from all 88 NEA weather stations.
    If a postal code or subzone is provided, maps to the geographically closest weather station
    and computes the local precipitation rate (mm/hr) and hydroplaning multiplier.
    """
    try:
        raw = _http_get("https://api-open.data.gov.sg/v2/real-time/api/rainfall")
        data = raw.get("data", {})
        stations = data.get("stations", [])
        readings = data.get("readings", [])
        
        # Build station mapping: id -> {name, lat, lng}
        station_map = {}
        for s in stations:
            loc = s.get("location", {})
            station_map[s["id"]] = {
                "id": s["id"],
                "name": s.get("name", "Unknown Station"),
                "lat": loc.get("latitude", 1.3521),
                "lng": loc.get("longitude", 103.8198)
            }
        
        # Get latest reading set
        latest_readings = readings[0].get("data", []) if readings else []
        station_rainfall = {}
        max_rain = 0.0
        max_station = None

        for r in latest_readings:
            st_id = r.get("stationId")
            val_5min = float(r.get("value", 0.0))
            # 5-min reading extrapolated to hourly mm/hr equivalent
            val_hourly = round(val_5min * 12.0, 2)
            if st_id in station_map:
                st_info = station_map[st_id].copy()
                st_info["rainfall_5min_mm"] = val_5min
                st_info["rainfall_hourly_mm"] = val_hourly
                station_rainfall[st_id] = st_info
                if val_hourly > max_rain:
                    max_rain = val_hourly
                    max_station = st_info

        # If location target given, find closest station
        target_info = None
        if postal_code_or_subzone:
            prefix = postal_code_or_subzone[:2] if postal_code_or_subzone.isdigit() else ""
            coord = CORRIDOR_CENTROIDS.get(prefix, {"name": postal_code_or_subzone, "lat": 1.3521, "lng": 103.8198})
            
            best_st = None
            min_dist = 999999.0
            for st_id, st_info in station_rainfall.items():
                d = math.hypot(coord["lat"] - st_info["lat"], coord["lng"] - st_info["lng"])
                if d < min_dist:
                    min_dist = d
                    best_st = st_info

            if best_st:
                dist_km = round(min_dist * 111.0, 2)
                rain_hr = best_st["rainfall_hourly_mm"]
                
                # Hydroplaning hazard multiplier
                if rain_hr <= 0.0:
                    m_rain = 1.0
                    condition = "DRY"
                elif rain_hr < 5.0:
                    m_rain = 1.55  # Wet-onset oil lift
                    condition = "LIGHT_RAIN_OIL_SLICK"
                elif rain_hr < 15.0:
                    m_rain = 1.85
                    condition = "MODERATE_RAIN_WET_ASPHALT"
                else:
                    m_rain = min(2.60, 1.85 + ((rain_hr - 15.0) / 20.0) * 0.75)
                    condition = "CONVECTIVE_DELUGE_HYDROPLANING_ALERT"

                target_info = {
                    "matched_location": coord.get("name", postal_code_or_subzone),
                    "closest_weather_station": best_st["name"],
                    "station_id": best_st["id"],
                    "distance_to_station_km": dist_km,
                    "rainfall_rate_mm_hr": rain_hr,
                    "road_condition": condition,
                    "weather_risk_multiplier": round(m_rain, 2)
                }

        return {
            "status": "live",
            "source": "NEA / data.gov.sg v2 Real-Time Rainfall API",
            "active_weather_stations_count": len(station_rainfall),
            "islandwide_max_rainfall_mm_hr": max_rain,
            "islandwide_max_rain_station": max_station["name"] if max_station else "None (Islandwide Dry)",
            "location_assessment": target_info,
            "sample_active_stations": list(station_rainfall.values())[:10]
        }
    except Exception as e:
        return {"status": "error", "message": str(e), "fallback_multiplier": 1.0}


@mcp.tool()
def get_live_weather_nowcast(town_or_subzone: Optional[str] = None) -> Dict[str, Any]:
    """
    Fetch live 2-hour town weather nowcasts across Singapore (e.g. "Heavy Thundery Showers", "Moderate Rain", "Fair").
    Covers all 47 towns and planning areas.
    """
    try:
        raw = _http_get("https://api-open.data.gov.sg/v2/real-time/api/two-hr-forecast")
        data = raw.get("data", {})
        forecasts = data.get("items", [{}])[0].get("forecasts", [])
        
        target_forecast = None
        if town_or_subzone:
            for f in forecasts:
                if town_or_subzone.lower() in f.get("area", "").lower():
                    target_forecast = f
                    break

        return {
            "status": "live",
            "source": "NEA / data.gov.sg v2 Two-Hour Nowcast API",
            "total_areas": len(forecasts),
            "matched_area": target_forecast,
            "all_forecasts_sample": forecasts[:15]
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


@mcp.tool()
def compute_hydroplaning_and_braking_risk(
    rainfall_mm_hr: float,
    vehicle_speed_kmh: float = 80.0,
    vehicle_type: str = "sedan_mass",
    tire_pressure_psi: float = 32.0,
    tread_depth_mm: float = 4.0
) -> Dict[str, Any]:
    """
    Calculate physical tire hydroplaning dynamic velocity (Horne formula),
    wet-road friction coefficient degradation, and stopping distance expansion.
    """
    # Horne's Dynamic Hydroplaning Equation: V_p = 10.35 * sqrt(Tire Pressure in PSI) in km/h
    # For cars with good tread: V_p ≈ 10.35 * sqrt(P)
    v_hydroplane_kmh = round(10.35 * math.sqrt(tire_pressure_psi) * (tread_depth_mm / 8.0) ** 0.35, 1)

    # Dry asphalt friction coefficient: μ ≈ 0.75 - 0.82
    # Wet asphalt under rain: μ drops as water film thickens
    if rainfall_mm_hr <= 0:
        mu = 0.78
        regime = "DRY_CLEAN"
    elif rainfall_mm_hr < 5.0:
        mu = 0.58  # Wet-onset oil sheen
        regime = "FIRST_20_MINS_OIL_LIFT"
    elif rainfall_mm_hr < 15.0:
        mu = 0.48
        regime = "WET_RUNOFF"
    else:
        mu = 0.38  # Severe deluge
        regime = "DYNAMIC_PONDING_HYDROPLANE_HAZARD"

    # Stopping Distance formula: d = v^2 / (2 * g * mu) where v in m/s
    g = 9.81
    v_ms = (vehicle_speed_kmh * 1000.0) / 3600.0
    braking_distance_m = round((v_ms ** 2) / (2.0 * g * mu), 1)
    dry_distance_m = round((v_ms ** 2) / (2.0 * g * 0.78), 1)
    distance_increase_pct = round(((braking_distance_m - dry_distance_m) / dry_distance_m) * 100.0, 1)

    # Two-wheeler lean-angle stability penalty
    motorcycle_spinout_odds = "CRITICAL" if rainfall_mm_hr > 5.0 and vehicle_speed_kmh > 60.0 else "MODERATE"
    ev_torque_spin_odds = "HIGH" if rainfall_mm_hr > 8.0 and vehicle_type == "sports_high_torque_ev" else "NORMAL"

    return {
        "rainfall_intensity_mm_hr": rainfall_mm_hr,
        "surface_friction_coefficient_mu": mu,
        "friction_loss_percentage": f"-{round((1.0 - mu/0.78)*100, 1)}%",
        "pavement_regime": regime,
        "critical_hydroplaning_speed_kmh": v_hydroplane_kmh,
        "speed_vs_hydroplane_status": "HYDROPLANING_RISK_ACTIVE" if vehicle_speed_kmh >= v_hydroplane_kmh else "BELOW_HYDROPLANE_LIMIT",
        "dry_braking_distance_80kmh_m": dry_distance_m,
        "wet_braking_distance_m": braking_distance_m,
        "stopping_distance_increase": f"+{distance_increase_pct}%",
        "motorcycle_cornering_hazard": motorcycle_spinout_odds,
        "ev_instant_torque_spin_hazard": ev_torque_spin_odds
    }


if __name__ == "__main__":
    mcp.run()

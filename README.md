# Singapore Spatio-Temporal Road Accident Prediction Engine & ERP 2.0 Telemetry Suite

A full-stack, data-driven engine to quantify, visualize, and predict real-time and historical road accident probabilities across all **55 URA Planning Areas, 332 Subzones, 28 Postal Districts, and 6-digit Postal Codes** in Singapore.

Calibrated against official **Singapore Police Force (SPF) Annual 2025 & Mid-Year 2026 Road Traffic Situation Reports** and the **July 2026 statutory alcohol tolerance amendments**.

---

## Key Features

1. **Multi-Variate Risk Modeling**:
   - **Vehicle Fleet Normalization**: Calibrated multipliers for Motorcycles ($3.65\times$ base risk, $55.6\%$ of 1H2026 accidents), High-Torque EVs / Sports Coupes ($1.44\times$), Lorries with/without $60\text{ km/h}$ speed limiters ($1.21\times$ vs $1.68\times$), PHV/Hybrids ($1.28\times$), and $>10$-year COE vehicles ($+18\%$).
   - **Speed Bands & Speed-Shear Shockwaves**: Fusing LTA DataMall `v4/TrafficSpeedBands` (Bands 1–8) and inter-link speed drops ($|\Delta\text{Band}| \ge 3 \implies 2.35\times$ collision probability).
   - **Hydroplaning & Wet-Onset Slick**: Convective rainfall ($>15\text{ mm/hr}$) and first 20 minutes oil-film lift ($1.55\times$).
   - **Nightlife Kernel & July 2026 BAC Amendment**: Gaussian spatial density ($\sigma = 650\text{ m}$) across Clarke Quay, Orchard, Geylang, Club Street, evaluating driver Blood Alcohol Concentration against both the legacy $80\text{ mg/100ml}$ limit and the **July 2026 statutory limit of $30\text{ mg/100ml}$ blood ($15\,\mu\text{g/100ml}$ breath)**.
   - **Elderly Pedestrian Knockdown & Silver Zones**: Senior citizens ($\ge 65\text{ yrs}$) accounted for $75.0\%$ of pedestrian deaths in 2025; modeled with LTA Silver Zone engineering mitigation (up to $-75\%$ casualties).
2. **7×24 Temporal Intensity Heatmap**:
   - Hourly hazard curves across all 168 hours of the week.
   - Peak avoidance windows: Friday evening commute (17:30–19:45) and weekend late-night alcohol plumes (23:30–03:30).
3. **Secondary Aim A: ERP 2.0 OBU GNSS Telemetry Simulator**:
   - **Intoxication Triangulation**: Entertainment venue parking dwell ($\ge 90\text{ min}$) + nocturnal departure (23:00–04:30) + 1 Hz heading micro-weaving ($\sigma_\theta > 4.2^\circ$).
   - **Zero-Velocity Crash / Stall Detection**: Stationary OBU on live lane ($v = 0\text{ km/h}$ for $>45\text{ s}$) + upstream speed-band drop ($\Delta v < -20\text{ km/h}$) triggering sub-60s V2X virtual gantry alerts and EMAS dispatch.
4. **Secondary Aim B: Google Data Commons International Benchmarking**:
   - Unveils the **COE Utilization Paradox**: Singapore has a low per-capita mortality ($2.44 / 100\text{k}$ pop) but $2.6\times$ higher per-vehicle mortality ($11.0 / 100\text{k}$ registered vehicles) than Japan ($3.4$) or Sweden ($3.8$) due to intense daily vehicle exposure and high two-wheeler density.
5. **3-Tier Ground-Truth Sieve & Online Bayesian Self-Improving Loop**:
   - Tier 1: LTA DataMall real-time feeds.
   - Tier 2: CNA / Straits Times / AsiaOne public news NLP entity corroborator with debiasing weights.
   - Tier 3: SingStat TableBuilder keyless macro auditor.
   - Conjugate Gamma-Poisson online Bayesian updates with EWMA YoY trend velocity $\tau_s$.

---

## Live Interactive Dashboard (GitHub Pages)

Experience the live interactive engine, 7×24 heatmap, and simulation suite on **GitHub Pages**:  
🌐 **[https://lauyeehow1986-hub.github.io/Rta/](https://lauyeehow1986-hub.github.io/Rta/)**

Or open [`index.html`](index.html) locally in any web browser.

---

## Longitudinal Historical Trends & Risk Trajectory (2015 – 2026)

Official audited longitudinal data from **SingStat TableBuilder & Singapore Police Force (SPF)** reveals clear multi-year shifts in Singapore's road safety trajectory:

### Audited 11-Year Incident & Enforcement Matrix

| Year | Injury Crashes | Fatalities | Fatality Rate / 100k | Motorcycle Crashes | Elderly Ped. Crashes | Speeding Violations | Red-Light Crashes |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **2015** | 8,058 | 151 | 2.73 | 4,410 | 218 (24 deaths) | 248,910 | 164 |
| **2016** | 8,277 | 141 | 2.51 | 4,545 | 212 (28 deaths) | 181,050 | 152 |
| **2017** | 7,726 | 121 | 2.16 | 4,350 | 204 (24 deaths) | 160,681 | 139 |
| **2018** | 7,690 | 124 | 2.20 | 4,376 | 217 (24 deaths) | 181,958 | 135 |
| **2019** | 7,822 | 118 | 2.07 | 4,444 | 235 (27 deaths) | 172,040 | 153 |
| **2020 (COVID)** | 5,660 | 107 | 1.49 | 3,194 | 152 (15 deaths) | 162,447 | 125 |
| **2021** | 5,939 | 107 | 1.96 | 3,464 | 158 (14 deaths) | 139,276 | 136 |
| **2022** | 6,779 | 108 | 1.92 | 3,892 | 167 (19 deaths) | 125,530 | 137 |
| **2023** | 6,949 | 136 | 2.30 | 3,792 | 228 (23 deaths) | 116,440 | 112 |
| **2024** | 7,053 | 142 | 2.35 | 3,973 | 203 (11 deaths) | 201,358 | 96 |
| **2025** | **7,560** | **149** | **2.44** | **4,227** | **247 (27 deaths)** | **253,550** | **122** |
| **1H2026** | **3,869** | **61** | **2.04** | **2,186** | **144 (9 deaths)** | **126,976** | **102** |

### Critical Rising Trends & Root Causes

1. **The Senior Pedestrian Crisis (+62.5% Rise Since 2020 Low)**:
   - Elderly pedestrian accidents rose from **152 in 2020** to **247 in 2025 (+62.5%)** and another **144 in 1H2026 (+19.0% YoY)**.
   - Elderly pedestrians ($\ge 65\text{ yrs}$) accounted for **$75.0\%$ of all pedestrian deaths** and **$83.3\%$ of jaywalking deaths in 2025**.
   - *Demographic Driver*: Singapore officially attained "super-aged" status in 2026, with over $21\%$ of residents aged $\ge 65$. Slower walking speed ($0.8\text{ m/s}$ vs $1.2\text{ m/s}$), degraded contrast perception in low-light conditions, and crossing wider multi-lane arterials in mature towns (Toa Payoh, Bishan, Bedok, Chinatown) drive severe vulnerability.
2. **Post-COVID Traffic V-Shaped Rebound (+33.6%)**:
   - Total injury crashes plummeted to a historical low of 5,660 during the 2020 Circuit Breaker before climbing steadily (+33.6% by 2025) as work commutes, cross-border Causeway crossings, and vehicle miles traveled returned to full capacity.
3. **Persistent Motorcycle Majority (55.6% of Crashes)**:
   - Motorcycle involvement climbed from 3,194 in 2020 to **4,227 in 2025 (+32.3%)** and **2,186 in 1H2026**.
   - Two-wheelers consistently represent over half of all casualties despite accounting for only $15.0\%$ of registered motor vehicles, driven by gig-economy delivery deadlines and heavy cross-border traffic along the BKE corridor.
4. **Speed Enforcement Explosion (+117.8% Jump)**:
   - Speeding violations detected by Traffic Police cameras doubled from 116,440 in 2023 to **253,550 in 2025**, following the nationwide activation of speed enforcement functions in red-light cameras.
5. **July 2026 Statutory Alcohol Limit Reduction**:
   - In response to persistent drink-driving accidents (156 in 2025, 888 arrests in 1H2026), Parliament passed the Road Traffic (Miscellaneous Amendments) Act lowering the statutory limit to **$30\text{ mg/100ml}$ blood ($15\,\mu\text{g/100ml}$ breath)**, matching international best practices in Japan and South Korea.

---

## Interactive Dashboard

Open [`index.html`](index.html) in any modern browser for:
- Interactive 7×24 day $\times$ hour accident density heatmap
- Interactive 11-year historical trends & demographic progression chart
- Singapore vector GIS corridor map
- Real-time multi-variate risk odds calculator
- ERP 2.0 in-cabin OBU simulation display
- Global benchmarking radar table

---

## FastMCP Server Configuration (`mcp_config.json`)

```json
{
  "mcpServers": {
    "sg-road-accident-risk-engine": {
      "command": "python3",
      "args": ["./skills/sg-road-accident-risk-engine/scripts/mcp_server.py"],
      "env": {
        "PYTHONUTF8": "1",
        "LTA_DATAMALL_API_KEY": "YOUR_LTA_KEY",
        "ONEMAP_API_TOKEN": "YOUR_ONEMAP_TOKEN"
      }
    },
    "singstat-traffic-verifier": {
      "command": "python3",
      "args": ["./skills/sg-road-accident-risk-engine/scripts/singstat_verifier_mcp.py"]
    },
    "sg-news-accident-corroborator": {
      "command": "python3",
      "args": ["./skills/sg-road-accident-risk-engine/scripts/sg_news_corroborator_mcp.py"]
    },
    "datacommons-road-safety-benchmark": {
      "command": "python3",
      "args": ["./skills/sg-road-accident-risk-engine/scripts/datacommons_benchmark_mcp.py"]
    }
  }
}
```

---

## Directory Structure

```text
├── index.html                                        # Standalone Interactive HTML Dashboard
├── requirements.txt                                  # Python dependencies (mcp, httpx, pydantic)
├── mcp_config.json                                   # FastMCP client configuration
├── ANTIGRAVITY_MASTER_PROMPT.md                      # Full specification & engineering prompt
└── skills/
    └── sg-road-accident-risk-engine/
        ├── SKILL.md                                  # Antigravity skill definition
        ├── references/
        │   └── mathematical_model.md                 # Cox-Hawkes intensity & speed-shear math
        └── scripts/
            ├── mcp_server.py                         # Core FastMCP risk server & ERP 2.0 engine
            ├── singstat_verifier_mcp.py              # SingStat TableBuilder macro-auditor
            ├── sg_news_corroborator_mcp.py           # CNA/Straits Times RSS NLP extractor
            ├── datacommons_benchmark_mcp.py          # Data Commons international benchmarker
            └── bayesian_self_improver.py             # Gamma-Poisson conjugate Bayesian loop
```

---

## License

Educational and research analytics tool — not for clinical or real-time statutory enforcement. Grounded in Singapore Police Force Annual 2025 and Mid-Year 2026 Road Traffic Situation data.

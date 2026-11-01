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

## Interactive Dashboard

Open [`index.html`](index.html) in any modern browser for:
- Interactive 7×24 day $\times$ hour accident density heatmap
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

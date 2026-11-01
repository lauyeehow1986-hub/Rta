---
name: sg-road-accident-risk-engine
description: Spatio-temporal Singapore road accident prediction engine, live A-to-B route hazard calculator, ERP 2.0 OBU GNSS intoxication/stall triangulation simulator, SingStat TableBuilder macro-auditor, Public News NLP incident corroborator, Google Data Commons international country-to-country road safety benchmarker, and online Bayesian self-improving risk index across Singapore URA subzones and 6-digit postal codes. Use whenever analyzing Singapore traffic accidents, LTA DataMall Speed Bands/Traffic Incidents, SingStat/SPF casualty verification, news incident extraction, vehicle/driver risk profiles, pedestrian/jaywalking blackspots, nightlife drink-driving plumes, or ERP 2.0 telemetry.
allowed-tools: google default_api skills
---
# Singapore Road Accident Spatio-Temporal Risk Engine, SingStat/News Verifier & ERP 2.0 Suite

End-to-end framework for predicting and verifying road accident probability across Singapore URA Subzones, expressway corridors, and 6-digit postal codes by fusing a **3-Tier Ground-Truth Verification Architecture**:
- **Tier 1 (Real-Time Telemetry Stream)**: LTA DataMall `TrafficIncidents` & `v4/TrafficSpeedBands`, NEA 5-minute `rainfall`, and SLA OneMap Routing.
- **Tier 2 (Public News & SPF Media Room NLP Corroborator)**: Real-time RSS/web extraction from Channel NewsAsia (CNA), The Straits Times, AsiaOne, Mothership, and SPF News Releases to fill the "LTA Attribute Blind Spot" (extracting vehicle make/model, driver age, solo vs. peer passengers, pedestrian jaywalking, hit-and-run/drink-driving charges, and hospital casualty counts).
- **Tier 3 (SingStat TableBuilder & data.gov.sg Macro-Statistical Auditor)**: Keyless REST queries to SingStat TableBuilder (`tablebuilder.singstat.gov.sg/api/table/tabledata/{resourceId}`) and `data.gov.sg` to anchor annual/semi-annual casualty totals, subzone senior ($\ge 65\text{ yrs}$) population denominators, and registered vehicle population by make/fuel type—neutralizing media reporting bias via Iterative Proportional Fitting (IPF) and Empirical Bayes shrinkage.

## When to Use

- Predicting road accident odds at any Singapore 6-digit postal code, URA subzone, or A-to-B route at a specific day and hour
- Auditing or verifying road traffic statistics, vehicle fleet denominators, and subzone senior demographics against official **SingStat TableBuilder** and **SPF Annual / Mid-Year Road Traffic Situation** baselines
- Extracting micro-level causal attributes (car make/model, driver age cohort, passenger occupancy, elderly jaywalking, hospital conveyances) from breaking Singapore traffic news (CNA, Straits Times, AsiaOne, SPF Media Room) to enrich sparse 1-line LTA `TrafficIncidents` alerts
- Analyzing how vehicle class/make/power-to-weight, COE age, lorry speed limiters, driver age, passenger load, BAC tolerance limits ($80\text{ mg/100ml}$ vs. July 2026 amended $30\text{ mg/100ml}$ blood / $15\,\mu\text{g/100ml}$ breath), and wet-road hydroplaning interact
- Simulating ERP 2.0 On-Board Unit (OBU) GNSS trajectory triangulation for nightlife intoxication profiling and stationary crash/stall detection
- Deploying the unified or modular FastMCP servers (`mcp_server.py`, `nea_weather_mcp.py`, `singstat_verifier_mcp.py`, `sg_news_corroborator_mcp.py`) in Antigravity IDE with Gemini 3.8 Flash

## Step-by-Step Workflow

### Step 1: Compute Base Spatio-Temporal Hazard & Trend Velocity

1. **Resolve Spatial Unit**:
   - Map 6-digit postal codes (via SLA OneMap Search/Reverse Geocode API) to their parent 2-digit Postal Sector, URA Subzone, and adjacent Expressway/Arterial Corridor.
2. **Apply Spatio-Temporal Cox-Hawkes Hazard Function**:
   - Compute instantaneous accident intensity $\lambda(s, t)$ per subzone $s$ and hour $t$:
     $$\lambda(s, t) = \kappa_{\text{SingStat}} \cdot \lambda_0(s) \cdot \exp\left(\beta_{\text{temp}}(d, h) + \beta_{\text{trend}}(s)\cdot \Delta t + \mathbf{w}^\top \mathbf{x}(s, t)\right) + \sum_{t_i < t} \alpha \exp(-\omega (t - t_i))$$
   - Where $\kappa_{\text{SingStat}}$ is the macro-calibration scaling factor anchoring the sum of subzone expectations to the audited SingStat/SPF national casualty total, $\beta_{\text{trend}}(s)$ captures the subzone's YoY accident growth velocity, and the Hawkes self-exciting decay $\alpha \exp(-\omega(t - t_i))$ captures secondary rear-end pile-ups triggered within 45 minutes of a primary collision.

### Step 2: Apply Multi-Factor Risk Multipliers

1. **Average Road Speed & Speed Variance Paradox ($M_{\text{speed}}$)**:
   - Query LTA DataMall `v4/TrafficSpeedBands` (Bands 1 to 8).
   - Model the bimodal hazard curve plus inter-band shear:
     - **Congestion Stop-and-Go Regime (Bands 1-2, $<20\text{ km/h}$)**: Elevated multi-vehicle tailgating and lane-filtering motorcycle side-swipes ($M_{\text{freq}} = 1.42\times$).
     - **Free-Flow Overspeed Regime (Bands 7-8, $\ge 70\text{ km/h}$ arterial or $>90\text{ km/h}$ expressway)**: Exponential kinetic energy severity ($E_k = \frac{1}{2}mv^2$).
     - **Speed Shear Shockwave ($|\Delta \text{Band}| \ge 3$ between adjacent links)**: Highest overall crash probability ($2.35\times$) when Band 7/8 free-flow traffic slams into a sudden Band 1/2 queue at expressway merges.
2. **Weather & Hydroplaning Coupling ($M_{\text{weather}}$) via `sg-nea-weather-mcp`**:
   - Query NEA Real-Time APIs (keyless v2 endpoints via `api-open.data.gov.sg`):
     - **5-Minute Station Rainfall**: `https://api-open.data.gov.sg/v2/real-time/api/rainfall` (across all 88 active stations islandwide).
     - **2-Hour Town Nowcast**: `https://api-open.data.gov.sg/v2/real-time/api/two-hr-forecast` (47 planning area forecast strings).
     - **Wind Speed & Direction**: `https://api-open.data.gov.sg/v2/real-time/api/wind-speed` (detecting lateral bridge crosswinds).
   - **Tire-Pavement Friction Degradation & Hydroplaning Physics**:
     - *Dry Asphalt*: Friction coefficient $\mu \approx 0.78 - 0.82$.
     - *First 20 Minutes (Wet-Onset Oil-Film Lift)*: Rain emulsifies deposited road oils into a slick film ($1.55\times$ hazard, $\mu \approx 0.58$).
     - *Moderate Rain ($5 - 15\text{ mm/hr}$)*: Continuous surface water sheeting ($\mu \approx 0.48$, braking distance increases $+62\%$ at $80\text{ km/h}$).
     - *Convective Deluge ($>15\text{ mm/hr}$)*: Deep ponding triggers tire hydroplaning ($2.60\times$ hazard, $\mu \approx 0.38$, stopping distance increases $+105\%$).
   - **Horne's Dynamic Hydroplaning Threshold Equation**:
     $$V_{\text{hydro}} = 10.35 \cdot \sqrt{P_{\text{tire}}} \cdot \left(\frac{D_{\text{tread}}}{8.0}\right)^{0.35}$$
     At standard passenger tire pressure ($32\text{ psi}$) with $4\text{ mm}$ tread depth, critical hydroplaning occurs at **$58.5\text{ km/h}$**; vehicles traveling at expressway limits ($90\text{ km/h}$) completely lose directional steering.
3. **Bar / Pub / Coffee-Shop Kernel Density & BAC Tolerance ($M_{\text{alcohol}}$)**:
   - Compute spatial Gaussian kernel density $K_{\text{bar}}(s)$ with $\sigma = 650\text{ m}$ over licensed nightlife clusters and late-night coffee shops.
   - Activate diurnal nightlife plume multiplier between **22:00 and 04:30**, scaling risk by driver BAC relative to both the legacy $80\text{ mg/100ml}$ ($35\,\mu\text{g/100ml}$ breath) threshold and the July 2026 Road Traffic Act amendment threshold of **$30\text{ mg/100ml}$ blood ($15\,\mu\text{g/100ml}$ breath)**.
4. **Fleet-Normalized Vehicle Make, Model, Type & Age Profile ($M_{\text{veh}}$)**:
   - Normalize crash counts by registered fleet size from SingStat/LTA `MVP01-6_Cars_by_make`:
     $$R_{\text{make}} = \frac{\text{Accidents}_{\text{make}} / \text{Total Accidents}}{\text{Registered Fleet}_{\text{make}} / \text{Total Fleet}}$$
   - Apply calibrated multipliers: Motorcycles ($3.65\times$), Un-limited Commercial Lorries ($1.68\times$) vs. $60\text{ km/h}$ Speed-Limiter Compliant Lorries ($1.21\times$), High-Torque EVs/Sports Coupes ($1.44\times$), PHV/High-Mileage Hybrids ($1.28\times$), Mass-Market Sedans/SUVs ($1.00\times$), and $>10$-year COE vehicles ($+18\%$).
5. **Driver Profile & Pedestrian Knockdown Vulnerability ($M_{\text{driver}}, M_{\text{ped}}$)**:
   - Weight U-shaped driver age curve ($18\text{--}25\text{ yrs}$ $1.72\times$, $31\text{--}50\text{ yrs}$ $1.00\times$, $\ge 65\text{ yrs}$ $1.48\times$), social occupancy (solo night fatigue $1.38\times$, young peer passengers $1.52\times$, family $0.86\times$), and subzone senior pedestrian share ($\ge 65\text{ yrs}$, $75.0\%$ of pedestrian deaths and $83.3\%$ of jaywalking deaths in 2025), mitigated by $-75\%$ inside LTA Silver Zones.

### Step 3: Execute ERP 2.0 OBU GNSS Triangulation & Anomaly Detection

1. **Social & Venue Dwell-Time Intoxication Triangulation**:
   - Fuse entertainment-zone parking dwell duration $D \ge 90\text{ min}$ ($<250\text{ m}$ of bars/clubs), departure time $t_{\text{dep}} \in [23:00, 04:30]$, and 1 Hz GNSS heading oscillation variance ($\sigma_{\theta} > 4.2^\circ$) to compute the real-time **Intoxication Probability Score ($\text{IPS} \in [0, 1]$)**.
2. **Zero-Velocity Crash / Stall Triangulation**:
   - Detect stationary OBU dwell ($v = 0\text{ km/h}$ for $>45\text{ s}$) on live expressway/arterial lanes paired with an immediate upstream speed-band drop ($\Delta v < -20\text{ km/h}$), triggering V2X virtual gantry warnings $1.5\text{ km}$ upstream and EMAS dispatch.

### Step 4: Execute 3-Tier Ground-Truth Verification (SingStat MCP + Public News MCP)

1. **Why Both MCPs Are Essential**:
   - **LTA DataMall `TrafficIncidents`** gives fast coordinates and timestamps (`(31/10)08:02 Accident on TPE...`), but lacks vehicle make, driver age, passenger count, pedestrian jaywalking, or drink-driving context.
   - **Public News MCP (`sg_news_corroborator_mcp.py`)** scrapes CNA (`channelnewsasia.com/api/v1/rss-outbound-feed?_format=xml`), The Straits Times, AsiaOne, and SPF Media Releases to extract rich micro-attributes (e.g., *"Two arrested over fatal hit-and-run Tampines accident; man, 30, to be charged"*, *"Motorcycle catches fire after 4-vehicle accident on TPE; 40-year-old lorry driver and six passengers aged 21-61, plus two motorcyclists aged 25 and 37 hospitalized"*).
   - **SingStat TableBuilder MCP (`singstat_verifier_mcp.py`)** queries `https://tablebuilder.singstat.gov.sg/api/table/tabledata/{resourceId}` (no API key required) to enforce official macro totals and neutralize news selection/sensationalism bias.
2. **Iterative Proportional Fitting (IPF) & Debiased Bayesian Update**:
   - Run `reconcile_three_tier_truth` in `scripts/mcp_server.py` or `scripts/bayesian_self_improver.py`:
     - Use Public News NLP records to update **conditional feature likelihoods** $P(\text{DriverAge}, \text{Make}, \text{Occupancy}, \text{Cause} \mid \text{Severe Crash}, s)$ with importance-sampling weight $w_{\text{debias}} = \frac{\pi_{\text{SingStat}}(c)}{\pi_{\text{News}}(c)}$ so over-reported supercar/fire crashes do not skew baseline probabilities.
     - Use SingStat TableBuilder & SPF official totals to constrain $\sum_{s, t} \lambda(s, t) = N_{\text{SingStat/SPF}}$ and detect macro drift ($|\Delta_{\text{drift}}| > 2.5\%$ triggers automatic recalibration).


### Step 5: Execute Secondary Aim B — Country-to-Country Benchmarking via Google Data Commons MCP

1. **Connect Official `datacommons-mcp` + `datacommons_benchmark_mcp.py`**:
   - Use Google's hosted or local Data Commons MCP (`uvx datacommons-mcp` or `https://api.datacommons.org/mcp`) alongside `scripts/datacommons_benchmark_mcp.py` to query cross-national indicators across DCIDs (`country/SGP`, `country/JPN`, `country/SWE`, `country/GBR`, `country/KOR`, `country/AUS`, `country/MYS`).
2. **Normalize Across Both Per-Capita and Per-Vehicle Denominators**:
   - Always compute **both**:
     - **Fatalities per 100,000 Population**: Singapore is low (`2.44` in 2025 vs. Asia-Pacific average `15.2` and ASEAN average `14.4`), placing it close to Japan (`2.10`), Sweden (`2.00`), and the UK (`2.50`).
     - **Fatalities per 100,000 Registered Motor Vehicles**: Because Singapore's Vehicle Quota System (COE) caps motorization at `165.7 vehicles per 1,000 population` (vs. `540–740` in OECD peers), Singapore's per-vehicle fatality rate (`~11.0 per 100,000 vehicles`) is **$2.6\times$ to $3.2\times$ higher** than Japan (`3.4`), Sweden (`3.8`), and the UK (`4.2`), driven by intense daily mileage per vehicle and high two-wheeler/cross-border exposure (`53.0%` of deaths).
3. **Hard Isolation Guardrail (Anti-Contamination Rule)**:
   - **NEVER** allow stale country-level observations from `datacommons.org` (which often lag 2–3 years from WHO/UN feeds) to overwrite Singapore's domestic `singstat-traffic-verifier` or SPF 2025/2026 numbers (`7,560` injury crashes in 2025; `3,929` total crashes in 1H2026).
   - Use Data Commons strictly as a **read-only comparative policy lens** to transfer proven international interventions (e.g., Japan/South Korea's `30 mg/100ml` BAC enforcement, UK's SPECS average speed cameras, Sweden's Vision Zero median/junction treatments) into Singapore's subzone risk simulator.

## Gotchas

- **SingStat User-Agent Header**: SingStat TableBuilder API requires no API key, but blocks bare Python `urllib` requests unless you pass `'User-Agent': 'Mozilla/5.0'` and `'Accept': 'application/json'`.
- **News Sensationalism Bias**: Never add raw news article counts directly to subzone frequency priors without multiplying by the SingStat Empirical Bayes shrinkage factor $w_{\text{debias}}$; news outlets report $\sim 85\%$ of fatal/multi-vehicle expressway crashes but $<3\%$ of routine arterial injury accidents.

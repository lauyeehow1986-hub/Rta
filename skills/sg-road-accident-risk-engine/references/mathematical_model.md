# Spatio-Temporal Hazard, Speed-Shear & ERP 2.0 Triangulation Formulation

## 1. Hierarchical Cox-Hawkes Spatio-Temporal Intensity
For any Singapore URA Subzone or 6-digit Postal Code centroid $s$ at day-of-week $d \in \{0..6\}$ and hour $h \in [0, 24)$:

$$\lambda(s, t) = \lambda_0(s) \cdot (1 + \tau_s)^{\Delta y} \cdot \prod_{k \in \mathcal{F}} M_k(s, t) + \sum_{t_i < t} \alpha \exp(-\omega (t - t_i))$$

Where:
- $\lambda_0(s)$: Gamma-Poisson posterior baseline rate per 1,000 vehicle-trips in subzone $s$.
- $\tau_s$: YoY accident trend velocity (e.g., $+14.2\%$ along TPE/Punggol-Sengkang, $+13.5\%$ in ageing Toa Payoh/Bishan estates due to senior pedestrian casualties, $+12.9\%$ along PIE Jurong/Tuas logistics corridor).
- $\alpha \exp(-\omega(t - t_i))$: Self-exciting Hawkes secondary crash kernel ($\omega = 1.33\text{ hr}^{-1}$) modeling rubbernecking and sudden queue-tail pile-ups following an initial incident.

## 2. Average Speed Band & Inter-Link Shear Factor ($M_{\text{speed}}$)
Using LTA DataMall `v4/TrafficSpeedBands` (Bands 1 to 8):
- **Band 1–2 ($0\text{–}20\text{ km/h}$)**: Elevated side-swipe and rear-end frequency ($1.42\times$), particularly for lane-splitting motorcycles ($55.6\%$ of all Singapore traffic accidents in 1H2026).
- **Band 7–8 ($\ge 70\text{ km/h}$ arterial, $>90\text{ km/h}$ expressway)**: Kinetic severity scales as $(v/v_0)^{2.4}$.
- **Inter-Link Speed Shear ($|\Delta v|$ between upstream link $e_{i-1}$ and downstream link $e_i$)**:
  $$M_{\text{shear}} = 1 + 1.35 \cdot \max\left(0, \frac{v_{i-1} - v_i - 15}{25}\right)$$

## 3. Nightlife Kernel & 2026 Amended BAC Tolerance Decay ($M_{\text{alcohol}}$)
Following the **Road Traffic (Miscellaneous Amendments) Act (passed July/August 2026)**, Singapore lowered the statutory limit from $80\text{ mg/100ml}$ blood ($35\,\mu\text{g/100ml}$ breath) to **$30\text{ mg/100ml}$ blood ($15\,\mu\text{g/100ml}$ breath)**, while Widmark elimination follows $C(t) = \max(0, C_0 - \beta_{\text{elim}} \cdot t)$ with $\beta_{\text{elim}} \approx 15\text{ mg/(100ml}\cdot\text{hr)}$.

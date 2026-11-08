# Youth Influence Intelligence – Exploratory Findings  
## 2025 National Youth Risk Behavior Survey (YRBS)

**Data:** CDC 2025 National YRBS cleaned file (N = 10,710 student records).  
**Design:** Stratified, two-stage cluster sample. All estimates are **weighted** and use Taylor-linearization variance with the survey design variables (`weight`, `stratum`, `psu`). Confidence intervals are 95% (t-based).  
**Important:** Results describe associations only. No causal claims are made. Individual students are never labelled “high-risk.”

---

### 1. Overall prevalence of current substance use (past 30 days)

| Behavior | Weighted % | 95% CI | Unweighted n |
|----------|------------|--------|--------------|
| Current alcohol use | 20.3 | 18.0 – 22.5 | 10,259 |
| Current e-vapor product use | 16.0 | 14.2 – 17.9 | 10,532 |
| Current cigarette use | 3.5 | 2.7 – 4.3 | 10,535 |

- Alcohol is the most common of the three current-use behaviors.  
- E-vapor use is substantially more prevalent than cigarette smoking.  
- Ever-use of e-vapor products is 30.2% (27.4–33.0); ever cigarette smoking is 14.1% (11.8–16.3) among those who answered the ever-smoked item (note: higher missingness on that item).

---

### 2. Age and grade gradients

Current use rises with both age and grade for all three substances.

**By grade (selected):**
- 9th grade: alcohol 11.5%, e-vapor 11.1%, cigarettes 2.1%  
- 12th grade: alcohol 30.9%, e-vapor 19.5%, cigarettes 5.1%

**By age (selected):**
- Age 14: alcohol 9.2%, e-vapor 11.2%, cigarettes 1.6%  
- Age ≥18: alcohol 32.1%, e-vapor 18.9%, cigarettes 5.2%

The steepest absolute increase is for alcohol between 9th and 12th grade.

---

### 3. Parental monitoring

Among students who answered the parental-monitoring question (n ≈ 6,500; **39% of the sample is blank on this item**):

| Monitoring level | Alcohol % (CI) | E-vapor % (CI) | Cigarette % (CI) |
|------------------|----------------|----------------|------------------|
| High (most/always know location & companions) | 20.0 (17.0–23.0) | 15.2 (12.7–17.7) | 2.6 (1.7–3.6) |
| Lower | 34.2 (28.9–39.5) | 30.0 (26.3–33.8) | 8.2 (5.4–11.0) |

Students reporting lower parental monitoring have markedly higher weighted prevalence of all three current substance-use behaviors. Because of the large block of missing answers, these estimates apply only to students who completed the monitoring item; they cannot be generalized to the full sample without further assumptions.

---

### 4. School connectedness

Students who agree or strongly agree that they “feel close to people at their school” (63.2% overall):

| Connectedness | Alcohol % | E-vapor % | Cigarette % |
|---------------|-----------|-----------|-------------|
| High | 21.8 | 15.7 | 3.1 |
| Lower | 19.5 | 18.2 | 4.2 |

Differences are modest and confidence intervals overlap for alcohol. E-vapor and cigarette use are slightly higher among students reporting lower connectedness; the pattern is weaker than the parental-monitoring contrast.

---

### 5. Mental-health indicators

Clear positive associations appear between several mental-health indicators and current substance use.

**Felt sad or hopeless almost every day for ≥2 weeks (past 12 months):**
- Yes → alcohol 28.1%, e-vapor 26.1%, cigarettes 5.8%  
- No  → alcohol 16.6%, e-vapor 11.2%, cigarettes 2.3%

**Seriously considered suicide (past 12 months):**
- Yes → alcohol 35.8%, e-vapor 34.2%, cigarettes 8.2%  
- No  → alcohol 17.7%, e-vapor 12.9%, cigarettes 2.7%

**Mental health “not good” most of the time or always (past 30 days):**
- Yes → alcohol 28.5%, e-vapor 25.3%, cigarettes 5.1%  
- No  → alcohol 18.0%, e-vapor 13.3%, cigarettes 2.6%

Similar elevations are observed for self-harm, suicide planning, and suicide attempts (see `by_mental_health.csv`). These are associations in cross-sectional data; directionality and confounding cannot be assessed here.

---

### 6. Peer-related indicators (proxies only)

The 2025 YRBS contains **no direct measure of peer substance use or peer influence**. Three peer-/online-context proxies were examined:

**Bullied on school property (past 12 months):**
- Yes → alcohol 26.9%, e-vapor 25.4%, cigarettes 6.8%  
- No  → alcohol 18.6%, e-vapor 13.7%, cigarettes 2.6%

**Electronically bullied:**
- Parallel elevation among those who experienced electronic bullying (see data files).

**High social-media use (several times a day or more – 80.2% of students):**
- Yes → alcohol 23.1%, e-vapor 17.9%, cigarettes 3.4%  
- No  → alcohol 8.7%, e-vapor 8.6%, cigarettes 2.5%

These proxies capture exposure to bullying and intensity of online activity; they should **not** be interpreted as measures of peer influence or peer norms around substance use.

---

### 7. Meaningful patterns (descriptive)

1. **Alcohol and e-vapor** are the dominant current-use behaviors; cigarette smoking remains relatively uncommon.  
2. **Clear age/grade gradient** – especially for alcohol.  
3. **Lower parental monitoring** is associated with substantially higher prevalence of all three substances (with the caveat of high missingness).  
4. **Mental-health distress indicators** (sad/hopeless, suicidal ideation, poor current mental health) show consistent positive associations with current substance use.  
5. **School connectedness** shows only modest, less consistent differences.  
6. **Bullying experiences and high social-media use** are associated with higher substance-use prevalence, but remain proxies rather than direct peer-influence measures.

---

### 8. Limitations

- **Cross-sectional design** – no temporal or causal inference is possible.  
- **Self-report** – subject to recall and social-desirability bias.  
- **Missing data** – especially high for parental monitoring (≈39% blank) and some mental-health items. Students missing these items are not a random subset; results for those variables describe only respondents.  
- **No direct peer-influence items** – the survey does not ask about friends’ substance use.  
- **Complex sample** – standard errors incorporate the design; unweighted percentages would misrepresent national figures.  
- **Response rate** – overall response rate reported by CDC is 30.6%; weights adjust for non-response at school and student levels, but residual bias cannot be ruled out.  
- **Q31 (ever cigarette)** has elevated missingness; CDC’s own ever-smoked flag is also blank for those students.

---

### Files produced for Streamlit / further use

```
yrbs_analysis/
├── analysis_results.json          # all estimates
├── overall_prevalences.csv
├── by_age.csv / by_grade.csv
├── by_parental_monitoring.csv
├── by_school_connectedness.csv
├── by_mental_health.csv
├── by_peer_proxies.csv
├── FINDINGS_SUMMARY.md            # this document
└── charts/
    ├── 01_overall_substance.{html,png}
    ├── 02_by_grade.{html,png}
    ├── 03_by_age.{html,png}
    ├── 04_parental_monitoring.{html,png}
    ├── 05_school_connectedness.{html,png}
    ├── 06_mental_health_sad.{html,png}
    ├── 07_bullying_proxies.html / 07a_*.png / 07b_*.png
    └── 08_social_media.{html,png}
```

Interactive Plotly HTML files and static PNGs are ready for embedding in a Streamlit application.

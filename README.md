# Youth Influence Intelligence

Interactive public-health analytics platform using the **2025 CDC National Youth Risk Behavior Survey (YRBS)**.

Helps schools, parents, and youth organizations explore patterns associated with alcohol, nicotine, and vaping among U.S. high-school students.

**Important:** Results describe **associations only**. This tool does **not** establish causation and does **not** predict any individual student’s behavior.

---

## What’s inside

| Page | Purpose |
|------|---------|
| **Executive Dashboard** | National snapshot of current alcohol, e-vapor, and cigarette use + grade trends |
| **Substance Explorer** | Compare substances by grade or age with confidence intervals |
| **Influence Explorer** | Parental monitoring, school connectedness, mental health, peer-related proxies |
| **Prevention Intelligence** | Rule-based, evidence-informed prevention suggestions linked to observed findings |
| **Data & Methodology** | Dataset description, weighting, variable definitions, limitations, citations |

All estimates are **survey-weighted** and use the complex sample design (stratum + PSU) with Taylor-linearization variance.

---

## Quick start (local)

### 1. Prerequisites
- Python 3.9+  
- A terminal (Mac Terminal, Windows PowerShell, or VS Code terminal)

### 2. Install dependencies
```bash
cd youth_influence_intelligence
python -m venv .venv

# Mac / Linux
source .venv/bin/activate

# Windows
.venv\Scripts\activate

pip install -r requirements.txt
```

### 3. Run the app
```bash
streamlit run app.py
```

Your browser should open to `http://localhost:8501`.

---

## Deploy free on Streamlit Community Cloud

You do **not** need paid hosting or any API key.

### Step A — Put the project on GitHub

1. Create a free account at [github.com](https://github.com) if you don’t have one.
2. Create a **new repository** (e.g. `youth-influence-intelligence`). Leave it empty (no README).
3. On your computer, open a terminal in the project folder and run:

```bash
git init
git add .
git commit -m "Initial Youth Influence Intelligence app"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/youth-influence-intelligence.git
git push -u origin main
```

Replace `YOUR_USERNAME` with your GitHub username.

### Step B — Deploy on Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub.
2. Click **New app**.
3. Select your repository, branch `main`, and set the main file path to:  
   `app.py`
4. Click **Deploy**.

Streamlit Cloud will install packages from `requirements.txt` and host the app for free.  
You get a public URL you can share.

---

## Project structure

```
youth_influence_intelligence/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── README.md              # This file
├── .streamlit/
│   └── config.toml        # Theme (navy / teal / white)
├── data/
│   ├── yrbs2025_cleaned.csv
│   └── yrbs2025_data_dictionary.xlsx
└── analysis/
    ├── analysis_results.json
    ├── overall_prevalences.csv
    ├── by_age.csv
    ├── by_grade.csv
    ├── by_parental_monitoring.csv
    ├── by_school_connectedness.csv
    ├── by_mental_health.csv
    ├── by_peer_proxies.csv
    ├── FINDINGS_SUMMARY.md
    └── charts/            # PNG + interactive HTML charts
```

---

## Data notes

- Source: CDC 2025 National YRBS.  
- Analytic sample: 10,710 student records.  
- Weights and design variables (`weight`, `stratum`, `psu`) are used for all primary estimates.  
- See **Data & Methodology** inside the app and `analysis/FINDINGS_SUMMARY.md` for full details and limitations.

---

## License & attribution

This application is provided for educational and public-health planning purposes.  
YRBS data are collected and released by the U.S. Centers for Disease Control and Prevention.  
Always cite CDC when reporting figures derived from YRBS.

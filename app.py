"""
Youth Influence Intelligence
Interactive public-health analytics platform using 2025 CDC National YRBS data.
Associations only — no causal claims, no individual prediction.
"""

from pathlib import Path
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st

# ---------------------------------------------------------------------------
# Paths & theme
# ---------------------------------------------------------------------------
BASE = Path(__file__).parent
DATA_DIR = BASE / "data"
ANALYSIS_DIR = BASE / "analysis"
CHARTS_DIR = ANALYSIS_DIR / "charts"

NAVY = "#1A365D"
TEAL = "#0D7377"
TEAL_LIGHT = "#14A3A8"
WHITE = "#FFFFFF"
LIGHT_BG = "#F7FAFC"
CARD_BG = "#FFFFFF"
MUTED = "#718096"
ACCENT = "#2C7A7B"

SUBSTANCE_COLORS = {
    "Current alcohol use (past 30d)": "#2B6CB0",
    "Current e-vapor use (past 30d)": "#DD6B20",
    "Current cigarette use (past 30d)": "#38A169",
    "alcohol": "#2B6CB0",
    "e-vapor": "#DD6B20",
    "cigarette": "#38A169",
}

# ---------------------------------------------------------------------------
# Data loading (cached)
# ---------------------------------------------------------------------------
@st.cache_data(show_spinner=False)
def load_json_results():
    path = ANALYSIS_DIR / "analysis_results.json"
    with open(path, encoding="utf-8") as f:
        return json.load(f)


@st.cache_data(show_spinner=False)
def load_csv(name: str) -> pd.DataFrame:
    return pd.read_csv(ANALYSIS_DIR / name)


@st.cache_data(show_spinner=False)
def load_cleaned_sample(nrows: int = 500) -> pd.DataFrame:
    """Small sample of cleaned data for methodology page only."""
    return pd.read_csv(DATA_DIR / "yrbs2025_cleaned.csv", nrows=nrows)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def pct_ci(row) -> str:
    return f"{row['pct']:.1f}% ({row['ci_low']:.1f}–{row['ci_high']:.1f})"


def metric_card(label: str, value: str, help_text: str = ""):
    st.markdown(
        f"""
        <div style="
            background: {CARD_BG};
            border-left: 4px solid {TEAL};
            border-radius: 8px;
            padding: 1rem 1.25rem;
            box-shadow: 0 1px 3px rgba(0,0,0,0.08);
            margin-bottom: 0.5rem;
        ">
            <div style="font-size:0.8rem; color:{MUTED}; text-transform:uppercase; letter-spacing:0.04em;">{label}</div>
            <div style="font-size:1.75rem; font-weight:700; color:{NAVY}; margin-top:0.25rem;">{value}</div>
            <div style="font-size:0.75rem; color:{MUTED}; margin-top:0.35rem;">{help_text}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_header(title: str, subtitle: str = ""):
    st.markdown(
        f"""
        <h2 style="color:{NAVY}; margin-bottom:0.15rem;">{title}</h2>
        <p style="color:{MUTED}; margin-top:0; margin-bottom:1.25rem;">{subtitle}</p>
        """,
        unsafe_allow_html=True,
    )


def disclaimer_box():
    st.info(
        "**Important:** All results describe **associations** observed in the 2025 National YRBS. "
        "They do **not** establish causation. This tool does not predict any individual student’s behavior."
    )


def apply_plotly_theme(fig, title: str = ""):
    fig.update_layout(
        title=dict(text=title, font=dict(size=16, color=NAVY), x=0.02),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="sans-serif", color=NAVY),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0),
        margin=dict(t=60, b=40, l=40, r=20),
        height=420,
    )
    fig.update_xaxes(showgrid=False, zeroline=False)
    fig.update_yaxes(showgrid=True, gridcolor="#E2E8F0", zeroline=False, title_text="Weighted percent")
    return fig


# ---------------------------------------------------------------------------
# Page: Executive Dashboard
# ---------------------------------------------------------------------------
def page_executive(results: dict):
    section_header(
        "Executive Dashboard",
        "National snapshot of current substance use among U.S. high-school students (2025 YRBS)."
    )
    disclaimer_box()

    overall = pd.DataFrame(results["overall"])
    # Keep the three main current-use indicators
    main = overall[overall["label"].str.contains("Current", na=False)].copy()
    main = main.sort_values("pct", ascending=False)

    st.markdown("### Current substance use (past 30 days)")
    cols = st.columns(3)
    for i, (_, row) in enumerate(main.iterrows()):
        with cols[i]:
            metric_card(
                row["label"].replace(" (past 30d)", ""),
                f"{row['pct']:.1f}%",
                f"95% CI: {row['ci_low']:.1f}–{row['ci_high']:.1f}% · n={int(row['n_unweighted']):,}"
            )

    # Bar chart
    fig = go.Figure()
    for _, row in main.iterrows():
        color = SUBSTANCE_COLORS.get(row["label"], TEAL)
        fig.add_trace(go.Bar(
            x=[row["label"].replace(" (past 30d)", "")],
            y=[row["pct"]],
            error_y=dict(type="data", array=[row["ci_high"] - row["pct"]],
                         arrayminus=[row["pct"] - row["ci_low"]], visible=True),
            marker_color=color,
            text=[f"{row['pct']:.1f}%"],
            textposition="outside",
            name=row["label"],
            showlegend=False,
        ))
    fig = apply_plotly_theme(fig, "Weighted prevalence of current substance use")
    fig.update_layout(yaxis_range=[0, max(main["ci_high"]) * 1.25])
    st.plotly_chart(fig, use_container_width=True)

    # Grade gradient
    st.markdown("### Grade gradient")
    by_grade = pd.DataFrame(results["by_grade"])
    # Restrict to main grades 9–12
    by_grade = by_grade[by_grade["grade_label"].isin(["9th", "10th", "11th", "12th"])]
    fig2 = go.Figure()
    for outcome, color in [
        ("Current alcohol use (past 30d)", SUBSTANCE_COLORS["alcohol"]),
        ("Current e-vapor use (past 30d)", SUBSTANCE_COLORS["e-vapor"]),
        ("Current cigarette use (past 30d)", SUBSTANCE_COLORS["cigarette"]),
    ]:
        sub = by_grade[by_grade["outcome"] == outcome].sort_values("grade")
        fig2.add_trace(go.Scatter(
            x=sub["grade_label"],
            y=sub["pct"],
            error_y=dict(type="data", array=sub["ci_high"] - sub["pct"],
                         arrayminus=sub["pct"] - sub["ci_low"]),
            mode="lines+markers",
            name=outcome.replace(" (past 30d)", ""),
            line=dict(color=color, width=2),
            marker=dict(size=8),
        ))
    fig2 = apply_plotly_theme(fig2, "Current substance use by grade")
    fig2.update_xaxes(title_text="Grade")
    st.plotly_chart(fig2, use_container_width=True)

    st.markdown(
        """
        **Key takeaways (descriptive)**  
        - Alcohol is the most common of the three current-use behaviors (~20%).  
        - E-vapor use is substantially more prevalent than cigarette smoking.  
        - Prevalence rises with grade for all three substances; the steepest absolute increase is for alcohol.  
        """
    )

    st.caption(
        "Data source: CDC 2025 National Youth Risk Behavior Survey (YRBS). "
        "Estimates are survey-weighted with Taylor-linearization variance. "
        "Sample: N = 10,710 student records."
    )


# ---------------------------------------------------------------------------
# Page: Substance Explorer
# ---------------------------------------------------------------------------
def page_substance(results: dict):
    section_header(
        "Substance Explorer",
        "Compare alcohol, e-vapor and cigarette use by grade and age. All estimates are weighted."
    )
    disclaimer_box()

    view = st.radio(
        "Compare by",
        ["Grade", "Age"],
        horizontal=True,
        label_visibility="collapsed",
    )

    if view == "Grade":
        df = pd.DataFrame(results["by_grade"])
        df = df[df["grade_label"].isin(["9th", "10th", "11th", "12th"])]
        x_col, x_label = "grade_label", "Grade"
        order = ["9th", "10th", "11th", "12th"]
    else:
        df = pd.DataFrame(results["by_age"])
        # Keep readable ages
        df = df[df["age_label"].isin(["14", "15", "16", "17", "≥18"])]
        x_col, x_label = "age_label", "Age"
        order = ["14", "15", "16", "17", "≥18"]

    substances = st.multiselect(
        "Substances to display",
        options=[
            "Current alcohol use (past 30d)",
            "Current e-vapor use (past 30d)",
            "Current cigarette use (past 30d)",
        ],
        default=[
            "Current alcohol use (past 30d)",
            "Current e-vapor use (past 30d)",
            "Current cigarette use (past 30d)",
        ],
    )

    if not substances:
        st.warning("Select at least one substance.")
        return

    fig = go.Figure()
    for outcome in substances:
        sub = df[df["outcome"] == outcome].copy()
        sub[x_col] = pd.Categorical(sub[x_col], categories=order, ordered=True)
        sub = sub.sort_values(x_col)
        color = SUBSTANCE_COLORS.get(outcome, TEAL)
        fig.add_trace(go.Scatter(
            x=sub[x_col],
            y=sub["pct"],
            error_y=dict(
                type="data",
                array=sub["ci_high"] - sub["pct"],
                arrayminus=sub["pct"] - sub["ci_low"],
            ),
            mode="lines+markers",
            name=outcome.replace(" (past 30d)", ""),
            line=dict(color=color, width=2),
            marker=dict(size=9),
        ))
    fig = apply_plotly_theme(fig, f"Current substance use by {x_label.lower()}")
    fig.update_xaxes(title_text=x_label)
    st.plotly_chart(fig, use_container_width=True)

    # Table
    st.markdown("#### Detailed estimates")
    show = df[df["outcome"].isin(substances)].copy()
    show["Estimate"] = show.apply(pct_ci, axis=1)
    show["n"] = show["n_unweighted"].astype(int)
    table = show[[x_col, "outcome", "Estimate", "n"]].rename(
        columns={x_col: x_label, "outcome": "Behavior", "n": "Unweighted n"}
    )
    st.dataframe(table, use_container_width=True, hide_index=True)

    st.markdown(
        """
        **How to read this page**  
        - Lines show weighted prevalence; error bars are 95% confidence intervals.  
        - Overlapping confidence intervals suggest differences may not be statistically distinguishable.  
        - Initiation items (ever use, age of first use) are available in the underlying data dictionary but current-use indicators are the primary outcomes shown here.
        """
    )


# ---------------------------------------------------------------------------
# Page: Influence Explorer
# ---------------------------------------------------------------------------
def page_influence(results: dict):
    section_header(
        "Influence Explorer",
        "Associations between contextual factors and current substance use. These are observational associations only."
    )
    disclaimer_box()

    tab1, tab2, tab3, tab4 = st.tabs([
        "Parental monitoring",
        "School connectedness",
        "Mental health",
        "Peer-related proxies",
    ])

    # --- Parental monitoring ---
    with tab1:
        st.markdown(
            "Students reporting that parents **most of the time or always** know where they are going "
            "and with whom, versus lower monitoring. "
            "**Note:** ~39% of the sample did not answer this item; results apply only to respondents."
        )
        df = pd.DataFrame(results["by_parental_monitoring"])
        fig = go.Figure()
        for outcome, color in [
            ("Current alcohol use (past 30d)", SUBSTANCE_COLORS["alcohol"]),
            ("Current e-vapor use (past 30d)", SUBSTANCE_COLORS["e-vapor"]),
            ("Current cigarette use (past 30d)", SUBSTANCE_COLORS["cigarette"]),
        ]:
            sub = df[df["outcome"] == outcome]
            fig.add_trace(go.Bar(
                x=sub["monitoring"],
                y=sub["pct"],
                error_y=dict(
                    type="data",
                    array=sub["ci_high"] - sub["pct"],
                    arrayminus=sub["pct"] - sub["ci_low"],
                ),
                name=outcome.replace(" (past 30d)", ""),
                marker_color=color,
            ))
        fig = apply_plotly_theme(fig, "Current substance use by parental monitoring level")
        fig.update_layout(barmode="group")
        fig.update_xaxes(title_text="Parents know location / companions")
        st.plotly_chart(fig, use_container_width=True)

        st.markdown(
            """
            **Pattern observed:** Students reporting lower parental monitoring have higher weighted prevalence 
            of alcohol, e-vapor, and cigarette use. Because of substantial missing data on this item, 
            these estimates cannot be generalized to the full national sample without further assumptions.
            """
        )

    # --- School connectedness ---
    with tab2:
        st.markdown(
            'Students who **agree or strongly agree** that they “feel close to people at their school” '
            "versus those who do not."
        )
        df = pd.DataFrame(results["by_school_connectedness"])
        fig = go.Figure()
        for outcome, color in [
            ("Current alcohol use (past 30d)", SUBSTANCE_COLORS["alcohol"]),
            ("Current e-vapor use (past 30d)", SUBSTANCE_COLORS["e-vapor"]),
            ("Current cigarette use (past 30d)", SUBSTANCE_COLORS["cigarette"]),
        ]:
            sub = df[df["outcome"] == outcome]
            fig.add_trace(go.Bar(
                x=sub["connectedness"],
                y=sub["pct"],
                error_y=dict(
                    type="data",
                    array=sub["ci_high"] - sub["pct"],
                    arrayminus=sub["pct"] - sub["ci_low"],
                ),
                name=outcome.replace(" (past 30d)", ""),
                marker_color=color,
            ))
        fig = apply_plotly_theme(fig, "Current substance use by school connectedness")
        fig.update_layout(barmode="group")
        fig.update_xaxes(title_text="Feel close to people at school")
        st.plotly_chart(fig, use_container_width=True)

        st.markdown(
            """
            **Pattern observed:** Differences are modest. E-vapor and cigarette use are slightly higher among 
            students reporting lower connectedness; confidence intervals often overlap, especially for alcohol. 
            The association is weaker than the parental-monitoring contrast.
            """
        )

    # --- Mental health ---
    with tab3:
        st.markdown(
            "Associations between selected mental-health indicators and current substance use. "
            "Cross-sectional data — directionality cannot be determined."
        )
        df = pd.DataFrame(results["by_mental_health"])
        indicators = sorted(df["mh_indicator"].unique())
        chosen = st.selectbox("Mental-health indicator", indicators, index=0)
        sub = df[df["mh_indicator"] == chosen]

        fig = go.Figure()
        for outcome, color in [
            ("Current alcohol use (past 30d)", SUBSTANCE_COLORS["alcohol"]),
            ("Current e-vapor use (past 30d)", SUBSTANCE_COLORS["e-vapor"]),
            ("Current cigarette use (past 30d)", SUBSTANCE_COLORS["cigarette"]),
        ]:
            s = sub[sub["outcome"] == outcome]
            fig.add_trace(go.Bar(
                x=s["mh_level"],
                y=s["pct"],
                error_y=dict(
                    type="data",
                    array=s["ci_high"] - s["pct"],
                    arrayminus=s["pct"] - s["ci_low"],
                ),
                name=outcome.replace(" (past 30d)", ""),
                marker_color=color,
            ))
        fig = apply_plotly_theme(fig, f"Current substance use by: {chosen}")
        fig.update_layout(barmode="group")
        fig.update_xaxes(title_text=chosen)
        st.plotly_chart(fig, use_container_width=True)

        st.markdown(
            """
            **Pattern observed:** Across multiple mental-health indicators (sad/hopeless feelings, 
            suicidal ideation, poor current mental health), students reporting distress show higher 
            weighted prevalence of current alcohol, e-vapor, and cigarette use. These are associations 
            only; confounding and reverse causation are possible.
            """
        )

    # --- Peer proxies ---
    with tab4:
        st.markdown(
            """
            The 2025 YRBS **does not contain a direct measure of peer substance use or peer influence**.  
            The items below are **proxies** for peer-related context (bullying) and online activity intensity.  
            They should **not** be interpreted as measures of peer norms around substance use.
            """
        )
        df = pd.DataFrame(results["by_peer_proxies"])
        indicators = sorted(df["peer_indicator"].unique())
        chosen = st.selectbox("Peer-related indicator", indicators, index=0, key="peer_sel")
        sub = df[df["peer_indicator"] == chosen]

        fig = go.Figure()
        for outcome, color in [
            ("Current alcohol use (past 30d)", SUBSTANCE_COLORS["alcohol"]),
            ("Current e-vapor use (past 30d)", SUBSTANCE_COLORS["e-vapor"]),
            ("Current cigarette use (past 30d)", SUBSTANCE_COLORS["cigarette"]),
        ]:
            s = sub[sub["outcome"] == outcome]
            fig.add_trace(go.Bar(
                x=s["peer_level"],
                y=s["pct"],
                error_y=dict(
                    type="data",
                    array=s["ci_high"] - s["pct"],
                    arrayminus=s["pct"] - s["ci_low"],
                ),
                name=outcome.replace(" (past 30d)", ""),
                marker_color=color,
            ))
        fig = apply_plotly_theme(fig, f"Current substance use by: {chosen}")
        fig.update_layout(barmode="group")
        fig.update_xaxes(title_text=chosen)
        st.plotly_chart(fig, use_container_width=True)

        st.markdown(
            """
            **Pattern observed:** Students who experienced bullying (school or electronic) or who report 
            high social-media use show higher weighted prevalence of current substance use. These remain 
            contextual proxies, not measures of peer influence.
            """
        )


# ---------------------------------------------------------------------------
# Page: Prevention Intelligence (rule-based)
# ---------------------------------------------------------------------------
def page_prevention(results: dict):
    section_header(
        "Prevention Intelligence",
        "Evidence-informed prevention suggestions linked to patterns observed in the 2025 YRBS. "
        "Rule-based — no AI generation. Not a substitute for local needs assessment or professional guidance."
    )
    disclaimer_box()

    st.markdown(
        """
        Recommendations below are **general, evidence-informed suggestions** that map observed 
        associations to commonly used prevention approaches. They do not claim that implementing 
        any single action will reduce substance use. Local context, culture, and capacity matter.
        """
    )

    recommendations = [
        {
            "title": "Strengthen family engagement and parental monitoring supports",
            "finding": "Students reporting lower parental monitoring had substantially higher prevalence of current alcohol (~34% vs ~20%), e-vapor (~30% vs ~15%), and cigarette use (~8% vs ~3%).",
            "actions": [
                "Offer family workshops that teach practical monitoring strategies (knowing location, companions, and activities) without framing parents as “the problem.”",
                "Provide simple tools (shared calendars, check-in routines, conversation prompts) that work for diverse family structures.",
                "Partner with parent organizations and community groups already trusted by families.",
            ],
            "caveat": "About 39% of students did not answer the monitoring item; findings apply to respondents only.",
        },
        {
            "title": "Integrate mental-health promotion with substance-use prevention",
            "finding": "Students who felt sad/hopeless for ≥2 weeks, who considered suicide, or who reported poor current mental health had markedly higher current substance-use prevalence across all three substances.",
            "actions": [
                "Ensure school-based mental-health supports (counseling access, screening pathways, crisis protocols) are visible and low-barrier.",
                "Train staff to recognize that substance use and mental-health distress often co-occur; avoid punitive-only responses.",
                "Coordinate prevention messaging so it does not stigmatize students who are struggling.",
            ],
            "caveat": "Associations are cross-sectional; directionality is unknown. Mental-health care is not a substitute for substance-use prevention, and vice versa.",
        },
        {
            "title": "Build school connectedness intentionally",
            "finding": "Feeling close to people at school showed modest associations with substance use (weaker than parental monitoring or mental-health indicators).",
            "actions": [
                "Support advisory programs, mentoring, and extracurricular access that help students feel known and valued.",
                "Reduce barriers to participation (cost, transportation, eligibility rules) so connectedness opportunities are equitable.",
                "Track connectedness climate (climate surveys) alongside academic metrics.",
            ],
            "caveat": "Connectedness differences were smaller and less consistent than other factors examined.",
        },
        {
            "title": "Address bullying and electronic harassment as part of a broader climate strategy",
            "finding": "Students who experienced bullying at school or electronic bullying had higher prevalence of current alcohol, e-vapor, and cigarette use.",
            "actions": [
                "Maintain clear anti-bullying policies with consistent follow-through and support for targets of bullying.",
                "Include digital citizenship and online safety in health education.",
                "Create safe reporting channels that students actually trust.",
            ],
            "caveat": "Bullying items are peer-context proxies, not measures of peer substance-use norms.",
        },
        {
            "title": "Tailor messaging by grade and developmental stage",
            "finding": "Current alcohol use rose sharply from 9th grade (~11%) to 12th grade (~31%); e-vapor and cigarette use also increased with grade and age.",
            "actions": [
                "Deliver prevention content earlier (middle school into 9th grade) before prevalence rises steeply.",
                "Adapt messaging for older students who may already be experimenting (skills for refusal, harm reduction where appropriate, and help-seeking).",
                "Avoid one-size-fits-all assemblies; use grade-banded approaches.",
            ],
            "caveat": "Age/grade gradients describe population patterns, not individual trajectories.",
        },
        {
            "title": "Use peer education carefully and with adult support",
            "finding": "No direct peer-influence or peer-substance-use items exist in the 2025 YRBS. High social-media use (a rough online-context proxy) was associated with higher substance-use prevalence.",
            "actions": [
                "If using peer educators, train them thoroughly and pair them with adult facilitators.",
                "Focus peer roles on norms that support healthy choices and help-seeking, not on personal disclosure of use.",
                "Evaluate peer programs; enthusiasm alone is not evidence of effectiveness.",
            ],
            "caveat": "Absence of direct peer-use measures means peer-influence pathways cannot be quantified from this dataset.",
        },
    ]

    for i, rec in enumerate(recommendations, 1):
        with st.expander(f"{i}. {rec['title']}", expanded=(i == 1)):
            st.markdown(f"**Supporting finding from this analysis**  \n{rec['finding']}")
            st.markdown("**Suggested actions**")
            for a in rec["actions"]:
                st.markdown(f"- {a}")
            st.caption(f"Caveat: {rec['caveat']}")

    st.markdown("---")
    st.markdown(
        """
        ### How these recommendations were generated
        - Rule-based mapping from observed associations → commonly recommended prevention approaches in the public-health literature.  
        - No generative AI and no paid API.  
        - Recommendations are transparent and fully inspectable in the source code.  
        - Always combine national patterns with local data, community voice, and professional judgment.
        """
    )


# ---------------------------------------------------------------------------
# Page: Data & Methodology
# ---------------------------------------------------------------------------
def page_methodology():
    section_header(
        "Data & Methodology",
        "Transparency about the CDC dataset, weighting, variable definitions, and limitations."
    )

    st.markdown(
        """
        ### Dataset
        - **Source:** Centers for Disease Control and Prevention (CDC), National Youth Risk Behavior Survey (YRBS), 2025.  
        - **Sample:** 10,710 student records after cleaning (national high-school sample).  
        - **Design:** Stratified, two-stage cluster sample. Schools are primary sampling units; students are sampled within schools.  
        - **Overall response rate (CDC-reported):** 30.6%. Weights adjust for school and student non-response and for oversampling of Black and Hispanic students.

        ### Survey weights and variance
        All prevalence estimates use the CDC-provided survey weight (`weight`) and design variables (`stratum`, `psu`).  
        Variance estimation uses Taylor linearization. Confidence intervals are 95% (t-based).  
        Unweighted percentages would misrepresent national figures and are not shown as primary results.

        ### Outcome definitions (current use)
        | Indicator | YRBS item | Definition used |
        |-----------|-----------|-----------------|
        | Current alcohol use | QN41 | ≥1 drink of alcohol on ≥1 day in past 30 days |
        | Current e-vapor use | QN36 | Used an electronic vapor product on ≥1 day in past 30 days |
        | Current cigarette use | QN33 | Smoked cigarettes on ≥1 day in past 30 days |

        Yes/No flags follow CDC coding (1 = Yes, 2 = No). Blank means no usable answer (never means “No”).

        ### Contextual variables examined
        - **Parental monitoring (Q104 / QN104):** How often parents/adults know where the student is going and with whom.  
        - **School connectedness (Q102 / QN102):** Agree/disagree that student feels close to people at school.  
        - **Mental health:** Sad/hopeless ≥2 weeks (Q26), considered suicide (Q27), made a plan (Q28), attempted (Q29), self-harm (Q25), current mental health not good (Q81), counseling experience (Q98).  
        - **Peer-related proxies:** Bullied at school (Q23), electronically bullied (Q24), social-media frequency (Q77).  
          *There is no direct item on friends’ substance use.*

        ### Missing data
        - Blank answers are treated as missing; they are never coded as “No.”  
        - Parental monitoring has high missingness (~39%). Estimates for that domain describe respondents only.  
        - Some substance-use follow-up items are legitimately blank when the student reported no current use (skip patterns). Status flags document this.

        ### What this tool does *not* do
        - Does not establish causal relationships.  
        - Does not predict any individual student’s future behavior.  
        - Does not label individual students as “high risk.”  
        - Does not replace local surveillance, needs assessment, or clinical judgment.

        ### Citations & further reading
        - CDC Youth Risk Behavior Surveillance System: https://www.cdc.gov/yrbs  
        - 2025 YRBS data and documentation are released by CDC; consult the official data user’s guide for questionnaire text, codebooks, and analytic recommendations.  
        - Methodology follows standard complex-survey practice (e.g., CDC guidance and survey-sampling references such as Korn & Graubard).

        ### Project files
        - Cleaned analytic file: `data/yrbs2025_cleaned.csv`  
        - Data dictionary: `data/yrbs2025_data_dictionary.xlsx`  
        - Precomputed estimates: `analysis/*.csv` and `analysis/analysis_results.json`  
        - Charts: `analysis/charts/`
        """
    )

    with st.expander("Preview a few rows of the cleaned dataset"):
        sample = load_cleaned_sample(8)
        st.dataframe(sample, use_container_width=True)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    st.set_page_config(
        page_title="Youth Influence Intelligence",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # Sidebar branding & nav
    st.sidebar.markdown(
        f"""
        <div style="padding:0.5rem 0 1rem 0;">
            <div style="font-size:1.35rem; font-weight:700; color:{NAVY};">Youth Influence</div>
            <div style="font-size:1.1rem; font-weight:600; color:{TEAL};">Intelligence</div>
            <div style="font-size:0.75rem; color:{MUTED}; margin-top:0.35rem;">2025 National YRBS · Associations only</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    page = st.sidebar.radio(
        "Navigate",
        [
            "Executive Dashboard",
            "Substance Explorer",
            "Influence Explorer",
            "Prevention Intelligence",
            "Data & Methodology",
        ],
        label_visibility="collapsed",
    )

    st.sidebar.markdown("---")
    st.sidebar.caption(
        "Built for schools, parents, and youth organizations. "
        "Data: CDC 2025 National YRBS. No individual prediction."
    )

    results = load_json_results()

    if page == "Executive Dashboard":
        page_executive(results)
    elif page == "Substance Explorer":
        page_substance(results)
    elif page == "Influence Explorer":
        page_influence(results)
    elif page == "Prevention Intelligence":
        page_prevention(results)
    else:
        page_methodology()


if __name__ == "__main__":
    main()

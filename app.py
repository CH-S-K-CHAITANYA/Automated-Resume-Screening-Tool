"""
app.py
======
Premium SaaS-style Streamlit Dashboard for the Automated Resume Screening Tool.
Run with:  streamlit run app.py
"""

import os
import io
import tempfile
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

from src.extractor import extract_text
from src.cleaner import clean_text
from src.scorer import (
    compute_tfidf_scores,
    compute_skill_scores,
    compute_final_scores,
    rank_candidates,
    get_summary,
)
from src.reporter import generate_csv_report, generate_json_report

# ─────────────────────────────────────────────
# PAGE CONFIG — must be first Streamlit call
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="RecruitIQ · Resume Screener",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# CUSTOM CSS — Premium SaaS Dark Theme
# ─────────────────────────────────────────────
st.markdown("""
<style>
/* ── Google Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;1,9..40,300&display=swap');

/* ── Root Variables ── */
:root {
    --bg-primary: #0a0a0f;
    --bg-secondary: #111118;
    --bg-card: #16161f;
    --bg-card-hover: #1c1c28;
    --accent-cyan: #00d4ff;
    --accent-violet: #7b5ea7;
    --accent-green: #00e5a0;
    --accent-amber: #ffb84d;
    --accent-red: #ff5c5c;
    --text-primary: #f0f0f8;
    --text-secondary: #8888aa;
    --text-muted: #555570;
    --border: #222232;
    --border-accent: rgba(0, 212, 255, 0.2);
    --glow-cyan: 0 0 30px rgba(0, 212, 255, 0.15);
    --glow-violet: 0 0 30px rgba(123, 94, 167, 0.2);
}

/* ── Base ── */
html, body, .stApp {
    background-color: var(--bg-primary) !important;
    font-family: 'DM Sans', sans-serif;
    color: var(--text-primary);
}

/* ── Hide Streamlit Branding ── */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: var(--bg-secondary) !important;
    border-right: 1px solid var(--border) !important;
}
section[data-testid="stSidebar"] .block-container {
    padding: 2rem 1.2rem;
}

/* ── Main Container ── */
.main .block-container {
    padding: 2rem 2.5rem;
    max-width: 1400px;
}

/* ── Headings ── */
h1, h2, h3, h4 {
    font-family: 'Syne', sans-serif !important;
    color: var(--text-primary) !important;
    letter-spacing: -0.02em;
}

/* ── Metric Cards ── */
.metric-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1.5rem;
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
}
.metric-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, var(--accent-cyan), var(--accent-violet));
}
.metric-card:hover {
    background: var(--bg-card-hover);
    border-color: var(--border-accent);
    box-shadow: var(--glow-cyan);
    transform: translateY(-2px);
}
.metric-label {
    font-size: 0.75rem;
    font-weight: 500;
    color: var(--text-secondary);
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
}
.metric-value {
    font-family: 'Syne', sans-serif;
    font-size: 2.2rem;
    font-weight: 800;
    color: var(--text-primary);
    line-height: 1;
}
.metric-sub {
    font-size: 0.75rem;
    color: var(--text-muted);
    margin-top: 0.4rem;
}
.metric-value.cyan { color: var(--accent-cyan); }
.metric-value.green { color: var(--accent-green); }
.metric-value.amber { color: var(--accent-amber); }
.metric-value.red { color: var(--accent-red); }

/* ── Status Badges ── */
.badge {
    display: inline-block;
    padding: 0.2rem 0.8rem;
    border-radius: 100px;
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.05em;
}
.badge-green {
    background: rgba(0, 229, 160, 0.12);
    color: var(--accent-green);
    border: 1px solid rgba(0, 229, 160, 0.3);
}
.badge-red {
    background: rgba(255, 92, 92, 0.12);
    color: var(--accent-red);
    border: 1px solid rgba(255, 92, 92, 0.3);
}

/* ── Section Headers ── */
.section-header {
    font-family: 'Syne', sans-serif;
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: var(--text-muted);
    margin-bottom: 1rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid var(--border);
}

/* ── Candidate Row Card ── */
.candidate-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    margin-bottom: 0.75rem;
    display: flex;
    align-items: center;
    gap: 1rem;
    transition: all 0.2s ease;
}
.candidate-card:hover {
    border-color: var(--border-accent);
    box-shadow: var(--glow-cyan);
}
.rank-badge {
    font-family: 'Syne', sans-serif;
    font-size: 1.4rem;
    font-weight: 800;
    color: var(--text-muted);
    min-width: 2.5rem;
}
.rank-badge.top { color: var(--accent-amber); }

/* ── Progress Bar ── */
.score-bar-wrap {
    flex: 1;
}
.score-bar-bg {
    background: var(--border);
    border-radius: 100px;
    height: 6px;
    overflow: hidden;
}
.score-bar-fill {
    height: 100%;
    border-radius: 100px;
    background: linear-gradient(90deg, var(--accent-cyan), var(--accent-violet));
}

/* ── Streamlit native overrides ── */
.stButton > button {
    background: linear-gradient(135deg, var(--accent-cyan), var(--accent-violet)) !important;
    color: #0a0a0f !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.85rem !important;
    letter-spacing: 0.05em !important;
    padding: 0.6rem 1.8rem !important;
    transition: all 0.3s !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 24px rgba(0, 212, 255, 0.3) !important;
}

.stFileUploader {
    background: var(--bg-card) !important;
    border: 1px dashed var(--border-accent) !important;
    border-radius: 14px !important;
    padding: 1rem !important;
}
.stFileUploader label { color: var(--text-secondary) !important; }

.stTextArea textarea {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    color: var(--text-primary) !important;
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.85rem !important;
}
.stTextArea textarea:focus {
    border-color: var(--accent-cyan) !important;
    box-shadow: var(--glow-cyan) !important;
}

.stSlider [data-testid="stSlider"] {
    accent-color: var(--accent-cyan);
}
.stSlider label { color: var(--text-secondary) !important; font-size: 0.8rem !important; }

.stDataFrame {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
}
.stDataFrame [data-testid="dataframe"] {
    background: transparent !important;
}

.stSelectbox [data-testid="stSelectbox"] > div {
    background: var(--bg-card) !important;
    border-color: var(--border) !important;
    color: var(--text-primary) !important;
}

div[data-testid="stTabContent"] {
    background: transparent !important;
}

.stAlert { border-radius: 10px !important; }

/* ── Logo / Brand ── */
.brand-logo {
    font-family: 'Syne', sans-serif;
    font-size: 1.4rem;
    font-weight: 800;
    background: linear-gradient(135deg, var(--accent-cyan), var(--accent-violet));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: -0.03em;
    margin-bottom: 0.2rem;
}
.brand-tagline {
    font-size: 0.7rem;
    color: var(--text-muted);
    letter-spacing: 0.1em;
    text-transform: uppercase;
}

/* ── Hero Header ── */
.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: 2.6rem;
    font-weight: 800;
    letter-spacing: -0.04em;
    line-height: 1.1;
    background: linear-gradient(135deg, #f0f0f8 40%, var(--accent-cyan));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.5rem;
}
.hero-subtitle {
    font-size: 1rem;
    color: var(--text-secondary);
    font-weight: 300;
    margin-bottom: 2.5rem;
}

/* ── Skill chip ── */
.skill-chip {
    display: inline-block;
    background: rgba(0, 212, 255, 0.08);
    border: 1px solid rgba(0, 212, 255, 0.2);
    color: var(--accent-cyan);
    font-size: 0.7rem;
    font-weight: 500;
    padding: 0.15rem 0.6rem;
    border-radius: 100px;
    margin: 0.15rem;
}
.skill-chip.missing {
    background: rgba(255, 92, 92, 0.08);
    border-color: rgba(255, 92, 92, 0.2);
    color: var(--accent-red);
}

/* ── Tab styling ── */
.stTabs [data-testid="stTab"] {
    background: transparent !important;
    color: var(--text-secondary) !important;
    border: none !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.8rem !important;
    letter-spacing: 0.05em !important;
}
.stTabs [aria-selected="true"] {
    color: var(--accent-cyan) !important;
    border-bottom: 2px solid var(--accent-cyan) !important;
}

/* ── Divider ── */
.styled-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--border), transparent);
    margin: 2rem 0;
}

/* ── Info box ── */
.info-box {
    background: rgba(0, 212, 255, 0.05);
    border: 1px solid rgba(0, 212, 255, 0.15);
    border-radius: 12px;
    padding: 1rem 1.25rem;
    font-size: 0.85rem;
    color: var(--text-secondary);
}

/* Scrollbar */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--bg-primary); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--accent-violet); }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# DEFAULT JOB DESCRIPTION
# ─────────────────────────────────────────────
DEFAULT_JD = """We are looking for a skilled Data Scientist / ML Engineer to join our AI team.

Responsibilities:
- Build and deploy machine learning and deep learning models
- Perform data analysis, feature engineering, and statistical modeling
- Write clean Python code and maintain pipelines using Pandas, NumPy, Scikit-learn
- Work with NLP tasks using TensorFlow, PyTorch, or HuggingFace
- Collaborate with cross-functional teams and communicate findings
- Manage code using Git, deploy models with Docker and REST APIs
- Work with SQL databases and cloud platforms (AWS preferred)
- Build data visualizations and dashboards

Requirements:
- 2+ years of Python programming experience
- Strong knowledge of machine learning, deep learning, and NLP
- Experience with TensorFlow or PyTorch
- Proficiency in Pandas, NumPy, Scikit-learn
- SQL and database experience
- Familiarity with Flask or FastAPI for API development
- Version control with Git
- Problem solving and communication skills
"""

DEFAULT_SKILLS = [
    "python", "machine learning", "deep learning", "tensorflow", "pytorch",
    "scikit-learn", "pandas", "numpy", "sql", "data analysis",
    "natural language processing", "nlp", "data visualization",
    "statistics", "git", "docker", "rest api", "flask", "fastapi",
    "aws", "feature engineering", "neural networks", "regression",
    "classification", "problem solving", "communication",
]


# ─────────────────────────────────────────────
# SESSION STATE INITIALIZATION
# ─────────────────────────────────────────────
for key in ["results_df", "summary", "ranked", "has_run"]:
    if key not in st.session_state:
        st.session_state[key] = None
if "has_run" not in st.session_state:
    st.session_state.has_run = False


# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="brand-logo">RecruitIQ</div>', unsafe_allow_html=True)
    st.markdown('<div class="brand-tagline">AI Resume Intelligence</div>', unsafe_allow_html=True)
    st.markdown('<div class="styled-divider"></div>', unsafe_allow_html=True)

    st.markdown('<div class="section-header">Upload Resumes</div>', unsafe_allow_html=True)
    uploaded_files = st.file_uploader(
        "Drop PDF, DOCX, or TXT files",
        type=["pdf", "docx", "txt"],
        accept_multiple_files=True,
        label_visibility="collapsed",
    )
    if uploaded_files:
        for f in uploaded_files:
            st.markdown(f'<span class="skill-chip">📄 {f.name}</span>', unsafe_allow_html=True)

    st.markdown('<div class="styled-divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-header">Scoring Weights</div>', unsafe_allow_html=True)

    tfidf_w = st.slider("TF-IDF Similarity Weight", 0.0, 1.0, 0.5, 0.05)
    skill_w = round(1.0 - tfidf_w, 2)
    st.markdown(f'<div class="info-box">Skill Match Weight auto-set to <b style="color:#00d4ff">{skill_w}</b></div>', unsafe_allow_html=True)

    threshold = st.slider("Shortlist Threshold", 0.10, 0.90, 0.40, 0.05,
                          help="Minimum final score to be shortlisted")

    st.markdown('<div class="styled-divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-header">Navigation</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="font-size:0.8rem; color: var(--text-secondary); line-height:2">
    🏠 Dashboard<br>
    📊 Analytics<br>
    📋 Candidates<br>
    📥 Export
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# MAIN CONTENT
# ─────────────────────────────────────────────
st.markdown('<div class="hero-title">Resume Intelligence<br>Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-subtitle">AI-powered screening · TF-IDF + Skill Matching · Real-time ranking</div>', unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["⚡  SCREEN", "📊  ANALYTICS", "🏆  CANDIDATES", "📥  EXPORT"])


# ──────────────────────────────
# TAB 1 — Screen
# ──────────────────────────────
with tab1:
    col_jd, col_skills = st.columns([3, 2], gap="large")

    with col_jd:
        st.markdown('<div class="section-header">Job Description</div>', unsafe_allow_html=True)
        job_description = st.text_area(
            "job_description",
            value=DEFAULT_JD,
            height=350,
            label_visibility="collapsed",
            placeholder="Paste your job description here...",
        )

    with col_skills:
        st.markdown('<div class="section-header">Required Skills</div>', unsafe_allow_html=True)
        skills_raw = st.text_area(
            "required_skills",
            value="\n".join(DEFAULT_SKILLS),
            height=350,
            label_visibility="collapsed",
            placeholder="One skill per line...",
        )
        skills_list = [s.strip().lower() for s in skills_raw.strip().split("\n") if s.strip()]

    # Run button
    st.markdown("<br>", unsafe_allow_html=True)
    btn_col, info_col = st.columns([2, 5])
    with btn_col:
        run_btn = st.button("🚀  Run Screening", use_container_width=True)

    with info_col:
        if not uploaded_files:
            st.markdown('<div class="info-box">⬅️ Upload resume files in the sidebar to begin screening.</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="info-box">✅ <b>{len(uploaded_files)} resume(s)</b> ready · <b>{len(skills_list)} skills</b> configured · Threshold: <b style="color:#00d4ff">{int(threshold*100)}%</b></div>', unsafe_allow_html=True)

    # ── RUN PIPELINE ──
    if run_btn:
        if not uploaded_files:
            st.error("Please upload at least one resume file from the sidebar.")
        elif not job_description.strip():
            st.error("Please enter a job description.")
        else:
            with st.spinner("🧠 Analyzing resumes..."):
                # Save uploads to temp dir
                resume_texts = {}
                for uf in uploaded_files:
                    suffix = os.path.splitext(uf.name)[1]
                    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                        tmp.write(uf.read())
                        tmp_path = tmp.name
                    text = extract_text(tmp_path)
                    if text:
                        resume_texts[uf.name] = text
                    os.unlink(tmp_path)

                if not resume_texts:
                    st.error("Could not extract text from uploaded files. Check file formats.")
                else:
                    # Clean
                    cleaned_jd = clean_text(job_description, remove_stops=True)
                    cleaned_resumes = {f: clean_text(t, remove_stops=True) for f, t in resume_texts.items()}

                    # Score
                    tfidf_scores = compute_tfidf_scores(cleaned_jd, cleaned_resumes)
                    skill_scores = compute_skill_scores(skills_list, cleaned_resumes)
                    final_scores = compute_final_scores(tfidf_scores, skill_scores, tfidf_w, skill_w)
                    ranked = rank_candidates(final_scores, threshold=threshold)
                    summary = get_summary(ranked, threshold=threshold)

                    # Build DataFrame
                    df = pd.DataFrame(ranked)
                    df["final_pct"] = (df["final_score"] * 100).round(1)
                    df["tfidf_pct"] = (df["tfidf_score"] * 100).round(1)
                    df["skill_pct"] = (df["skill_score"] * 100).round(1)

                    st.session_state.results_df = df
                    st.session_state.summary = summary
                    st.session_state.ranked = ranked
                    st.session_state.has_run = True

            st.success(f"✅ Screening complete! {summary['shortlisted_count']} shortlisted, {summary['rejected_count']} rejected.")


# ──────────────────────────────
# TAB 2 — Analytics
# ──────────────────────────────
with tab2:
    if not st.session_state.has_run:
        st.markdown('<div class="info-box" style="text-align:center; padding:3rem;">Run a screening first to see analytics.</div>', unsafe_allow_html=True)
    else:
        df = st.session_state.results_df
        summary = st.session_state.summary

        # Metric cards
        m1, m2, m3, m4 = st.columns(4)

        with m1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Total Screened</div>
                <div class="metric-value cyan">{summary['total_resumes']}</div>
                <div class="metric-sub">Resumes analyzed</div>
            </div>""", unsafe_allow_html=True)

        with m2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Shortlisted</div>
                <div class="metric-value green">{summary['shortlisted_count']}</div>
                <div class="metric-sub">Above {int(threshold*100)}% threshold</div>
            </div>""", unsafe_allow_html=True)

        with m3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Rejected</div>
                <div class="metric-value red">{summary['rejected_count']}</div>
                <div class="metric-sub">Below threshold</div>
            </div>""", unsafe_allow_html=True)

        with m4:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Top Score</div>
                <div class="metric-value amber">{summary['top_score']*100:.0f}%</div>
                <div class="metric-sub">{summary['top_candidate'][:20]}</div>
            </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Charts
        chart_col1, chart_col2 = st.columns([3, 2], gap="large")

        with chart_col1:
            st.markdown('<div class="section-header">Score Distribution</div>', unsafe_allow_html=True)
            fig_bar = go.Figure()
            colors = ["#00e5a0" if "SHORTLISTED" in s else "#ff5c5c" for s in df["status"]]
            fig_bar.add_trace(go.Bar(
                x=df["resume"],
                y=df["final_pct"],
                marker_color=colors,
                marker_line_width=0,
                hovertemplate="<b>%{x}</b><br>Score: %{y:.1f}%<extra></extra>",
            ))
            fig_bar.add_hline(
                y=threshold * 100,
                line_dash="dash",
                line_color="#00d4ff",
                line_width=1,
                annotation_text=f"Threshold ({int(threshold*100)}%)",
                annotation_font_color="#00d4ff",
                annotation_font_size=11,
            )
            fig_bar.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font_color="#8888aa",
                font_family="DM Sans",
                xaxis=dict(tickfont_size=10, gridcolor="#222232", tickangle=-20),
                yaxis=dict(ticksuffix="%", gridcolor="#222232", range=[0, 105]),
                margin=dict(l=10, r=10, t=10, b=10),
                showlegend=False,
                height=300,
            )
            st.plotly_chart(fig_bar, use_container_width=True)

        with chart_col2:
            st.markdown('<div class="section-header">Pass / Fail Ratio</div>', unsafe_allow_html=True)
            fig_pie = go.Figure(go.Pie(
                labels=["Shortlisted", "Rejected"],
                values=[summary["shortlisted_count"], summary["rejected_count"]],
                hole=0.65,
                marker_colors=["#00e5a0", "#ff5c5c"],
                textinfo="none",
                hovertemplate="<b>%{label}</b>: %{value}<extra></extra>",
            ))
            fig_pie.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                font_color="#8888aa",
                font_family="DM Sans",
                showlegend=True,
                legend=dict(font_color="#8888aa", bgcolor="rgba(0,0,0,0)"),
                margin=dict(l=0, r=0, t=10, b=0),
                height=300,
                annotations=[dict(
                    text=f"<b>{int(summary['shortlisted_count']/summary['total_resumes']*100)}%</b>",
                    x=0.5, y=0.5,
                    font_size=24,
                    font_family="Syne",
                    font_color="#f0f0f8",
                    showarrow=False,
                )],
            )
            st.plotly_chart(fig_pie, use_container_width=True)

        # Score comparison radar
        st.markdown('<div class="section-header">TF-IDF vs Skill Match Comparison</div>', unsafe_allow_html=True)
        fig_scatter = go.Figure()
        for _, row in df.iterrows():
            color = "#00e5a0" if "SHORTLISTED" in row["status"] else "#ff5c5c"
            fig_scatter.add_trace(go.Scatter(
                x=[row["tfidf_pct"]],
                y=[row["skill_pct"]],
                mode="markers+text",
                marker=dict(size=14, color=color, line=dict(color="#0a0a0f", width=2)),
                text=[row["resume"][:15] + "…" if len(row["resume"]) > 15 else row["resume"]],
                textposition="top center",
                textfont=dict(size=9, color="#8888aa"),
                hovertemplate=f"<b>{row['resume']}</b><br>TF-IDF: {row['tfidf_pct']:.1f}%<br>Skill: {row['skill_pct']:.1f}%<extra></extra>",
                name=row["resume"],
                showlegend=False,
            ))
        fig_scatter.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="#8888aa",
            font_family="DM Sans",
            xaxis=dict(title="TF-IDF Score (%)", gridcolor="#222232", ticksuffix="%"),
            yaxis=dict(title="Skill Match (%)", gridcolor="#222232", ticksuffix="%"),
            margin=dict(l=10, r=10, t=20, b=10),
            height=340,
        )
        st.plotly_chart(fig_scatter, use_container_width=True)


# ──────────────────────────────
# TAB 3 — Candidates
# ──────────────────────────────
with tab3:
    if not st.session_state.has_run:
        st.markdown('<div class="info-box" style="text-align:center; padding:3rem;">Run a screening first to see candidates.</div>', unsafe_allow_html=True)
    else:
        df = st.session_state.results_df
        ranked = st.session_state.ranked

        filter_col, search_col = st.columns([2, 3])
        with filter_col:
            filter_opt = st.selectbox("Filter", ["All", "Shortlisted Only", "Rejected Only"], label_visibility="collapsed")
        with search_col:
            search_q = st.text_input("Search by filename", placeholder="🔍  Search resumes...", label_visibility="collapsed")

        filtered = ranked
        if filter_opt == "Shortlisted Only":
            filtered = [r for r in ranked if "SHORTLISTED" in r["status"]]
        elif filter_opt == "Rejected Only":
            filtered = [r for r in ranked if "REJECTED" in r["status"]]
        if search_q:
            filtered = [r for r in filtered if search_q.lower() in r["resume"].lower()]

        st.markdown(f'<div class="section-header">{len(filtered)} Candidates</div>', unsafe_allow_html=True)

        for c in filtered:
            is_shortlisted = "SHORTLISTED" in c["status"]
            badge_class = "badge-green" if is_shortlisted else "badge-red"
            badge_text = "SHORTLISTED" if is_shortlisted else "REJECTED"
            rank_class = "top" if c["rank"] <= 3 else ""
            score_pct = c["final_score"] * 100

            with st.expander(f"#{c['rank']}  {c['resume']}  —  {score_pct:.1f}%", expanded=(c["rank"] == 1)):
                d1, d2, d3, d4 = st.columns(4)
                d1.metric("Final Score", f"{score_pct:.1f}%")
                d2.metric("TF-IDF Match", f"{c['tfidf_score']*100:.1f}%")
                d3.metric("Skill Match", f"{c['skill_score']*100:.1f}%")
                d4.metric("Skills Found", c["skills_matched"])

                st.markdown("**Matched Skills:**")
                if c["matched_skills"] and c["matched_skills"] != "None":
                    chips = "".join([f'<span class="skill-chip">{s}</span>' for s in c["matched_skills"].split(", ")])
                    st.markdown(chips, unsafe_allow_html=True)
                else:
                    st.markdown("_No skills matched_")

                st.markdown("**Missing Skills:**")
                if c["missing_skills"] and c["missing_skills"] != "None":
                    chips = "".join([f'<span class="skill-chip missing">{s}</span>' for s in c["missing_skills"].split(", ")])
                    st.markdown(chips, unsafe_allow_html=True)
                else:
                    st.markdown("_All skills present!_ 🎉")

                # Score bar
                st.markdown(f"""
                <div class="score-bar-wrap" style="margin-top:1rem;">
                    <div style="font-size:0.7rem; color:var(--text-muted); margin-bottom:4px">MATCH SCORE</div>
                    <div class="score-bar-bg">
                        <div class="score-bar-fill" style="width:{min(score_pct, 100)}%"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)


# ──────────────────────────────
# TAB 4 — Export
# ──────────────────────────────
with tab4:
    if not st.session_state.has_run:
        st.markdown('<div class="info-box" style="text-align:center; padding:3rem;">Run a screening first to export results.</div>', unsafe_allow_html=True)
    else:
        df = st.session_state.results_df
        ranked = st.session_state.ranked
        summary = st.session_state.summary

        st.markdown('<div class="section-header">Export Results</div>', unsafe_allow_html=True)

        exp_col1, exp_col2 = st.columns(2, gap="large")

        with exp_col1:
            # CSV download
            export_df = df[["rank", "resume", "final_pct", "tfidf_pct", "skill_pct", "skills_matched", "matched_skills", "missing_skills", "status"]].copy()
            export_df.columns = ["Rank", "Resume", "Final %", "TF-IDF %", "Skill %", "Skills Matched", "Matched Skills", "Missing Skills", "Status"]
            csv_bytes = export_df.to_csv(index=False).encode("utf-8")

            st.download_button(
                label="⬇️  Download CSV Report",
                data=csv_bytes,
                file_name=f"screening_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True,
            )

        with exp_col2:
            import json
            json_data = {"summary": summary, "candidates": ranked}
            json_bytes = json.dumps(json_data, indent=2).encode("utf-8")
            st.download_button(
                label="⬇️  Download JSON Report",
                data=json_bytes,
                file_name=f"screening_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True,
            )

        st.markdown('<div class="styled-divider"></div>', unsafe_allow_html=True)
        st.markdown('<div class="section-header">Full Results Table</div>', unsafe_allow_html=True)
        st.dataframe(
            export_df.style.background_gradient(
                cmap="Greens", subset=["Final %"],
            ).applymap(
                lambda v: "color: #00e5a0" if "SHORTLISTED" in str(v) else "color: #ff5c5c",
                subset=["Status"]
            ),
            use_container_width=True,
            height=400,
        )

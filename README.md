<div align="center">

<img src="https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
<img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white"/>
<img src="https://img.shields.io/badge/Scikit--Learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white"/>
<img src="https://img.shields.io/badge/NLP-TF--IDF-blue?style=for-the-badge"/>
<img src="https://img.shields.io/badge/Cosine-Similarity-success?style=for-the-badge"/>
<img src="https://img.shields.io/badge/Plotly-Visualization-6A0DAD?style=for-the-badge"/>
<img src="https://img.shields.io/badge/CSV-JSON_Reports-success?style=for-the-badge"/>
<img src="https://img.shields.io/badge/ATS-Recruitment_Analytics-critical?style=for-the-badge"/>
<img src="https://img.shields.io/badge/Status-Production--Style-success?style=for-the-badge"/>

<br/><br/>

# 🤖 Automated Resume Screening Tool

### Enterprise-grade ATS simulation platform featuring NLP-powered resume ranking, TF-IDF semantic scoring, skill-gap analytics, recruiter workflows, and a premium SaaS-style Streamlit dashboard

[![License](https://img.shields.io/badge/License-CC%20BY--NC%204.0-green.svg)](LICENSE)
[![ML](https://img.shields.io/badge/ML-TFIDF%20%2B%20Cosine-orange)]()
[![Dashboard](https://img.shields.io/badge/UI-Streamlit-red)]()
[![Reports](https://img.shields.io/badge/Reports-CSV%20%2B%20JSON-blue)]()
[![NLP](https://img.shields.io/badge/NLP-Resume%20Analytics-success)]()
[![Status](https://img.shields.io/badge/Status-Recruiter--Ready-success)]()

<br/>

</div>

---

## 📌 Table of Contents

- [Overview](#overview)
- [Business Context](#business-context)
- [Core Features](#core-features)
- [Industry Relevance](#industry-relevance)
- [System Architecture](#system-architecture)
- [Operational Workflow](#operational-workflow)
- [ML & Analytics Engine](#ml--analytics-engine)
- [Visualization Layer](#visualization-layer)
- [Tech Stack](#tech-stack)
- [Scoring Formula](#scoring-formula)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [How to Run](#how-to-run)
- [Dashboard Overview](#dashboard-overview)
- [Screenshots & Outputs](#screenshots--outputs)
- [Verification Performed](#verification-performed)
- [Learning Outcomes](#learning-outcomes)
- [Future Improvements](#future-improvements)
- [License](#license)

---

<a id="overview"></a>

## 🔍 Overview

The **Automated Resume Screening Tool** is a production-style Applicant Tracking System (ATS) simulation platform designed to automate resume ingestion, candidate ranking, skill-gap analysis, and recruiter decision workflows using Natural Language Processing (NLP) techniques.

The system replicates core ATS pipeline behavior commonly used in enterprise recruitment platforms by combining:

- **TF-IDF semantic similarity scoring**
- **Cosine similarity-based candidate ranking**
- **Skill keyword intelligence**
- **Automated shortlisting pipelines**
- **Interactive Streamlit dashboarding**
- **CSV & JSON recruiter reporting**
- **Multi-format resume parsing**
- **Operational analytics visualization**

Unlike simplistic keyword-matching scripts, the platform introduces structured ranking logic, configurable scoring weights, recruiter-style analytics, and dashboard-driven candidate intelligence.

The project demonstrates practical engineering concepts used in:

- Recruitment technology platforms
- HR analytics systems
- NLP-based document intelligence
- Resume parsing engines
- Talent acquisition automation
- Candidate recommendation systems

---

<a id="business-context"></a>

## ❗ Business Context

Modern organizations receive hundreds or even thousands of resumes for a single hiring campaign.

Manual screening introduces several operational bottlenecks:

- **High Resume Volume**  
  Recruiters spend significant time manually reviewing repetitive candidate profiles.

- **Inconsistent Evaluation**  
  Human review processes often vary between recruiters and departments.

- **Skill Detection Challenges**  
  Critical technologies and competencies may be overlooked during rapid screening.

- **Lack of Standardized Ranking**  
  Organizations struggle to objectively prioritize candidates.

- **No Structured Analytics**  
  Traditional hiring workflows rarely provide measurable screening metrics.

- **Inefficient Candidate Shortlisting**  
  HR teams require faster methods to identify high-potential applicants.

This project addresses those challenges through an automated NLP-driven ranking pipeline capable of semantic analysis, weighted scoring, reporting automation, and recruiter dashboard visualization.

---

<a id="core-features"></a>

## 🚀 Core Features

### Resume Processing Engine

- Multi-format resume parsing
- PDF extraction using `pdfplumber`
- DOCX parsing with `python-docx`
- TXT ingestion with UTF-8 support
- Automated text normalization pipeline

### NLP & Candidate Intelligence

- TF-IDF vectorization
- Cosine similarity scoring
- Skill keyword extraction
- Semantic candidate matching
- Weighted scoring architecture
- Skill-gap analysis reporting

### Recruiter Workflow Automation

- Candidate ranking pipeline
- Automated shortlisting thresholds
- Recruiter-ready CSV reports
- Structured JSON analytics exports
- Candidate score breakdown visibility

### Streamlit Dashboard

- Premium dark SaaS-style UI
- Candidate analytics visualization
- Ranking dashboards
- Shortlist metrics display
- Interactive recruiter insights
- Operational score monitoring

### Reporting & Analytics

- Timestamped report generation
- Candidate ranking summaries
- Skill deficiency tracking
- Downloadable structured reports
- Screening audit visibility

### CLI & Workflow Support

- Command-line execution pipeline
- Configurable shortlist thresholds
- Resume directory scanning
- Batch processing workflow

---

<a id="industry-relevance"></a>

## 🏭 Industry Relevance

| Industry / Domain | Real-World Use Case | Equivalent Enterprise Workflow |
|---|---|---|
| **Human Resources** | Resume screening automation | Applicant Tracking Systems |
| **Recruitment Tech** | Candidate ranking | Talent intelligence platforms |
| **Enterprise Hiring** | Bulk applicant processing | ATS workflow orchestration |
| **HR Analytics** | Skill-gap reporting | Hiring analytics dashboards |
| **AI & NLP** | Semantic document analysis | NLP document intelligence |
| **Data Engineering** | Resume ETL pipelines | Recruitment data processing |
| **SaaS Platforms** | Recruiter dashboards | Talent acquisition portals |

The workflow mirrors modern ATS architectures:

```text
Resume Uploads → NLP Processing → TF-IDF Vectorization → Skill Matching → Ranking → Reporting → Recruiter Dashboard
```

---

<a id="system-architecture"></a>

## 🏗️ System Architecture

```text
+-------------------------------------------------------------------+
|                           INPUT LAYER                             |
|   PDF / DOCX / TXT Resumes + Job Description + Skill Keywords     |
+----------------------------------+--------------------------------+
                                   |
                                   v
+-------------------------------------------------------------------+
|                      EXTRACTION & CLEANING                        |
| * PDF Parsing            * DOCX Parsing                           |
| * Text Normalization     * Stopword Removal                       |
| * Regex Cleaning         * Noise Elimination                      |
+----------------------------------+--------------------------------+
                                   |
                                   v
+-------------------------------------------------------------------+
|                    NLP & ANALYTICS ENGINE                         |
| * TF-IDF Vectorization                                           |
| * Cosine Similarity Scoring                                      |
| * Skill Keyword Matching                                         |
| * Weighted Candidate Ranking                                     |
| * Shortlisting Logic                                             |
+----------------------------------+--------------------------------+
                                   |
                                   v
+-------------------------------------------------------------------+
|                    REPORTING & OUTPUT LAYER                       |
| * CSV Reports            * JSON Exports                           |
| * Candidate Ranking      * Skill Gap Reports                      |
| * Threshold Evaluation   * Recruiter Metrics                      |
+----------------------------------+--------------------------------+
                                   |
                                   v
+-------------------------------------------------------------------+
|                        DASHBOARD LAYER                            |
| * Streamlit UI            * Recruiter Analytics                   |
| * Candidate Monitoring    * Visualization & Reporting             |
+-------------------------------------------------------------------+
```

---

<a id="operational-workflow"></a>

## ⚙️ Operational Workflow

```text
1. Upload Resume Files
           ↓
2. Load Job Description
           ↓
3. Extract Resume Text
           ↓
4. Clean & Normalize Content
           ↓
5. Generate TF-IDF Vectors
           ↓
6. Compute Cosine Similarity
           ↓
7. Execute Skill Matching
           ↓
8. Apply Weighted Scoring
           ↓
9. Rank & Shortlist Candidates
           ↓
10. Generate CSV/JSON Reports
           ↓
11. Visualize Insights in Dashboard
```

---

<a id="ml--analytics-engine"></a>

## 🧠 ML & Analytics Engine

### TF-IDF Semantic Matching

The platform uses **Term Frequency–Inverse Document Frequency (TF-IDF)** vectorization to numerically represent resumes and job descriptions.

This enables semantic similarity evaluation rather than simple keyword counting.

### Cosine Similarity Scoring

Candidate relevance is calculated using cosine similarity between:

- Job description vectors
- Resume vectors

This produces normalized similarity scores between `0.0` and `1.0`.

### Skill Matching Pipeline

The system performs:

- Regex-based keyword matching
- Phrase-level skill detection
- Missing skill identification
- Recruiter-style skill-gap reporting

### Weighted Ranking Logic

The final score combines:

| Component | Purpose |
|---|---|
| TF-IDF Score | Semantic similarity |
| Skill Match Score | Explicit skill alignment |
| Threshold Logic | Shortlisting automation |

### Analytics Outputs

Generated outputs include:

- Ranked candidate tables
- Skill-gap analysis
- Shortlist metrics
- Candidate score distributions
- Recruiter-ready exports

---

<a id="visualization-layer"></a>

## 📊 Visualization Layer

The Streamlit dashboard acts as a recruiter operations console for candidate intelligence and hiring analytics.

### Dashboard Capabilities

- Candidate leaderboard
- Shortlisted candidate metrics
- Rejection statistics
- Top-score visualization
- Resume analytics monitoring
- Interactive Plotly charts
- Skill-gap visibility

### UI Characteristics

- Dark SaaS-inspired interface
- Enterprise-style layout hierarchy
- Recruiter-focused workflow design
- Real-time analytical presentation
- Dashboard-driven operational visibility

---

<a id="tech-stack"></a>

## 🛠️ Tech Stack

| Component | Technology | Purpose |
|---|---|---|
| Backend Engine | Python 3.9+ | Core application workflow |
| NLP Processing | Scikit-learn | TF-IDF & cosine similarity |
| Data Processing | Pandas, NumPy | Ranking & analytics |
| PDF Parsing | pdfplumber | PDF text extraction |
| DOCX Parsing | python-docx | Word document ingestion |
| Dashboard UI | Streamlit | Interactive recruiter dashboard |
| Visualization | Plotly | Analytical chart rendering |
| Text Cleaning | Regex (`re`) | Resume preprocessing |
| Reporting | CSV & JSON | Structured exports |
| CLI Interface | argparse | Command-line execution |

---

<a id="scoring-formula"></a>

## ⚖️ Scoring Formula

### Final Candidate Score

```text
Final Score =
(TF-IDF Cosine Similarity × Weight₁)
+
(Skill Match Percentage × Weight₂)
```

### Default Weight Configuration

```text
Final Score =
(TF-IDF × 0.5)
+
(Skill Match × 0.5)
```

### Formula Breakdown

| Metric | Description |
|---|---|
| TF-IDF Score | Semantic similarity between resume and JD |
| Skill Match Score | Percentage of required skills matched |
| Threshold | Determines shortlist eligibility |

### Shortlisting Logic

```text
Final Score ≥ Threshold   →   ✅ SHORTLISTED
Final Score < Threshold   →   ❌ REJECTED
```

---

<a id="project-structure"></a>

## 📁 Project Structure

```text
Automated-Resume-Screening-Tool/
|
|-- app.py
|-- main.py
|-- generate_sample_output.py
|-- requirements.txt
|-- README.md
|-- LICENSE
|
|-- data/
|   `-- job_description.txt
|
|-- resumes/
|   |-- arjun_sharma_data_scientist.txt
|   |-- divya_nair_ml_student.txt
|   |-- priya_menon_python_developer.txt
|   |-- rahul_krishnamurthy_nlp_engineer.txt
|   `-- sneha_patel_frontend_dev.txt
|
|-- src/
|   |-- __init__.py
|   |-- extractor.py
|   |-- cleaner.py
|   |-- scorer.py
|   `-- reporter.py
|
|-- outputs/
|   |-- screening_report_YYYYMMDD_HHMMSS.csv
|   `-- screening_report_YYYYMMDD_HHMMSS.json
|
|-- docs/
|
|-- images/
|
`-- screenshots/
    |-- dashboard.png
    |-- analytics.png
    `-- reports.png
```

---

<a id="installation"></a>

## ⚙️ Installation

### Step 1 — Clone Repository

```powershell
git clone https://github.com/CH-S-K-CHAITANYA/Automated-Resume-Screening-Tool.git
cd Automated-Resume-Screening-Tool
```

### Step 2 — Create Virtual Environment

```powershell
python -m venv .venv
.\.venv\Scripts\activate
```

### Step 3 — Install Dependencies

```powershell
pip install -r requirements.txt
```

### Step 4 — Verify Installation

```powershell
python main.py
```

---

<a id="how-to-run"></a>

## ▶️ How to Run

### Launch Streamlit Dashboard

```powershell
streamlit run app.py
```

Open browser:

```text
http://localhost:8501
```

### Run CLI Screening Workflow

```powershell
python main.py
```

### Run with Custom Parameters

```powershell
python main.py --resumes resumes/ --jd data/job_description.txt --threshold 0.40
```

### Generate Demo Outputs

```powershell
python generate_sample_output.py
```

---

<a id="dashboard-overview"></a>

## 🖥️ Dashboard Overview

### Recruiter Analytics Console

The dashboard provides centralized visibility into candidate screening workflows.

Capabilities include:

- Resume ranking analysis
- Shortlist monitoring
- Candidate comparison views
- Skill-match analytics
- Threshold adjustment workflows
- Interactive report exploration

### Candidate Intelligence Metrics

The dashboard surfaces:

- Total resumes screened
- Candidate shortlist ratio
- Top-performing candidates
- Rejection statistics
- Skill alignment scores
- Semantic relevance distributions

### Visualization Components

- Plotly bar charts
- Candidate ranking tables
- Shortlist pie charts
- Interactive recruiter metrics
- Threshold analytics dashboards

---

<a id="screenshots--outputs"></a>

## 🖼️ Screenshots & Outputs

<div align="center">

### Recruiter Dashboard

<img src="screenshots/dashboard.png" width="90%"/>

<br/><br/>

### Candidate Analytics

<img src="screenshots/analytics.png" width="90%"/>

<br/><br/>

### CSV & JSON Reporting

<img src="screenshots/reports.png" width="90%"/>

</div>

### Sample CLI Output

```text
══════════════════════════════════════════════════════════════
🤖 AUTOMATED RESUME SCREENING RESULTS
══════════════════════════════════════════════════════════════

📌 SUMMARY
Total Resumes Screened : 15
✅ Shortlisted         : 4
❌ Rejected            : 11
🏆 Top Score           : 60.6%

RANK   RESUME                           STATUS
1      arjun_sharma_data_scientist      ✅ SHORTLISTED
2      divya_nair_ml_student            ✅ SHORTLISTED
3      rahul_krishnamurthy_nlp_engineer ✅ SHORTLISTED
```

---

<a id="verification-performed"></a>

## ✅ Verification Performed

- Resume ingestion pipeline validated
- PDF extraction workflow tested
- DOCX parsing verified successfully
- TF-IDF vectorization confirmed operational
- Cosine similarity scoring validated
- Skill matching engine tested
- Streamlit dashboard launched successfully
- CSV report generation verified
- JSON export workflow validated
- CLI execution pipeline tested
- Threshold-based ranking confirmed
- Multi-format resume support verified

---

<a id="learning-outcomes"></a>

## 🎓 Learning Outcomes

### NLP & Machine Learning

- TF-IDF vectorization
- Cosine similarity algorithms
- Semantic document matching
- Skill extraction workflows
- NLP preprocessing pipelines

### Data Engineering

- ETL-style text processing
- Resume ingestion pipelines
- Structured report generation
- Ranking data workflows
- Candidate analytics processing

### Software Engineering

- Modular Python architecture
- Separation of concerns
- CLI workflow orchestration
- Scalable project structuring
- Production-style repository design

### Dashboard Engineering

- Streamlit UI development
- Interactive analytics visualization
- Recruiter-focused workflow design
- Plotly integration
- SaaS-style dashboard structuring

### Recruitment Technology Concepts

- ATS simulation architecture
- Candidate ranking systems
- Automated shortlisting workflows
- Skill-gap analytics
- Hiring intelligence pipelines

---

<a id="future-improvements"></a>

## 🔮 Future Improvements

- [ ] Sentence Transformers / BERT embeddings
- [ ] Named Entity Recognition (NER)
- [ ] Resume section classification
- [ ] Multi-language resume support
- [ ] PostgreSQL candidate persistence
- [ ] FastAPI REST API layer
- [ ] Recruiter authentication system
- [ ] Docker containerization
- [ ] Concurrent bulk-processing pipeline
- [ ] AI-powered resume summarization
- [ ] Bias-reduction anonymization workflows
- [ ] Cloud deployment pipeline

---

<a id="license"></a>

## 📄 License

This project is licensed under the  
[Creative Commons Attribution-NonCommercial 4.0 International License](LICENSE).

Commercial usage, SaaS redistribution,  
monetization, or proprietary deployment  
is prohibited without explicit written permission  
from the author.

Full License:  
https://creativecommons.org/licenses/by-nc/4.0/

---

<div align="center">

## 👨‍💻 Author

### **CH S K CHAITANYA**

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com/in/chskaitanya)

[![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/CH-S-K-CHAITANYA)

[![GitHub stars](https://img.shields.io/github/stars/CH-S-K-CHAITANYA/Automated-Resume-Screening-Tool?style=social)](https://github.com/CH-S-K-CHAITANYA/Automated-Resume-Screening-Tool)

<br/>

⭐ If you found this project useful, consider starring the repository.

</div>


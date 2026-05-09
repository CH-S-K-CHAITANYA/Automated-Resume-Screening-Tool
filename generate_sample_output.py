"""
generate_sample_output.py
=========================
Generates a sample screening output CSV without needing PDF parsing.
Run this to create demo output for GitHub README screenshots.

Usage: python generate_sample_output.py
"""

import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.cleaner import clean_text
from src.scorer import (
    compute_tfidf_scores,
    compute_skill_scores,
    compute_final_scores,
    rank_candidates,
    get_summary,
)
from src.reporter import generate_csv_report, generate_json_report, print_console_report
from main import DEFAULT_REQUIRED_SKILLS, load_job_description


def load_txt_resumes(folder):
    """Load all .txt resumes from folder."""
    resumes = {}
    for fname in os.listdir(folder):
        if fname.endswith(".txt"):
            with open(os.path.join(folder, fname), "r", encoding="utf-8") as f:
                resumes[fname] = f.read()
    return resumes


if __name__ == "__main__":
    print("\n🚀 Generating sample screening output...\n")

    # Load data
    raw_resumes = load_txt_resumes("resumes")
    raw_jd = load_job_description("data/job_description.txt")

    # Clean
    cleaned_jd = clean_text(raw_jd)
    cleaned_resumes = {f: clean_text(t) for f, t in raw_resumes.items()}

    # Score
    tfidf_scores = compute_tfidf_scores(cleaned_jd, cleaned_resumes)
    skill_scores = compute_skill_scores(DEFAULT_REQUIRED_SKILLS, cleaned_resumes)
    final_scores = compute_final_scores(tfidf_scores, skill_scores)
    ranked = rank_candidates(final_scores, threshold=0.40)
    summary = get_summary(ranked, threshold=0.40)

    # Output
    print_console_report(ranked, summary)
    generate_csv_report(ranked, "outputs", "Data_Scientist")
    generate_json_report(ranked, summary, "outputs", "Data_Scientist")

    print("✅ Sample output files generated in outputs/ folder!")

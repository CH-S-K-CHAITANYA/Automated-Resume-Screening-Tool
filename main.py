"""
main.py
=======
Command-line entry point for the Automated Resume Screening Tool.
Runs the full pipeline: Extract → Clean → Score → Rank → Report

Usage:
    python main.py

Or with custom arguments:
    python main.py --resumes resumes/ --jd data/job_description.txt --threshold 0.40
"""

import os
import argparse

from src.extractor import load_all_resumes
from src.cleaner import clean_text, extract_skills_from_text
from src.scorer import (
    compute_tfidf_scores,
    compute_skill_scores,
    compute_final_scores,
    rank_candidates,
    get_summary,
)
from src.reporter import generate_csv_report, generate_json_report, print_console_report


# ─────────────────────────────────────────────
# DEFAULT REQUIRED SKILLS
# Edit this list for your specific job role
# ─────────────────────────────────────────────
DEFAULT_REQUIRED_SKILLS = [
    "python", "machine learning", "deep learning", "tensorflow", "pytorch",
    "scikit-learn", "pandas", "numpy", "sql", "data analysis",
    "natural language processing", "nlp", "data visualization", "statistics",
    "git", "docker", "rest api", "flask", "fastapi", "aws",
    "feature engineering", "neural networks", "regression", "classification",
    "problem solving", "communication",
]


def load_job_description(jd_path: str) -> str:
    """Load job description text from a file."""
    if not os.path.exists(jd_path):
        print(f"[ERROR] Job description file not found: {jd_path}")
        return ""
    with open(jd_path, "r", encoding="utf-8") as f:
        return f.read()


def run_pipeline(
    resumes_dir: str = "resumes",
    jd_path: str = "data/job_description.txt",
    skills: list = None,
    threshold: float = 0.40,
    output_dir: str = "outputs",
    tfidf_weight: float = 0.5,
    skill_weight: float = 0.5,
):
    """
    Run the complete resume screening pipeline.
    
    Pipeline:
        1. Load resumes from directory
        2. Load job description from file
        3. Clean all texts
        4. Compute TF-IDF cosine similarity scores
        5. Compute skill match scores
        6. Combine scores with weights
        7. Rank candidates
        8. Generate reports
    """
    print("\n" + "=" * 60)
    print("   🤖  AUTOMATED RESUME SCREENING TOOL  🤖")
    print("=" * 60)

    if skills is None:
        skills = DEFAULT_REQUIRED_SKILLS

    # ── STEP 1: Load Resumes ──
    print("\n[STEP 1/6] Loading and extracting resume text...")
    raw_resumes = load_all_resumes(resumes_dir)

    if not raw_resumes:
        print("[ABORT] No resumes found. Add PDF/DOCX/TXT files to the 'resumes/' folder.")
        return

    # ── STEP 2: Load Job Description ──
    print("\n[STEP 2/6] Loading job description...")
    raw_jd = load_job_description(jd_path)

    if not raw_jd:
        print("[ABORT] Job description is empty or missing.")
        return

    print(f"  ✅ Job description loaded ({len(raw_jd)} characters)")

    # ── STEP 3: Clean All Texts ──
    print("\n[STEP 3/6] Cleaning and preprocessing text...")
    cleaned_jd = clean_text(raw_jd, remove_stops=True)
    cleaned_resumes = {fname: clean_text(text, remove_stops=True) for fname, text in raw_resumes.items()}
    print(f"  ✅ Cleaned {len(cleaned_resumes)} resume(s)")

    # ── STEP 4: TF-IDF Scoring ──
    print("\n[STEP 4/6] Computing TF-IDF cosine similarity scores...")
    tfidf_scores = compute_tfidf_scores(cleaned_jd, cleaned_resumes)
    for fname, score in tfidf_scores.items():
        print(f"  → {fname}: {score*100:.1f}%")

    # ── STEP 5: Skill Matching ──
    print("\n[STEP 5/6] Matching required skills...")
    print(f"  Required skills ({len(skills)}): {', '.join(skills[:5])}...")
    skill_scores = compute_skill_scores(skills, cleaned_resumes)
    for fname, data in skill_scores.items():
        print(f"  → {fname}: {data['score']*100:.1f}% ({len(data['matched'])}/{len(skills)} skills)")

    # ── STEP 6: Final Scoring + Ranking ──
    print("\n[STEP 6/6] Computing final scores and ranking candidates...")
    final_scores = compute_final_scores(tfidf_scores, skill_scores, tfidf_weight, skill_weight)
    ranked = rank_candidates(final_scores, threshold=threshold)
    summary = get_summary(ranked, threshold=threshold)

    # ── OUTPUT ──
    print_console_report(ranked, summary)

    # Detect job title from JD file name for report naming
    job_title = os.path.splitext(os.path.basename(jd_path))[0].replace("_", " ").title()

    csv_path = generate_csv_report(ranked, output_dir, job_title)
    json_path = generate_json_report(ranked, summary, output_dir, job_title)

    print(f"\n✅ Pipeline complete! Reports saved to: {output_dir}/")
    return ranked, summary


# ─────────────────────────────────────────────
# ARGUMENT PARSER
# ─────────────────────────────────────────────

def parse_args():
    parser = argparse.ArgumentParser(description="Automated Resume Screening Tool")
    parser.add_argument("--resumes", default="resumes", help="Path to resumes folder")
    parser.add_argument("--jd", default="data/job_description.txt", help="Path to job description file")
    parser.add_argument("--threshold", type=float, default=0.40, help="Shortlist threshold (0.0-1.0)")
    parser.add_argument("--output", default="outputs", help="Output directory for reports")
    parser.add_argument("--tfidf-weight", type=float, default=0.5, help="Weight for TF-IDF score")
    parser.add_argument("--skill-weight", type=float, default=0.5, help="Weight for skill match score")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    run_pipeline(
        resumes_dir=args.resumes,
        jd_path=args.jd,
        skills=DEFAULT_REQUIRED_SKILLS,
        threshold=args.threshold,
        output_dir=args.output,
        tfidf_weight=args.tfidf_weight,
        skill_weight=args.skill_weight,
    )

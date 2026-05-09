"""
reporter.py
===========
Generates CSV reports and formatted console output for screening results.
Outputs are saved in the /outputs directory.
"""

import os
import csv
import json
from datetime import datetime


def generate_csv_report(ranked_candidates: list, output_dir: str, job_title: str = "Job") -> str:
    """
    Save full screening results to a CSV file.
    
    Args:
        ranked_candidates: Sorted list of candidate dicts from rank_candidates().
        output_dir: Folder where the CSV will be saved.
        job_title: Used in the filename.
    Returns:
        Full path of the saved CSV file.
    """
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_title = job_title.replace(" ", "_").replace("/", "_")
    filename = f"screening_report_{safe_title}_{timestamp}.csv"
    filepath = os.path.join(output_dir, filename)

    if not ranked_candidates:
        print("[WARNING] No candidates to write to CSV.")
        return ""

    fieldnames = [
        "rank", "resume", "final_score", "tfidf_score", "skill_score",
        "skills_matched", "matched_skills", "missing_skills", "status"
    ]

    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for candidate in ranked_candidates:
            # Write only the fields we want
            row = {k: candidate[k] for k in fieldnames}
            writer.writerow(row)

    print(f"\n📊 CSV Report saved: {filepath}")
    return filepath


def generate_json_report(ranked_candidates: list, summary: dict, output_dir: str, job_title: str = "Job") -> str:
    """
    Save full results as a JSON file (useful for APIs and dashboards).
    
    Args:
        ranked_candidates: List of candidate dicts.
        summary: Summary dict from get_summary().
        output_dir: Output folder path.
        job_title: Used in filename.
    Returns:
        Full path of the saved JSON file.
    """
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_title = job_title.replace(" ", "_").replace("/", "_")
    filename = f"screening_report_{safe_title}_{timestamp}.json"
    filepath = os.path.join(output_dir, filename)

    report = {
        "job_title": job_title,
        "generated_at": datetime.now().isoformat(),
        "summary": summary,
        "candidates": ranked_candidates,
    }

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    print(f"📋 JSON Report saved: {filepath}")
    return filepath


def print_console_report(ranked_candidates: list, summary: dict) -> None:
    """
    Pretty-print the screening results to the terminal.
    
    Args:
        ranked_candidates: Sorted list of candidate dicts.
        summary: Summary dict.
    """
    print("\n" + "═" * 80)
    print("              🤖  AUTOMATED RESUME SCREENING RESULTS  🤖")
    print("═" * 80)

    # Summary box
    print(f"\n📌 SUMMARY")
    print(f"   Total Resumes Screened : {summary['total_resumes']}")
    print(f"   ✅ Shortlisted         : {summary['shortlisted_count']}")
    print(f"   ❌ Rejected            : {summary['rejected_count']}")
    print(f"   🏆 Top Candidate       : {summary['top_candidate']}")
    print(f"   🎯 Top Score           : {summary['top_score'] * 100:.1f}%")
    print(f"   📏 Threshold Used      : {summary['threshold_used'] * 100:.0f}%")

    # Candidate table
    print("\n" + "─" * 80)
    print(f"{'RANK':<6} {'RESUME':<30} {'FINAL':>7} {'TFIDF':>7} {'SKILL':>7} {'STATUS':<20}")
    print("─" * 80)

    for c in ranked_candidates:
        print(
            f"{c['rank']:<6} "
            f"{c['resume'][:28]:<30} "
            f"{c['final_score']*100:>6.1f}% "
            f"{c['tfidf_score']*100:>6.1f}% "
            f"{c['skill_score']*100:>6.1f}% "
            f"  {c['status']}"
        )

    print("─" * 80)

    # Shortlisted details
    shortlisted = [c for c in ranked_candidates if "SHORTLISTED" in c["status"]]
    if shortlisted:
        print("\n✅ SHORTLISTED CANDIDATES — SKILL DETAIL")
        print("─" * 80)
        for c in shortlisted:
            print(f"\n  #{c['rank']} {c['resume']}")
            print(f"     Final Score   : {c['final_score']*100:.1f}%")
            print(f"     Matched Skills: {c['matched_skills']}")
            print(f"     Missing Skills: {c['missing_skills']}")

    print("\n" + "═" * 80 + "\n")

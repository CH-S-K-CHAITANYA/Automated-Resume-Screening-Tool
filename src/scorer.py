"""
scorer.py
=========
Core NLP engine for resume screening.
Uses TF-IDF vectorization + cosine similarity to score resumes
against a job description. Also performs direct skill keyword matching.
"""

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from src.cleaner import extract_skills_from_text, clean_text


# ─────────────────────────────────────────────
# TFIDF + COSINE SIMILARITY SCORING
# ─────────────────────────────────────────────

def compute_tfidf_scores(job_description: str, resume_texts: dict) -> dict:
    """
    Compute TF-IDF cosine similarity between the job description
    and each resume.
    
    How it works:
    - TF-IDF converts text into numerical vectors where each dimension
      represents a word's importance (Term Frequency × Inverse Document Freq)
    - Cosine similarity measures the angle between two vectors
    - Score of 1.0 = perfect match, 0.0 = no overlap
    
    Args:
        job_description: Cleaned job description text.
        resume_texts: Dict of {filename: cleaned_resume_text}.
    Returns:
        Dict of {filename: tfidf_score (0.0 to 1.0)}.
    """
    if not resume_texts:
        return {}

    filenames = list(resume_texts.keys())
    texts = [job_description] + [resume_texts[f] for f in filenames]

    # Build TF-IDF matrix
    vectorizer = TfidfVectorizer(
        ngram_range=(1, 2),   # unigrams + bigrams ("machine learning", "data science")
        max_features=5000,    # cap vocabulary size
        sublinear_tf=True,    # apply log normalization to term frequency
    )
    tfidf_matrix = vectorizer.fit_transform(texts)

    # JD is index 0; resumes are index 1..n
    jd_vector = tfidf_matrix[0]
    resume_vectors = tfidf_matrix[1:]

    scores = cosine_similarity(jd_vector, resume_vectors).flatten()

    return {filenames[i]: round(float(scores[i]), 4) for i in range(len(filenames))}


# ─────────────────────────────────────────────
# SKILL KEYWORD MATCHING SCORING
# ─────────────────────────────────────────────

def compute_skill_scores(required_skills: list, resume_texts: dict) -> dict:
    """
    Compute what percentage of required skills are found in each resume.
    
    Args:
        required_skills: List of skills from the job description.
        resume_texts: Dict of {filename: cleaned_text}.
    Returns:
        Dict of {filename: {'score': float, 'matched': list, 'missing': list}}.
    """
    results = {}
    total_skills = len(required_skills)

    if total_skills == 0:
        return {f: {"score": 0.0, "matched": [], "missing": []} for f in resume_texts}

    for filename, text in resume_texts.items():
        matched = extract_skills_from_text(text, required_skills)
        missing = [s for s in required_skills if s not in matched]
        score = round(len(matched) / total_skills, 4)

        results[filename] = {
            "score": score,
            "matched": matched,
            "missing": missing,
        }

    return results


# ─────────────────────────────────────────────
# COMBINED FINAL SCORE
# ─────────────────────────────────────────────

def compute_final_scores(
    tfidf_scores: dict,
    skill_scores: dict,
    tfidf_weight: float = 0.5,
    skill_weight: float = 0.5,
) -> dict:
    """
    Combine TF-IDF score and skill match score into one final weighted score.
    
    Formula:
        final_score = (tfidf_score × tfidf_weight) + (skill_score × skill_weight)
    
    Default weights: 50% TF-IDF, 50% Skill Match.
    
    Args:
        tfidf_scores: Dict {filename: tfidf_score}.
        skill_scores: Dict {filename: {score, matched, missing}}.
        tfidf_weight: Weight for TF-IDF (0.0–1.0).
        skill_weight: Weight for skill match (0.0–1.0).
    Returns:
        Dict {filename: {final_score, tfidf_score, skill_score, matched, missing}}.
    """
    all_files = set(tfidf_scores.keys()) | set(skill_scores.keys())
    results = {}

    for filename in all_files:
        ts = tfidf_scores.get(filename, 0.0)
        sk = skill_scores.get(filename, {}).get("score", 0.0)
        matched = skill_scores.get(filename, {}).get("matched", [])
        missing = skill_scores.get(filename, {}).get("missing", [])

        final = round((ts * tfidf_weight) + (sk * skill_weight), 4)

        results[filename] = {
            "final_score": final,
            "tfidf_score": ts,
            "skill_score": sk,
            "matched_skills": matched,
            "missing_skills": missing,
            "skills_matched_count": len(matched),
        }

    return results


# ─────────────────────────────────────────────
# RANKING AND SHORTLISTING
# ─────────────────────────────────────────────

def rank_candidates(scores: dict, threshold: float = 0.40) -> list:
    """
    Sort candidates by final score (descending) and assign:
    - Status: SHORTLISTED (≥ threshold) or REJECTED (< threshold)
    - Rank: 1 = best match
    
    Args:
        scores: Output of compute_final_scores().
        threshold: Minimum final_score to be shortlisted (0.0–1.0).
    Returns:
        List of candidate dicts sorted by score, with rank and status.
    """
    ranked = sorted(scores.items(), key=lambda x: x[1]["final_score"], reverse=True)

    results = []
    for rank, (filename, data) in enumerate(ranked, start=1):
        status = "✅ SHORTLISTED" if data["final_score"] >= threshold else "❌ REJECTED"
        results.append({
            "rank": rank,
            "resume": filename,
            "final_score": data["final_score"],
            "tfidf_score": data["tfidf_score"],
            "skill_score": data["skill_score"],
            "skills_matched": data["skills_matched_count"],
            "matched_skills": ", ".join(data["matched_skills"]) if data["matched_skills"] else "None",
            "missing_skills": ", ".join(data["missing_skills"]) if data["missing_skills"] else "None",
            "status": status,
        })

    return results


def get_summary(ranked_candidates: list, threshold: float = 0.40) -> dict:
    """
    Generate a quick summary of the screening results.
    
    Args:
        ranked_candidates: Output of rank_candidates().
        threshold: Shortlist threshold used.
    Returns:
        Summary dictionary with counts and top candidates.
    """
    total = len(ranked_candidates)
    shortlisted = [c for c in ranked_candidates if "SHORTLISTED" in c["status"]]
    rejected = [c for c in ranked_candidates if "REJECTED" in c["status"]]

    return {
        "total_resumes": total,
        "shortlisted_count": len(shortlisted),
        "rejected_count": len(rejected),
        "threshold_used": threshold,
        "top_candidate": ranked_candidates[0]["resume"] if ranked_candidates else "N/A",
        "top_score": ranked_candidates[0]["final_score"] if ranked_candidates else 0.0,
        "shortlisted_names": [c["resume"] for c in shortlisted],
    }

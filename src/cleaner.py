"""
cleaner.py
==========
Cleans and normalizes raw resume text for NLP processing.
Removes noise, standardizes formatting, and prepares text for TF-IDF.
"""

import re
import string


# Common English stop words relevant to resumes (lightweight, no NLTK needed)
STOP_WORDS = {
    "a", "an", "the", "and", "or", "but", "in", "on", "at", "to", "for",
    "of", "with", "by", "from", "is", "are", "was", "were", "be", "been",
    "have", "has", "had", "do", "does", "did", "will", "would", "could",
    "should", "may", "might", "shall", "can", "this", "that", "these",
    "those", "i", "me", "my", "we", "our", "you", "your", "he", "she",
    "it", "they", "them", "his", "her", "its", "their", "as", "if",
    "then", "than", "so", "up", "out", "about", "into", "through",
    "also", "more", "very", "just", "not", "no", "nor", "yet", "both",
    "either", "each", "any", "all", "some", "such", "own", "same",
    "other", "another", "over", "under", "again", "further", "once",
}


def lowercase(text: str) -> str:
    """Convert all text to lowercase."""
    return text.lower()


def remove_emails(text: str) -> str:
    """Remove email addresses (not useful for skill matching)."""
    return re.sub(r'\S+@\S+', ' ', text)


def remove_urls(text: str) -> str:
    """Remove URLs and hyperlinks."""
    return re.sub(r'http\S+|www\.\S+', ' ', text)


def remove_phone_numbers(text: str) -> str:
    """Remove phone numbers."""
    return re.sub(r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]', ' ', text)


def remove_special_characters(text: str) -> str:
    """
    Remove punctuation and special characters.
    Keeps alphanumeric and spaces. The '+' in 'C++' is preserved
    by replacing it with 'plus' before stripping.
    """
    # Preserve C++ → cplus, C# → csharp
    text = text.replace("c++", "cplusplus").replace("c#", "csharp")
    text = text.replace(".net", "dotnet")
    # Remove remaining punctuation
    text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)
    return text


def remove_extra_whitespace(text: str) -> str:
    """Collapse multiple spaces/newlines into a single space."""
    return re.sub(r'\s+', ' ', text).strip()


def remove_stopwords(text: str) -> str:
    """
    Remove common stop words that don't contribute to skill matching.
    """
    tokens = text.split()
    filtered = [word for word in tokens if word not in STOP_WORDS and len(word) > 1]
    return " ".join(filtered)


def clean_text(text: str, remove_stops: bool = True) -> str:
    """
    Full cleaning pipeline:
    1. Lowercase
    2. Remove emails, URLs, phones
    3. Remove special characters
    4. Remove extra whitespace
    5. Optionally remove stop words
    
    Args:
        text: Raw extracted text.
        remove_stops: Whether to remove stop words (True for TF-IDF).
    Returns:
        Cleaned, normalized text string.
    """
    if not text or not text.strip():
        return ""

    text = lowercase(text)
    text = remove_emails(text)
    text = remove_urls(text)
    text = remove_phone_numbers(text)
    text = remove_special_characters(text)
    text = remove_extra_whitespace(text)

    if remove_stops:
        text = remove_stopwords(text)

    return text


def extract_skills_from_text(text: str, skill_list: list) -> list:
    """
    Find which skills from a predefined list appear in the resume text.
    Uses whole-word matching to avoid false positives.
    
    Args:
        text: Cleaned resume text (lowercase).
        skill_list: List of required skills (lowercase).
    Returns:
        List of matched skills.
    """
    matched = []
    for skill in skill_list:
        # Use word boundary matching for multi-word and single skills
        pattern = r'\b' + re.escape(skill.lower()) + r'\b'
        if re.search(pattern, text):
            matched.append(skill)
    return matched


def get_word_frequency(text: str) -> dict:
    """
    Count word frequency in text.
    Useful for keyword analysis and debugging.
    
    Args:
        text: Cleaned text.
    Returns:
        Dictionary of {word: count}, sorted by frequency.
    """
    tokens = text.split()
    freq = {}
    for token in tokens:
        freq[token] = freq.get(token, 0) + 1
    return dict(sorted(freq.items(), key=lambda x: x[1], reverse=True))

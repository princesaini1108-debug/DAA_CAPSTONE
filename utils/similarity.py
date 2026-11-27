
import re
from difflib import SequenceMatcher


def calculate_similarity(text1, text2):

    words1 = re.findall(r"\b[a-zA-Z]+\b", text1.lower())
    words2 = re.findall(r"\b[a-zA-Z]+\b", text2.lower())

    if not words1 and not words2:
        return 100.0

    if not words1 or not words2:
        return 0.0

    used_words = set()
    total_score = 0.0

    for word1 in words1:

        best_score = 0.0
        best_index = None

        for index, word2 in enumerate(words2):

            if index in used_words:
                continue

            score = SequenceMatcher(
                None,
                word1,
                word2,
                autojunk=False
            ).ratio()

            if score > best_score:
                best_score = score
                best_index = index

        if best_index is not None:
            total_score += best_score
            used_words.add(best_index)

    similarity = (
        total_score / max(len(words1), len(words2))
    ) * 100

    return round(similarity, 2)

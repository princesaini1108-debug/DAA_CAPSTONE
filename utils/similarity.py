def calculate_similarity(text1, text2):
    words1 = set(text1.split())
    words2 = set(text2.split())

    if not words1 or not words2:
        return 0.0

    common_words = words1.intersection(words2)
    all_words = words1.union(words2)

    return round((len(common_words) / len(all_words)) * 100, 2)

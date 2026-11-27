
from pathlib import Path
import re
import time
from difflib import SequenceMatcher

from algorithms.naive import naive_search
from algorithms.rabin_karp import rabin_karp_search
from algorithms.kmp import kmp_search


BASE_DIR = Path(__file__).resolve().parent
BENCHMARK_RUNS = 100

ALGORITHMS = {
    "Naive": {
        "function": naive_search,
        "working": "Checks the pattern at every possible position in the text.",
        "best": "O(n)",
        "average": "O(n*m)",
        "worst": "O(n*m)",
        "space": "O(1) auxiliary space"
    },
    "Rabin-Karp": {
        "function": rabin_karp_search,
        "working": "Uses hashing and rolling hash to find pattern matches.",
        "best": "O(n+m)",
        "average": "O(n+m) expected",
        "worst": "O(n*m)",
        "space": "O(1) auxiliary space"
    },
    "KMP": {
        "function": kmp_search,
        "working": "Uses LPS (Longest Prefix Suffix) to avoid repeated comparisons.",
        "best": "O(n+m)",
        "average": "O(n+m)",
        "worst": "O(n+m)",
        "space": "O(m) for LPS array"
    }
}


def get_document(name):

    print(f"\nEnter {name} text:")
    print("Type END on a new line when finished.\n")

    lines = []

    while True:
        line = input()

        if line.strip().upper() == "END":
            break

        lines.append(line)

    text = "\n".join(lines).lower().strip()

    print("\nInput received:", repr(text))
    print("Character count:", len(text))

    return text


def normalize_text(text):
    text = text.lower()
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def get_sentences(text):

    sentences = re.split(r'(?<=[.!?])\s+', text)

    return [s.strip() for s in sentences if s.strip()]


def get_words(text):

    return re.findall(r'\b[a-zA-Z]+\b', text.lower())


def word_similarity(word1, word2):

    return SequenceMatcher(
        None, word1, word2, autojunk=False
    ).ratio()


def calculate_similarity(text1, text2):

    words1 = get_words(text1)
    words2 = get_words(text2)

    if not words1 and not words2:
        return 100.0

    if not words1 or not words2:
        return 0.0

    used_words = set()
    total_score = 0.0

    for word1 in words1:

        best_score = 0
        best_index = None

        for index, word2 in enumerate(words2):

            if index in used_words:
                continue

            score = word_similarity(word1, word2)

            if score > best_score:
                best_score = score
                best_index = index

        if best_index is not None and best_score >= 0.60:

            total_score += best_score
            used_words.add(best_index)

    similarity = (
        total_score / max(len(words1), len(words2))
    ) * 100

    return round(similarity, 2)


def find_similar_words(text1, text2):

    words1 = set(get_words(text1))
    words2 = set(get_words(text2))

    results = []

    for word1 in words1:

        for word2 in words2:

            if word1 == word2:
                continue

            if min(len(word1), len(word2)) < 3:
                continue

            score = word_similarity(word1, word2)

            if score >= 0.60:

                results.append({
                    "word1": word1,
                    "word2": word2,
                    "score": round(score * 100, 2)
                })

    return results


def find_partial_matches(text1, text2):

    sentences1 = get_sentences(text1)
    sentences2 = get_sentences(text2)

    results = []

    for sentence1 in sentences1:

        words1 = get_words(sentence1)

        for sentence2 in sentences2:

            words2 = get_words(sentence2)

            if not words1 or not words2:
                continue

            used = set()
            matched = []

            for word1 in words1:

                best_score = 0
                best_index = None

                for index, word2 in enumerate(words2):

                    if index in used:
                        continue

                    score = word_similarity(word1, word2)

                    if score > best_score:
                        best_score = score
                        best_index = index

                if best_index is not None and best_score >= 0.60:

                    matched.append(word1)
                    used.add(best_index)

            percentage = (
                len(matched) / max(len(words1), len(words2))
            ) * 100

            if percentage >= 40:

                results.append({
                    "sentence1": sentence1,
                    "sentence2": sentence2,
                    "matched_words": matched,
                    "percentage": round(percentage, 2)
                })

    return results


def find_exact_matches(algorithm, text1, text2):

    sentences1 = get_sentences(text1)
    sentences2 = get_sentences(text2)

    matches = []

    for sentence in sentences1:

        pattern = normalize_text(sentence)

        if pattern and algorithm(normalize_text(text2), pattern):

            matches.append({
                "direction": "Document 1 -> Document 2",
                "sentence": sentence
            })

    for sentence in sentences2:

        pattern = normalize_text(sentence)

        if pattern and algorithm(normalize_text(text1), pattern):

            matches.append({
                "direction": "Document 2 -> Document 1",
                "sentence": sentence
            })

    return matches


def benchmark_algorithm(algorithm, text1, text2):

    start = time.perf_counter()

    for _ in range(BENCHMARK_RUNS):

        find_exact_matches(algorithm, text1, text2)

    end = time.perf_counter()

    total_time = end - start

    average_time = total_time / BENCHMARK_RUNS

    return total_time, average_time


def compare_documents(text1, text2):

    similarity = calculate_similarity(text1, text2)

    print("\n========================================")
    print("       DOCUMENT INFORMATION")
    print("========================================")

    print("Document 1 Characters:", len(text1))
    print("Document 2 Characters:", len(text2))

    print("Document 1 Sentences:", len(get_sentences(text1)))
    print("Document 2 Sentences:", len(get_sentences(text2)))

    print("\nDocument Similarity:", similarity, "%")

    report = []

    report.append("PLAGIARISM DETECTION REPORT")
    report.append(f"Document 1 Characters: {len(text1)}")
    report.append(f"Document 2 Characters: {len(text2)}")
    report.append(f"Document Similarity: {similarity}%")

    performance = []

    for name, details in ALGORITHMS.items():

        algorithm = details["function"]

        print("\n========================================")
        print("ALGORITHM:", name)
        print("========================================")

        print("\nWorking:")
        print(details["working"])

        print("\nTime Complexity:")
        print("Best Case:", details["best"])
        print("Average Case:", details["average"])
        print("Worst Case:", details["worst"])

        print("\nSpace Complexity:")
        print(details["space"])

        matches = find_exact_matches(
            algorithm, text1, text2
        )

        total_time, average_time = benchmark_algorithm(
            algorithm, text1, text2
        )

        print("\nExact Matching Sentences:", len(matches))

        for match in matches:

            print("\nDirection:", match["direction"])
            print("Sentence:", match["sentence"])

        print("\nExecution Time:")
        print("Total Time:", f"{total_time:.8f} seconds")
        print("Average Time:", f"{average_time:.8f} seconds")
        print("Average Time:", f"{average_time * 1000:.6f} ms")

        performance.append({
            "name": name,
            "matches": len(matches),
            "total": total_time,
            "average": average_time
        })

        report.append(f"\nALGORITHM: {name}")
        report.append(f"Working: {details['working']}")
        report.append(f"Best Case: {details['best']}")
        report.append(f"Average Case: {details['average']}")
        report.append(f"Worst Case: {details['worst']}")
        report.append(f"Space Complexity: {details['space']}")
        report.append(f"Exact Matches: {len(matches)}")
        report.append(f"Total Time: {total_time:.8f} seconds")
        report.append(f"Average Time: {average_time:.8f} seconds")

        for match in matches:
            report.append(
                f"{match['direction']}: {match['sentence']}"
            )

    # Partial matching

    print("\n========================================")
    print("       PARTIAL SENTENCE MATCHING")
    print("========================================")

    partial_matches = find_partial_matches(text1, text2)

    print("Partial Matching Sentences:", len(partial_matches))

    report.append(
        f"\nPartial Matching Sentences: {len(partial_matches)}"
    )

    for match in partial_matches:

        print("\nDocument 1:", match["sentence1"])
        print("Document 2:", match["sentence2"])
        print("Matching Words:", match["matched_words"])
        print("Similarity:", match["percentage"], "%")

        report.append(
            f"Partial Match: {match['percentage']}%"
        )

        report.append(
            f"Matched Words: {match['matched_words']}"
        )

    # Similar word matching

    print("\n========================================")
    print("          SIMILAR WORDS")
    print("========================================")

    similar_words = find_similar_words(text1, text2)

    if similar_words:

        for item in similar_words:

            print(
                item["word1"],
                "<->",
                item["word2"],
                ":",
                item["score"],
                "%"
            )

            report.append(
                f"Similar Words: {item['word1']} <-> "
                f"{item['word2']}: {item['score']}%"
            )

    else:
        print("No similar words found.")

    # Performance comparison

    print("\n========================================")
    print("       PERFORMANCE COMPARISON")
    print("========================================")

    print(
        f"{'Algorithm':<15}"
        f"{'Matches':<12}"
        f"{'Total (sec)':<18}"
        f"{'Average (ms)':<15}"
    )

    for item in performance:

        print(
            f"{item['name']:<15}"
            f"{item['matches']:<12}"
            f"{item['total']:<18.8f}"
            f"{item['average'] * 1000:<15.6f}"
        )

    fastest = min(performance, key=lambda x: x["average"])

    print("\nFastest Algorithm in this test:", fastest["name"])

    report.append("\nPERFORMANCE COMPARISON")

    for item in performance:

        report.append(
            f"{item['name']}: "
            f"Total={item['total']:.8f}s, "
            f"Average={item['average']:.8f}s"
        )

    report.append(f"Fastest Algorithm: {fastest['name']}")

    # Final result

    print("\n========================================")
    print("             FINAL RESULT")
    print("========================================")

    print("Document Similarity:", similarity, "%")

    if text1 == text2:
        print("Both documents are identical.")

    elif similarity >= 50:
        print("High content similarity detected.")

    elif similarity >= 20:
        print("Moderate content similarity detected.")

    elif similarity > 0:
        print("Low content similarity detected.")

    else:
        print("No significant similarity detected.")

    # Save files

    documents_folder = BASE_DIR / "documents"
    documents_folder.mkdir(exist_ok=True)

    (documents_folder / "document1.txt").write_text(
        text1, encoding="utf-8"
    )

    (documents_folder / "document2.txt").write_text(
        text2, encoding="utf-8"
    )

    results_folder = BASE_DIR / "results"
    results_folder.mkdir(exist_ok=True)

    (results_folder / "comparison.txt").write_text(
        "\n".join(report), encoding="utf-8"
    )

    print("\nDocuments saved successfully!")
    print("Report saved in results/comparison.txt")


def main():

    print("========================================")
    print("      PLAGIARISM DETECTION SYSTEM")
    print("========================================")

    document1 = get_document("DOCUMENT 1")
    document2 = get_document("DOCUMENT 2")

    if not document1 or not document2:

        print("\nBoth documents must contain text.")
        return

    compare_documents(document1, document2)


if __name__ == "__main__":
    main()

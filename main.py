
from pathlib import Path
import time
import re

from algorithms.naive import naive_search
from algorithms.rabin_karp import rabin_karp_search
from algorithms.kmp import kmp_search
from utils.similarity import calculate_similarity


BASE_DIR = Path(__file__).resolve().parent


def get_document(document_name):

    print(f"\nEnter {document_name} text:")
    print("Type END on a new line when finished.\n")

    lines = []

    while True:
        line = input()

        if line.strip().upper() == "END":
            break

        lines.append(line)

    return "\n".join(lines).lower()


def get_sentences(text):

    sentences = re.split(r'(?<=[.!?])\s+', text)

    return [s.strip() for s in sentences if s.strip()]


def compare_documents(text1, text2):

    similarity = calculate_similarity(text1, text2)

    algorithms = {
        "Naive": naive_search,
        "Rabin-Karp": rabin_karp_search,
        "KMP": kmp_search
    }

    sentences1 = get_sentences(text1)
    sentences2 = get_sentences(text2)

    comparisons = [
        ("Document 1 vs Document 2", sentences1, text2),
        ("Document 2 vs Document 1", sentences2, text1)
    ]

    report = []

    print("\n====================================")
    print("       PLAGIARISM DETECTION")
    print("====================================")

    print("\nDocument 1 Characters:", len(text1))
    print("Document 2 Characters:", len(text2))
    print("Document Similarity:", similarity, "%")

    for title, sentences, target in comparisons:

        print("\n------------------------------------")
        print(title)
        print("------------------------------------")

        report.append("\n" + title)

        for name, algorithm in algorithms.items():

            start = time.perf_counter()

            matched_sentences = []

            for sentence in sentences:

                positions = algorithm(target, sentence)

                if positions:
                    matched_sentences.append(sentence)

            end = time.perf_counter()

            execution_time = end - start

            print("\nAlgorithm:", name)
            print("Matching Sentences:", len(matched_sentences))
            print("Execution Time:", round(execution_time, 8), "seconds")

            if matched_sentences:
                for sentence in matched_sentences:
                    print("Matched:", sentence)

            report.append(
                f"{name}: {len(matched_sentences)} matching sentences, "
                f"Time: {execution_time:.8f} seconds"
            )

    print("\n====================================")
    print("          FINAL RESULT")
    print("====================================")

    print("Similarity:", similarity, "%")

    if text1 == text2:
        print("Both documents are exactly identical.")
    elif similarity > 0:
        print("Some common content has been detected.")
    else:
        print("No common words detected.")

    report.append(f"\nDocument Similarity: {similarity}%")

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

    print("====================================")
    print("     PLAGIARISM DETECTION SYSTEM")
    print("====================================")

    document1 = get_document("DOCUMENT 1")

    document2 = get_document("DOCUMENT 2")

    if not document1.strip() or not document2.strip():
        print("\nBoth documents must contain text.")
        return

    compare_documents(document1, document2)


if __name__ == "__main__":
    main()

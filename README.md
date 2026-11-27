# Plagiarism Detection Using String Matching Algorithms

A beginner-friendly Python project that compares two text documents using:
1. Naive Pattern Matching
2. Rabin-Karp
3. Knuth-Morris-Pratt (KMP)

It also calculates a basic Jaccard word similarity score and records execution times.

## Project structure

```text
Plagiarism-Detection/
├── main.py
├── algorithms/
│   ├── __init__.py
│   ├── naive.py
│   ├── rabin_karp.py
│   └── kmp.py
├── utils/
│   ├── __init__.py
│   ├── file_handler.py
│   └── similarity.py
├── documents/
│   ├── document1.txt
│   └── document2.txt
├── results/
│   └── comparison.txt
└── README.md
```

## Requirements
- Python 3.8 or newer
- No external libraries required

## Run
Open a terminal inside this folder and run:

```bash
python main.py
```

Edit `documents/document1.txt` and `documents/document2.txt` to test your own documents.

## Notes
- Pattern matching is exact and case-insensitive because input files are converted to lowercase.
- The similarity score is Jaccard similarity over unique whitespace-separated words. It is a simple indicator, not proof of plagiarism.
- The program uses the first 3, 5, and 8 words of Document 1 as patterns and searches for them in Document 2.
- Execution times depend on your computer, document size, and Python version.

"""Generate Experiment 10 theory PDF (shingling, Jaccard, and LSH)."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from pdf_math_utils import LabPDF


def generate():
    pdf = LabPDF("Experiment 10 - Shingling and Locality Sensitive Hashing")
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.title_page(
        "Experiment 10",
        "Document Similarity Using Shingling and LSH",
        "Subject: Data Science Lab | Dataset: 5 short documents | Mapped CO(s): CO3",
    )

    pdf.section_title("1. Aim")
    pdf.body(
        "To measure how similar documents are with shingling and Jaccard similarity, "
        "and to find the similar ones with MinHash and Locality Sensitive Hashing."
    )

    pdf.section_title("2. Key Concepts")
    pdf.term_block("Shingle", "k consecutive words from a document. With k = 2, 'data science uses' gives 'data science' and 'science uses'.")
    pdf.term_block("Shingle set", "The set of shingles in a document. Repeated shingles are stored once.")
    pdf.term_block("Jaccard similarity", "Size of the intersection of two sets divided by the size of their union.")
    pdf.term_block("MinHash", "A short signature of a set. The probability that two signatures match equals the Jaccard similarity.")
    pdf.term_block("LSH", "An index that puts similar MinHash signatures in the same bucket, so a query skips most documents.")

    pdf.section_title("3. Formulae")
    pdf.math(r"J(A,B) = \frac{|A \cap B|}{|A \cup B|}")
    pdf.body("Example from this experiment: D1 and D2 share 8 shingles and their union has 12, so J = 8/12 = 0.667.")
    pdf.math(r"P[\mathrm{MinHash}(A) = \mathrm{MinHash}(B)] = J(A,B)")
    pdf.body("128 hash functions were used. The estimated scores were close to the exact scores: D1-D2 estimated 0.586 (exact 0.667) and D3-D4 estimated 0.781 (exact 0.833).")

    pdf.section_title("4. Documents and Jaccard scores (k = 2)")
    pdf.table(
        ["Pair", "Exact Jaccard", "MinHash estimate", "LSH at 0.5"],
        [
            ["D1-D2", "0.667", "0.586", "match"],
            ["D3-D4", "0.833", "0.781", "match"],
            ["D1-D3", "0.000", "0.000", "no match"],
            ["D1-D5", "0.000", "0.000", "no match"],
        ],
        [35, 40, 50, 40],
    )
    pdf.body("D1 and D2 are both about data science. D3 and D4 are both about a football match. D5 is a cooking sentence and matches nobody. At threshold 0.5, LSH returned D2 for D1, D4 for D3, and nothing for D5.")

    pdf.section_title("5. Exercise Answers")
    pdf.sub_title("Exercise 1: Jaccard of two documents")
    pdf.body("J(D1, D2) = 0.667. They differ only by large/big. J(D1, D5) = 0 because a data-science sentence and a cooking sentence share no 2-word shingle.")

    pdf.sub_title("Exercise 2: Change the shingle size")
    pdf.table(
        ["k", "D1-D2", "D3-D4", "D1-D3", "D1-D5"],
        [
            ["1", "0.818", "0.818", "0.000", "0.000"],
            ["2", "0.667", "0.833", "0.000", "0.000"],
            ["3", "0.636", "0.818", "0.000", "0.000"],
        ],
        [25, 35, 35, 35, 35],
    )
    pdf.body("A larger k is stricter. One changed word ('large' versus 'big', 'match' versus 'game') removes more overlapping shingles, so the score of the similar pairs falls. Unrelated pairs stay at 0.")

    pdf.sub_title("Exercise 3: Add a document and query LSH")
    pdf.body("D6 was 'data science uses statistics and machine learning to study large data'. Exact Jaccard: 0.667 with D1 and 0.538 with D2, and 0 with D3, D4, and D5. LSH at threshold 0.5 returned D1 and D2.")

    pdf.sub_title("Exercise 4: Different thresholds")
    pdf.body("At 0.3 and 0.5, D1 matched D2 and D6, and D3 matched D4. At 0.8 every query was empty. The MinHash estimates (0.586 and 0.781) are below 0.8, so the index missed D3-D4 even though the exact score is 0.833. LSH is an approximation, and the threshold must sit near the scores you care about.")

    pdf.sub_title("Exercise 5: Why LSH instead of comparing every pair")
    pdf.body("Comparing every pair takes about n squared set comparisons. MinHash stores a fixed-length signature, and LSH only checks documents that land in the same bucket. The six documents here are small enough to check exactly. The same index is what makes duplicate detection possible for a large collection.")

    pdf.add_page()
    pdf.section_title("6. Viva Questions")
    for q, a in [
        ("What is a shingle?", "k consecutive words. This experiment uses k = 2."),
        ("What is Jaccard similarity?", "Intersection size divided by union size. It is 1 when the sets are equal and 0 when they share nothing."),
        ("Why were D1 and D2 similar?", "They share 8 of 12 shingles. Only large/big differs. Score 0.667."),
        ("What is MinHash?", "A signature whose chance of matching equals the Jaccard similarity."),
        ("What does LSH return?", "Documents whose signatures fall in the same bucket as the query."),
        ("What happened at threshold 0.8?", "No matches. The estimates were below 0.8, so a high threshold can miss a similar pair."),
        ("Where is this used?", "Near-duplicate detection, plagiarism checks, and search."),
    ]:
        pdf.qa_block(q, a)

    out = Path("/Users/ojas/Desktop/DS Lab/Experiment10/Theory_and_Formulae.pdf")
    pdf.output(str(out))
    print("Wrote", out)


if __name__ == "__main__":
    generate()

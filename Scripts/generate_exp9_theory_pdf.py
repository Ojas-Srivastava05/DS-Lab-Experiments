"""Generate Experiment 9 theory PDF (text preprocessing and feature scaling)."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from pdf_math_utils import LabPDF


def generate():
    pdf = LabPDF("Experiment 9 - Text Preprocessing and Feature Scaling")
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.title_page(
        "Experiment 9",
        "Text Preprocessing and Feature Scaling Using Python",
        "Subject: Data Science Lab | Dataset: 5 sample sentences | Mapped CO(s): CO2",
    )

    pdf.section_title("1. Aim")
    pdf.body(
        "To preprocess text, convert it to numerical features with TF-IDF, "
        "and scale those features with normalization and standardization."
    )

    pdf.section_title("2. Key Concepts")
    pdf.term_block("Text preprocessing", "Cleaning raw text before a model sees it: lowercase, punctuation removal, tokenization, stop-word removal, then stemming or lemmatization.")
    pdf.term_block("Tokenization", "Splitting a sentence into words.")
    pdf.term_block("Stop words", "Common words such as the, and, and of. They are removed because they rarely help a model.")
    pdf.term_block("Stemming", "Chopping a word to a root, which may not be a real word. Porter stemmer: removes -> remov, characters -> charact.")
    pdf.term_block("Lemmatization", "Reducing a word to its dictionary form. removes -> remove, characters -> character.")
    pdf.term_block("Bag of Words", "A table of word counts. CountVectorizer builds it.")
    pdf.term_block("TF-IDF", "A weight that is high when a word is frequent in one document and rare in the others.")
    pdf.term_block("Normalization", "Min-Max scaling. Every feature is mapped to the range 0 to 1.")
    pdf.term_block("Standardization", "Z-score scaling. Every feature is shifted to mean 0 and standard deviation 1.")

    pdf.section_title("3. Formulae")
    pdf.sub_title("TF-IDF (scikit-learn)")
    pdf.math(r"\mathrm{tfidf}(t,d) = \mathrm{tf}(t,d) \times \mathrm{idf}(t)")
    pdf.math(r"\mathrm{idf}(t) = \ln \frac{1+n}{1+\mathrm{df}(t)} + 1")
    pdf.body("n is the number of documents. df(t) is the number of documents that contain term t. Each document vector is then divided by its length (L2 norm).")

    pdf.sub_title("Min-Max normalization")
    pdf.math(r"x' = \frac{x - x_{\min}}{x_{\max} - x_{\min}}")

    pdf.sub_title("Standardization")
    pdf.math(r"z = \frac{x - \mu}{\sigma}")

    pdf.section_title("4. What was done")
    for step in [
        "Loaded 5 sentences about text processing and machine learning.",
        "Lowercased the text, removed punctuation, tokenized, and removed 198 English stop words.",
        "Stemmed the remaining tokens with the Porter stemmer.",
        "Built a TF-IDF matrix of shape 5 documents by 29 features.",
        "Applied Min-Max scaling and standardization to that matrix.",
        "Repeated feature extraction with CountVectorizer and compared it with TF-IDF.",
        "Lemmatized the same tokens and compared them with the stems.",
        "Scaled a second table (Age, Income, Score) with both scalers.",
    ]:
        pdf.bullet(step)

    pdf.add_page()
    pdf.section_title("5. Exercise Answers")
    pdf.sub_title("Exercise 1: CountVectorizer")
    pdf.body("CountVectorizer on the stemmed sentences produced a 5 by 29 matrix of raw word counts. Every selected word in these sentences occurred once, so the displayed counts are 0 or 1.")

    pdf.sub_title("Exercise 2: TF-IDF versus CountVectorizer")
    pdf.body("Counts only say whether a word is present. TF-IDF gives a smaller weight to a word that appears in more than one document. In document 1, data has TF-IDF 0.379 while learn has 0.306, because data is the rarer of the two in this collection.")

    pdf.sub_title("Exercise 3: Lemmatization instead of stemming")
    pdf.table(
        ["Word", "Stem", "Lemma"],
        [
            ["removes", "remov", "remove"],
            ["characters", "charact", "character"],
            ["normalize", "normal", "normalize"],
            ["learning", "learn", "learn"],
            ["documents", "document", "document"],
        ],
        [50, 50, 50],
    )
    pdf.body("Stemming is faster and cruder. Lemmatization keeps a real word, so the features are easier to read.")

    pdf.sub_title("Exercise 4: Min-Max on another numerical dataset")
    pdf.body("Age, Income, and Score were scaled separately. Income values such as 20000 and 120000 became values between 0 and 1, on the same scale as Age and Score.")

    pdf.sub_title("Exercise 5: Normalization versus standardization")
    pdf.body("After Min-Max, each column has minimum 0 and maximum 1. After standardization, each column has mean 0 and standard deviation 1. Min-Max is used when a bounded range is needed. Standardization is used when a model assumes features are centered, as many distance-based models do.")

    pdf.section_title("6. Viva Questions")
    for q, a in [
        ("Why preprocess text?", "Raw text has capitals, punctuation, and words like the that do not help the model."),
        ("Stemming versus lemmatization?", "Stemming chops the word. Lemmatization returns the dictionary form."),
        ("What does TF-IDF measure?", "How important a word is in one document compared with the whole collection."),
        ("Why scale features?", "A column like Income would otherwise dominate a column like Age."),
        ("Min-Max versus standardization?", "Min-Max maps values to 0-1. Standardization maps them to mean 0 and standard deviation 1."),
        ("What did CountVectorizer produce?", "A bag-of-words count matrix for the same five sentences."),
    ]:
        pdf.qa_block(q, a)

    out = Path("/Users/ojas/Desktop/DS Lab/Experiment9/Theory_and_Formulae.pdf")
    pdf.output(str(out))
    print("Wrote", out)


if __name__ == "__main__":
    generate()

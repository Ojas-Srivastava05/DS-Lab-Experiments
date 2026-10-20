"""Build Experiment 9 notebook: text preprocessing and feature scaling."""

import nbformat as nbf
from pathlib import Path

nb = nbf.v4.new_notebook()
nb.metadata["kernelspec"] = {
    "display_name": "Python (DS Lab)",
    "language": "python",
    "name": "ds-lab",
}

def md(text):
    return nbf.v4.new_markdown_cell(text.strip() + "\n")

def code(text):
    return nbf.v4.new_code_cell(text.strip() + "\n")

cells = []

cells.append(md("""
# Experiment 9: Text Preprocessing and Feature Scaling Using Python

**Aim:** To perform text preprocessing, feature extraction, normalization, and feature scaling techniques for machine learning applications using Python.

**Mapped CO(s):** CO2
"""))

cells.append(md("## 1. Import Required Libraries"))
cells.append(code("""
import re

import matplotlib.pyplot as plt
import pandas as pd
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.preprocessing import MinMaxScaler, StandardScaler

pd.set_option("display.max_columns", 20)
pd.set_option("display.width", 120)
pd.set_option("display.max_colwidth", 80)
STOP_WORDS = set(stopwords.words("english"))
STEMMER = PorterStemmer()
LEMMATIZER = WordNetLemmatizer()
print("Libraries imported")
print("English stop words loaded:", len(STOP_WORDS))
"""))

cells.append(md("""
## 2. Load the Text Dataset

A small set of sentences is used so each preprocessing step can be checked by hand.
"""))
cells.append(code("""
texts = [
    "Machine learning models need clean and consistent text data.",
    "Text preprocessing removes punctuation, stop words, and special characters!",
    "Stemming and lemmatization normalize words before feature extraction.",
    "TF-IDF converts documents into numerical feature vectors.",
    "Feature scaling uses normalization and standardization for machine learning.",
]
df = pd.DataFrame({"Text": texts})
print("Dataset loaded successfully")
print("Shape:", df.shape)
df
"""))

cells.append(md("""
## 3. Text Preprocessing

Steps applied to every sentence:

1. Convert to lowercase.
2. Remove punctuation and special characters.
3. Tokenize on whitespace.
4. Remove stop words.
5. Stem the remaining tokens (Porter stemmer).
"""))
cells.append(code("""
def tokenize(text):
    cleaned = re.sub(r"[^a-z\\s]", " ", text.lower())
    return [token for token in cleaned.split() if token]


def normalize_tokens(tokens, method):
    if method == "stem":
        return [STEMMER.stem(token) for token in tokens]
    lemmas = []
    for token in tokens:
        verb = LEMMATIZER.lemmatize(token, pos="v")
        lemmas.append(LEMMATIZER.lemmatize(verb, pos="n"))
    return lemmas


def preprocess(text, method="stem"):
    tokens = [token for token in tokenize(text) if token not in STOP_WORDS]
    return normalize_tokens(tokens, method)


df["Tokens"] = df["Text"].apply(tokenize)
df["Without stop words"] = df["Tokens"].apply(lambda tokens: [t for t in tokens if t not in STOP_WORDS])
df["Stemmed"] = df["Without stop words"].apply(lambda tokens: normalize_tokens(tokens, "stem"))
df["Processed text"] = df["Stemmed"].apply(lambda tokens: " ".join(tokens))

print("Stop words removed and tokens stemmed")
df[["Text", "Without stop words", "Stemmed"]]
"""))

cells.append(md("""
## 4. TF-IDF Feature Extraction

TF-IDF turns each processed sentence into a numerical vector. A word that appears in many sentences gets a lower weight than a word that is concentrated in a few sentences.
"""))
cells.append(code("""
tfidf = TfidfVectorizer()
tfidf_matrix = tfidf.fit_transform(df["Processed text"])
tfidf_df = pd.DataFrame(
    tfidf_matrix.toarray().round(3),
    columns=tfidf.get_feature_names_out(),
    index=[f"Doc {i + 1}" for i in range(len(df))],
)
print("TF-IDF feature matrix generated")
print("Shape (documents, features):", tfidf_df.shape)
tfidf_df
"""))

cells.append(md("""
## 5. Normalize and Standardize the TF-IDF Features

- **Normalization (Min-Max):** scales each feature to the range 0 to 1.
- **Standardization (Z-score):** shifts each feature to mean 0 and standard deviation 1.
"""))
cells.append(code("""
minmax = MinMaxScaler()
standard = StandardScaler()
tfidf_minmax = pd.DataFrame(
    minmax.fit_transform(tfidf_df).round(3),
    columns=tfidf_df.columns,
    index=tfidf_df.index,
)
tfidf_standard = pd.DataFrame(
    standard.fit_transform(tfidf_df).round(3),
    columns=tfidf_df.columns,
    index=tfidf_df.index,
)
print("Min-Max scaled TF-IDF (values between 0 and 1)")
display(tfidf_minmax)
print("Standardized TF-IDF (mean about 0)")
display(tfidf_standard)
print("Min-Max range:", float(tfidf_minmax.min().min()), "to", float(tfidf_minmax.max().max()))
print("Standardized means (first 5 features):")
print(tfidf_standard.mean().round(3).head())
"""))

cells.append(md("""
---
## Exercises / Assignments
"""))

cells.append(md("### Exercise 1: Apply CountVectorizer to the same text dataset"))
cells.append(code("""
count_vectorizer = CountVectorizer()
count_matrix = count_vectorizer.fit_transform(df["Processed text"])
count_df = pd.DataFrame(
    count_matrix.toarray(),
    columns=count_vectorizer.get_feature_names_out(),
    index=tfidf_df.index,
)
print("CountVectorizer matrix (raw word counts)")
count_df
"""))

cells.append(md("### Exercise 2: Compare TF-IDF and CountVectorizer outputs"))
cells.append(code("""
shared_terms = ["learn", "data", "featur", "text", "normal"]
comparison = pd.DataFrame({
    "Count (Doc 1)": count_df.loc["Doc 1", shared_terms].values,
    "TF-IDF (Doc 1)": tfidf_df.loc["Doc 1", shared_terms].values,
    "Count (Doc 5)": count_df.loc["Doc 5", shared_terms].values,
    "TF-IDF (Doc 5)": tfidf_df.loc["Doc 5", shared_terms].values,
}, index=shared_terms)
print("CountVectorizer stores how often a word appears.")
print("TF-IDF down-weights words that appear in many documents, such as 'learn' and 'featur'.")
comparison
"""))

cells.append(md("### Exercise 3: Perform lemmatization instead of stemming"))
cells.append(code("""
sample_words = ["learning", "models", "removes", "characters", "normalize", "documents", "uses", "scaling"]
lemma_vs_stem = pd.DataFrame({
    "Word": sample_words,
    "Stem": [STEMMER.stem(word) for word in sample_words],
    "Lemma": [LEMMATIZER.lemmatize(LEMMATIZER.lemmatize(word, pos="v"), pos="n") for word in sample_words],
})
df["Lemmatized"] = df["Without stop words"].apply(lambda tokens: normalize_tokens(tokens, "lemma"))
print("Stemming chops words. Lemmatization returns a dictionary form.")
display(lemma_vs_stem)
print("Same sentences after lemmatization:")
df[["Stemmed", "Lemmatized"]]
"""))

cells.append(md("""
### Exercise 4: Apply Min-Max Scaling to another numerical dataset

Income is in the tens of thousands, while Age and Score are small numbers. Min-Max scaling puts every column on the same 0 to 1 range.
"""))
cells.append(code("""
numbers = pd.DataFrame({
    "Age": [18, 22, 35, 45, 60],
    "Income": [20000, 35000, 80000, 120000, 90000],
    "Score": [55, 70, 88, 92, 61],
})
numbers_minmax = pd.DataFrame(
    MinMaxScaler().fit_transform(numbers).round(3),
    columns=numbers.columns,
)
print("Original numerical dataset")
display(numbers)
print("After Min-Max scaling")
numbers_minmax
"""))

cells.append(md("""
### Exercise 5: Compare Normalization and Standardization results
"""))
cells.append(code("""
numbers_standard = pd.DataFrame(
    StandardScaler().fit_transform(numbers).round(3),
    columns=numbers.columns,
)
scaled_compare = pd.concat(
    {"Original": numbers, "Min-Max": numbers_minmax, "Standardized": numbers_standard},
    axis=1,
)
print("Min-Max keeps every value between 0 and 1. Standardization centers each column at 0.")
display(scaled_compare.round(3))
print("Column minimums and maximums")
print(pd.DataFrame({
    "Min-Max min": numbers_minmax.min(),
    "Min-Max max": numbers_minmax.max(),
    "Standard mean": numbers_standard.mean().round(3),
    "Standard std": numbers_standard.std(ddof=0).round(3),
}))

fig, axes = plt.subplots(1, 2, figsize=(10, 4))
numbers_minmax.plot(kind="bar", ax=axes[0], legend=False)
axes[0].set_title("Min-Max (0 to 1)")
axes[0].set_xlabel("Row")
numbers_standard.plot(kind="bar", ax=axes[1])
axes[1].set_title("Standardized (mean 0)")
axes[1].set_xlabel("Row")
axes[1].legend(loc="upper left")
fig.tight_layout()
plt.show()
"""))

cells.append(md("""
---
## Observation

- The five sentences were loaded and cleaned.
- Punctuation and stop words were removed, and the remaining words were stemmed.
- TF-IDF produced a numerical feature matrix.
- Min-Max scaling mapped those features to the range 0 to 1, and standardization centered them at mean 0.
- CountVectorizer kept raw counts. Lemmatization kept readable word forms where stemming chopped them.

## Result

Text preprocessing, TF-IDF feature extraction, normalization, and standardization were completed. The scaled numerical features are ready to be used by a machine learning model.

## Conclusion

Raw text is a poor input for most machine learning models. Cleaning, TF-IDF, and feature scaling turn that text into numbers on a comparable scale. Normalization is useful when a fixed 0 to 1 range is needed. Standardization is useful when features should share a mean of 0 and a standard deviation of 1.
"""))

nb.cells = cells
out = Path("/Users/ojas/Desktop/DS Lab/Experiment9/Notebook.ipynb")
nbf.write(nb, out)
print("Wrote", out)

# DS Lab

Organized Data Science Lab experiments (1-10).

## Folder Structure

```
DS Lab/
├── Experiment1/          Frequency, Probability & Correlation
│   ├── Assignment.pdf
│   ├── Notebook.ipynb
│   ├── U24AI028_Experiment1_Output.pdf
│   └── Theory_and_Formulae.pdf
├── Experiment2/          EDA, Descriptive Stats & Visualization
│   ├── Assignment.pdf
│   ├── Notebook.ipynb
│   ├── U24AI028_Experiment2_Output.pdf
│   └── Theory_and_Formulae.pdf
├── Experiment3/          PCA Dimensionality Reduction
│   ├── Assignment.pdf
│   ├── Notebook.ipynb
│   ├── U24AI028_Experiment3_Output.pdf
│   └── Theory_and_Formulae.pdf
├── Experiment4/          Statistical Hypothesis Testing
│   ├── Assignment.pdf
│   ├── Notebook.ipynb
│   ├── U24AI028_Experiment4_Output.pdf
│   └── Theory_and_Formulae.pdf
├── Experiment5/          Hadoop Installation, Configuration & HDFS
│   ├── Assignment.pdf
│   ├── Notebook.ipynb
│   ├── U24AI028_Experiment5_Output.pdf
│   ├── Theory_and_Formulae.pdf
│   └── local_files/      sample.txt, file1.txt, file2.txt
├── Experiment6/          Word Count using Hadoop MapReduce
│   ├── Assignment.pdf
│   ├── Notebook.ipynb
│   ├── U24AI028_Experiment6_Output.pdf
│   ├── Theory_and_Formulae.pdf
│   ├── src/WordCount.java
│   └── local_files/      input.txt, input_modified.txt, another.txt
├── Experiment7/          Data Processing & Analysis using Apache Pig
│   ├── Assignment.pdf
│   ├── Notebook.ipynb
│   ├── U24AI028_Experiment7_Output.pdf
│   ├── Theory_and_Formulae.pdf
│   └── src/              titanic_analysis.pig, exercises.pig
├── Experiment8/          Query Processing using Apache Hive
│   ├── Assignment.pdf
│   ├── Notebook.ipynb
│   ├── U24AI028_Experiment8_Output.pdf
│   ├── Theory_and_Formulae.pdf
│   └── src/              create_titanic.hql, exercises.hql
├── Experiment9/          Text Preprocessing and Feature Scaling
│   ├── Assignment.pdf
│   ├── Notebook.ipynb
│   ├── U24AI028_Experiment9_Output.pdf
│   └── Theory_and_Formulae.pdf
├── Experiment10/         Shingling and Locality Sensitive Hashing
│   ├── Assignment.pdf
│   ├── Notebook.ipynb
│   ├── U24AI028_Experiment10_Output.pdf
│   └── Theory_and_Formulae.pdf
├── Shared/
│   ├── Graphs_Types_and_Usages.pdf
│   ├── titanic.csv
│   ├── Titanic-Dataset.csv   (Kaggle version, used by Exp 7 & 8)
│   └── requirements.txt
├── Scripts/              PDF generators / helpers
└── .venv/                Python virtual environment
```

## How to Run

```bash
cd "DS Lab"
source .venv/bin/activate
# Open any Notebook.ipynb and Run All
# Or: jupyter nbconvert --execute --inplace Experiment5/Notebook.ipynb

Experiments 5-8 need Java 17 and Hadoop 3.4.1 at `/Users/ojas/hadoop-3.4.1`.
Experiment 7 needs Pig 0.18.0 at `/Users/ojas/pig-0.18.0`; Experiment 8 needs
Hive 4.2.1 at `/Users/ojas/apache-hive-4.2.1-bin` and Java 21 (`brew install openjdk@21`).
Install both with `Scripts/install_pig_hive.sh`.
Experiments 7 and 8 run HDFS on port 8020.
Experiments 9 and 10 need NLTK (stopwords and wordnet) and datasketch,
listed in Shared/requirements.txt.
```

## Export notebook PDFs (with outputs)

```bash
source .venv/bin/activate
python Scripts/export_notebooks_to_pdf.py
```

Creates `U24AI028_ExperimentN_Output.pdf` in each experiment folder, with a cover page (Ojas Srivastava, U24AI028).

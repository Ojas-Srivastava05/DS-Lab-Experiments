"""Generate Experiment 4 theory PDF and organize DS Lab into folders."""

from pathlib import Path
import shutil

from pdf_math_utils import LabPDF


def generate_exp4_theory():
    pdf = LabPDF("Experiment 4 - Hypothesis Testing Theory & Formulae")
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.title_page(
        "Experiment 4",
        "Statistical Hypothesis Testing Using Python",
        "Subject: Data Science Lab | Dataset: Titanic | Mapped CO(s): CO2",
    )

    pdf.section_title("1. Aim")
    pdf.body(
        "To perform statistical hypothesis testing on the Titanic dataset using Python "
        "and interpret the results using p-values."
    )

    pdf.section_title("2. Key Concepts & Definitions")
    pdf.term_block(
        "Hypothesis Testing",
        "A method to decide whether sample data provides enough evidence to support a claim about a population.",
    )
    pdf.term_block(
        "Null Hypothesis (H0)",
        "Assumes no significant difference or relationship. Example: mean ages are equal.",
    )
    pdf.term_block(
        "Alternative Hypothesis (H1)",
        "Assumes there is a significant difference or relationship. Example: mean ages differ.",
    )
    pdf.term_block(
        "Significance Level (alpha)",
        "Threshold for deciding significance. Commonly alpha = 0.05 (5%).",
        latex=r"\alpha = 0.05",
    )
    pdf.term_block(
        "p-value",
        "Probability of observing a result at least as extreme as the sample result, assuming H0 is true.",
    )
    pdf.term_block(
        "Decision Rule",
        "If p < alpha, reject H0. If p >= alpha, fail to reject H0.",
    )
    pdf.term_block(
        "Independent Sample t-test",
        "Compares means of two independent groups (e.g. survived vs not survived).",
    )
    pdf.term_block(
        "Chi-Square Test of Independence",
        "Tests association between two categorical variables (e.g. Sex vs Survived).",
    )

    pdf.section_title("3. Hypotheses for This Experiment (Age)")
    pdf.body("H0: Mean age of survived passengers = mean age of non-survived passengers")
    pdf.math(r"H_0:\; \mu_{\text{survived}} = \mu_{\text{not survived}}")
    pdf.body("H1: Mean ages are not equal")
    pdf.math(r"H_1:\; \mu_{\text{survived}} \neq \mu_{\text{not survived}}")

    pdf.add_page()
    pdf.section_title("4. Important Formulae")

    pdf.sub_title("(A) Two-sample t-statistic (unequal variances)")
    pdf.math(
        r"t = \frac{\bar{x}_1 - \bar{x}_2}"
        r"{\sqrt{\dfrac{s_1^2}{n_1} + \dfrac{s_2^2}{n_2}}}"
    )

    pdf.sub_title("(B) Decision rule")
    pdf.math(r"\text{Reject } H_0 \text{ if } p < \alpha")
    pdf.math(r"\text{Fail to reject } H_0 \text{ if } p \geq \alpha")

    pdf.sub_title("(C) Chi-square statistic")
    pdf.math(
        r"\chi^2 = \sum \frac{(O_{ij} - E_{ij})^2}{E_{ij}}"
    )
    pdf.body("O = observed frequency, E = expected frequency under independence.")

    pdf.section_title("5. Algorithm")
    for i, step in enumerate([
        "Import Pandas, NumPy, SciPy, Matplotlib, Seaborn",
        "Load Titanic dataset",
        "Select Age and Survived; drop missing ages",
        "Split into survived and not-survived groups",
        "Perform independent t-test (scipy.stats.ttest_ind)",
        "Compare p-value with alpha = 0.05 and conclude",
    ], 1):
        pdf.bullet(f"{i}. {step}")
    pdf.ln(1)

    pdf.section_title("6. Symbol Glossary")
    pdf.table(
        ["Symbol", "Meaning"],
        [
            ["H0", "Null hypothesis"],
            ["H1", "Alternative hypothesis"],
            ["alpha", "Significance level"],
            ["p", "p-value"],
            ["t", "t-statistic"],
            ["x-bar", "Sample mean"],
            ["s", "Sample standard deviation"],
            ["n", "Sample size"],
            ["chi^2", "Chi-square statistic"],
        ],
        [35, 120],
    )

    pdf.section_title("7. Viva Q&A")
    for q, a in [
        ("What is H0?", "Null hypothesis - assumes no significant difference."),
        ("What is p-value?", "Probability of extreme results under H0."),
        ("When do we reject H0?", "When p-value < alpha (usually 0.05)."),
        ("What is an independent t-test?", "Compares means of two independent groups."),
        ("What is a Chi-square test?", "Tests association between two categorical variables."),
    ]:
        pdf.qa_block(q, a)

    pdf.section_title("8. Conclusion")
    pdf.body(
        "Hypothesis testing was applied on Titanic Age (and Fare) using an independent t-test, "
        "and association between Sex and Survived was tested using Chi-square. Decisions were "
        "made by comparing p-values with the chosen significance level."
    )
    return pdf


def organize_lab(base: Path):
    """Create Experiment1-4 folders and move related files."""

    mapping = {
        "Experiment1": [
            ("Ds_Experiment1 (1).pdf", "Assignment.pdf"),
            ("Experiment1_Frequency_Probability_Correlation.ipynb", "Notebook.ipynb"),
            ("Experiment1_Theory_and_Formulae.pdf", "Theory_and_Formulae.pdf"),
        ],
        "Experiment2": [
            ("Ds_Experiment2 (1).pdf", "Assignment.pdf"),
            ("Experiment2_EDA_Descriptive_Visualization.ipynb", "Notebook.ipynb"),
            ("Experiment2_Theory_and_Formulae.pdf", "Theory_and_Formulae.pdf"),
        ],
        "Experiment3": [
            ("Ds_Experiment3 (1).pdf", "Assignment.pdf"),
            ("Experiment3_PCA_Dimensionality_Reduction.ipynb", "Notebook.ipynb"),
            ("Experiment3_Theory_and_Formulae.pdf", "Theory_and_Formulae.pdf"),
        ],
        "Experiment4": [
            ("DS_Experiment4.pdf", "Assignment.pdf"),
            ("Experiment4_Hypothesis_Testing.ipynb", "Notebook.ipynb"),
            ("Experiment4_Theory_and_Formulae.pdf", "Theory_and_Formulae.pdf"),
        ],
    }

    shared = base / "Shared"
    scripts = base / "Scripts"
    shared.mkdir(exist_ok=True)
    scripts.mkdir(exist_ok=True)

    for folder, files in mapping.items():
        dest_dir = base / folder
        dest_dir.mkdir(exist_ok=True)
        for src_name, dest_name in files:
            src = base / src_name
            dest = dest_dir / dest_name
            if src.exists():
                shutil.move(str(src), str(dest))
                print(f"Moved: {src_name} -> {folder}/{dest_name}")
            elif dest.exists():
                print(f"Already in place: {folder}/{dest_name}")
            else:
                print(f"Missing: {src_name}")

    # Shared resources
    shared_files = {
        "Graphs_Types_and_Usages.pdf": "Graphs_Types_and_Usages.pdf",
        "titanic.csv": "titanic.csv",
        "requirements.txt": "requirements.txt",
    }
    for src_name, dest_name in shared_files.items():
        src = base / src_name
        dest = shared / dest_name
        if src.exists():
            shutil.move(str(src), str(dest))
            print(f"Moved: {src_name} -> Shared/{dest_name}")

    # Scripts
    for src_name in [
        "generate_all_theory_pdfs.py",
        "generate_graphs_guide_pdf.py",
        "generate_pca_theory_pdf.py",
        "pdf_math_utils.py",
        "generate_exp4_and_organize.py",
    ]:
        src = base / src_name
        if src.exists():
            shutil.move(str(src), str(scripts / src_name))
            print(f"Moved: {src_name} -> Scripts/{src_name}")

    # outputs folder into Shared if present
    outputs = base / "outputs"
    if outputs.exists() and outputs.is_dir():
        dest = shared / "outputs"
        if dest.exists():
            shutil.rmtree(dest)
        shutil.move(str(outputs), str(dest))
        print("Moved: outputs -> Shared/outputs")

    # cleanup pycache
    pycache = base / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)
        print("Removed: __pycache__")

    # README
    readme = base / "README.md"
    readme.write_text(
        """# DS Lab

Organized Data Science Lab experiments (1-4).

## Folder Structure

```
DS Lab/
├── Experiment1/          Frequency, Probability & Correlation
│   ├── Assignment.pdf
│   ├── Notebook.ipynb
│   └── Theory_and_Formulae.pdf
├── Experiment2/          EDA, Descriptive Stats & Visualization
│   ├── Assignment.pdf
│   ├── Notebook.ipynb
│   └── Theory_and_Formulae.pdf
├── Experiment3/          PCA Dimensionality Reduction
│   ├── Assignment.pdf
│   ├── Notebook.ipynb
│   └── Theory_and_Formulae.pdf
├── Experiment4/          Statistical Hypothesis Testing
│   ├── Assignment.pdf
│   ├── Notebook.ipynb
│   └── Theory_and_Formulae.pdf
├── Shared/
│   ├── Graphs_Types_and_Usages.pdf
│   ├── titanic.csv
│   └── requirements.txt
├── Scripts/              PDF generators / helpers
└── .venv/                Python virtual environment
```

## How to Run

```bash
cd "DS Lab"
source .venv/bin/activate
# Open any Notebook.ipynb and Run All
# Or: jupyter nbconvert --execute --inplace Experiment4/Notebook.ipynb
```

Use kernel: Python from `.venv`.
""",
        encoding="utf-8",
    )
    print("Created: README.md")


def main():
    base = Path("/Users/ojas/Desktop/DS Lab")

    # Write Exp4 theory PDF into base first (before organize moves it)
    theory_path = base / "Experiment4_Theory_and_Formulae.pdf"
    generate_exp4_theory().output(str(theory_path))
    print(f"Created: {theory_path}")

    # Ensure requirements mentions scipy
    req = base / "requirements.txt"
    if req.exists():
        text = req.read_text()
        if "scipy" not in text:
            req.write_text(text.rstrip() + "\nscipy>=1.10\n")
    else:
        (base / "requirements.txt").write_text(
            "pandas>=2.0\nnumpy>=1.24\nmatplotlib>=3.7\nseaborn>=0.13\nscikit-learn>=1.3\nscipy>=1.10\n"
        )

    organize_lab(base)

    # Print final tree
    print("\n=== Final structure ===")
    for p in sorted(base.rglob("*")):
        if ".venv" in p.parts or "__pycache__" in p.parts:
            continue
        rel = p.relative_to(base)
        indent = "  " * (len(rel.parts) - 1)
        print(f"{indent}{rel.name}{'/' if p.is_dir() else ''}")


if __name__ == "__main__":
    main()

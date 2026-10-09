"""Generate theory PDFs with properly formatted mathematical equations."""

from pdf_math_utils import EXP1_FORMULAS, EXP2_FORMULAS, EXP3_FORMULAS, LabPDF


def generate_experiment1():
    F = EXP1_FORMULAS
    pdf = LabPDF("Experiment 1 - Frequency, Probability & Correlation")
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.title_page(
        "Experiment 1",
        "Frequency Analysis and Probability in Data Science Using Python",
        "Subject: Data Science Lab | Dataset: Titanic | Mapped CO(s): CO1, CO2",
    )

    pdf.section_title("1. Aim")
    pdf.body(
        "To perform frequency analysis, calculate probability measures, and analyze correlation "
        "using the Titanic dataset in Python."
    )

    pdf.section_title("2. Key Concepts & Definitions")

    pdf.term_block(
        "Frequency Analysis",
        "A statistical method to count how often each category or value appears in a dataset.",
        latex=F["abs_freq"],
    )
    pdf.term_block(
        "Relative Frequency",
        "The proportion (percentage) of observations in each category, where n = total observations.",
        latex=F["rel_freq"],
    )
    pdf.term_block(
        "Cumulative Frequency",
        "Running total of frequencies up to a given category.",
        latex=F["cum_freq"],
    )
    pdf.term_block(
        "Probability P(A)",
        "Measure of how likely an event is to occur, ranging from 0 (impossible) to 1 (certain).",
        latex=F["prob"],
    )
    pdf.term_block("Event", "A subset of outcomes from a sample space. Example: surviving the Titanic disaster.")
    pdf.term_block(
        "Sample Space (S)",
        "The set of all possible outcomes. Example: S = {Survived, Did Not Survive}.",
    )
    pdf.term_block(
        "Contingency Table",
        "A two-way table showing the frequency distribution of two categorical variables together.",
    )
    pdf.term_block(
        "Joint Probability",
        "Probability that two events A and B occur together.",
        latex=F["joint"],
    )
    pdf.term_block(
        "Marginal Probability",
        "Probability of a single event, ignoring other variables.",
        latex=F["marginal"],
    )
    pdf.term_block(
        "Conditional Probability",
        "Probability of event A given that event B has already occurred.",
        latex=F["conditional"],
    )
    pdf.term_block(
        "Variance Var(X)",
        "Measures how spread out a single variable is from its mean.",
        latex=F["variance"],
    )
    pdf.term_block(
        "Standard Deviation (sigma)",
        "Square root of variance. Same units as the original data.",
        latex=F["std"],
    )
    pdf.term_block(
        "Covariance Cov(X, Y)",
        "Measures the direction of linear relationship between two variables.",
        latex=F["covariance"],
    )
    pdf.body(
        "Interpretation: Cov(X,Y) > 0: variables increase together; "
        "Cov(X,Y) < 0: one increases as other decreases; Cov(X,Y) ~ 0: no linear trend."
    )
    pdf.term_block(
        "Correlation (r)",
        "Standardized covariance. Measures strength and direction of linear relationship (-1 to +1).",
        latex=F["correlation"],
    )
    pdf.term_block(
        "Covariance vs Correlation",
        "Covariance depends on units (unbounded). Correlation is unitless and always in [-1, +1].",
    )
    pdf.term_block(
        "Pearson Correlation Coefficient",
        "Most common measure of linear correlation between two numerical variables.",
        latex=F["pearson"],
    )

    pdf.add_page()
    pdf.section_title("3. Symbol Glossary")
    symbols = [
        ("n", "Total number of observations"),
        ("f_i", "Frequency of category i"),
        ("x_i, y_i", "i-th values of variables X and Y"),
        ("x-bar, y-bar", "Sample means of X and Y"),
        ("P(A)", "Probability of event A"),
        ("P(A cap B)", "Joint probability of A and B"),
        ("P(A | B)", "Conditional probability of A given B"),
        ("Var(X)", "Variance of X"),
        ("sigma", "Standard deviation"),
        ("Cov(X, Y)", "Covariance between X and Y"),
        ("r", "Pearson correlation coefficient"),
    ]
    pdf.table(["Symbol", "Meaning"], symbols, [40, 115])

    pdf.section_title("4. Important Formulae (Summary)")

    pdf.sub_title("(A) Mean")
    pdf.math(F["mean_x"])
    pdf.math(F["mean_y"])

    pdf.sub_title("(B) Absolute, Relative & Cumulative Frequency")
    pdf.math(F["abs_freq"])
    pdf.math(F["rel_freq"])
    pdf.math(F["cum_freq"])

    pdf.sub_title("(C) Probability Measures")
    pdf.math(F["joint"])
    pdf.math(F["marginal"])
    pdf.math(F["conditional"])

    pdf.sub_title("(D) Variance & Standard Deviation")
    pdf.math(F["variance"])
    pdf.math(F["std"])

    pdf.sub_title("(E) Covariance & Correlation")
    pdf.math(F["covariance"])
    pdf.math(F["correlation"])
    pdf.math(F["pearson"])

    pdf.sub_title("(F) Range of Pearson r")
    pdf.math(F["range_r"])
    pdf.bullet("r = +1 -> perfect positive correlation")
    pdf.bullet("r = -1 -> perfect negative correlation")
    pdf.bullet("r = 0 -> no linear relationship")
    pdf.ln(1)

    pdf.section_title("5. Algorithm")
    for i, step in enumerate([
        "Import Pandas, NumPy, Matplotlib, Seaborn",
        "Load Titanic dataset",
        "Create frequency table for passenger class",
        "Calculate absolute, relative, and cumulative frequencies",
        "Create contingency table: Sex vs Survived using pd.crosstab()",
        "Calculate joint, marginal, and conditional probabilities",
        "Select Age and Fare; handle missing values",
        "Compute Pearson correlation",
        "Plot heatmap, scatter plot, and stacked bar chart",
    ], 1):
        pdf.bullet(f"{i}. {step}")
    pdf.ln(1)

    pdf.section_title("6. Experimental Results")
    pdf.sub_title("Frequency Table -  Passenger Class")
    pdf.table(
        ["Class", "Absolute Freq", "Relative (%)", "Cumulative"],
        [["First", "216", "24.24", "216"], ["Second", "184", "20.65", "400"], ["Third", "491", "55.11", "891"]],
        [35, 40, 40, 40],
    )
    pdf.sub_title("Contingency Table -  Sex vs Survived")
    pdf.table(
        ["Sex", "Not Survived (0)", "Survived (1)", "Total"],
        [["female", "81", "233", "314"], ["male", "468", "109", "577"], ["All", "549", "342", "891"]],
        [30, 45, 40, 30],
    )
    pdf.sub_title("Joint Probability P(Sex and Survived)")
    pdf.table(
        ["Sex", "0", "1"],
        [["female", "0.0909", "0.2615"], ["male", "0.5253", "0.1223"]],
        [40, 40, 40],
    )
    pdf.sub_title("Conditional Probability P(Survived | Sex)")
    pdf.table(
        ["Sex", "Not Survived", "Survived"],
        [["female", "0.2580", "0.7420"], ["male", "0.8111", "0.1889"]],
        [40, 45, 45],
    )
    pdf.sub_title("Pearson Correlation -  Age vs Fare")
    pdf.bullet("r = 0.0961 -> very weak positive linear relationship")

    pdf.add_page()
    pdf.section_title("7. Exercise Answers")
    pdf.bullet("Frequency table for Embarked: absolute, relative, cumulative frequencies computed")
    pdf.bullet("P(Survived) = 0.3838 (38.38%)")
    pdf.bullet("Pearson r (Age, Fare) = 0.0961")
    pdf.bullet("Stacked bar chart: survival by passenger class plotted")
    pdf.ln(1)

    pdf.section_title("8. Viva Q&A")
    for q, a in [
        ("What is covariance?", "Measure of how two variables change together (see formula above)."),
        ("What is correlation?", "Standardized covariance: r = Cov(X,Y)/(sigma_X sigma_Y), range -1 to +1."),
        ("Difference between covariance and correlation?", "Covariance is unbounded and unit-dependent; correlation is standardized."),
        ("What is conditional probability?", "P(A|B) = P(A and B)/P(B) - probability of A given B occurred."),
        ("What does r = 0.0961 mean?", "Very weak positive linear correlation between Age and Fare."),
    ]:
        pdf.qa_block(q, a)

    pdf.section_title("9. Conclusion")
    pdf.body(
        "Frequency analysis, probability calculations, and correlation analysis were successfully "
        "performed on the Titanic dataset using Python."
    )
    return pdf


def generate_experiment2():
    F = EXP2_FORMULAS
    pdf = LabPDF("Experiment 2 - EDA, Descriptive Statistics & Visualization")
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.title_page(
        "Experiment 2",
        "Exploratory Data Analysis, Descriptive Statistics, and Data Visualization",
        "Subject: Data Science Lab | Dataset: Titanic | Mapped CO(s): CO1, CO2",
    )

    pdf.section_title("1. Aim")
    pdf.body("To perform EDA, descriptive statistical analysis, and data visualization on the Titanic dataset.")

    pdf.section_title("2. Key Concepts & Definitions")
    pdf.term_block("Exploratory Data Analysis (EDA)", "Examining data to understand structure, patterns, and missing values before modeling.")
    pdf.term_block("Mean (x-bar)", "Average value -  sum of all observations divided by count.", latex=F["mean"])
    pdf.term_block("Median", "Middle value when sorted. Robust to outliers.")
    pdf.term_block("Mode", "Most frequently occurring value.")
    pdf.term_block("Variance (s^2)", "Average squared deviation from the mean.", latex=F["variance"])
    pdf.term_block("Standard Deviation (sigma)", "Square root of variance.", latex=F["std"])
    pdf.term_block("Quartiles", "Q1 = 25th percentile, Q2 = median (50th), Q3 = 75th percentile.")
    pdf.term_block("Interquartile Range (IQR)", "Spread of the middle 50% of data.", latex=F["iqr"])
    pdf.term_block(
        "Outlier",
        "Extreme value far from the rest of the data.",
        latex=r"x < Q_1 - 1.5\,\mathrm{IQR} \quad \text{or} \quad x > Q_3 + 1.5\,\mathrm{IQR}",
    )
    pdf.term_block("Skewness", "Asymmetry of distribution. Right-skewed: mean > median.")
    pdf.term_block("Missing Value", "Empty/NaN entry. Must be identified before analysis.", latex=F["missing"])
    pdf.term_block("Covariance", "How two variables change together.", latex=F["covariance"])
    pdf.term_block("Correlation (r)", "Standardized linear relationship measure.", latex=F["correlation"])

    pdf.add_page()
    pdf.section_title("3. Symbol Glossary")
    pdf.table(
        ["Symbol", "Meaning"],
        [
            ("n", "Number of observations"),
            ("x_i", "i-th data value"),
            ("x-bar", "Sample mean"),
            ("s^2", "Sample variance"),
            ("sigma", "Standard deviation"),
            ("Q1, Q2, Q3", "First, second (median), third quartile"),
            ("IQR", "Interquartile range"),
            ("Cov(X,Y)", "Covariance"),
            ("r", "Pearson correlation"),
        ],
        [40, 115],
    )

    pdf.section_title("4. Important Formulae (Summary)")
    pdf.math(F["mean"])
    pdf.math(F["variance"])
    pdf.math(F["std"])
    pdf.math(F["iqr"])
    pdf.math(F["lower"])
    pdf.math(F["upper"])
    pdf.math(F["missing"])
    pdf.math(F["covariance"])
    pdf.math(F["correlation"])

    pdf.section_title("5. Algorithm")
    for i, step in enumerate([
        "Import libraries; load Titanic dataset",
        "Display head(), info(), dtypes; check missing values",
        "Generate describe(); plot bar charts, histograms, box plots",
        "Create scatter plot and correlation heatmap; interpret results",
    ], 1):
        pdf.bullet(f"{i}. {step}")
    pdf.ln(1)

    pdf.section_title("6. Experimental Results")
    pdf.bullet("Shape: (891, 15)")
    pdf.sub_title("Missing Values")
    pdf.table(
        ["Column", "Missing", "Missing %"],
        [["deck", "688", "77.22"], ["age", "177", "19.87"], ["embarked", "2", "0.22"]],
        [45, 45, 45],
    )
    pdf.sub_title("Descriptive Statistics")
    pdf.table(
        ["Variable", "Mean", "Std Dev", "Min", "Max"],
        [
            ["age", "29.70", "14.53", "0.42", "80.00"],
            ["fare", "32.20", "49.69", "0.00", "512.33"],
            ["sibsp", "0.52", "1.10", "0", "8"],
        ],
        [30, 30, 30, 25, 30],
    )
    pdf.sub_title("Outlier Analysis -  Fare")
    pdf.bullet("IQR = 23.09, Upper fence = 65.63, Outliers = 116")

    pdf.add_page()
    pdf.section_title("7. Visualizations")
    for name, desc in [
        ("Bar Chart", "Categorical distributions (sex, class, survived)"),
        ("Histogram", "Numerical distributions (Age, Fare)"),
        ("Box Plot", "Median, quartiles, outliers"),
        ("Heatmap", "Correlation matrix of numerical variables"),
    ]:
        pdf.bullet(f"{name}: {desc}")
    pdf.ln(1)

    pdf.section_title("8. Viva Q&A")
    for q, a in [
        ("What is variance?", "Var(X) = (1/(n-1)) sum of (x_i - x-bar)^2 - measures spread."),
        ("What is IQR?", "Q3 - Q1 - spread of the middle 50% of data."),
        ("What is covariance?", "Cov(X,Y) - measures co-movement of two variables (see formula)."),
        ("Mean vs median?", "Mean is average; median is middle value. Median is robust to outliers."),
    ]:
        pdf.qa_block(q, a)

    pdf.section_title("9. Conclusion")
    pdf.body("EDA and visualization successfully revealed structure, missing values, outliers, and relationships in the Titanic dataset.")
    return pdf


def generate_experiment3():
    F = EXP3_FORMULAS
    pdf = LabPDF("Experiment 3 - PCA Theory & Formulae")
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.title_page(
        "Experiment 3",
        "Dimensionality Reduction Using Principal Component Analysis (PCA)",
        "Subject: Data Science Lab | Dataset: Titanic | Mapped CO(s): CO2, CO4",
    )

    pdf.section_title("1. Aim")
    pdf.body("To perform dimensionality reduction using PCA on the Titanic dataset.")

    pdf.section_title("2. Key Concepts & Definitions")
    pdf.term_block("Dimensionality Reduction", "Reducing number of features while retaining important information.")
    pdf.term_block("PCA", "Transforms correlated variables into uncorrelated components preserving maximum variance.")
    pdf.term_block("Variance", "Measure of data spread.", latex=F["variance"])
    pdf.term_block("Covariance Cov(X,Y)", "How two variables change together.", latex=F["cov_pair"])
    pdf.term_block("Covariance Matrix C", "Matrix of pairwise covariances -  input to PCA.", latex=F["cov_matrix"])
    pdf.term_block("Standardization (Z-score)", "Scale to mean 0, std 1.", latex=F["zscore"])
    pdf.term_block("Eigenvalue (lambda)", "Variance captured by each principal component.")
    pdf.term_block("Eigenvector (v)", "Direction of a principal component.", latex=F["eigen"])
    pdf.term_block("Principal Component", "New uncorrelated variable.", latex=F["pc"])
    pdf.term_block("Loadings", "Feature weights (eigenvector components) showing PC composition.")
    pdf.term_block("Explained Variance Ratio", "Fraction of total variance per PC.", latex=F["evr"])
    pdf.term_block("Cumulative Explained Variance", "Total variance retained by first k PCs.", latex=F["cev"])
    pdf.term_block("Orthogonality", "PCs are uncorrelated.", latex=F["ortho"])

    pdf.add_page()
    pdf.section_title("3. Symbol Glossary")
    pdf.table(
        ["Symbol", "Meaning"],
        [
            ("X", "Standardized data matrix (n × p)"),
            ("n", "Number of samples (714)"),
            ("p", "Number of features (5)"),
            ("mu", "Population/sample mean"),
            ("sigma", "Standard deviation"),
            ("C", "Covariance matrix"),
            ("lambda", "Eigenvalue"),
            ("v", "Eigenvector"),
            ("W", "Matrix of eigenvectors"),
            ("Z", "Transformed PCA data"),
        ],
        [40, 115],
    )

    pdf.section_title("4. Important Formulae (Summary)")
    pdf.math(F["zscore"])
    pdf.math(F["cov_pair"])
    pdf.math(F["cov_matrix"])
    pdf.math(F["eigen"])
    pdf.math(F["transform"])
    pdf.math(F["pc"])
    pdf.math(F["evr"])
    pdf.math(F["cev"])
    pdf.math(F["ortho"])

    pdf.section_title("5. Algorithm")
    for i, step in enumerate([
        "Select numerical features; remove missing values",
        "Standardize with StandardScaler",
        "Compute covariance matrix; find eigenvalues/eigenvectors",
        "Transform data; compute explained variance; plot PC1 vs PC2",
    ], 1):
        pdf.bullet(f"{i}. {step}")
    pdf.ln(1)

    pdf.section_title("6. Experimental Results")
    pdf.bullet("714 rows, 5 features -> 2 PCs (67.10% variance retained)")
    pdf.table(
        ["PC", "Variance %", "Cumulative %"],
        [["PC1", "34.83", "34.83"], ["PC2", "32.27", "67.10"], ["PC3", "13.82", "80.92"]],
        [40, 45, 45],
    )
    pdf.sub_title("Feature Loadings")
    pdf.table(
        ["Feature", "PC1", "PC2"],
        [
            ["age", "-0.5459", "-0.1972"], ["fare", "-0.4201", "0.5267"],
            ["sibsp", "0.3115", "0.5399"], ["parch", "0.2058", "0.5630"], ["pclass", "0.6213", "-0.2743"],
        ],
        [35, 35, 35],
    )

    pdf.add_page()
    pdf.section_title("7. Viva Q&A")
    for q, a in [
        ("What is covariance matrix?", "C = (1/(n-1)) X^T X - matrix of all pairwise covariances."),
        ("What is an eigenvalue?", "lambda - variance along the corresponding PC direction."),
        ("Why standardize before PCA?", "So features with larger scales (e.g. fare) do not dominate."),
        ("What is explained variance ratio?", "EVR_k = lambda_k / sum(lambda_i) - fraction of total variance in PC_k."),
    ]:
        pdf.qa_block(q, a)

    pdf.section_title("8. Conclusion")
    pdf.body("PCA reduced 5 features to 2 components retaining 67.10% variance, simplifying visualization and analysis.")
    return pdf


def main():
    base = "/Users/ojas/Desktop/DS Lab"
    for name, gen in [
        ("Experiment1_Theory_and_Formulae.pdf", generate_experiment1),
        ("Experiment2_Theory_and_Formulae.pdf", generate_experiment2),
        ("Experiment3_Theory_and_Formulae.pdf", generate_experiment3),
    ]:
        path = f"{base}/{name}"
        gen().output(path)
        print(f"Created: {path}")


if __name__ == "__main__":
    main()

from fpdf import FPDF


class PCAPDF(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(80, 80, 80)
        self.cell(0, 8, "Experiment 3 - PCA Theory & Formulae", align="C", new_x="LMARGIN", new_y="NEXT")
        self.ln(1)

    def footer(self):
        self.set_y(-12)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(120, 120, 120)
        self.cell(0, 8, f"Page {self.page_no()}", align="C")

    def section_title(self, title):
        self.ln(2)
        self.set_font("Helvetica", "B", 13)
        self.set_text_color(20, 60, 120)
        self.multi_cell(0, 7, title)
        self.ln(1)

    def sub_title(self, title):
        self.ln(1)
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(40, 40, 40)
        self.multi_cell(0, 6, title)
        self.ln(0.5)

    def body(self, text):
        self.set_x(self.l_margin)
        self.set_font("Helvetica", "", 10)
        self.set_text_color(30, 30, 30)
        self.multi_cell(0, 5.5, text)
        self.ln(1)

    def formula(self, text):
        self.set_x(self.l_margin)
        self.set_font("Courier", "", 10)
        self.set_fill_color(245, 245, 245)
        self.multi_cell(0, 6, text, fill=True)
        self.ln(1)

    def bullet(self, text):
        self.set_x(self.l_margin)
        self.set_font("Helvetica", "", 10)
        self.set_text_color(30, 30, 30)
        self.multi_cell(0, 5.5, f"- {text}")


pdf = PCAPDF()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_page()

pdf.set_font("Helvetica", "B", 18)
pdf.set_text_color(20, 60, 120)
pdf.multi_cell(0, 10, "Experiment 3\nDimensionality Reduction Using PCA\nTheory, Formulae & Results")
pdf.ln(2)
pdf.set_font("Helvetica", "", 10)
pdf.set_text_color(60, 60, 60)
pdf.multi_cell(0, 5, "Subject: Data Science Lab | Dataset: Titanic | Mapped CO(s): CO2, CO4")

pdf.section_title("1. Aim")
pdf.body(
    "To perform dimensionality reduction using Principal Component Analysis (PCA) on the "
    "Titanic dataset using Python."
)

pdf.section_title("2. What is PCA?")
pdf.body(
    "Principal Component Analysis (PCA) is an unsupervised machine learning technique used "
    "for dimensionality reduction. It transforms a large set of correlated variables into a "
    "smaller set of new variables called Principal Components, while preserving as much "
    "variance (information) as possible."
)
pdf.bullet("First principal component (PC1) captures maximum variance.")
pdf.bullet("Each next component captures remaining variance and is orthogonal to previous ones.")
pdf.ln(1)
pdf.body("In this experiment:")
pdf.bullet("Before PCA: 5 features - age, fare, sibsp, parch, pclass")
pdf.bullet("After PCA: 2 (or 3) principal components")
pdf.bullet("Rows used: 714 (after removing missing age values from 891 rows)")

pdf.section_title("3. Important Terms")
terms = [
    ("Dimensionality Reduction", "Reducing number of features while keeping important information"),
    ("Variance", "Spread of data; PCA tries to preserve maximum variance"),
    ("Principal Component", "New axis/direction of maximum variance"),
    ("Eigenvalue (lambda)", "Variance along a principal component"),
    ("Eigenvector (v)", "Direction of a principal component"),
    ("Loadings", "Weights showing contribution of original features to each PC"),
    ("Explained Variance Ratio", "Percentage of total variance captured by one PC"),
    ("Standardization", "Scaling features to mean 0 and standard deviation 1"),
]
for term, meaning in terms:
    pdf.set_x(pdf.l_margin)
    pdf.set_font("Helvetica", "B", 10)
    pdf.multi_cell(0, 5.5, term)
    pdf.set_x(pdf.l_margin)
    pdf.set_font("Helvetica", "", 10)
    pdf.multi_cell(0, 5.5, meaning)
    pdf.ln(0.5)

pdf.section_title("4. All Important Formulae")

pdf.sub_title("(A) Data Matrix")
pdf.body("If there are n samples and p features:")
pdf.formula(
    "X = [x_ij]   where i = 1..n, j = 1..p\n"
    "In our experiment: n = 714, p = 5"
)

pdf.sub_title("(B) Mean of a Feature")
pdf.formula("mu_j = (1/n) * SUM(x_ij)   for i = 1 to n")

pdf.sub_title("(C) Standard Deviation")
pdf.formula("sigma_j = sqrt( (1/(n-1)) * SUM( (x_ij - mu_j)^2 ) )")

pdf.sub_title("(D) Standardization (Z-score) - StandardScaler")
pdf.formula("z_ij = (x_ij - mu_j) / sigma_j")
pdf.body(
    "Why standardize? Features like fare (0-500) and sibsp (0-8) have different scales. "
    "Without standardization, fare would dominate PCA."
)

pdf.sub_title("(E) Covariance Matrix")
pdf.formula("C = (1/(n-1)) * X^T * X")
pdf.body("Size: p x p (5 x 5 in our case). Shows how features vary together.")

pdf.sub_title("(F) Eigenvalue Equation (Core of PCA)")
pdf.formula("C * v = lambda * v")
pdf.body(
    "C = covariance matrix, lambda = eigenvalue (variance of PC), v = eigenvector (direction). "
    "Largest lambda gives PC1, second largest gives PC2, and so on."
)

pdf.sub_title("(G) Principal Component Transformation")
pdf.formula("Z = X * W")
pdf.body("X = standardized data, W = matrix of eigenvectors, Z = transformed PCA data.")
pdf.formula("PC_k = X * v_k")

pdf.sub_title("(H) Explained Variance Ratio")
pdf.formula("EVR_k = lambda_k / SUM(lambda_i)   for i = 1 to p")
pdf.body("Fraction of total variance captured by the k-th principal component.")

pdf.sub_title("(I) Cumulative Explained Variance")
pdf.formula("CEV_k = SUM(EVR_i)   for i = 1 to k")
pdf.body("Total variance retained when keeping the first k components.")

pdf.sub_title("(J) Total Variance")
pdf.formula("Total Variance = SUM(lambda_i) = trace(C)")

pdf.sub_title("(K) Loadings")
pdf.formula("Loading of feature j on PC_k = eigenvector component v_jk")
pdf.body("Higher absolute loading means stronger influence of that feature on the PC.")

pdf.sub_title("(L) Orthogonality")
pdf.formula("PC_i . PC_j = 0   for i != j")
pdf.body("Principal components are uncorrelated (orthogonal) to each other.")

pdf.add_page()
pdf.section_title("5. PCA Algorithm (Step-by-Step)")
steps = [
    "Import required libraries (Pandas, NumPy, Matplotlib, Seaborn, Scikit-learn)",
    "Load the Titanic dataset",
    "Select numerical features: age, fare, sibsp, parch, pclass",
    "Handle missing values (drop rows with NaN)",
    "Standardize data using StandardScaler",
    "Compute covariance matrix",
    "Find eigenvalues and eigenvectors",
    "Sort eigenvalues in descending order",
    "Select top k principal components",
    "Transform data: Z = X * W",
    "Calculate explained variance ratio",
    "Visualize principal components using scatter plot",
    "Interpret the results",
]
for i, step in enumerate(steps, 1):
    pdf.bullet(f"{i}. {step}")
pdf.ln(1)

pdf.section_title("6. Python Libraries Used")
libs = [
    ("pandas", "Load and handle data"),
    ("numpy", "Mathematical operations"),
    ("matplotlib / seaborn", "Visualization"),
    ("StandardScaler (sklearn)", "Feature standardization"),
    ("PCA (sklearn)", "Apply PCA"),
]
for lib, use in libs:
    pdf.set_x(pdf.l_margin)
    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(55, 6, lib)
    pdf.set_font("Helvetica", "", 10)
    pdf.multi_cell(0, 6, use)

pdf.section_title("7. Experimental Results (Titanic Dataset)")

pdf.sub_title("Preprocessing")
pdf.bullet("Original rows: 891")
pdf.bullet("After removing missing values: 714")
pdf.bullet("Features before PCA: 5")
pdf.bullet("Features after PCA (2 components): 2")
pdf.ln(1)

pdf.sub_title("Explained Variance - 2 Components")
pdf.set_font("Helvetica", "B", 10)
pdf.cell(45, 7, "Component", border=1)
pdf.cell(55, 7, "Explained Variance", border=1)
pdf.cell(55, 7, "Cumulative Variance", border=1, new_x="LMARGIN", new_y="NEXT")
pdf.set_font("Helvetica", "", 10)
for comp, ev, cv in [("PC1", "34.83%", "34.83%"), ("PC2", "32.27%", "67.10%")]:
    pdf.cell(45, 7, comp, border=1)
    pdf.cell(55, 7, ev, border=1)
    pdf.cell(55, 7, cv, border=1, new_x="LMARGIN", new_y="NEXT")
pdf.ln(2)

pdf.sub_title("Explained Variance - 3 Components")
pdf.set_font("Helvetica", "B", 10)
pdf.cell(45, 7, "Component", border=1)
pdf.cell(55, 7, "Explained Variance", border=1)
pdf.cell(55, 7, "Cumulative Variance", border=1, new_x="LMARGIN", new_y="NEXT")
pdf.set_font("Helvetica", "", 10)
for comp, ev, cv in [
    ("PC1", "34.83%", "34.83%"),
    ("PC2", "32.27%", "67.10%"),
    ("PC3", "13.82%", "80.92%"),
]:
    pdf.cell(45, 7, comp, border=1)
    pdf.cell(55, 7, ev, border=1)
    pdf.cell(55, 7, cv, border=1, new_x="LMARGIN", new_y="NEXT")
pdf.ln(2)

pdf.sub_title("Feature Loadings")
pdf.set_font("Helvetica", "B", 10)
pdf.cell(35, 7, "Feature", border=1)
pdf.cell(35, 7, "PC1", border=1)
pdf.cell(35, 7, "PC2", border=1, new_x="LMARGIN", new_y="NEXT")
pdf.set_font("Helvetica", "", 10)
loadings = [
    ("age", "-0.5459", "-0.1972"),
    ("fare", "-0.4201", "0.5267"),
    ("sibsp", "0.3115", "0.5399"),
    ("parch", "0.2058", "0.5630"),
    ("pclass", "0.6213", "-0.2743"),
]
for feat, pc1, pc2 in loadings:
    pdf.cell(35, 7, feat, border=1)
    pdf.cell(35, 7, pc1, border=1)
    pdf.cell(35, 7, pc2, border=1, new_x="LMARGIN", new_y="NEXT")
pdf.ln(2)

pdf.section_title("8. Interpretation of Principal Components")
pdf.sub_title("PC1 (34.83% variance)")
pdf.body(
    "Strongly influenced by pclass (+0.62) and age (-0.55). Separates passengers mainly "
    "by passenger class and age (socioeconomic / demographic pattern)."
)
pdf.sub_title("PC2 (32.27% variance)")
pdf.body(
    "Strongly influenced by parch (+0.56), sibsp (+0.54), and fare (+0.53). Reflects "
    "family structure (siblings, parents/children aboard) and ticket fare patterns."
)

pdf.section_title("9. Before vs After PCA")
pdf.set_font("Helvetica", "B", 10)
pdf.cell(45, 7, "Metric", border=1)
pdf.cell(45, 7, "Before PCA", border=1)
pdf.cell(45, 7, "After PCA", border=1, new_x="LMARGIN", new_y="NEXT")
pdf.set_font("Helvetica", "", 10)
comparison = [
    ("Rows", "714", "714"),
    ("Columns", "5", "2"),
    ("Missing values", "0", "0"),
    ("Feature correlation", "Present", "PCs uncorrelated"),
]
for metric, before, after in comparison:
    pdf.cell(45, 7, metric, border=1)
    pdf.cell(45, 7, before, border=1)
    pdf.cell(45, 7, after, border=1, new_x="LMARGIN", new_y="NEXT")
pdf.ln(2)

pdf.section_title("10. Benefits of PCA")
benefits = [
    "Reduces number of features",
    "Removes redundancy among correlated variables",
    "Improves data visualization (5D to 2D)",
    "Improves computational efficiency",
    "Prepares data for machine learning models",
    "Helps reduce noise",
]
for b in benefits:
    pdf.bullet(b)
pdf.ln(1)

pdf.section_title("11. Limitations of PCA")
limits = [
    "Principal components are harder to interpret than original features",
    "Assumes linear relationships between variables",
    "Sensitive to outliers",
    "Works only on numerical data",
    "Some information is lost during dimensionality reduction",
]
for l in limits:
    pdf.bullet(l)
pdf.ln(1)

pdf.add_page()
pdf.section_title("12. Exercise Answers")

pdf.sub_title("Exercise 1: PCA with 3 components")
pdf.body("Shape becomes (714, 3). Cumulative variance retained = 80.92%.")

pdf.sub_title("Exercise 2: Explained variance plot")
pdf.body(
    "Bar chart shows variance of each component. Line chart shows cumulative variance. "
    "Used to decide how many components to keep (often 90% rule)."
)

pdf.sub_title("Exercise 3: Compare before and after PCA")
pdf.body(
    "Same number of rows. Columns reduced from 5 to 2. Original features were correlated; "
    "PC1 and PC2 are uncorrelated."
)

pdf.sub_title("Exercise 4: Interpret first two PCs")
pdf.body("PC1 relates to class/age. PC2 relates to family size and fare.")

pdf.sub_title("Exercise 5: PCA on Iris dataset")
pdf.bullet("4 features reduced to 2 components")
pdf.bullet("PC1 explains 72.96%, PC2 explains 22.85%")
pdf.bullet("Total cumulative variance = 95.81%")
pdf.bullet("Species separate clearly in scatter plot")
pdf.ln(1)

pdf.section_title("13. One-Line Definitions (Viva)")
definitions = [
    ("PCA", "Technique to reduce dimensions while retaining maximum variance"),
    ("Principal Component", "New variable capturing maximum remaining variance"),
    ("Eigenvalue", "Variance along a principal component"),
    ("Eigenvector", "Direction of a principal component"),
    ("Explained Variance", "Percentage of total variance captured by a PC"),
    ("Standardization", "Converting data to mean 0 and standard deviation 1"),
    ("Loadings", "Contribution of original features to principal components"),
    ("Dimensionality Reduction", "Reducing number of input features"),
]
for term, defn in definitions:
    pdf.set_x(pdf.l_margin)
    pdf.set_font("Helvetica", "B", 10)
    pdf.multi_cell(0, 5.5, term + ":")
    pdf.set_x(pdf.l_margin)
    pdf.set_font("Helvetica", "", 10)
    pdf.multi_cell(0, 5.5, defn)
    pdf.ln(0.5)

pdf.section_title("14. Sample Viva Q&A")
qa = [
    (
        "Why did we use PCA?",
        "To reduce 5 numerical features to 2 components for easier visualization and analysis while retaining most variance.",
    ),
    (
        "Why standardize before PCA?",
        "Features have different scales; standardization ensures each feature contributes equally.",
    ),
    (
        "What does PC1 represent?",
        "Direction of maximum variance, mainly influenced by pclass and age.",
    ),
    (
        "How much information is retained?",
        "67.10% with 2 components, 80.92% with 3 components.",
    ),
    (
        "Are principal components correlated?",
        "No, they are orthogonal (uncorrelated).",
    ),
    (
        "What is the explained variance ratio formula?",
        "EVR_k = lambda_k / SUM(lambda_i)",
    ),
]
for q, a in qa:
    pdf.set_x(pdf.l_margin)
    pdf.set_font("Helvetica", "B", 10)
    pdf.multi_cell(0, 5.5, f"Q: {q}")
    pdf.set_x(pdf.l_margin)
    pdf.set_font("Helvetica", "", 10)
    pdf.multi_cell(0, 5.5, f"A: {a}")
    pdf.ln(1)

pdf.section_title("15. Conclusion")
pdf.body(
    "The experiment demonstrated how Principal Component Analysis (PCA) can effectively "
    "reduce the dimensionality of a dataset while retaining maximum variance. PCA simplifies "
    "data visualization, reduces computational complexity, and improves the efficiency of "
    "machine learning algorithms. On the Titanic dataset, 5 numerical features were reduced "
    "to 2 principal components while retaining 67.10% of the total variance."
)

output = "/Users/ojas/Desktop/DS Lab/Experiment3_PCA_Theory_and_Formulae.pdf"
pdf.output(output)
print(f"Created: {output}")

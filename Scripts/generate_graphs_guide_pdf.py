"""Generate PDF guide on types of graphs and their usages in Data Science Lab."""

from pdf_math_utils import LabPDF


GRAPHS = [
    {
        "name": "1. Bar Chart (Count Plot)",
        "what": "A chart with rectangular bars whose heights represent the frequency or count of each category.",
        "when": [
            "Compare counts across categories",
            "Show distribution of a categorical variable",
            "Compare groups (e.g. male vs female passengers)",
        ],
        "data": "Categorical variable (sex, class, survived, embarked)",
        "shows": "How many observations fall in each category",
        "python": "sns.countplot() / df.value_counts().plot(kind='bar')",
        "exp": "Exp 1, Exp 2",
        "example": "Count of passengers by class (First, Second, Third) or by sex",
    },
    {
        "name": "2. Stacked Bar Chart",
        "what": "A bar chart where each bar is divided into segments showing sub-category proportions.",
        "when": [
            "Compare composition of two categorical variables",
            "Show part-to-whole relationship within each group",
            "Compare survival rates across passenger classes",
        ],
        "data": "Two categorical variables (e.g. class + survived)",
        "shows": "How one categorical variable is distributed within levels of another",
        "python": "pd.crosstab(...).plot(kind='bar', stacked=True)",
        "exp": "Exp 1",
        "example": "Survival distribution by passenger class - survived vs not survived stacked",
    },
    {
        "name": "3. Histogram",
        "what": "A bar chart for numerical data showing frequency in continuous bins (intervals).",
        "when": [
            "Understand distribution of a numerical variable",
            "Check skewness (symmetric, left, or right skewed)",
            "Identify central tendency and spread of Age or Fare",
        ],
        "data": "Single numerical variable (age, fare)",
        "shows": "Shape of distribution - where most values cluster",
        "python": "sns.histplot() / plt.hist() with bins and optional KDE curve",
        "exp": "Exp 2",
        "example": "Histogram of Age showing peak around 20-30 years; Fare right-skewed",
    },
    {
        "name": "4. Box Plot (Box-and-Whisker Plot)",
        "what": "Shows median, quartiles (Q1, Q3), and outliers using a box and whiskers.",
        "when": [
            "Summarize numerical data in five numbers",
            "Detect outliers visually",
            "Compare distributions across groups",
        ],
        "data": "Numerical variable (fare, age); optionally grouped by category",
        "shows": "Median (line in box), IQR (box width), min/max whiskers, outlier points",
        "python": "sns.boxplot() / df.boxplot()",
        "exp": "Exp 2",
        "example": "Fare box plot - 116 outliers above upper fence; median << mean (right skew)",
    },
    {
        "name": "5. Scatter Plot",
        "what": "Plots individual data points using two numerical axes (x and y).",
        "when": [
            "Examine relationship between two numerical variables",
            "Detect correlation, clusters, or trends",
            "Visualize PCA results (PC1 vs PC2)",
        ],
        "data": "Two numerical variables (age vs fare, PC1 vs PC2)",
        "shows": "Pattern of co-variation; can color by a third variable (survival, species)",
        "python": "sns.scatterplot(x=..., y=..., hue=...)",
        "exp": "Exp 1, Exp 2, Exp 3",
        "example": "Age vs Fare (weak correlation); PC1 vs PC2 colored by survival",
    },
    {
        "name": "6. Heatmap (Correlation Heatmap)",
        "what": "Color-coded matrix where cell color intensity represents value magnitude.",
        "when": [
            "Show correlation between multiple numerical variables",
            "Identify strongly related feature pairs",
            "Visualize correlation matrix from df.corr()",
        ],
        "data": "Numerical variables - correlation matrix or contingency table",
        "shows": "Strength and direction of relationships (red=negative, blue=positive)",
        "python": "sns.heatmap(corr_matrix, annot=True, cmap='coolwarm')",
        "exp": "Exp 1, Exp 2, Exp 3",
        "example": "Correlation among age, fare, sibsp, parch, pclass; Age-Fare r=0.096",
    },
    {
        "name": "7. Line Chart",
        "what": "Connects data points with lines, usually over an ordered x-axis.",
        "when": [
            "Show trend over time or ordered categories",
            "Plot cumulative explained variance in PCA",
            "Display time series data",
        ],
        "data": "Ordered x (time, component number) and numerical y",
        "shows": "Trend, increase/decrease, rate of change",
        "python": "plt.plot() / sns.lineplot()",
        "exp": "Exp 3",
        "example": "Cumulative explained variance vs number of PCA components",
    },
    {
        "name": "8. Pie Chart",
        "what": "Circle divided into slices proportional to category frequencies.",
        "when": [
            "Show simple part-to-whole for few categories (2-5)",
            "Present percentage breakdown to non-technical audience",
        ],
        "data": "Single categorical variable",
        "shows": "Proportion of each category as a slice",
        "python": "plt.pie() - use sparingly; bar charts often clearer",
        "exp": "General (not primary in our labs)",
        "example": "Survived vs not survived as percentages - bar chart preferred in EDA",
    },
]


def graph_section(pdf, g):
    pdf.sub_title(g["name"])
    pdf.body(g["what"])
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(0, 5.5, "When to use:")
    pdf.set_font("Helvetica", "", 10)
    for item in g["when"]:
        pdf.bullet(item)
    pdf.ln(0.5)
    pdf.table(
        ["Aspect", "Detail"],
        [
            ["Data type", g["data"]],
            ["What it shows", g["shows"]],
            ["Python (Seaborn/Matplotlib)", g["python"]],
            ["Used in experiment", g["exp"]],
            ["Titanic example", g["example"]],
        ],
        [35, 120],
    )


def generate_graphs_pdf():
    pdf = LabPDF("Data Science Lab - Types of Graphs & Their Usages")
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.title_page(
        "Data Visualization Guide",
        "Types of Graphs and Their Usages",
        "Subject: Data Science Lab | Covers Experiments 1, 2 & 3 | Dataset: Titanic",
    )

    pdf.section_title("1. Introduction")
    pdf.body(
        "Data visualization converts numbers into pictures, making patterns, trends, outliers, "
        "and relationships easier to understand. Choosing the right graph depends on the type of "
        "variable (categorical vs numerical) and the question you want to answer."
    )
    pdf.table(
        ["Variable Type", "Best Graph Options"],
        [
            ["Categorical", "Bar chart, Count plot, Stacked bar, Pie chart"],
            ["Numerical (one variable)", "Histogram, Box plot"],
            ["Numerical (two variables)", "Scatter plot, Heatmap (correlation)"],
            ["Two categorical", "Stacked/grouped bar, Contingency heatmap"],
            ["Many numerical", "Correlation heatmap, PCA scatter"],
        ],
        [45, 110],
    )

    pdf.section_title("2. Types of Graphs (Detailed)")

    for g in GRAPHS[:4]:
        graph_section(pdf, g)

    pdf.add_page()
    for g in GRAPHS[4:]:
        graph_section(pdf, g)

    pdf.add_page()
    pdf.section_title("3. Quick Comparison Table")
    pdf.table(
        ["Graph", "Variables", "Main Purpose", "Experiment"],
        [
            ["Bar Chart", "1 categorical", "Compare category counts", "Exp 1, 2"],
            ["Stacked Bar", "2 categorical", "Composition within groups", "Exp 1"],
            ["Histogram", "1 numerical", "Show distribution shape", "Exp 2"],
            ["Box Plot", "1 numerical", "Median, IQR, outliers", "Exp 2"],
            ["Scatter Plot", "2 numerical", "Relationship between vars", "Exp 1, 2, 3"],
            ["Heatmap", "Many numerical", "Correlation matrix", "Exp 1, 2, 3"],
            ["Line Chart", "Ordered + numerical", "Trend over order/time", "Exp 3"],
            ["Pie Chart", "1 categorical", "Part-to-whole proportions", "General"],
        ],
        [30, 30, 55, 30],
    )

    pdf.section_title("4. How to Choose the Right Graph")
    pdf.bullet("Want counts of categories? -> Bar chart / Count plot")
    pdf.bullet("Want distribution of one number? -> Histogram or Box plot")
    pdf.bullet("Want relationship between two numbers? -> Scatter plot")
    pdf.bullet("Want correlation among many numbers? -> Heatmap")
    pdf.bullet("Want composition of two categories? -> Stacked bar chart")
    pdf.bullet("Want to detect outliers? -> Box plot")
    pdf.bullet("Want PCA / dimensionality reduction view? -> Scatter plot (PC1 vs PC2)")
    pdf.bullet("Want trend across ordered values? -> Line chart")
    pdf.ln(1)

    pdf.section_title("5. Graph Usage by Experiment")

    pdf.sub_title("Experiment 1 - Frequency, Probability & Correlation")
    pdf.bullet("Bar chart: absolute frequency of passenger class")
    pdf.bullet("Stacked bar chart: survival by class")
    pdf.bullet("Heatmap: correlation between Age and Fare")
    pdf.bullet("Scatter plot: Age vs Fare relationship")
    pdf.ln(1)

    pdf.sub_title("Experiment 2 - EDA & Descriptive Statistics")
    pdf.bullet("Bar chart: sex, class, survived counts")
    pdf.bullet("Histogram: Age and Fare distributions")
    pdf.bullet("Box plot: Fare outliers (116 above upper fence)")
    pdf.bullet("Scatter plot: Age vs Fare colored by survival")
    pdf.bullet("Heatmap: correlation of all numerical variables")
    pdf.ln(1)

    pdf.sub_title("Experiment 3 - PCA")
    pdf.bullet("Scatter plot: PC1 vs PC2 (2D visualization after reduction)")
    pdf.bullet("Bar chart: explained variance per component")
    pdf.bullet("Line chart: cumulative explained variance")
    pdf.ln(1)

    pdf.section_title("6. Box Plot - Key Elements")
    pdf.body("Understanding box plot components (important for viva):")
    pdf.table(
        ["Element", "Meaning"],
        [
            ["Box", "Middle 50% of data (Q1 to Q3)"],
            ["Line inside box", "Median (Q2)"],
            ["Whiskers", "Extend to 1.5 x IQR from Q1 and Q3"],
            ["Dots/points", "Outliers beyond whiskers"],
            ["IQR", "Q3 - Q1 (interquartile range)"],
        ],
        [40, 115],
    )

    pdf.section_title("7. Viva Q&A")
    qa = [
        ("When do you use a bar chart?", "To compare counts or frequencies of categorical variables."),
        ("Bar chart vs histogram?", "Bar = categories (discrete). Histogram = numerical bins (continuous)."),
        ("When do you use a box plot?", "To show median, quartiles, and detect outliers in numerical data."),
        ("When do you use a scatter plot?", "To examine relationship between two numerical variables."),
        ("When do you use a heatmap?", "To visualize correlation or values in a matrix form."),
        ("What is a stacked bar chart used for?", "To show how one categorical variable splits within another."),
        ("Which graph detects outliers?", "Box plot (points beyond 1.5 x IQR fences)."),
        ("Which graph shows distribution shape?", "Histogram (with optional KDE curve)."),
        ("Why use heatmap in correlation analysis?", "Quickly see which variable pairs are strongly correlated."),
        ("Which graph is used after PCA?", "Scatter plot of PC1 vs PC2 to visualize reduced dimensions."),
    ]
    for q, a in qa:
        pdf.qa_block(q, a)

    pdf.section_title("8. Conclusion")
    pdf.body(
        "Selecting the appropriate graph is essential for effective data analysis. Categorical data "
        "is best shown with bar charts; numerical distributions with histograms and box plots; "
        "relationships with scatter plots and heatmaps. Our three experiments use these visualizations "
        "on the Titanic dataset to explore frequencies, distributions, correlations, and PCA results."
    )

    return pdf


def main():
    path = "/Users/ojas/Desktop/DS Lab/Graphs_Types_and_Usages.pdf"
    generate_graphs_pdf().output(path)
    print(f"Created: {path}")


if __name__ == "__main__":
    main()

"""Generate Experiment 7 theory PDF (Apache Pig)."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from pdf_math_utils import LabPDF


def generate():
    pdf = LabPDF("Experiment 7 - Data Processing and Analysis Using Apache Pig")
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.title_page(
        "Experiment 7",
        "Data Processing and Analysis Using Apache Pig",
        "Subject: Data Science Lab | Environment: Hadoop 3.4.1 + Pig 0.18.0 | Mapped CO(s): CO2",
    )

    pdf.section_title("1. Aim")
    pdf.body(
        "To perform data processing and analysis on a dataset using Apache Pig and Pig Latin scripts."
    )

    pdf.section_title("2. Key Concepts")
    pdf.term_block(
        "Apache Pig",
        "High-level platform on Hadoop for analysing large datasets. Scripts are written in Pig Latin and compiled into MapReduce jobs.",
    )
    pdf.term_block(
        "Pig Latin",
        "Data-flow language. Each statement takes a relation and produces a new relation (LOAD -> FILTER -> GROUP -> STORE).",
    )
    pdf.term_block(
        "Relation / Bag / Tuple / Field",
        "A relation is a bag (collection) of tuples. A tuple is an ordered set of fields, like a row. A field is one value.",
    )
    pdf.term_block(
        "Grunt shell",
        "Pig's interactive shell. Scripts can also be run in batch mode: pig -x mapreduce script.pig.",
    )
    pdf.term_block(
        "Execution modes",
        "Local mode (-x local) reads the local file system in one JVM. MapReduce mode (-x mapreduce) reads HDFS and runs Hadoop jobs.",
    )
    pdf.term_block(
        "Lazy evaluation",
        "Pig only builds a plan until DUMP or STORE is reached. Then the whole plan is optimised and executed.",
    )
    pdf.term_block(
        "Piggybank / CSVExcelStorage",
        "Piggybank is Pig's library of user-contributed functions. CSVExcelStorage parses CSV files with quoted commas and can skip the header row.",
    )

    pdf.section_title("3. Pig Architecture")
    pdf.table(
        ["Component", "Role"],
        [
            ["Parser", "Checks syntax, builds the logical plan (DAG)"],
            ["Optimizer", "Rewrites plan, e.g. pushes FILTER early"],
            ["Compiler", "Turns plan into a chain of MapReduce jobs"],
            ["Execution engine", "Submits jobs to Hadoop, reads/writes HDFS"],
        ],
        [45, 135],
    )

    pdf.section_title("4. Pig Latin Operators")
    pdf.table(
        ["Operator", "Purpose", "Example"],
        [
            ["LOAD", "Read data", "LOAD 'f' USING PigStorage(',')"],
            ["DUMP", "Print relation", "DUMP t;"],
            ["DESCRIBE", "Show schema", "DESCRIBE t;"],
            ["FILTER", "Keep matching rows", "FILTER t BY Sex == 'female'"],
            ["FOREACH", "Transform rows", "FOREACH t GENERATE Name, Fare"],
            ["GROUP", "Group by key", "GROUP t BY Pclass"],
            ["COUNT/SUM/AVG", "Aggregate a bag", "COUNT(t)"],
            ["ORDER", "Sort", "ORDER t BY Fare DESC"],
            ["LIMIT", "First N rows", "LIMIT t 5"],
            ["STORE", "Save to HDFS", "STORE t INTO 'dir'"],
        ],
        [35, 50, 95],
    )

    pdf.add_page()
    pdf.section_title("5. Algorithm")
    steps = [
        "Start Hadoop and HDFS (NameNode, DataNode).",
        "Upload Titanic-Dataset.csv to /user/lab7/titanic in HDFS.",
        "Launch Pig in MapReduce mode: pig -x mapreduce script.pig.",
        "LOAD the CSV with a schema (PassengerId, Survived, Pclass, Name, Sex, Age, ...).",
        "DUMP the first records using LIMIT.",
        "FILTER records on a condition (Survived == 1, Sex == 'female').",
        "GROUP records by Pclass.",
        "COUNT passengers in each group with FOREACH ... GENERATE.",
        "ORDER the results.",
        "STORE the output in a new HDFS directory and verify with hdfs dfs -cat.",
    ]
    for i, step in enumerate(steps, 1):
        pdf.bullet(f"{i}. {step}")

    pdf.section_title("6. Core Script")
    for line in [
        "titanic = LOAD '/user/lab7/titanic/Titanic-Dataset.csv' USING CSVExcelStorage(...) AS (...);",
        "survivors = FILTER titanic BY Survived == 1;",
        "by_class = GROUP titanic BY Pclass;",
        "stats = FOREACH by_class GENERATE group AS Pclass, COUNT(titanic) AS passengers;",
        "sorted = ORDER stats BY passengers DESC;",
        "STORE sorted INTO '/user/lab7/output/class_stats' USING PigStorage(',');",
    ]:
        pdf.body(line)

    pdf.section_title("7. Results (Titanic, 891 passengers)")
    pdf.table(
        ["Pclass", "Passengers", "Survived", "Avg Fare", "Survival %"],
        [
            ["1", "216", "136", "84.15", "62.96"],
            ["2", "184", "87", "20.66", "47.28"],
            ["3", "491", "119", "13.68", "24.24"],
        ],
        [30, 38, 38, 37, 37],
    )
    pdf.body("Survivors (FILTER Survived == 1): 342. Female passengers: 314.")

    pdf.add_page()
    pdf.section_title("8. Exercise Answers")
    pdf.sub_title("Exercise 1: Filter only female passengers")
    pdf.body("females = FILTER titanic BY Sex == 'female';  -> 314 records.")
    pdf.sub_title("Exercise 2: Count passengers in each class")
    pdf.body("GROUP titanic BY Pclass; FOREACH ... GENERATE group, COUNT(titanic);  -> 1: 216, 2: 184, 3: 491.")
    pdf.sub_title("Exercise 3: Sort passengers by Fare (descending)")
    pdf.body(
        "ORDER fare_view BY Fare DESC;  -> highest fare 512.33 (Ward, Cardeza, Lesurer - all 1st class); "
        "lowest fares are 0.0."
    )
    pdf.sub_title("Exercise 4: Store output in a new HDFS directory")
    pdf.body(
        "STORE female_summary INTO '/user/lab7/exercises/ex4_female_summary' USING PigStorage(',');  "
        "The directory contains _SUCCESS and part-r-00000. Female survival: 1st 96.81%, 2nd 92.11%, 3rd 50.0%."
    )
    pdf.sub_title("Exercise 5: FILTER vs FOREACH")
    pdf.table(
        ["", "FILTER", "FOREACH ... GENERATE"],
        [
            ["Works on", "Rows (tuples)", "Columns (fields)"],
            ["Purpose", "Select rows by condition", "Transform / project each row"],
            ["Row count", "Same or fewer", "Same as input"],
            ["Columns", "All kept", "Chosen / computed"],
            ["SQL analogy", "WHERE", "SELECT list"],
            ["Example", "FILTER t BY Age > 70", "FOREACH t GENERATE Name, Fare*2"],
        ],
        [35, 70, 75],
    )
    pdf.body("Demo: FILTER Age > 70 gave 5 rows x 12 columns; FOREACH on that gave 5 rows x 4 new columns.")

    pdf.add_page()
    pdf.section_title("9. Viva Q&A")
    qa = [
        ("What is Apache Pig?", "A high-level data-flow platform on Hadoop that runs Pig Latin scripts as MapReduce jobs."),
        ("Why use Pig instead of Java MapReduce?", "Far fewer lines of code, built-in operators (JOIN, GROUP, ORDER), and automatic optimisation."),
        ("What is a relation in Pig?", "A bag of tuples, similar to a table, with an optional schema."),
        ("Difference between a bag and a tuple?", "A tuple is one ordered record; a bag is an unordered collection of tuples."),
        ("Local vs MapReduce mode?", "Local uses the local file system in one JVM; MapReduce uses HDFS and Hadoop jobs."),
        ("What does DUMP do?", "Executes the plan and prints a relation to the console."),
        ("DUMP vs STORE?", "DUMP prints to screen; STORE writes the relation into a file system directory."),
        ("What does GROUP produce?", "Tuples of (group, bag of matching tuples), e.g. (1, {all 1st-class rows})."),
        ("Why CSVExcelStorage?", "Names contain commas inside quotes; PigStorage(',') would split them incorrectly."),
        ("What is lazy evaluation in Pig?", "Statements only build a plan; nothing runs until DUMP or STORE."),
        ("What is a UDF?", "User Defined Function written in Java/Python to extend Pig with custom logic."),
        ("Pig vs Hive?", "Pig is a procedural data-flow language (good for ETL); Hive is declarative SQL (good for reporting)."),
        ("What is DESCRIBE?", "Shows the schema of a relation."),
        ("Can STORE overwrite an existing directory?", "No. The output directory must not exist, or the job fails."),
    ]
    for q, a in qa:
        pdf.qa_block(q, a)

    pdf.section_title("10. One-Line Definitions")
    for term, defn in [
        ("Pig Latin", "Data-flow scripting language of Apache Pig"),
        ("Relation", "Bag of tuples (Pig's table)"),
        ("Tuple", "Ordered set of fields (a row)"),
        ("Bag", "Collection of tuples"),
        ("Grunt", "Interactive Pig shell"),
        ("LOAD", "Reads data into a relation"),
        ("FILTER", "Selects rows by condition"),
        ("FOREACH", "Processes each row and generates fields"),
        ("GROUP", "Collects rows with the same key"),
        ("STORE", "Writes a relation to HDFS"),
    ]:
        pdf.term_block(term, defn)

    out = Path("/Users/ojas/Desktop/DS Lab/Experiment7/Theory_and_Formulae.pdf")
    pdf.output(str(out))
    print("Wrote", out)


if __name__ == "__main__":
    generate()

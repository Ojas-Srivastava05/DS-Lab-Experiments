"""Generate Experiment 8 theory PDF (Apache Hive)."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from pdf_math_utils import LabPDF


def generate():
    pdf = LabPDF("Experiment 8 - Query Processing Using Apache Hive")
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.title_page(
        "Experiment 8",
        "Query Processing on Large Datasets Using Apache Hive",
        "Subject: Data Science Lab | Environment: Hadoop 3.4.1 + Hive 4.2.1 | Mapped CO(s): CO2",
    )

    pdf.section_title("1. Aim")
    pdf.body("To perform SQL-like querying, aggregation, and analysis of large datasets using Apache Hive.")

    pdf.section_title("2. Key Concepts")
    pdf.term_block(
        "Apache Hive",
        "Open-source data warehouse on Hadoop. Users query HDFS data with HiveQL, and Hive turns queries into MapReduce/Tez/Spark jobs.",
    )
    pdf.term_block("HiveQL", "SQL-like query language of Hive (SELECT, WHERE, GROUP BY, ORDER BY, JOIN, ...).")
    pdf.term_block(
        "Metastore",
        "Database that stores table definitions (schema, location, SerDe). This lab uses an embedded Derby metastore.",
    )
    pdf.term_block(
        "Schema-on-read",
        "Data stays as files in HDFS; the schema is applied only when the data is read, not when it is loaded.",
    )
    pdf.term_block(
        "Managed vs External table",
        "Managed: Hive owns the data under /user/hive/warehouse and DROP deletes it. External: data stays at its own location; DROP removes only metadata.",
    )
    pdf.term_block(
        "SerDe",
        "Serializer/Deserializer that tells Hive how to read rows. OpenCSVSerde handles quoted CSV fields like \"Braund, Mr. Owen Harris\".",
    )
    pdf.term_block(
        "CTAS",
        "CREATE TABLE ... AS SELECT. Creates a new table from a query result (used here to build a typed ORC table).",
    )
    pdf.term_block("ORC", "Optimized Row Columnar file format: compressed, columnar, fast for analytical queries.")

    pdf.section_title("3. Hive Architecture")
    pdf.table(
        ["Component", "Role"],
        [
            ["Beeline / CLI", "Client that submits HiveQL"],
            ["HiveServer2", "JDBC/ODBC service that accepts queries"],
            ["Driver", "Compiler + optimizer + executor of queries"],
            ["Metastore", "Table schemas and HDFS locations"],
            ["Execution engine", "MapReduce (this lab), Tez, or Spark"],
            ["HDFS", "Stores the table data files"],
        ],
        [45, 135],
    )

    pdf.add_page()
    pdf.section_title("4. HiveQL Statements Used")
    pdf.table(
        ["Statement", "Purpose"],
        [
            ["CREATE DATABASE titanic_db", "Create a database"],
            ["CREATE TABLE ... ROW FORMAT SERDE", "Define a table and how rows are parsed"],
            ["LOAD DATA INPATH '...' INTO TABLE", "Move an HDFS file into a table"],
            ["CREATE TABLE t STORED AS ORC AS SELECT", "Build a typed table from a query"],
            ["SHOW DATABASES / SHOW TABLES", "List databases / tables"],
            ["DESCRIBE titanic", "Show table schema"],
            ["SELECT ... WHERE", "Filter rows"],
            ["GROUP BY + COUNT/AVG/SUM", "Aggregate per group"],
            ["ORDER BY ... DESC", "Sort results"],
            ["MAX() / MIN()", "Largest / smallest value"],
        ],
        [85, 95],
    )

    pdf.section_title("5. Algorithm")
    steps = [
        "Start HDFS (NameNode, DataNode) and upload Titanic-Dataset.csv to /user/lab8/titanic.",
        "Configure hive-site.xml (Derby metastore, warehouse dir, execution engine = mr).",
        "Initialise the metastore: schematool -dbType derby -initSchema.",
        "CREATE DATABASE titanic_db and a staging table using OpenCSVSerde.",
        "LOAD DATA INPATH the CSV into the staging table.",
        "CTAS into a typed ORC table titanic (INT/DOUBLE columns, empty strings -> NULL).",
        "Run SELECT, WHERE, GROUP BY, ORDER BY and aggregate queries with beeline.",
        "Analyse and verify the results.",
    ]
    for i, step in enumerate(steps, 1):
        pdf.bullet(f"{i}. {step}")

    pdf.section_title("6. Aggregation Formulas")
    pdf.math(r"AVG(fare) = \frac{1}{n}\sum_{i=1}^{n} fare_i")
    pdf.math(r"Survival\ \% = \frac{SUM(survived)}{COUNT(*)} \times 100 = AVG(survived) \times 100")
    pdf.body("AVG and other aggregate functions ignore NULL values (e.g. the 177 passengers without an age).")

    pdf.section_title("7. Results (Titanic, 891 passengers)")
    pdf.table(
        ["Pclass", "Passengers", "Survived", "Survival %", "Avg Age", "Avg Fare"],
        [
            ["1", "216", "136", "62.96", "38.23", "84.15"],
            ["2", "184", "87", "47.28", "29.88", "20.66"],
            ["3", "491", "119", "24.24", "25.14", "13.68"],
        ],
        [25, 32, 30, 32, 30, 31],
    )
    pdf.body("By sex: female 314 passengers, 74.20% survived; male 577 passengers, 18.89% survived.")

    pdf.add_page()
    pdf.section_title("8. Exercise Answers")
    pdf.sub_title("Exercise 1: Display only female passengers")
    pdf.body("SELECT passengerid, name, pclass, age, fare, survived FROM titanic WHERE sex = 'female';  -> 314 rows.")
    pdf.sub_title("Exercise 2: Average fare for each passenger class")
    pdf.body("SELECT pclass, ROUND(AVG(fare), 2) FROM titanic GROUP BY pclass;  -> 1: 84.15, 2: 20.66, 3: 13.68.")
    pdf.sub_title("Exercise 3: Number of passengers who survived")
    pdf.body("SELECT COUNT(*) FROM titanic WHERE survived = 1;  -> 342 (38.38%).")
    pdf.sub_title("Exercise 4: Sort passengers by age (descending)")
    pdf.body(
        "SELECT ... FROM titanic WHERE age IS NOT NULL ORDER BY age DESC;  -> 714 rows. "
        "Oldest: Barkworth, Mr. Algernon Henry Wilson (80). Youngest: 0.42 years."
    )
    pdf.sub_title("Exercise 5: Maximum and minimum fare")
    pdf.body("SELECT MAX(fare), MIN(fare) FROM titanic;  -> max 512.33 (3 passengers), min 0.0 (15 passengers).")

    pdf.section_title("9. Hive vs Pig vs RDBMS")
    pdf.table(
        ["", "Hive", "Pig", "RDBMS"],
        [
            ["Language", "HiveQL (declarative)", "Pig Latin (procedural)", "SQL"],
            ["Best for", "Reporting, BI", "ETL pipelines", "Transactions"],
            ["Schema", "On read", "Optional", "On write"],
            ["Latency", "High (batch)", "High (batch)", "Low"],
            ["Data size", "Petabytes", "Petabytes", "GB-TB"],
        ],
        [30, 50, 50, 50],
    )

    pdf.add_page()
    pdf.section_title("10. Viva Q&A")
    qa = [
        ("What is Apache Hive?", "A data warehouse system on Hadoop that lets you query HDFS data using SQL-like HiveQL."),
        ("What is the Hive Metastore?", "A database storing table metadata: column names, types, SerDe, and HDFS location."),
        ("What is schema-on-read?", "Hive applies the schema when reading data, so loading is just a file move."),
        ("Managed vs external table?", "DROP on a managed table deletes data; on an external table only the metadata is removed."),
        ("What does LOAD DATA INPATH do?", "Moves the HDFS file into the table's warehouse directory (no parsing)."),
        ("Why OpenCSVSerde?", "Names contain commas inside quotes; the default delimiter would split them."),
        ("Why was a WHERE clause used to drop the header?", "The MapReduce CTAS job did not apply skip.header.line.count, so the header row was filtered explicitly."),
        ("How does Hive execute a query?", "Driver parses and optimizes HiveQL, then runs it as MapReduce/Tez jobs."),
        ("Why are simple SELECT ... LIMIT queries fast?", "Hive uses a fetch task (reads files directly) without launching a MapReduce job."),
        ("ORDER BY vs SORT BY?", "ORDER BY gives a total order using one reducer; SORT BY sorts within each reducer only."),
        ("What is partitioning?", "Splitting a table into sub-directories by a column value (e.g. year) to skip unneeded data."),
        ("What is bucketing?", "Hashing rows into a fixed number of files by a column, useful for sampling and joins."),
        ("How do aggregates treat NULL?", "COUNT(col), AVG, SUM, MAX, MIN ignore NULLs; COUNT(*) counts all rows."),
        ("Is Hive suitable for OLTP?", "No. It is designed for batch analytics with high latency, not row-level transactions."),
    ]
    for q, a in qa:
        pdf.qa_block(q, a)

    pdf.section_title("11. One-Line Definitions")
    for term, defn in [
        ("Hive", "SQL-on-Hadoop data warehouse"),
        ("HiveQL", "Hive's SQL-like query language"),
        ("Metastore", "Catalog of table metadata"),
        ("Beeline", "JDBC command-line client for Hive"),
        ("HiveServer2", "Service that runs client queries"),
        ("SerDe", "Reads/writes rows in a file format"),
        ("Warehouse", "/user/hive/warehouse - default table location"),
        ("CTAS", "Create a table from a SELECT result"),
        ("Partition", "Sub-directory per column value"),
        ("Bucket", "Hash-based file split of a table"),
    ]:
        pdf.term_block(term, defn)

    out = Path("/Users/ojas/Desktop/DS Lab/Experiment8/Theory_and_Formulae.pdf")
    pdf.output(str(out))
    print("Wrote", out)


if __name__ == "__main__":
    generate()

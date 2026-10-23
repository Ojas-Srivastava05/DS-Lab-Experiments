"""Viva preparation PDF for Experiments 6, 7, and 8, following each experiment."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from pdf_math_utils import LabPDF


def generate():
    pdf = LabPDF("Viva Preparation - Experiments 6, 7, and 8")
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.title_page(
        "Viva Preparation",
        "Experiments 6, 7, and 8",
        "Data Science Lab | Questions follow each experiment | Ojas Srivastava, U24AI028",
    )

    pdf.section_title("Hadoop on this Mac (needed before Experiment 6)")
    pdf.sub_title("Install once")
    pdf.bullet("brew install openjdk@17")
    pdf.bullet("Download Hadoop 3.4.1 and extract it to /Users/ojas/hadoop-3.4.1")
    pdf.bullet("Keep it outside the DS Lab folder (the space in that path breaks Hadoop)")
    pdf.sub_title("Every time you open a terminal")
    pdf.bullet("export JAVA_HOME=/opt/homebrew/opt/openjdk@17/libexec/openjdk.jdk/Contents/Home")
    pdf.bullet("export HADOOP_HOME=/Users/ojas/hadoop-3.4.1")
    pdf.bullet('export PATH="$JAVA_HOME/bin:$HADOOP_HOME/bin:$HADOOP_HOME/sbin:$PATH"')
    pdf.bullet("Check with java -version and hadoop version")
    pdf.sub_title("Start HDFS")
    pdf.bullet("core-site.xml: fs.defaultFS = hdfs://localhost:9000")
    pdf.bullet("hdfs-site.xml: replication 1, NameNode and DataNode folders")
    pdf.bullet("hdfs namenode -format once per fresh run (this wipes HDFS)")
    pdf.bullet("hdfs --daemon start namenode")
    pdf.bullet("hdfs --daemon start datanode")
    pdf.bullet("Check with jps (NameNode, DataNode)")
    pdf.sub_title("Stop HDFS")
    pdf.bullet("hdfs --daemon stop datanode")
    pdf.bullet("hdfs --daemon stop namenode")

    # ----- Experiment 6 -----
    pdf.add_page()
    pdf.section_title("Experiment 6: Word Count using MapReduce")
    pdf.sub_title("Aim")
    pdf.body("Count how often each word appears in a text file, using a Hadoop MapReduce program.")
    pdf.sub_title("What you did")
    pdf.bullet("Started HDFS and uploaded input.txt to /user/lab6/input.")
    pdf.bullet("Wrote WordCount.java: a Mapper, a Reducer, and a Driver.")
    pdf.bullet("Compiled it with javac using the Hadoop classpath and packed it into wordcount.jar.")
    pdf.bullet("Ran: hadoop jar wordcount.jar WordCount <input> <output>")
    pdf.bullet("Read the result with hdfs dfs -cat <output>/part-r-00000")
    pdf.sub_title("What to say about the program")
    pdf.bullet("Mapper: reads one line, splits it into words, and emits (word, 1).")
    pdf.bullet("Shuffle and Sort: Hadoop groups every value for the same word and sends them to one Reducer.")
    pdf.bullet("Reducer: adds the 1s and writes (word, total).")
    pdf.bullet("The same Reducer is also the Combiner, so counts are added on the map side before data is sent across.")
    pdf.bullet("The Driver sets the Mapper, Reducer, input path, and output path, then submits the job.")
    pdf.sub_title("Result for input.txt")
    pdf.bullet("14 words, 10 unique. hadoop, big, data, and mapreduce appear twice. The rest appear once.")
    pdf.bullet("Output file: part-r-00000. _SUCCESS means the job finished.")
    pdf.bullet("The output folder must not already exist. Delete it with hdfs dfs -rm -r before running again.")

    pdf.sub_title("Exercises")
    pdf.qa_block(
        "1. Modify the input and observe the output.",
        "Two lines were added. Words went from 14 to 28, unique words from 10 to 18. hadoop went from 2 to 4.",
    )
    pdf.qa_block(
        "2. Ignore common words such as is, the, and a.",
        "Run with -D wordcount.skip.stopwords=true. The Mapper skips those words. Map output records dropped from 28 to 22.",
    )
    pdf.qa_block(
        "3. Run the program on another text file.",
        "another.txt gave 39 words and 29 unique. The same JAR works on any text file.",
    )
    pdf.qa_block(
        "4. Compare the output before and after changing the input.",
        "Some words stayed the same. hadoop, is, big, and data increased. New words appeared, such as hdfs, blocks, and scalable.",
    )
    pdf.qa_block(
        "5. Explain the Mapper and the Reducer.",
        "The Mapper emits (word, 1) for each word and does not count across lines. The Reducer adds those 1s to get the final count.",
    )

    pdf.sub_title("Questions from this experiment")
    for q, a in [
        ("What is MapReduce?", "A way to process data in parallel: Map produces (key, value) pairs, Reduce combines the values for each key."),
        ("What does the Mapper emit here?", "(word, 1) for every word."),
        ("What does the Reducer do?", "It sums the counts for one word and writes (word, total)."),
        ("What is the Combiner?", "A local reduce on the map side. It cuts down how much data is sent to the Reducer."),
        ("What is Shuffle and Sort?", "The step that groups values by key and sends each group to one Reducer."),
        ("Why Text and IntWritable?", "Hadoop needs these types to send data between machines."),
        ("What is part-r-00000?", "The file written by reducer number 0."),
        ("Where is the output stored?", "In HDFS, in the output directory you pass to the job."),
    ]:
        pdf.qa_block(q, a)

    # ----- Experiment 7 -----
    pdf.add_page()
    pdf.section_title("Experiment 7: Data processing with Apache Pig")
    pdf.sub_title("Aim")
    pdf.body("Analyze the Titanic dataset with Apache Pig. Pig Latin is turned into MapReduce jobs, so you do not write Java.")
    pdf.sub_title("Dataset")
    pdf.body("Titanic-Dataset.csv, 891 passengers. Columns used: Survived, Pclass, Sex, Age, Fare, Embarked.")
    pdf.sub_title("What you did")
    pdf.bullet("Started HDFS and uploaded the CSV to /user/lab7/titanic.")
    pdf.bullet("Ran the script in MapReduce mode: pig -x mapreduce script.pig")
    pdf.bullet("LOAD the file, FILTER survivors, GROUP by Pclass, COUNT passengers, ORDER the result, STORE it in HDFS.")
    pdf.sub_title("Operators in the script")
    pdf.bullet("LOAD: read the CSV into a relation. CSVExcelStorage is used because names contain commas inside quotes.")
    pdf.bullet("DUMP: print a relation. STORE: save it to an HDFS directory.")
    pdf.bullet("FILTER: keep rows that match a condition.")
    pdf.bullet("GROUP: collect rows that share a key, for example the same Pclass.")
    pdf.bullet("FOREACH: produce new fields, such as the count and the average fare.")
    pdf.bullet("ORDER: sort the result.")
    pdf.sub_title("Result")
    pdf.table(
        ["Pclass", "Passengers", "Survived", "Avg fare", "Survival %"],
        [
            ["1", "216", "136", "84.15", "62.96"],
            ["2", "184", "87", "20.66", "47.28"],
            ["3", "491", "119", "13.68", "24.24"],
        ],
        [30, 38, 36, 38, 38],
    )
    pdf.body("Survivors: 342. Female passengers: 314.")

    pdf.sub_title("Exercises")
    pdf.qa_block(
        "1. Filter only female passengers.",
        "FILTER titanic BY Sex == 'female'. Result: 314 rows.",
    )
    pdf.qa_block(
        "2. Count passengers in each class.",
        "GROUP by Pclass, then COUNT. Class 1: 216, class 2: 184, class 3: 491.",
    )
    pdf.qa_block(
        "3. Sort passengers by Fare, descending.",
        "ORDER BY Fare DESC. Highest fare is 512.33. Lowest fares are 0.0.",
    )
    pdf.qa_block(
        "4. Store the output in a new HDFS directory.",
        "STORE ... INTO '/user/lab7/exercises/ex4_female_summary'. The directory has part-r-00000 and _SUCCESS. Female survival: 1st class 96.81%, 2nd 92.11%, 3rd 50%.",
    )
    pdf.qa_block(
        "5. Difference between FILTER and FOREACH.",
        "FILTER keeps or drops rows. FOREACH changes the columns of each row. Age > 70 kept 5 rows. FOREACH on those rows kept 5 rows but only 4 columns.",
    )

    pdf.sub_title("Questions from this experiment")
    for q, a in [
        ("What is Apache Pig?", "A tool on Hadoop. You write Pig Latin, and Pig runs it as MapReduce jobs."),
        ("Why use Pig instead of Java MapReduce?", "The same work takes a few lines. FILTER, GROUP, and ORDER are built in."),
        ("What is a relation?", "Pig's table: a collection of rows (tuples)."),
        ("Local mode versus MapReduce mode?", "Local mode reads the local disk. MapReduce mode reads HDFS and runs Hadoop jobs. This experiment uses MapReduce mode."),
        ("DUMP versus STORE?", "DUMP prints on the screen. STORE writes a directory in HDFS."),
        ("What is lazy evaluation?", "Nothing runs until DUMP or STORE. The earlier lines only build a plan."),
        ("Why CSVExcelStorage?", "Passenger names contain commas inside quotes. A plain comma split would break those names."),
    ]:
        pdf.qa_block(q, a)

    # ----- Experiment 8 -----
    pdf.add_page()
    pdf.section_title("Experiment 8: Query processing with Apache Hive")
    pdf.sub_title("Aim")
    pdf.body("Query the Titanic dataset with HiveQL, which is similar to SQL. Hive turns the queries into MapReduce jobs.")
    pdf.sub_title("Dataset")
    pdf.body("Same Titanic file, 891 passengers, loaded from HDFS.")
    pdf.sub_title("What you did")
    pdf.bullet("Started HDFS and uploaded Titanic-Dataset.csv to /user/lab8/titanic.")
    pdf.bullet("Created the database titanic_db.")
    pdf.bullet("Created a staging table titanic_raw and loaded the CSV with LOAD DATA INPATH.")
    pdf.bullet("Created a typed table titanic from that data and ran SELECT queries in Beeline.")
    pdf.sub_title("What to say about the tables")
    pdf.bullet("titanic_raw reads the CSV. OpenCSVSerde keeps commas that sit inside quoted names.")
    pdf.bullet("titanic is the table used for analysis. Age and Fare are numbers, so AVG and MAX work.")
    pdf.bullet("LOAD DATA only moves the file into the table. Hive applies the column types when the query runs.")
    pdf.sub_title("Result")
    pdf.bullet("Same class counts as Pig: 216, 184, and 491 passengers.")
    pdf.bullet("Females: 314 passengers, 74.20% survived. Males: 577 passengers, 18.89% survived.")
    pdf.bullet("Survivors: 342 (38.38%).")
    pdf.bullet("Oldest: Barkworth, age 80. Youngest: 0.42 years. 177 passengers have no age.")
    pdf.bullet("Highest fare 512.33. Lowest fare 0.0.")

    pdf.sub_title("Exercises")
    pdf.qa_block(
        "1. Display only female passengers.",
        "SELECT ... FROM titanic WHERE sex = 'female'. Result: 314 rows.",
    )
    pdf.qa_block(
        "2. Average fare for each passenger class.",
        "SELECT pclass, AVG(fare) FROM titanic GROUP BY pclass. Class 1: 84.15, class 2: 20.66, class 3: 13.68.",
    )
    pdf.qa_block(
        "3. Count passengers who survived.",
        "SELECT COUNT(*) FROM titanic WHERE survived = 1. Result: 342.",
    )
    pdf.qa_block(
        "4. Sort passengers by age, descending.",
        "SELECT ... FROM titanic WHERE age IS NOT NULL ORDER BY age DESC. 714 rows. Oldest is 80.",
    )
    pdf.qa_block(
        "5. Maximum and minimum fare.",
        "SELECT MAX(fare), MIN(fare) FROM titanic. Maximum 512.33, minimum 0.0.",
    )

    pdf.sub_title("Questions from this experiment")
    for q, a in [
        ("What is Apache Hive?", "A data warehouse on Hadoop. You query HDFS data with SQL-like HiveQL."),
        ("What is the metastore?", "The place Hive stores table names, column types, and the HDFS location of the data. This lab uses Derby."),
        ("What does LOAD DATA INPATH do?", "It moves the file from HDFS into the table. It does not parse the file."),
        ("Why OpenCSVSerde?", "Names contain commas inside quotes. The default comma split would break them."),
        ("Managed versus external table?", "Dropping a managed table deletes the data. Dropping an external table removes only the table definition."),
        ("How does a query run?", "Hive turns HiveQL into a MapReduce job and runs it on Hadoop."),
        ("Pig versus Hive, from these two experiments?", "Pig scripts list the steps (LOAD, FILTER, GROUP, STORE). Hive queries say what you want (SELECT, WHERE, GROUP BY). Both run on Hadoop."),
    ]:
        pdf.qa_block(q, a)

    out = Path("/Users/ojas/Desktop/DS Lab/Viva_Experiments_6_7_8.pdf")
    pdf.output(str(out))
    print("Wrote", out)


if __name__ == "__main__":
    generate()

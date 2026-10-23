"""Centralized viva PDF for Experiments 4, 5, and 6."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from pdf_math_utils import LabPDF


def generate():
    pdf = LabPDF("Viva Preparation - Experiments 4, 5, and 6")
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.title_page(
        "Viva Preparation",
        "Experiments 4, 5, and 6",
        "Data Science Lab | Hypothesis testing, HDFS, MapReduce Word Count | Ojas Srivastava, U24AI028",
    )

    pdf.section_title("How to answer")
    pdf.body(
        "State the aim, what you did on the Titanic or Hadoop setup, your numbers or command, then the conclusion. "
        "For statistics: H0, H1, test used, p-value, alpha = 0.05, reject or fail to reject."
    )

    # ----- Experiment 4 -----
    pdf.add_page()
    pdf.section_title("Experiment 4: Statistical hypothesis testing")
    pdf.sub_title("Aim")
    pdf.body("Test claims about the Titanic data using Python and decide with p-values (alpha = 0.05).")
    pdf.sub_title("Dataset")
    pdf.body("Titanic, 891 passengers. Main variables: Age, Fare, Survived, Sex. Rows with missing Age were dropped for the age test.")

    pdf.sub_title("Key ideas")
    pdf.bullet("H0: no difference / no association. H1: there is a difference or association.")
    pdf.bullet("p-value: how surprising your result is if H0 is true. If p < 0.05, reject H0.")
    pdf.bullet("Independent t-test: compare means of two groups (survived vs not survived). Use when spread in the population is unknown; use sample s (Welch t-test, equal_var=False in SciPy).")
    pdf.bullet("Chi-square: test link between two categories (Sex vs Survived).")
    pdf.bullet("t-test vs z-test: unknown variance and small/medium sample -> t. Known population variance or large-n normal approximation -> z. This lab uses t.")

    pdf.sub_title("Main result (Age)")
    pdf.bullet("H0: mean age same for survived and not survived. H1: means differ.")
    pdf.bullet("Test: scipy.stats.ttest_ind(..., equal_var=False)")
    pdf.bullet("p-value = 0.041 (< 0.05) -> Reject H0.")
    pdf.bullet("Conclusion: mean age differs significantly between survived and not-survived passengers.")

    pdf.sub_title("Other results from the notebook")
    pdf.bullet("Fare t-test: p about 2.7e-11 -> reject H0; mean fare differs by survival.")
    pdf.bullet("Sex vs Survived chi-square: chi2 about 260.7, p about 1.2e-58 -> reject H0; sex and survival are associated.")

    pdf.sub_title("Exercises")
    pdf.qa_block("1. t-test on Fare instead of Age.", "Same two groups. Fare p-value is very small; reject H0. Survivors paid higher fares on average.")
    pdf.qa_block("2. Change alpha from 0.05 to 0.01 (Age test).", "p = 0.041. Still reject at 0.05; fail to reject at 0.01 (0.041 is not < 0.01).")
    pdf.qa_block("3. Interpret the p-value.", "Probability of a difference at least this large if H0 were true. Small p -> evidence against H0.")
    pdf.qa_block("4. Chi-square on Sex vs Survived.", "Build a contingency table; stats.chi2_contingency. Strong association; reject independence.")
    pdf.qa_block("5. Hypotheses for Fare.", "H0: equal mean fare. H1: unequal mean fare. Same as exercise 1.")

    pdf.sub_title("Viva questions")
    for q, a in [
        ("What is H0?", "No significant difference or no association."),
        ("When reject H0?", "When p-value < alpha (here 0.05)."),
        ("What is alpha?", "Significance level; risk of false alarm. Usually 0.05."),
        ("Independent t-test?", "Compares means of two separate groups."),
        ("Chi-square test?", "Checks if two categorical variables are independent."),
        ("What library?", "SciPy stats: ttest_ind, chi2_contingency."),
    ]:
        pdf.qa_block(q, a)

    # ----- Experiment 5 -----
    pdf.add_page()
    pdf.section_title("Experiment 5: Hadoop and HDFS")
    pdf.sub_title("Aim")
    pdf.body("Install/configure Hadoop on one machine and run basic HDFS file commands.")
    pdf.sub_title("Components")
    pdf.bullet("HDFS stores data in blocks on DataNodes. NameNode holds metadata only.")
    pdf.bullet("YARN schedules jobs. MapReduce processes data (used in Exp 6).")
    pdf.bullet("Single-node lab: replication = 1. fs.defaultFS = hdfs://localhost:9000")

    pdf.sub_title("Hadoop on this Mac")
    pdf.bullet("Java 17: brew install openjdk@17")
    pdf.bullet("Hadoop 3.4.1 at /Users/ojas/hadoop-3.4.1 (not inside DS Lab folder)")
    pdf.bullet("Each new terminal: export JAVA_HOME, HADOOP_HOME, PATH (see Hadoop_Download_Steps.pdf)")
    pdf.bullet("Format once per fresh run: hdfs namenode -format")
    pdf.bullet("Start: hdfs --daemon start namenode; hdfs --daemon start datanode")
    pdf.bullet("Check: jps shows NameNode and DataNode; hdfs dfsadmin -report shows live DataNodes")

    pdf.sub_title("Linux vs Hadoop commands")
    pdf.body(
        "ls, mkdir, cat, cp, rm on your Mac disk are normal shell commands. "
        "hdfs dfs -ls, -mkdir, -cat, -cp, -rm work on HDFS. "
        "put uploads local to HDFS; get downloads HDFS to local. "
        "cp is source first, then destination."
    )

    pdf.sub_title("Commands to remember")
    pdf.table(
        ["Command", "Purpose"],
        [
            ["hdfs dfs -mkdir -p /path", "Create folder"],
            ["hdfs dfs -put file /path/", "Upload"],
            ["hdfs dfs -ls /path", "List"],
            ["hdfs dfs -cat /path/file", "Show contents"],
            ["hdfs dfs -cp src dest", "Copy inside HDFS"],
            ["hdfs dfs -get hdfs local", "Download"],
            ["hdfs dfs -rm -r /path", "Delete folder"],
            ["hdfs dfs -df -h /", "Space summary"],
            ["hdfs dfsadmin -report", "Cluster health, live DataNodes"],
        ],
        [75, 105],
    )

    pdf.sub_title("Exercises")
    pdf.qa_block("1. New directory and multiple files.", "mkdir -p /user/lab/exercise1; put file1.txt file2.txt; ls.")
    pdf.qa_block("2. Copy between HDFS folders.", "cp /user/lab/exercise1/file1.txt /user/lab/exercise2/file1_copied.txt")
    pdf.qa_block("3. Delete a directory.", "hdfs dfs -rm -r /user/lab/to_delete")
    pdf.qa_block("4. Display file contents.", "hdfs dfs -cat /user/lab/exercise1/file2.txt")
    pdf.qa_block("5. Check space.", "hdfs dfs -df -h / and hdfs dfsadmin -report")

    pdf.sub_title("Viva questions")
    for q, a in [
        ("NameNode vs DataNode?", "NameNode: metadata. DataNode: actual blocks."),
        ("What is a block?", "Fixed-size chunk of a file (default 128 MB)."),
        ("What does dfs mean?", "Distributed file system; hdfs dfs runs file ops on HDFS."),
        ("put vs get?", "put: local to HDFS. get: HDFS to local."),
        ("Why format NameNode?", "Creates empty namespace; only once per new setup; wipes HDFS if repeated."),
        ("What does dfsadmin -report do?", "Shows capacity and whether DataNodes are alive."),
    ]:
        pdf.qa_block(q, a)

    # ----- Experiment 6 -----
    pdf.add_page()
    pdf.section_title("Experiment 6: Word Count (MapReduce)")
    pdf.sub_title("Aim")
    pdf.body("Count word frequencies in a text file using a Java MapReduce program on HDFS.")
    pdf.sub_title("Original input.txt (3 lines)")
    pdf.body(
        "Hadoop is a big data framework.\n"
        "Hadoop uses MapReduce.\n"
        "MapReduce processes big data efficiently."
    )
    pdf.bullet("14 words, 10 unique. hadoop, big, data, mapreduce count 2 each.")
    pdf.sub_title("input_modified.txt")
    pdf.body("Same 3 lines plus: 'HDFS stores big data in blocks.' and 'Hadoop is open source and Hadoop is scalable.' -> 28 words, 18 unique.")

    pdf.sub_title("What you did")
    pdf.bullet("Upload input to HDFS. Compile WordCount.java to wordcount.jar.")
    pdf.bullet("hadoop jar wordcount.jar WordCount <input> <output>")
    pdf.bullet("Read hdfs dfs -cat <output>/part-r-00000")

    pdf.sub_title("MapReduce flow")
    pdf.bullet("Mapper: each line -> (word, 1)")
    pdf.bullet("Combiner: local sum (same class as Reducer)")
    pdf.bullet("Shuffle/Sort: group by word")
    pdf.bullet("Reducer: sum counts -> (word, total)")
    pdf.bullet("Output must be a new directory; delete old output with hdfs dfs -rm -r")

    pdf.sub_title("Exercises")
    pdf.qa_block("1. Modify input.", "28 words, 18 unique; hadoop 2 to 4.")
    pdf.qa_block("2. Skip stopwords.", "-D wordcount.skip.stopwords=true; map output 28 to 22.")
    pdf.qa_block("3. Another file.", "another.txt: 39 words, 29 unique.")
    pdf.qa_block("4. Compare outputs.", "Some words unchanged; some increased; new words (hdfs, blocks, ...).")
    pdf.qa_block("5. Mapper and Reducer roles.", "Mapper emits (word,1) per line; Reducer sums for final count.")

    pdf.sub_title("Viva questions")
    for q, a in [
        ("What is MapReduce?", "Map builds key-value pairs; Reduce aggregates by key."),
        ("Combiner?", "Mini-reducer on map side; less network traffic."),
        ("Shuffle and Sort?", "Groups all values for each key before reduce."),
        ("Why Text, IntWritable?", "Hadoop serializable types for cluster I/O."),
        ("part-r-00000?", "Output file from reducer 0."),
        ("_SUCCESS?", "Marker that job completed."),
    ]:
        pdf.qa_block(q, a)

    out = Path("/Users/ojas/Desktop/DS Lab/Viva_Experiments_4_5_6.pdf")
    pdf.output(str(out))
    print("Wrote", out)


if __name__ == "__main__":
    generate()

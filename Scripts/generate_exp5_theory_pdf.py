"""Generate Experiment 5 theory PDF (Hadoop / HDFS)."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from pdf_math_utils import LabPDF


def generate():
    pdf = LabPDF("Experiment 5 - Hadoop Installation, Configuration & HDFS")
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.title_page(
        "Experiment 5",
        "Hadoop Installation, Configuration, and HDFS Operations",
        "Subject: Data Science Lab | Environment: Single-node Hadoop | Mapped CO(s): CO2",
    )

    pdf.section_title("1. Aim")
    pdf.body(
        "To install and configure Hadoop in a single-node environment and perform "
        "basic HDFS operations using command-line tools."
    )

    pdf.section_title("2. Key Concepts")
    pdf.term_block(
        "Apache Hadoop",
        "Open-source framework for reliable, scalable storage and processing of large datasets across machines.",
    )
    pdf.term_block(
        "HDFS (Hadoop Distributed File System)",
        "Storage layer. Files are split into blocks and stored on DataNodes. The NameNode keeps the metadata (what file lives where).",
    )
    pdf.term_block(
        "NameNode",
        "Master daemon. Stores the file-system namespace and block locations. It does not store the actual file data.",
    )
    pdf.term_block(
        "DataNode",
        "Worker daemon. Stores the actual data blocks and reports to the NameNode.",
    )
    pdf.term_block(
        "YARN",
        "Yet Another Resource Negotiator. Manages cluster CPU/memory and schedules jobs.",
    )
    pdf.term_block(
        "MapReduce",
        "Processing model: Map produces key-value pairs, Reduce aggregates them in parallel.",
    )
    pdf.term_block(
        "Replication",
        "Each block is copied to more than one DataNode so data survives disk/node failure. Single-node labs use replication = 1.",
    )
    pdf.term_block(
        "Pseudo-distributed / single-node mode",
        "NameNode and DataNode run on the same machine. Same commands as a real cluster, smaller setup.",
    )

    pdf.section_title("3. Important Configuration Files")
    pdf.table(
        ["File", "Purpose"],
        [
            ["hadoop-env.sh", "JAVA_HOME and environment"],
            ["core-site.xml", "Default file system URI"],
            ["hdfs-site.xml", "Replication, NameNode/DataNode dirs"],
            ["mapred-site.xml", "MapReduce framework (optional here)"],
            ["yarn-site.xml", "YARN resource manager (optional here)"],
        ],
        [45, 135],
    )

    pdf.sub_title("core-site.xml")
    pdf.body("fs.defaultFS = hdfs://localhost:9000")
    pdf.sub_title("hdfs-site.xml")
    pdf.bullet("dfs.replication = 1")
    pdf.bullet("dfs.namenode.name.dir = local NameNode metadata folder")
    pdf.bullet("dfs.datanode.data.dir = local DataNode block folder")

    pdf.add_page()
    pdf.section_title("4. Algorithm (Single-Node Setup)")
    steps = [
        "Install JDK 8+ and Hadoop.",
        "Set JAVA_HOME, HADOOP_HOME, HADOOP_CONF_DIR, and PATH.",
        "Configure core-site.xml and hdfs-site.xml.",
        "Format the NameNode (once): hdfs namenode -format",
        "Start daemons: hdfs --daemon start namenode ; hdfs --daemon start datanode",
        "Verify with jps and hdfs dfsadmin -report.",
        "Create directories, upload, list, cat, copy, download, delete.",
    ]
    for i, step in enumerate(steps, 1):
        pdf.bullet(f"{i}. {step}")

    pdf.section_title("5. HDFS Command Cheat Sheet")
    pdf.table(
        ["Command", "What it does"],
        [
            ["hadoop version", "Show Hadoop version"],
            ["hdfs namenode -format", "Initialize NameNode metadata"],
            ["hdfs --daemon start namenode", "Start NameNode"],
            ["hdfs --daemon start datanode", "Start DataNode"],
            ["jps", "List Java daemons"],
            ["hdfs dfs -mkdir -p /path", "Create directory"],
            ["hdfs dfs -put local hdfs", "Upload file"],
            ["hdfs dfs -ls /path", "List files"],
            ["hdfs dfs -cat /path/file", "Print file contents"],
            ["hdfs dfs -cp src dest", "Copy inside HDFS"],
            ["hdfs dfs -get hdfs local", "Download to local disk"],
            ["hdfs dfs -rm /path/file", "Delete file"],
            ["hdfs dfs -rm -r /path", "Delete directory"],
            ["hdfs dfs -df -h /", "Show HDFS space"],
            ["hdfs dfsadmin -report", "Cluster / DataNode report"],
        ],
        [75, 105],
    )

    pdf.section_title("6. Exercise Answers")
    pdf.sub_title("Exercise 1: New directory + multiple files")
    pdf.body("hdfs dfs -mkdir -p /user/lab/exercise1")
    pdf.body("hdfs dfs -put file1.txt file2.txt /user/lab/exercise1/")
    pdf.body("hdfs dfs -ls /user/lab/exercise1")

    pdf.sub_title("Exercise 2: Copy file between HDFS directories")
    pdf.body("hdfs dfs -cp /user/lab/exercise1/file1.txt /user/lab/exercise2/file1_copied.txt")

    pdf.sub_title("Exercise 3: Delete a directory")
    pdf.body("hdfs dfs -rm -r /user/lab/to_delete")

    pdf.sub_title("Exercise 4: Display file contents")
    pdf.body("hdfs dfs -cat /user/lab/exercise1/file2.txt")

    pdf.sub_title("Exercise 5: Check available space")
    pdf.body("hdfs dfs -df -h /")
    pdf.body("hdfs dfsadmin -report")

    pdf.add_page()
    pdf.section_title("7. Viva Q&A")
    qa = [
        ("What is Hadoop?", "Open-source framework for distributed storage (HDFS) and processing (MapReduce/YARN) of big data."),
        ("What is HDFS?", "Hadoop's distributed file system. Files are split into blocks and stored on DataNodes."),
        ("NameNode vs DataNode?", "NameNode stores metadata (namespace). DataNode stores actual blocks."),
        ("What is a block in HDFS?", "Fixed-size chunk of a file (default 128 MB in Hadoop 2/3). Last block can be smaller."),
        ("Why replication?", "Fault tolerance. If one DataNode dies, copies on other nodes keep the file available."),
        ("Default replication factor?", "3 in a real cluster. This lab uses 1 because there is only one node."),
        ("What does formatting the NameNode do?", "Creates an empty file-system namespace. It wipes previous HDFS metadata."),
        ("fs.defaultFS?", "Property in core-site.xml that tells Hadoop where the file system lives, e.g. hdfs://localhost:9000."),
        ("put vs get?", "put uploads local -> HDFS. get downloads HDFS -> local."),
        ("mkdir -p?", "Create the directory and any missing parent directories."),
        ("How do you check daemons?", "jps should show NameNode and DataNode."),
        ("HDFS vs local FS?", "Local FS is one disk on one machine. HDFS is designed for many machines, large files, and replication."),
        ("Can you edit a file in HDFS?", "HDFS is write-once, read-many. You typically replace a file, not edit in place."),
        ("What is YARN?", "Resource manager that allocates CPU/memory and runs applications on the cluster."),
        ("Single-node vs cluster?", "Same software and commands. Cluster has many DataNodes; single-node runs both roles locally."),
    ]
    for q, a in qa:
        pdf.qa_block(q, a)

    pdf.section_title("8. One-Line Definitions")
    for term, defn in [
        ("HDFS", "Distributed storage layer of Hadoop"),
        ("NameNode", "Master that stores file-system metadata"),
        ("DataNode", "Worker that stores data blocks"),
        ("Block", "Fixed-size piece of an HDFS file"),
        ("Replication", "Keeping extra copies of each block"),
        ("YARN", "Cluster resource manager and scheduler"),
        ("MapReduce", "Parallel map-then-reduce processing model"),
        ("fs.defaultFS", "URI of the default file system"),
        ("hadoop fs / hdfs dfs", "Shell for HDFS file operations"),
        ("jps", "Lists running Java processes / daemons"),
    ]:
        pdf.term_block(term, defn)

    out = Path("/Users/ojas/Desktop/DS Lab/Experiment5/Theory_and_Formulae.pdf")
    pdf.output(str(out))
    print("Wrote", out)


if __name__ == "__main__":
    generate()

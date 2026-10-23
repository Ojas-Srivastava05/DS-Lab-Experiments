"""Experiment 5 PDF: steps used to download Hadoop on this Mac."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from pdf_math_utils import LabPDF


def generate():
    pdf = LabPDF("Experiment 5 - Hadoop Download Steps")
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.title_page(
        "Experiment 5",
        "Steps to Download Hadoop",
        "Data Science Lab | Hadoop 3.4.1 on this Mac | Ojas Srivastava, U24AI028",
    )

    pdf.section_title("1. Install Java")
    pdf.bullet("brew install openjdk@17")
    pdf.bullet("JAVA_HOME=/opt/homebrew/opt/openjdk@17/libexec/openjdk.jdk/Contents/Home")
    pdf.bullet("Check with: java -version")

    pdf.section_title("2. Download Hadoop")
    pdf.bullet("Download the Hadoop 3.4.1 binary tarball:")
    pdf.bullet("https://archive.apache.org/dist/hadoop/common/hadoop-3.4.1/hadoop-3.4.1.tar.gz")
    pdf.bullet("Extract it in the home folder:")
    pdf.bullet("tar -xzf hadoop-3.4.1.tar.gz -C /Users/ojas")
    pdf.bullet("Hadoop is then at /Users/ojas/hadoop-3.4.1")
    pdf.bullet("Keep it outside the DS Lab folder. The space in that path breaks Hadoop.")

    pdf.section_title("3. Every time you open a terminal")
    pdf.bullet("export JAVA_HOME=/opt/homebrew/opt/openjdk@17/libexec/openjdk.jdk/Contents/Home")
    pdf.bullet("export HADOOP_HOME=/Users/ojas/hadoop-3.4.1")
    pdf.bullet('export PATH="$JAVA_HOME/bin:$HADOOP_HOME/bin:$HADOOP_HOME/sbin:$PATH"')
    pdf.bullet("Check with: hadoop version")
    pdf.body("The version line should say Hadoop 3.4.1.")

    pdf.section_title("4. Start HDFS after the download")
    pdf.bullet("core-site.xml: fs.defaultFS = hdfs://localhost:9000")
    pdf.bullet("hdfs-site.xml: replication 1, NameNode and DataNode folders")
    pdf.bullet("hdfs namenode -format once per fresh run (this wipes HDFS)")
    pdf.bullet("hdfs --daemon start namenode")
    pdf.bullet("hdfs --daemon start datanode")
    pdf.bullet("Check with jps. It should list NameNode and DataNode.")

    pdf.section_title("5. Stop HDFS")
    pdf.bullet("hdfs --daemon stop datanode")
    pdf.bullet("hdfs --daemon stop namenode")

    out = Path("/Users/ojas/Desktop/DS Lab/Experiment5/Hadoop_Download_Steps.pdf")
    pdf.output(str(out))
    print("Wrote", out)


if __name__ == "__main__":
    generate()

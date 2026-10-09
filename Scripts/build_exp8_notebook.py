"""Build the Experiment 8 (Query Processing on Large Datasets Using Apache Hive) notebook."""

from pathlib import Path

import nbformat as nbf

NB_PATH = Path(__file__).resolve().parent.parent / "Experiment8" / "Notebook.ipynb"

cells = []


def md(text):
    cells.append(nbf.v4.new_markdown_cell(text.strip("\n")))


def code(text):
    cells.append(nbf.v4.new_code_cell(text.strip("\n")))


md("""
# Experiment 8: Query Processing on Large Datasets Using Apache Hive

**Aim:** To perform SQL-like querying, aggregation, and analysis of large datasets using Apache Hive.

**Mapped CO(s):** CO2

**Dataset:** Titanic Dataset (`Titanic-Dataset.csv`, 891 passengers)
""")

md("## 1. Import Required Libraries")
code("""
import os
import re
import shutil
import subprocess
import time
from io import StringIO
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid")
plt.rcParams["figure.figsize"] = (8, 5)
""")

md("""
## 2. Apache Hive (Brief Theory)

Apache Hive is a **data warehouse system on top of Hadoop**. Users write **HiveQL** (SQL-like), and Hive converts each query into MapReduce (or Tez/Spark) jobs that read data from HDFS.

**Hive architecture**

| Component | Role |
|---|---|
| **Beeline / CLI** | Client used to submit HiveQL statements |
| **HiveServer2** | Accepts client connections over JDBC (embedded inside Beeline in this lab) |
| **Driver** (compiler, optimizer, executor) | Parses HiveQL, builds an execution plan, and runs it as MapReduce jobs |
| **Metastore** | Stores table schemas and HDFS locations (here an embedded **Derby** database) |
| **HDFS** | Stores the actual table data under `/user/hive/warehouse` |

**Common HiveQL operations**

| Statement | Purpose |
|---|---|
| `CREATE DATABASE` | Create a new database |
| `CREATE TABLE` | Define a table schema (columns, row format, storage) |
| `LOAD DATA INPATH` | Move a file from HDFS into a table |
| `SELECT ... WHERE` | Retrieve and filter rows |
| `GROUP BY` | Group rows for aggregation |
| `ORDER BY` | Sort the final result |
| `COUNT()`, `AVG()`, `MAX()`, `MIN()` | Aggregate functions |

Hive uses **schema-on-read**. The file stays as plain text in HDFS, and the schema is applied when the data is queried.
""")

md("""
## 3. Set Java, Hadoop and Hive Environment

HDFS runs on Java 17. Hive 4.2.1 is compiled for Java 21, so the `beeline` and `schematool` launchers run with Java 21.
""")
code("""
EXP_DIR = Path("/Users/ojas/Desktop/DS Lab/Experiment8")
SRC_DIR = EXP_DIR / "src"
DATASET = Path("/Users/ojas/Desktop/DS Lab/Shared/Titanic-Dataset.csv")

WORK_DIR = Path("/tmp/exp8")
BIN_DIR = WORK_DIR / "bin"
LOCAL_DIR = WORK_DIR / "local"
HDFS_DATA = WORK_DIR / "hdfs-data"
CONF_DIR = WORK_DIR / "hadoop-conf"
HIVE_CONF = WORK_DIR / "hive-conf"
METASTORE = WORK_DIR / "metastore_db"
LOG_DIR = WORK_DIR / "logs"

JAVA_HOME = Path("/opt/homebrew/opt/openjdk@17/libexec/openjdk.jdk/Contents/Home")
JAVA21_HOME = Path("/opt/homebrew/opt/openjdk@21/libexec/openjdk.jdk/Contents/Home")
HADOOP_HOME = Path("/Users/ojas/hadoop-3.4.1")
HIVE_HOME = Path("/Users/ojas/apache-hive-4.2.1-bin")

os.environ["JAVA_HOME"] = str(JAVA_HOME)
os.environ["HADOOP_HOME"] = str(HADOOP_HOME)
os.environ["HADOOP_CONF_DIR"] = str(CONF_DIR)
os.environ["HADOOP_LOG_DIR"] = str(LOG_DIR)
os.environ["HIVE_HOME"] = str(HIVE_HOME)
os.environ["HIVE_CONF_DIR"] = str(HIVE_CONF)
os.environ["HADOOP_CLIENT_OPTS"] = "-Dorg.jline.terminal.provider=dumb"
os.environ["PATH"] = (
    f"{BIN_DIR}:{JAVA_HOME / 'bin'}:{HADOOP_HOME / 'bin'}:{HADOOP_HOME / 'sbin'}:"
    + os.environ["PATH"]
)

for folder in (BIN_DIR, LOCAL_DIR, LOG_DIR, HIVE_CONF):
    folder.mkdir(parents=True, exist_ok=True)

for tool in ("beeline", "schematool"):
    launcher = BIN_DIR / tool
    launcher.write_text(
        "#!/bin/bash\\n"
        f'export JAVA_HOME="{JAVA21_HOME}"\\n'
        f'exec "{HIVE_HOME}/bin/{tool}" "$@"\\n'
    )
    launcher.chmod(0o755)


NOISE = ("NativeCodeLoader", "log4j", "WARN ", " INFO ", "SLF4J")


def clean(text):
    return "\\n".join(
        line for line in (text or "").splitlines()
        if not any(word in line for word in NOISE)
    ).strip()


def capture(cmd, check=True):
    result = subprocess.run(
        cmd, shell=True, text=True, capture_output=True, env=os.environ.copy(),
        cwd=WORK_DIR, stdin=subprocess.DEVNULL,
    )
    if check and result.returncode != 0:
        print(result.stdout[-3000:])
        print(result.stderr[-4000:])
        raise RuntimeError(f"Command failed with exit code {result.returncode}: {cmd}")
    return result


def run(cmd, check=True):
    print(f"$ {cmd}")
    result = capture(cmd, check)
    for text in (clean(result.stdout), clean(result.stderr)):
        if text:
            print(text)


run("java -version")
print()
run("hadoop version | head -1")
print()
run("beeline --version")
""")

md("""
## 4. Start Hadoop (HDFS)

Single-node setup: `fs.defaultFS = hdfs://localhost:8020`, replication = 1. Hive's MapReduce jobs run with the local job runner and read/write HDFS.
""")
code("""
if CONF_DIR.exists():
    shutil.rmtree(CONF_DIR)
shutil.copytree(HADOOP_HOME / "etc" / "hadoop", CONF_DIR)

(CONF_DIR / "core-site.xml").write_text(\"\"\"<?xml version="1.0" encoding="UTF-8"?>
<configuration>
  <property>
    <name>fs.defaultFS</name>
    <value>hdfs://localhost:8020</value>
  </property>
</configuration>
\"\"\")

(CONF_DIR / "hdfs-site.xml").write_text(f\"\"\"<?xml version="1.0" encoding="UTF-8"?>
<configuration>
  <property><name>dfs.replication</name><value>1</value></property>
  <property><name>dfs.namenode.name.dir</name><value>file://{HDFS_DATA / 'namenode'}</value></property>
  <property><name>dfs.datanode.data.dir</name><value>file://{HDFS_DATA / 'datanode'}</value></property>
  <property><name>dfs.namenode.http-address</name><value>localhost:9870</value></property>
  <property><name>dfs.datanode.address</name><value>localhost:9866</value></property>
  <property><name>dfs.datanode.http.address</name><value>localhost:9864</value></property>
  <property><name>dfs.datanode.ipc.address</name><value>localhost:9867</value></property>
  <property><name>dfs.permissions.enabled</name><value>false</value></property>
</configuration>
\"\"\")

(CONF_DIR / "mapred-site.xml").write_text(\"\"\"<?xml version="1.0" encoding="UTF-8"?>
<configuration>
  <property>
    <name>mapreduce.framework.name</name>
    <value>local</value>
  </property>
</configuration>
\"\"\")

capture("hdfs --daemon stop datanode", check=False)
capture("hdfs --daemon stop namenode", check=False)
time.sleep(2)
if HDFS_DATA.exists():
    shutil.rmtree(HDFS_DATA)
HDFS_DATA.mkdir(parents=True)

capture("hdfs namenode -format -force -nonInteractive")
print("NameNode formatted.")
run("hdfs --daemon start namenode")
run("hdfs --daemon start datanode")

for _ in range(30):
    time.sleep(1)
    report = capture("hdfs dfsadmin -report", check=False)
    if "Live datanodes (1)" in report.stdout:
        break

run("jps")
""")

md("""
## 5. Configure Hive and Initialize the Metastore

`hive-site.xml` sets an embedded Derby metastore, the HDFS warehouse directory, and the MapReduce execution engine. Automatic map-join conversion is turned off so that every join runs as a normal MapReduce job. `schematool -initSchema` creates the metastore tables.
""")
code("""
(HIVE_CONF / "hive-site.xml").write_text(f\"\"\"<?xml version="1.0" encoding="UTF-8"?>
<configuration>
  <property><name>javax.jdo.option.ConnectionURL</name><value>jdbc:derby:;databaseName={METASTORE};create=true</value></property>
  <property><name>hive.metastore.warehouse.dir</name><value>/user/hive/warehouse</value></property>
  <property><name>hive.metastore.schema.verification</name><value>false</value></property>
  <property><name>hive.execution.engine</name><value>mr</value></property>
  <property><name>hive.server2.enable.doAs</name><value>false</value></property>
  <property><name>hive.exec.scratchdir</name><value>/tmp/hive-scratch</value></property>
  <property><name>hive.exec.local.scratchdir</name><value>{WORK_DIR / 'local-scratch'}</value></property>
  <property><name>hive.downloaded.resources.dir</name><value>{WORK_DIR / 'resources'}</value></property>
  <property><name>hive.querylog.location</name><value>{WORK_DIR / 'querylog'}</value></property>
  <property><name>hive.stats.autogather</name><value>false</value></property>
  <property><name>hive.resultset.use.unique.column.names</name><value>false</value></property>
  <property><name>hive.auto.convert.join</name><value>false</value></property>
</configuration>
\"\"\")

if METASTORE.exists():
    shutil.rmtree(METASTORE)
result = capture("schematool -dbType derby -initSchema")
print("\\n".join(l for l in result.stdout.splitlines() if "Initialization script" in l))

run("hdfs dfs -mkdir -p /user/hive/warehouse /tmp/hive-scratch")
run("hdfs dfs -chmod -R 777 /tmp/hive-scratch")
""")

md("## 6. Store the Titanic Dataset in HDFS")
code("""
shutil.copy2(DATASET, LOCAL_DIR / DATASET.name)

run("hdfs dfs -mkdir -p /user/lab8/titanic")
run(f"hdfs dfs -put -f {LOCAL_DIR / DATASET.name} /user/lab8/titanic/")
run("hdfs dfs -ls /user/lab8/titanic")
print()
run("hdfs dfs -cat /user/lab8/titanic/Titanic-Dataset.csv | head -4")
""")

md("""
## 7. HiveQL Helper Functions

- `statements(sql)` removes `--` comments and splits a script into statements.
- `hive_script(sql)` runs DDL statements (CREATE / LOAD) with `beeline` and prints each statement plus the MapReduce jobs it launched.
- `hive_query(sql)` runs one `SELECT` and returns the result as a pandas DataFrame.

Beeline connects with `jdbc:hive2://` (embedded HiveServer2), so no separate server process is needed.
""")
code("""
BEELINE = "beeline -u jdbc:hive2:// -n ojas --silent=true --outputformat=tsv2"
JOB_LINES = ("Total jobs", "Launching Job", "Ended Job")


def statements(sql):
    body = "\\n".join(l for l in sql.splitlines() if not l.strip().startswith("--"))
    return [s.strip() for s in body.split(";") if s.strip()]


def beeline(stmts):
    script = " ".join(s + ";" for s in stmts)
    result = capture(f"{BEELINE} -e {sh_quote(script)}")
    failures = [l for l in result.stderr.splitlines() if re.match(r"^(Error: |FAILED: )", l)]
    if failures:
        print("\\n".join(failures))
        raise RuntimeError("Hive statement failed")
    return result


def sh_quote(text):
    return "'" + text.replace("'", "'\\\\''") + "'"


def hive_script(sql, db=None):
    stmts = statements(sql)
    for s in stmts:
        print("hive>", " ".join(s.split())[:110] + (" ..." if len(" ".join(s.split())) > 110 else ""))
    result = beeline(([f"USE {db}"] if db else []) + stmts)
    jobs = [l.split(": ")[-1] if "]: " in l else l for l in result.stderr.splitlines() if any(k in l for k in JOB_LINES)]
    if jobs:
        print("\\n" + "\\n".join(jobs))
    print("\\nOK")


def hive_query(sql, db="titanic_db", show_sql=True):
    stmt = statements(sql)[0]
    if show_sql:
        print("hive>", stmt, "\\n")
    result = beeline([f"USE {db}", stmt])
    return pd.read_csv(StringIO(result.stdout), sep="\\t", na_values=["NULL"], keep_default_na=False)
""")

md("""
## 8. Create the Database and Table, and Load the Dataset

`create_titanic.hql`:

1. Creates the database `titanic_db`.
2. Creates a staging table `titanic_raw` with **OpenCSVSerde**, because passenger names contain commas inside quotes.
3. Loads the CSV from HDFS with `LOAD DATA INPATH`.
4. Creates the typed table `titanic` (INT/DOUBLE columns, ORC format) with `CREATE TABLE ... AS SELECT`. Empty ages become `NULL`.
""")
code("""
create_sql = (SRC_DIR / "create_titanic.hql").read_text()
print(create_sql)
""")
code("""
hive_script(create_sql)
""")

md("### Verify: databases, tables, schema, and warehouse location in HDFS")
code("""
display(hive_query("SHOW DATABASES", db="default"))
display(hive_query("SHOW TABLES"))
display(hive_query("DESCRIBE titanic"))
run("hdfs dfs -ls /user/hive/warehouse/titanic_db.db")
""")

md("## 9. Display the Table Contents (SELECT)")
code("""
display(hive_query("SELECT * FROM titanic LIMIT 10"))
""")
code("""
display(hive_query("SELECT COUNT(*) AS total_passengers FROM titanic"))
""")

md("## 10. Filtering (WHERE)")
code("""
seniors = hive_query(\"\"\"
SELECT passengerid, name, sex, pclass, age, survived
FROM titanic
WHERE age >= 65
ORDER BY age DESC
\"\"\")
display(seniors)
print("Passengers aged 65 or more:", len(seniors))
""")

md("## 11. Grouping and Aggregation (GROUP BY, COUNT, AVG)")
code("""
class_stats = hive_query(\"\"\"
SELECT pclass,
       COUNT(*)                     AS passengers,
       SUM(survived)                AS survived,
       ROUND(AVG(survived) * 100, 2) AS survival_pct,
       ROUND(AVG(age), 2)           AS avg_age,
       ROUND(AVG(fare), 2)          AS avg_fare
FROM titanic
GROUP BY pclass
ORDER BY pclass
\"\"\")
display(class_stats)
""")
code("""
sex_stats = hive_query(\"\"\"
SELECT sex, COUNT(*) AS passengers, SUM(survived) AS survived,
       ROUND(AVG(survived) * 100, 2) AS survival_pct
FROM titanic
GROUP BY sex
ORDER BY survival_pct DESC
\"\"\")
display(sex_stats)

fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))
sns.barplot(data=class_stats, x="pclass", y="survival_pct", ax=axes[0], color="steelblue")
axes[0].set_title("Survival % by Class (HiveQL)")
sns.barplot(data=sex_stats, x="sex", y="survival_pct", ax=axes[1], palette=["mediumvioletred", "slategray"], hue="sex", legend=False)
axes[1].set_title("Survival % by Sex (HiveQL)")
for ax in axes:
    ax.set_ylim(0, 100)
plt.tight_layout()
plt.show()
""")

md("## 12. Sorting (ORDER BY) and Embarkation Port Analysis")
code("""
port_stats = hive_query(\"\"\"
SELECT embarked, COUNT(*) AS passengers, ROUND(AVG(fare), 2) AS avg_fare
FROM titanic
WHERE embarked IS NOT NULL
GROUP BY embarked
ORDER BY passengers DESC
\"\"\")
port_stats["port"] = port_stats["embarked"].map({"S": "Southampton", "C": "Cherbourg", "Q": "Queenstown"})
display(port_stats)
""")

md("### Cross-check with pandas")
code("""
df = pd.read_csv(DATASET)
check = df.groupby("Pclass").agg(
    passengers=("PassengerId", "count"),
    survived=("Survived", "sum"),
    avg_fare=("Fare", "mean"),
).round(2).reset_index()
display(check)
print("Hive and pandas results match:",
      class_stats[["passengers", "survived", "avg_fare"]].equals(check[["passengers", "survived", "avg_fare"]]))
""")

md("""
---
## Exercises / Assignments

All exercise queries are saved in `exercises.hql`. Each one is run separately below.
""")
code("""
exercise_sql = (SRC_DIR / "exercises.hql").read_text()
print(exercise_sql)
EX = [s for s in statements(exercise_sql) if not s.upper().startswith("USE")]
""")

md("### Exercise 1: Display only female passengers")
code("""
females = hive_query(EX[0])
print("Female passengers:", len(females))
display(females.head(10))
""")
md("""
`WHERE sex = 'female'` returns **314** of the 891 passengers.
""")

md("### Exercise 2: Find the average fare for each passenger class")
code("""
avg_fare = hive_query(EX[1])
display(avg_fare)

sns.barplot(data=avg_fare, x="pclass", y="avg_fare", color="darkorange")
plt.title("Average Fare by Passenger Class")
plt.ylabel("Average fare")
plt.tight_layout()
plt.show()
""")
md("""
1st class paid about **84.15** on average, roughly 4 times the 2nd-class fare (**20.66**) and 6 times the 3rd-class fare (**13.68**).
""")

md("### Exercise 3: Count the number of passengers who survived")
code("""
survived = hive_query(EX[2])
display(survived)
total = len(df)
n = int(survived.iloc[0, 0])
print(f"Survived: {n} of {total} ({n / total:.2%})")
""")
md("""
**342** passengers survived, a survival rate of 38.38%.
""")

md("### Exercise 4: Sort passengers by age in descending order")
code("""
by_age = hive_query(EX[3])
print("Passengers with a known age:", len(by_age))
print("Oldest 10:")
display(by_age.head(10))
print("Youngest 5:")
display(by_age.tail(5))
""")
md("""
177 passengers have no age recorded, so `WHERE age IS NOT NULL` keeps 714 rows. The oldest passenger is 80 (Barkworth, Mr. Algernon Henry Wilson), and the youngest is an infant aged 0.42.
""")

md("### Exercise 5: Find the maximum and minimum fare using HiveQL")
code("""
fare_range = hive_query(EX[4])
display(fare_range)

who = hive_query(\"\"\"
SELECT passengerid, name, pclass, fare
FROM titanic
WHERE fare = (SELECT MAX(fare) FROM titanic) OR fare = 0
ORDER BY fare DESC, passengerid
\"\"\")
display(who)
""")
md("""
The maximum fare is **512.33** (three 1st-class passengers), and the minimum fare is **0.0** (15 passengers, most likely crew or complimentary tickets).
""")

md("""
---
## Observation

- The Hive database `titanic_db` and the tables `titanic_raw` / `titanic` were created successfully.
- The Titanic dataset was loaded from HDFS into the Hive table (891 rows).
- SQL-like queries (`SELECT`, `WHERE`, `GROUP BY`, `ORDER BY`) were executed successfully. Hive ran aggregations as MapReduce jobs.
- `COUNT` and `AVG` produced the expected results: 342 survivors, and average fares of 84.15 / 20.66 / 13.68 for classes 1 / 2 / 3.
- The results matched an independent pandas calculation.

## Result

Apache Hive successfully processed and analyzed the Titanic dataset using SQL-like queries. Query execution and aggregation operations demonstrated Hive's capability to analyze large datasets efficiently.

## Conclusion

The experiment demonstrated how Apache Hive provides a simple SQL-like interface for querying and analyzing large datasets stored in Hadoop. HiveQL made it easy to perform filtering, grouping, sorting, and aggregation operations, making Hive an effective tool for big data analytics.
""")

nb = nbf.v4.new_notebook()
nb["cells"] = cells
nb["metadata"] = {
    "kernelspec": {"display_name": ".venv", "language": "python", "name": "python3"},
    "language_info": {"name": "python", "pygments_lexer": "ipython3"},
}
nbf.write(nb, NB_PATH)
print("Wrote", NB_PATH)

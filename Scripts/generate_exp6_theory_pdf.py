"""Generate Experiment 6 theory PDF (Word Count with Hadoop MapReduce)."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from pdf_math_utils import LabPDF


def generate():
    pdf = LabPDF("Experiment 6 - Word Count using Hadoop MapReduce")
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.title_page(
        "Experiment 6",
        "Word Count Application using Hadoop MapReduce",
        "Subject: Data Science Lab | Environment: Hadoop 3.4.1 + Java 17 | Mapped CO(s): CO2, CO3",
    )

    pdf.section_title("1. Aim")
    pdf.body(
        "To implement a Word Count application using the Hadoop MapReduce framework "
        "and analyze the frequency of words in a given text dataset."
    )

    pdf.section_title("2. Key Concepts")
    pdf.term_block(
        "MapReduce",
        "Programming model for processing large datasets in parallel. A job is split into a Map phase and a Reduce phase.",
    )
    pdf.term_block(
        "Mapper",
        "Reads one input record (a line) at a time and emits intermediate (key, value) pairs. For Word Count it emits (word, 1).",
    )
    pdf.term_block(
        "Shuffle and Sort",
        "Framework step between Map and Reduce. Groups all values with the same key and sends them to one Reducer, sorted by key.",
    )
    pdf.term_block(
        "Reducer",
        "Receives (key, list of values) and aggregates them. For Word Count it sums the 1s to get (word, total).",
    )
    pdf.term_block(
        "Combiner",
        "Optional mini-reducer that runs on Mapper output locally to reduce data sent over the network. Word Count reuses the Reducer.",
    )
    pdf.term_block(
        "InputSplit / RecordReader",
        "The input file is split into chunks; TextInputFormat's RecordReader gives the Mapper (byte offset, line) pairs.",
    )
    pdf.term_block(
        "Driver",
        "The main() class that configures the Job: Mapper, Combiner, Reducer, output types, input path, and output path.",
    )
    pdf.term_block(
        "Writable types",
        "Hadoop's serializable types: Text for strings, IntWritable for ints, LongWritable for offsets.",
    )

    pdf.section_title("3. Data Flow")
    pdf.math(r"(offset,\ line) \rightarrow (word,\ 1) \rightarrow (word,\ [1,1,\dots]) \rightarrow (word,\ \sum 1)")
    pdf.body("Map -> Shuffle/Sort -> Reduce")
    pdf.body("Count of a word w over all lines:")
    pdf.math(r"count(w) = \sum_{i=1}^{N} \mathbb{1}[token_i = w]")
    pdf.table(
        ["Phase", "Input", "Output"],
        [
            ["Map", "(LongWritable, Text line)", "(Text word, IntWritable 1)"],
            ["Combine", "(word, [1,1,...]) per mapper", "(word, partial sum)"],
            ["Shuffle/Sort", "All mapper outputs", "(word, [values]) grouped"],
            ["Reduce", "(word, [values])", "(word, total count)"],
        ],
        [35, 75, 70],
    )

    pdf.add_page()
    pdf.section_title("4. Algorithm")
    steps = [
        "Start HDFS (NameNode + DataNode) and upload input.txt to /user/lab6/input.",
        "Mapper: lowercase each line, remove punctuation, split into tokens, emit (token, 1).",
        "Combiner: locally sum counts for each word on the map side.",
        "Shuffle/Sort: framework groups pairs by word.",
        "Reducer: sum all counts for a word and emit (word, total).",
        "Driver: configure the Job, set input/output paths, submit and wait.",
        "Compile with javac using `hadoop classpath`, package into wordcount.jar.",
        "Run: hadoop jar wordcount.jar WordCount <input> <output>.",
        "Read result: hdfs dfs -cat <output>/part-r-00000.",
    ]
    for i, step in enumerate(steps, 1):
        pdf.bullet(f"{i}. {step}")

    pdf.section_title("5. Commands")
    pdf.table(
        ["Command", "Purpose"],
        [
            ["hdfs dfs -mkdir -p /user/lab6/input", "Create input directory"],
            ["hdfs dfs -put input.txt /user/lab6/input", "Upload input"],
            ["javac -classpath $(hadoop classpath) ...", "Compile WordCount.java"],
            ["jar cf wordcount.jar -C build .", "Package classes into JAR"],
            ["hadoop jar wordcount.jar WordCount in out", "Run the job"],
            ["hadoop jar ... -D wordcount.skip.stopwords=true", "Run with stopword filter"],
            ["hdfs dfs -cat out/part-r-00000", "View output"],
            ["hdfs dfs -rm -r out", "Delete old output (must not exist)"],
        ],
        [95, 85],
    )

    pdf.section_title("6. Sample Output (input.txt)")
    pdf.table(
        ["Word", "Count", "Word", "Count"],
        [
            ["a", "1", "hadoop", "2"],
            ["big", "2", "is", "1"],
            ["data", "2", "mapreduce", "2"],
            ["efficiently", "1", "processes", "1"],
            ["framework", "1", "uses", "1"],
        ],
        [50, 40, 50, 40],
    )
    pdf.body("Total words = 14, unique words = 10. Counters: Map output records = 14, Combine output records = 10, Reduce output records = 10.")

    pdf.add_page()
    pdf.section_title("7. Exercise Answers")
    pdf.sub_title("Exercise 1: Modify input and observe output")
    pdf.body(
        "Two lines were added (HDFS stores big data in blocks. / Hadoop is open source and Hadoop is scalable.). "
        "Total words grew from 14 to 28 and unique words from 10 to 18. hadoop: 2 -> 4, is: 1 -> 3, big and data: 2 -> 3."
    )
    pdf.sub_title("Exercise 2: Ignore common words")
    pdf.body(
        "The Mapper checks a STOPWORDS set (a, an, the, is, and, in, of, ...) when the job property "
        "wordcount.skip.stopwords=true is passed with -D. Words a, and, in, is disappeared from the output; "
        "Map output records dropped from 28 to 22."
    )
    pdf.sub_title("Exercise 3: Run on another text file")
    pdf.body(
        "another.txt (4 lines about data science and Hadoop) produced 39 words, 29 unique. "
        "Top words: data (4), the (4), and (3), distributed (2), science (2). The same JAR works on any text input."
    )
    pdf.sub_title("Exercise 4: Compare before vs after")
    pdf.body(
        "Joining the two outputs on word shows unchanged words (mapreduce, framework, uses...), increased words "
        "(hadoop +2, is +2, big +1, data +1), and new words (hdfs, blocks, open, source, scalable, stores, and, in)."
    )
    pdf.sub_title("Exercise 5: Role of Mapper and Reducer")
    pdf.bullet("Mapper: splits each line into words and emits (word, 1). Runs in parallel on every input split; it does no counting across lines.")
    pdf.bullet("Shuffle/Sort: groups identical words together and delivers them to the same Reducer.")
    pdf.bullet("Reducer: adds up all the 1s for a word to produce its final frequency.")
    pdf.bullet("Combiner: same logic as the Reducer applied locally to cut network traffic.")

    pdf.add_page()
    pdf.section_title("8. Viva Q&A")
    qa = [
        ("What is MapReduce?", "A programming model that processes data in parallel using a Map phase and a Reduce phase."),
        ("What does the Mapper emit in Word Count?", "(word, 1) for every word in the line."),
        ("What does the Reducer do?", "Sums the list of counts for each word and writes (word, total)."),
        ("What is a Combiner?", "A local reducer on the map side that reduces data transfer. It must be associative and commutative."),
        ("What is Shuffle and Sort?", "The framework phase that transfers Mapper output to Reducers, grouped and sorted by key."),
        ("Why Text and IntWritable?", "Hadoop needs serializable Writable types to move data between nodes."),
        ("Input format used?", "TextInputFormat: key = byte offset (LongWritable), value = line (Text)."),
        ("Why must the output directory not exist?", "Hadoop refuses to overwrite output to avoid accidentally losing results."),
        ("What is part-r-00000?", "Output file written by Reducer number 0. One file per reducer."),
        ("What is _SUCCESS?", "Empty marker file written when the job finishes successfully."),
        ("How many mappers run?", "Roughly one per input split (block). A small file gives one mapper."),
        ("How did you skip stopwords?", "Passed -D wordcount.skip.stopwords=true; the Mapper reads it from the Configuration in setup()."),
        ("What is ToolRunner?", "Helper that parses generic options like -D before calling run(), so properties reach the job Configuration."),
        ("Applications of Word Count?", "Search indexing, log analysis, text mining, trending topics, document similarity."),
    ]
    for q, a in qa:
        pdf.qa_block(q, a)

    pdf.section_title("9. One-Line Definitions")
    for term, defn in [
        ("Mapper", "Converts input records into (key, value) pairs"),
        ("Reducer", "Aggregates all values for a key"),
        ("Combiner", "Map-side local aggregation"),
        ("Partitioner", "Decides which Reducer gets a key"),
        ("Shuffle", "Moves map output to reducers"),
        ("Job", "One complete MapReduce program run"),
        ("InputSplit", "Chunk of input handled by one Mapper"),
        ("Writable", "Hadoop serialization interface"),
        ("Driver", "Class that configures and submits the job"),
        ("LocalJobRunner", "Runs MapReduce in a single JVM for testing"),
    ]:
        pdf.term_block(term, defn)

    out = Path("/Users/ojas/Desktop/DS Lab/Experiment6/Theory_and_Formulae.pdf")
    pdf.output(str(out))
    print("Wrote", out)


if __name__ == "__main__":
    generate()

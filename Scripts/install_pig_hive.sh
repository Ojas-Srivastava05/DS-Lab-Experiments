#!/usr/bin/env bash
# Downloads and extracts Apache Pig 0.18.0 and Apache Hive 4.2.1 into $HOME
# (paths without spaces, next to ~/hadoop-3.4.1), plus the Kaggle Titanic CSV.
set -euo pipefail

MIRROR="https://dlcdn.apache.org"
MAVEN="https://repo1.maven.org/maven2"
PIG_HOME="$HOME/pig-0.18.0"
PIG_JARS=(
    "org/apache/pig/pig/0.18.0/pig-0.18.0.jar"
    "org/apache/pig/piggybank/0.18.0/piggybank-0.18.0.jar"
    "org/antlr/antlr-runtime/3.4/antlr-runtime-3.4.jar"
    "dk/brics/automaton/automaton/1.11-8/automaton-1.11-8.jar"
    "joda-time/joda-time/2.14.0/joda-time-2.14.0.jar"
    "jline/jline/2.11/jline-2.11.jar"
    "org/codehaus/jackson/jackson-core-asl/1.9.13/jackson-core-asl-1.9.13.jar"
    "org/codehaus/jackson/jackson-mapper-asl/1.9.13/jackson-mapper-asl-1.9.13.jar"
)
HIVE_URL="$MIRROR/hive/hive-4.2.1/apache-hive-4.2.1-bin.tar.gz"
TITANIC_URL="https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
DATASET="/Users/ojas/Desktop/DS Lab/Shared/Titanic-Dataset.csv"

log() { printf '\n[%s] %s\n' "$(date +%H:%M:%S)" "$*"; }

download() {
    local url="$1" out="$2"
    log "Downloading $(basename "$url")"
    curl -L --fail --retry 5 --retry-delay 3 -C - --progress-bar -o "$out" "$url"
    log "Done: $(du -h "$out" | cut -f1) -> $out"
}

log "Step 1/5: Pig 0.18.0 jars from Maven Central -> $PIG_HOME/lib"
mkdir -p "$PIG_HOME/lib"
i=0
for jar in "${PIG_JARS[@]}"; do
    i=$((i + 1))
    name=$(basename "$jar")
    if [ -s "$PIG_HOME/lib/$name" ]; then
        echo "  [$i/${#PIG_JARS[@]}] $name (already present)"
    else
        echo "  [$i/${#PIG_JARS[@]}] $name"
        curl -L --fail --retry 5 -s -o "$PIG_HOME/lib/$name" "$MAVEN/$jar"
    fi
done
if [ ! -s "$PIG_HOME/lib/roaringbitmap-shaded-pig.jar" ]; then
    # Pig's MapReduce mode needs RoaringBitmap relocated to org.apache.pig.org.roaringbitmap
    # (bundled in the release tarball, but not in the Maven jar)
    log "Relocating RoaringBitmap for Pig MapReduce mode"
    curl -sfL -o /tmp/jarjar.jar "$MAVEN/com/googlecode/jarjar/jarjar/1.3/jarjar-1.3.jar"
    curl -sfL -o /tmp/roaring.jar "$MAVEN/org/roaringbitmap/RoaringBitmap/0.6.66/RoaringBitmap-0.6.66.jar"
    echo "rule org.roaringbitmap.** org.apache.pig.org.roaringbitmap.@1" > /tmp/jarjar-rules.txt
    /opt/homebrew/opt/openjdk@17/bin/java -jar /tmp/jarjar.jar process /tmp/jarjar-rules.txt \
        /tmp/roaring.jar "$PIG_HOME/lib/roaringbitmap-shaded-pig.jar"
fi
log "Pig jars ready: $(du -sh "$PIG_HOME/lib" | cut -f1)"

log "Step 2/5: Hive 4.2.1"
if [ -d "$HOME/apache-hive-4.2.1-bin" ]; then
    log "Already extracted at ~/apache-hive-4.2.1-bin, skipping"
else
    download "$HIVE_URL" /tmp/hive.tgz
    log "Verifying SHA-256"
    expected=$(curl -sL "$HIVE_URL.sha256" | awk '{print $1}')
    actual=$(shasum -a 256 /tmp/hive.tgz | awk '{print $1}')
    [ "$expected" = "$actual" ] && log "Checksum OK" || { log "Checksum MISMATCH"; exit 1; }
    log "Extracting Hive to ~/apache-hive-4.2.1-bin"
    tar xzf /tmp/hive.tgz -C "$HOME"
fi

log "Step 3/5: Titanic-Dataset.csv"
curl -sL --fail -o "$DATASET" "$TITANIC_URL"
log "Saved $(wc -l < "$DATASET" | tr -d ' ') lines -> $DATASET"

log "Step 4/5: Versions"
export JAVA_HOME=/opt/homebrew/opt/openjdk@17/libexec/openjdk.jdk/Contents/Home
export HADOOP_HOME="$HOME/hadoop-3.4.1"
java -cp "$PIG_HOME/lib/*:$("$HADOOP_HOME/bin/hadoop" classpath)" org.apache.pig.Main -version 2>/dev/null | head -1 || true
ls "$HOME/apache-hive-4.2.1-bin/lib" | grep -m1 '^hive-exec'

log "Step 5/5: Cleaning up tarballs"
rm -f /tmp/hive.tgz
log "ALL DONE"

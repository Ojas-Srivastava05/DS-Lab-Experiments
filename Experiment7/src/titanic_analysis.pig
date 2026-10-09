-- Experiment 7: Data processing and analysis of the Titanic dataset using Apache Pig
-- Run: pig -x mapreduce -param INPUT=<hdfs csv> -param OUTPUT=<hdfs dir> -param PIGGYBANK=<jar> titanic_analysis.pig

REGISTER '$PIGGYBANK';

-- 1. LOAD the dataset from HDFS (CSVExcelStorage handles quoted names like "Braund, Mr. Owen Harris")
titanic = LOAD '$INPUT'
    USING org.apache.pig.piggybank.storage.CSVExcelStorage(',', 'NO_MULTILINE', 'UNIX', 'SKIP_INPUT_HEADER')
    AS (PassengerId:int, Survived:int, Pclass:int, Name:chararray, Sex:chararray,
        Age:double, SibSp:int, Parch:int, Ticket:chararray, Fare:double,
        Cabin:chararray, Embarked:chararray);

-- 2. DISPLAY the first 5 records
first_five = LIMIT titanic 5;
DUMP first_five;

-- 3. FILTER: passengers who survived
survivors = FILTER titanic BY Survived == 1;
survivor_total = FOREACH (GROUP survivors ALL) GENERATE 'survivors' AS label, COUNT(survivors) AS total;
DUMP survivor_total;

-- 4. GROUP by passenger class
by_class = GROUP titanic BY Pclass;

-- 5. COUNT passengers (plus survivors and average fare) in each class
class_stats = FOREACH by_class GENERATE
    group AS Pclass,
    COUNT(titanic) AS passengers,
    SUM(titanic.Survived) AS survived,
    ROUND_TO(AVG(titanic.Fare), 2) AS avg_fare;

-- 6. ORDER the result by number of passengers (descending)
sorted_stats = ORDER class_stats BY passengers DESC;
DUMP sorted_stats;

-- 7. STORE the processed output back into HDFS
STORE sorted_stats INTO '$OUTPUT' USING PigStorage(',');

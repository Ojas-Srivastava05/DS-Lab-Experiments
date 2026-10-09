-- Experiment 7 exercises (Titanic dataset, Apache Pig)
-- Run: pig -x mapreduce -param INPUT=<hdfs csv> -param OUT_DIR=<hdfs dir> -param PIGGYBANK=<jar> exercises.pig

REGISTER '$PIGGYBANK';

titanic = LOAD '$INPUT'
    USING org.apache.pig.piggybank.storage.CSVExcelStorage(',', 'NO_MULTILINE', 'UNIX', 'SKIP_INPUT_HEADER')
    AS (PassengerId:int, Survived:int, Pclass:int, Name:chararray, Sex:chararray,
        Age:double, SibSp:int, Parch:int, Ticket:chararray, Fare:double,
        Cabin:chararray, Embarked:chararray);

-- Exercise 1: only female passengers
females = FILTER titanic BY Sex == 'female';
female_view = FOREACH females GENERATE PassengerId, Name, Pclass, Age, Fare, Survived;
STORE female_view INTO '$OUT_DIR/ex1_female_passengers' USING PigStorage('\t');

-- Exercise 2: number of passengers in each class
by_class = GROUP titanic BY Pclass;
class_count = FOREACH by_class GENERATE group AS Pclass, COUNT(titanic) AS passengers;
class_count_sorted = ORDER class_count BY Pclass ASC;
STORE class_count_sorted INTO '$OUT_DIR/ex2_class_count' USING PigStorage('\t');

-- Exercise 3: passengers sorted by Fare (highest first)
fare_view = FOREACH titanic GENERATE PassengerId, Name, Pclass, Fare;
by_fare = ORDER fare_view BY Fare DESC, PassengerId ASC;
STORE by_fare INTO '$OUT_DIR/ex3_sorted_by_fare' USING PigStorage('\t');

-- Exercise 4: processed output (female survival by class) stored in a new HDFS directory
female_by_class = GROUP females BY Pclass;
female_summary = FOREACH female_by_class GENERATE
    group AS Pclass,
    COUNT(females) AS female_passengers,
    SUM(females.Survived) AS female_survivors,
    ROUND_TO((double) SUM(females.Survived) * 100.0 / COUNT(females), 2) AS survival_pct;
female_summary_sorted = ORDER female_summary BY Pclass ASC;
STORE female_summary_sorted INTO '$OUT_DIR/ex4_female_summary' USING PigStorage(',');

-- Exercise 5: FILTER (removes rows) vs FOREACH (transforms columns)
filter_demo = FILTER titanic BY Age > 70.0;
foreach_demo = FOREACH filter_demo GENERATE Name, Age, UPPER(Sex) AS sex_upper, Fare * 2 AS double_fare;
STORE filter_demo INTO '$OUT_DIR/ex5_filter_demo' USING PigStorage('\t');
STORE foreach_demo INTO '$OUT_DIR/ex5_foreach_demo' USING PigStorage('\t');

-- Experiment 8: create the Hive database and Titanic tables, then load the dataset from HDFS

-- 1. Create a database
CREATE DATABASE IF NOT EXISTS titanic_db;
USE titanic_db;

DROP TABLE IF EXISTS titanic;
DROP TABLE IF EXISTS titanic_raw;

-- 2. Staging table: OpenCSVSerde understands quoted fields such as "Braund, Mr. Owen Harris"
CREATE TABLE titanic_raw (
    PassengerId STRING, Survived STRING, Pclass STRING, Name STRING, Sex STRING,
    Age STRING, SibSp STRING, Parch STRING, Ticket STRING, Fare STRING,
    Cabin STRING, Embarked STRING
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES ("separatorChar" = ",", "quoteChar" = "\"")
STORED AS TEXTFILE
TBLPROPERTIES ("skip.header.line.count" = "1");

-- 3. Load the dataset from HDFS into the staging table
LOAD DATA INPATH '/user/lab8/titanic/Titanic-Dataset.csv' INTO TABLE titanic_raw;

-- 4. Typed table used for analysis (empty Age/Cabin/Embarked become NULL).
--    The WHERE clause drops the CSV header row, which the MapReduce CTAS job does not skip.
CREATE TABLE titanic STORED AS ORC AS
SELECT
    CAST(PassengerId AS INT)              AS passengerid,
    CAST(Survived AS INT)                 AS survived,
    CAST(Pclass AS INT)                   AS pclass,
    Name                                  AS name,
    Sex                                   AS sex,
    CAST(NULLIF(Age, '') AS DOUBLE)       AS age,
    CAST(SibSp AS INT)                    AS sibsp,
    CAST(Parch AS INT)                    AS parch,
    Ticket                                AS ticket,
    CAST(Fare AS DOUBLE)                  AS fare,
    NULLIF(Cabin, '')                     AS cabin,
    NULLIF(Embarked, '')                  AS embarked
FROM titanic_raw
WHERE PassengerId <> 'PassengerId';

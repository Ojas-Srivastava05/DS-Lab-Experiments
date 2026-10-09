-- Experiment 8 exercises (HiveQL on titanic_db.titanic)
USE titanic_db;

-- Exercise 1: display only female passengers
SELECT passengerid, name, pclass, age, fare, survived
FROM titanic
WHERE sex = 'female'
ORDER BY passengerid;

-- Exercise 2: average fare for each passenger class
SELECT pclass, COUNT(*) AS passengers, ROUND(AVG(fare), 2) AS avg_fare
FROM titanic
GROUP BY pclass
ORDER BY pclass;

-- Exercise 3: number of passengers who survived
SELECT COUNT(*) AS survived_passengers
FROM titanic
WHERE survived = 1;

-- Exercise 4: passengers sorted by age (descending, unknown ages excluded)
SELECT passengerid, name, sex, pclass, age
FROM titanic
WHERE age IS NOT NULL
ORDER BY age DESC, passengerid ASC;

-- Exercise 5: maximum and minimum fare
SELECT MAX(fare) AS max_fare, MIN(fare) AS min_fare
FROM titanic;

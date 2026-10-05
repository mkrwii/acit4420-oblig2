# ACIT4420 - assignment 2
## Project title: Fitness Data Analysis Application
## Chosen alternative: 
A
## Student: 
Magnus K Wiik
## Student no: 
374992
## Disclaimer:
The file data_generator.py is not my work, and is included for convenience. The file was handed out on Canvas.
This project is essentially a fork of assignment 1, and will contain similar and/or duplicate code.
## Description:
This application uses Python OOP to structure, classify and present exercise data. The classes are defined in classes.py, where most of the logic is handled. tests.py and main.py provide two different ways of running the program. Synthetic data is provided by the data generator (see the above disclaimer), and processed as a shared service for main and tests in sample_data.py

The project does not use external libraries, and the provided requirements.txt is thus empty.

## Class design and responsibilities:
All classes contained in classes.py
Participant: Plain class representing the participant and their reference values
Observation: Represents a single observation. Responsible for validating data integrity, will dismiss impossible values
Session: Represents a group of Observations, connected to a single Participant. Responsible for storing these observations securely
SessionClassifier: Stores the logic for classifying a Session.

## Relations between classes: 
See next paragraph.

## Where composition, encapsulation, inheritance and overriding are represented:
The core of this assignment is to group together observations into sessions. This lends itself particularly well to composition: Observations constitute a Session, where one Participant participates, and one SessionClassifier classifies. Therefore, there are no examples of inheritance and overriding in this assignment. Encapsulation is done with the __observations attribute in Session. Observations that are already validated should not be changed, and the Session class only provides methods to add observations and retrieve observations and the number of observations in a Session.

## Assumptions and classification rules:
The primary assumption is that heart rate is the primary indicator for how hard a session is. Testing of the solution with the provided synthetic data has confirmed this. We rate a session as hard if it has an increase of at least 50% from the participants' reference value. A medium session requires more than 15% increase in the heart rate. Anything below this is seen as a Resting session. A session is rejected as insufficient if it either contains fewer than 3 valid observations, or if the signal quality is at less than 65%. In addition, a session is classified as recovering if the heart rate is at least 20% lower in the second half than in the first half. These percentages can be changed, see below.

The application does, as per its specifications, compare the skin response and temperature to the reference values of the participant, but this is a pure comparison, and it does not affect the classification.

## Exact installation and running instructions:
install: `git clone github.com/mkrwii/acit4420-oblig2`
running: run as prescribed in the assignment: `python3 main.py --profiles data/participants.csv --sessions data/fitness_sessions.csv --output output`

## Example output:
three files:
analysis_report.txt - readable reports from the sessions (similar to output from Oblig 1)
analys_summary.csv - machine-readable sessions
rejected_records.txt - error messages

## Known limitations:
The classification is not quite 100% accurate, and very rarely, a scenario that the data generator sees as "high" will be classified as "medium". However, the current tuning of the threshold values makes this a very rare occurrence.

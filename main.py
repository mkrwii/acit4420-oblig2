from classes import *
import data_generator as dg
import sample_data as sd
from filecontroller import readFitnessCSV

scenarios = dg.available_scenarios()

def main():
    readFitnessCSV("fitness_sessions.csv")
'''for scenario in scenarios:
        participant, session = sd.getScenarioData(scenario)
        result = SessionClassifier(session).getResult()
        printParticipantData(participant)
        printSessionReport(session, participant, result)
'''

if __name__ == "__main__":
    main()
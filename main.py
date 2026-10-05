from classes import *
from filecontroller import readSessionCSV, readParticipantCSV, writeAnalysisOutput, InvalidRecordError
import argparse

def handleargs():
    parser = argparse.ArgumentParser()
    parser.add_argument(
    "--profiles",
    required=True,
    help="Path to participant CSV file"
    )
    parser.add_argument(
    "--sessions",
    required=True,
    help="Path to session CSV file"
    )
    parser.add_argument(
    "--output",
    required=True,
    help="Output directory"
    )
    return parser.parse_args()

def main():
    sessions = None
    args = handleargs()
    participants, participant_errors = readParticipantCSV(args.profiles)
    try:
        sessions, session_errors = readSessionCSV(args.sessions, participants)
    except InvalidRecordError as e:
        print(f"Invalid record: {e}")
        sessions = None
    if participants:
        for p in participants:
            printParticipantData(p)
    else:
        print("There are no valid participants in the file provided.")
    if sessions:
        errors = participant_errors + session_errors
        writeAnalysisOutput(sessions, errors, args.output)
    else:
        print("There are no valid sessions in the file provided.")
'''for scenario in scenarios:
        participant, session = sd.getScenarioData(scenario)
        result = SessionClassifier(session).getResult()
        printParticipantData(participant)
        printSessionReport(session, participant, result)
'''

if __name__ == "__main__":
    main()
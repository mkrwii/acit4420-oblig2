from fitness.classes import *
from fitness.filecontroller import readSessionCSV, readParticipantCSV, writeAnalysisOutput
from fitness.exceptions import InvalidRecordError
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
    try:
        participants, participant_errors = readParticipantCSV(args.profiles)
    except KeyError as e:
        print(f"The profiles file is not compatible, it lacks (at least) the key {e}")
        return
    try:
        sessions, session_errors, lines = readSessionCSV(args.sessions, participants)
    except InvalidRecordError as e:
        print(f"Invalid record: {e}")
        sessions = None
    if not participants:
        print("There are no valid participants in the file provided.")
    if sessions:
        errors = participant_errors + session_errors
        created_files = writeAnalysisOutput(sessions, errors, args.output)
    else:
        print("There are no valid sessions in the file provided.")
    print(f"accepted observation rows: {lines - len(session_errors)}")
    print(f"rejected observation rows: {len(session_errors)}")
    print(f"number of files created: {created_files}")

if __name__ == "__main__":
    main()
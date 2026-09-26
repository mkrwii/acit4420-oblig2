import csv
import classes

DATA_FOLDER = "data/"
def readParticipantCSV(filename):
    participants = []
    path = DATA_FOLDER + filename
    with open(path, "r") as f:
        data = csv.DictReader(f)
        for row in data:
            participant = classes.Participant(
                    participant_id=row["participant_id"],
                    name=row["name"],
                    ref_heart_rate=row["baseline_heart_rate"],
                    ref_skin_response=row["baseline_skin_response"],
                    ref_temperature=row["baseline_temperature"],
                )
            print(f"Added participant {participant.participant_id}")
            participants.append(participant)
        return participants

def readSessionCSV(filename):
    path = DATA_FOLDER + filename
    with open(path, "r") as f:
        data = csv.DictReader(f)
        for row in data:
            print(row)


def main():
    print("This file is not intended to be run. Import it instead!")


if __name__ == "__main__":
    main()
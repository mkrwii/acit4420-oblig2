import csv
import classes

DATA_FOLDER = "data/"
def readParticipantCSV(filename):
    path = DATA_FOLDER + filename
    with open(path, "r") as f:
        data = csv.DictReader(f)
        for row in data:
            participant = classes.Participant(
                    participant_id=row["participant_id"],
                    ref_heart_rate=row["baseline_heart_rate"],
                    ref_skin_response=row["baseline_skin_response"],
                    ref_temperature=row["baseline_temperature"],
                    ref_activity_level=row.get("baseline_activity_level", 0.2),
                )
            classes.printParticipantData(participant)

def readSessionCSV(filename):
    path = DATA_FOLDER + filename
    with open(path, "r") as f:
        data = csv.DictReader(f)
        for row in data:
            print(row)
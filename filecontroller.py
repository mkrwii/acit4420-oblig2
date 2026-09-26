import csv
import classes

#this is the folder where the data files are stored
DATA_FOLDER = "data/"


def readParticipantCSV(filename):
    '''
    Reads participant data from a CSV file, and returns a list of Participant objects.
    '''
    
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
    '''
    Reads session data from a CSV file, and returns a list of Session objects.
    '''
    path = DATA_FOLDER + filename
    rawobservations = []
    with open(path, "r") as f:
        data = csv.DictReader(f)
        for row in data:
            observation = classes.Observation(
                    timestamp=int(row["timestamp"]),
                    heart_rate=float(row["heart_rate"]),
                    skin_response=float(row["skin_response"]),
                    temperature=float(row["temperature"]),
                    activity_level=float(row["activity_level"]),
                    signal_quality=float(row["signal_quality"])
                )
            rawobservations.append(observation)
        return rawobservations
            


def main():
    print("This file is not intended to be run. Import it instead!")


if __name__ == "__main__":
    main()
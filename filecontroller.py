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

def readSessionCSV(filename, participants):
    '''
    Reads observation data from a CSV file, grouped into Session objects
    and linked to their matching Participant from the given list.
    '''
    path = DATA_FOLDER + filename
    participants_by_id = {p.participant_id: p for p in participants}

    sessions = []
    raw_obs = []
    current_session_id = None

    with open(path, "r") as f:
        data = csv.DictReader(f)
        for row in data:
            if row.get("session_id") == current_session_id:
                raw_obs.append(row)
            else:
                if raw_obs:
                    sessions.append(_build_session(current_session_id, raw_obs, participants_by_id))
                current_session_id = row.get("session_id")
                raw_obs = [row]

    if raw_obs:
        sessions.append(_build_session(current_session_id, raw_obs, participants_by_id))

    return sessions or None


def _build_session(session_id, rows, participants_by_id):
    '''
    Converts a group of raw CSV rows (all sharing one session_id) into a
    Session object populated with validated Observation objects.
    '''
    participant_id = rows[0].get("participant_id")
    participant = participants_by_id.get(participant_id)
    if participant is None:
        print(f"Skipping session {session_id}: unknown participant {participant_id}")
        return None

    timestamps = [int(row["timestamp"]) for row in rows]
    session = classes.Session(
        session_id=session_id,
        participant=participant,
        start_time=min(timestamps),
        end_time=max(timestamps),
    )

    for row in rows:
        try:
            observation = classes.Observation(
                timestamp=int(row["timestamp"]),
                heart_rate=float(row["heart_rate"]),
                skin_response=float(row["skin_response"]),
                temperature=float(row["temperature"]),
                activity_level=float(row["activity_level"]),
                signal_quality=float(row["signal_quality"]),
            )
            session.addObservation(observation)
        except ValueError as e:
            print(f"Skipped invalid observation in session {session_id}: {e}")

    return session


def main():
    print("This file is not intended to be run. Import it instead!")


if __name__ == "__main__":
    main()
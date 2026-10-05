import csv
from pathlib import Path
import classes

class InvalidRecordError(ValueError):
    """Raised when a CSV record cannot be accepted."""


from pathlib import Path
import csv
import classes


def writeAnalysisOutput(sessions, rejected_records, output_dir):
    """
    Creates:
        analysis_summary.csv
        analysis_report.txt
        rejected_records.txt
    """

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    summary_file = output_path / "analysis_summary.csv"
    report_file = output_path / "analysis_report.txt"
    rejected_file = output_path / "rejected_records.txt"

    # analysis_summary.csv
    with open(summary_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        writer.writerow([
            "session_id",
            "participant_id",
            "classification",
            "reason",
            "usable_observations",
            "avg_heart_rate",
            "skin_response",
            "temperature"
        ])

        for session in sessions:
            result = classes.SessionClassifier(session).getResult()

            writer.writerow([
                session.session_id,
                session.participant.participant_id,
                result["classification"],
                result["reason"],
                result["usable_observations"],
                result["avg_heart_rate"],
                result["skin_response"],
                result["temperature"]
            ])

    # analysis_report.txt
    with open(report_file, "w", encoding="utf-8") as f:
        for session in sessions:
            result = classes.SessionClassifier(session).getResult()

            f.write("----- SESSION REPORT -----\n")
            f.write(f"Participant: {session.participant.name}\n")
            f.write(f"Participant ID: {session.participant.participant_id}\n")
            f.write(f"Session ID: {session.session_id}\n")
            f.write(f"Classification: {result['classification']}\n")
            f.write(f"Reason: {result['reason']}\n")
            f.write(f"Usable observations: {result['usable_observations']}\n")
            f.write(f"Average heart rate: {result['avg_heart_rate']}\n")
            f.write(f"Skin response: {result['skin_response']}\n")
            f.write(f"Temperature: {result['temperature']}\n")
            f.write("\n")

    # rejected_records.txt
    with open(rejected_file, "w", encoding="utf-8") as f:
        if rejected_records:
            for record in rejected_records:
                f.write(record + "\n")
        else:
            f.write("No rejected records.\n")

    return 3


def readParticipantCSV(filename):
    '''
    Reads participant data from a CSV file, and returns a list of Participant objects.
    '''
    
    participants = []
    errors = []
    path = filename
    with open(path, "r", encoding="utf-8", newline="") as f:
        data = csv.DictReader(f)
        for row in data:
            try:
                participant = classes.Participant(
                        participant_id=row["participant_id"],
                        name=row["name"],
                        ref_heart_rate=int(row["baseline_heart_rate"]),
                        ref_skin_response=float(row["baseline_skin_response"]),
                        ref_temperature=float(row["baseline_temperature"]),
                    )
                print(f"Added participant {participant.participant_id}")
                participants.append(participant)
            except ValueError as e:
                errors.append(f"{filename}: participant {row.get('participant_id')} - {e}")
        return participants, errors


def readSessionCSV(filename, participants):
    '''
    Reads observation data from a CSV file, grouped into Session objects
    and linked to their matching Participant from the given list.
    '''
    path = filename
    participants_by_id = {p.participant_id: p for p in participants}

    sessions = []
    errors = []
    raw_obs = []
    current_session_id = None

    with open(path, "r", encoding="utf-8", newline="") as f:
        data = csv.DictReader(f)
        for row in data:
            missing = [k for k, v in row.items()if v is None or v.strip() == ""]
            if missing:
                errors.append(f"{filename}: session {row.get('session_id')} - "f"Missing values for columns: {', '.join(missing)}")
                continue
            if row.get("session_id") == current_session_id:
                raw_obs.append(row)
            else:
                if raw_obs:
                    try:
                        session = _build_session(current_session_id, raw_obs, participants_by_id, errors)
                        if session is not None:
                            sessions.append(session)
                    except classes.InvalidIdentifierError as e:
                        errors.append(f"{row.get('session_id')}: {e}")
                current_session_id = row.get("session_id")
                raw_obs = [row]

    if raw_obs:

        session = _build_session(current_session_id, raw_obs, participants_by_id, errors)
        if session is not None:
            sessions.append(session)

    return sessions or None, errors


def _build_session(session_id, rows, participants_by_id, errors):
    '''
    Converts a group of raw CSV rows (all sharing one session_id) into a
    Session object populated with validated Observation objects.
    '''
    participant_id = rows[0].get("participant_id")
    participant = participants_by_id.get(participant_id)
    if participant is None:
        errors.append(f"{session_id}: unknown participant {participant_id}")
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
            errors.append(f"{session_id}: invalid observation - {e}")
    return session


def main():
    print("This file is not intended to be run. Import it instead!")


if __name__ == "__main__":
    main()
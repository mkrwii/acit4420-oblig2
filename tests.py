
from fitness.classes import *
from fitness.filecontroller import readParticipantCSV


def test():

    baddata = readParticipantCSV("data/fitness_sessions_invalid.csv")
    participants = readParticipantCSV("data/participants.csv")
    

    # test case 1: valid data
    assert len(participants[0]) == 3, f": expected 3, got {len(participants[0])}"
    print("Test case valid data PASSED")

    # test case 2: missing data
    assert len(readParticipantCSV("data/bogusdata.csv")[0]) == 0, f": expected higher than 0, got {len(readParticipantCSV("data/bogusdata.csv")[0])}"
    print("Test case missing data PASSED")

    # test case 3: invalid data
    assert len(baddata[1]) > 0, f": expected higher than 0, got {len(baddata[1])}"
    print("Test case invalid data PASSED")

    # test case 4: boundaries (one just above the threshold for validation, the other below)
    upper = Observation(
    timestamp=1,
    heart_rate=35,       # exactly at the valid minimum — should construct successfully
    skin_response=1.0,
    temperature=36.0,
    activity_level=0.2,
    signal_quality=0.9,
    )
    assert upper.heart_rate == 35
    print("upper boundary test PASSED")

    try:
        lower = Observation(
            timestamp=1,
            heart_rate=34,    # one below the valid minimum — should be rejected
            skin_response=1.0,
            temperature=36.0,
            activity_level=0.2,
            signal_quality=0.9,
        )
        assert False, "lower (heart_rate=34) should have raised ValueError but did not"
    except ValueError:
        print("lower boundary PASSED")

if __name__ == "__main__":
    print("--- Runnning tests: ---")
    test()
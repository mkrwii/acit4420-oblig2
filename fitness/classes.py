import re
from . import exceptions

class Observation:
    '''
    Checks for impossible values on object creation, as impossible data is unwanted.
    '''
    def __init__(self, timestamp, heart_rate, skin_response, temperature, activity_level, signal_quality):
        if isinstance(timestamp, int) and timestamp >= 0:
            self.timestamp = timestamp
        else:
            raise ValueError(f"Observation failed! {timestamp} is not a valid timestamp.")
        if isinstance(heart_rate, (int,float)) and 35 <= heart_rate <= 205:
            self.heart_rate = heart_rate
        else:
            raise ValueError(f"Observation failed! {heart_rate} is not a valid heart rate.")
        if isinstance(skin_response, (int,float)) and 0 <= skin_response:
            self.skin_response = skin_response
        else:
            raise ValueError(f"Observation failed! {skin_response} is not a valid skin response.")
        if isinstance(temperature, (int,float)) and 25 <= temperature <= 42:
            self.temperature = temperature
        else:
            raise ValueError(f"Observation failed! {temperature} is not a valid temperature.")
        if isinstance(activity_level, (int,float)) and 0 <= activity_level <= 1:
            self.activity_level = activity_level
        else:
            raise ValueError(f"Observation failed! {activity_level} is not a valid activity level.")
        if isinstance(signal_quality, (int,float)) and 0 <= signal_quality <= 1:
            self.signal_quality = signal_quality
        else:
            raise ValueError(f"Observation failed! {signal_quality} is not a valid activity level.")

class Participant:
    def __init__(self, participant_id, name,ref_heart_rate, ref_skin_response, ref_temperature):
        if isValidParticipant_id(participant_id):
            self.participant_id = participant_id
        else:
            raise exceptions.InvalidIdentifierError(f"Invalid identifier: {participant_id}")
        self.name = name
        if isinstance(ref_heart_rate, (int,float)) and 35 <= ref_heart_rate <= 205:
            self.ref_heart_rate = ref_heart_rate
        else:
            raise ValueError(f"Observation failed! {ref_heart_rate} is not a valid heart rate.")
        if isinstance(ref_skin_response, (int,float)) and 0 <= ref_skin_response:
            self.ref_skin_response = ref_skin_response
        else:
            raise ValueError(f"Observation failed! {ref_skin_response} is not a valid skin response.")
        if isinstance(ref_temperature, (int,float)) and 25 <= ref_temperature <= 42:
            self.ref_temperature = ref_temperature
        else:
            raise ValueError(f"Observation failed! {ref_temperature} is not a valid temperature.")


class Session:
    '''
    Stores the observations in a private list so that observations cannot be removed, but we are able to add new ones.
    '''
    def __init__(self, session_id, participant, start_time, end_time):
        if isValidSession_id(session_id):
            self.session_id = session_id
        else:
            raise exceptions.InvalidIdentifierError(f"Invalid identifier: {session_id}")
        self.participant = participant
        self.start_time = start_time
        self.end_time = end_time
        self.__observations = []
    def addObservation(self, observation):
        self.__observations.append(observation)
    def getObservations(self):
        return list(self.__observations)
    def getAverageHeartRate(self):
        if not self.__observations:
            return None
        values = [o.heart_rate for o in self.__observations]
        return sum(values) / len(values)
    def getNumberOfObservations(self):
        return len(self.__observations)


class SessionClassifier:
    '''
    Produces the classification, and handles 
    '''
    MIN_OBSERVATIONS_VALID = 3 # The minimum amount of observations required to classify a session
    RECOVERY_MARGIN = 0.20 # The decline in heart rate that triggers a recovery classification
    HIGH_HEART_RATE = 0.50 # The percentage of the baseline heart rate that is the lower bounds of high heart rate
    MEDIUM_HEART_RATE = 0.20 # Similarly, the lower bounds of what is medium heart rate
    MINIMUM_SIGNAL_QUALITY = 0.65 # An arbitrarily selected threshold for what is acceptable signal quality

    def __init__(self, session):
        self._session = session
        self._participant = session.participant
        self.category = self.classify()
        self.temperature = self.classifyTemperature()
        self.skinresponse = self.classifySkinResponse()
        
    def classifyTemperature(self):
        ref = self._participant.ref_temperature
        avg_temp = findAverage([o.temperature for o in self._session.getObservations()])
        if avg_temp is None:
            return "INSUFFICIENT"
        if avg_temp > ref: 
            return "HIGH"
        elif avg_temp < ref:
            return "NORMAL"
    
    def classifySkinResponse(self):
        ref = self._participant.ref_skin_response
        avg_skin = findAverage([o.skin_response for o in self._session.getObservations()])
        if avg_skin is None:
            return "INSUFFICIENT"
        if avg_skin > ref: 
            return "HIGH"
        elif avg_skin < ref:
            return "NORMAL"

    def classify(self):
        '''
        core classification logic
        '''
        if self._session.getNumberOfObservations() < self.MIN_OBSERVATIONS_VALID:
            self.reason = "FEW OBSERVATIONS"
            return "INSUFFICIENT"
        if findAverage([o.signal_quality for o in self._session.getObservations()]) < self.MINIMUM_SIGNAL_QUALITY:
            self.reason = "BAD DATA QUALITY"
            return "INSUFFICIENT"
        elif self._isRecovering():
            self.reason = "DECLINING HEART RATE"
            return "RECOVERY"
        elif self._isAboveBaseline(self._session.getAverageHeartRate(), self._participant.ref_heart_rate, self.HIGH_HEART_RATE):
            self.reason = "HIGH HEART RATE"
            return "HIGH"
        elif self._isAboveBaseline(self._session.getAverageHeartRate(), self._participant.ref_heart_rate, self.MEDIUM_HEART_RATE):
            self.reason = "MEDIUM HEART RATE"
            return "MEDIUM"
        else:
            self.reason = "LOW HEARTRATE"
            return "RESTING"
        
    def getResult(self):
        '''
        outputs a dictionary with the results, as specified in the assignment
        '''
        return{
            "classification": self.category,
            "reason": self.reason,
            "usable_observations": self._session.getNumberOfObservations(),
            "avg_heart_rate": self._session.getAverageHeartRate(),
            "skin_response": self.skinresponse,
            "temperature": self.temperature
        }
    
    @staticmethod
    def _isAboveBaseline(value, baseline, margin):
        '''
        determines if a value is over a threshold margin given a baseline
        static because it does not need the object itself to calculate
        '''
        return value > baseline * (1 + margin)
    
    def _isRecovering(self):
        '''
        Determines recovery sessions by finding out if the heart rate on average is higher in the first half of the session than in the second half.
        '''
        observations = self._session.getObservations()
        if len(observations) < self.MIN_OBSERVATIONS_VALID:
            return False
        mid = len(observations) // 2
        first_half = observations[:mid]
        second_half = observations[mid:]
        first_avg = findAverage([o.heart_rate for o in first_half])
        second_avg = findAverage([o.heart_rate for o in second_half])
        return isDeclining(first_avg, second_avg, self.RECOVERY_MARGIN)


# standalone functions

# helper functions

def findAverage(values):
    '''
    helper function to find the average of values
    '''
    if len(values) > 0:
        return sum(values) /len(values)
    else:
        return None


def isDeclining(value1, value2, margin):
    '''
    helper function that determines if there is a notable decline between two values, with a margin offset.
    '''
    decline = (value1 - value2) / value1
    return decline >= margin

# validation functions

def isValidParticipant_id(value):
    '''
    Checks whether value matches the required participant ID format: P followed by exactly three digits.
    '''
    return isinstance(value, str) and PARTICIPANT_ID_PATTERN.fullmatch(value) is not None


def isValidSession_id(value):
    '''
    Checks whether value matches the required session ID format: FIT-YYYY-NNN.
    '''
    return isinstance(value, str) and SESSION_ID_PATTERN.fullmatch(value) is not None

# printing functions

PARTICIPANT_ID_PATTERN = re.compile(r"^P\d{3}$")
SESSION_ID_PATTERN = re.compile(r"^FIT-\d{4}-\d{3}$")

def printSessionReport(session, participant, result):
    '''
    prints a classified session as a readable report
    '''
    print(f"--- SESSION REPORT ---")
    print(f"Participant id: {participant.participant_id}")
    print(f"Session ID: {session.session_id}")
    print(f"Usable Observations: {session.getNumberOfObservations()}")
    print(f"Average Heart rate: {session.getAverageHeartRate()} (Reference: {participant.ref_heart_rate})")
    print(f"Skin response: {result['skin_response']} (Reference: {participant.ref_skin_response})")
    print(f"Temperature: {result['temperature']} (Reference: {participant.ref_temperature})")
    print(f"Classification: {result["classification"]}")
    
def printParticipantData(participant):
    '''
    prints the participant's data in a readable format
    '''
    print(f"--- PARTICIPANT DATA ---")
    print(f"Name: {participant.name}")
    print(f"Participant id: {participant.participant_id}")
    print(f"Reference Heart rate: {participant.ref_heart_rate}")
    print(f"Reference Skin response: {participant.ref_skin_response}")
    print(f"Reference Temperature: {participant.ref_temperature}")

def printSessionData(session, participants):
    '''
    uses a Session object and a list of participants to print a single unclassified session in a readable format
    '''
    print(f"--- SINGLE SESSION ---")
    print(f"Session ID: {session.session_id}")
    print(f"Name: {session.participant.name}")
    print(f"Observations: {session.getNumberOfObservations()}")
    
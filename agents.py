import random

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Patient start~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#Patient agent
#attributes of: unique identifier, current state, patient satisfaction score
class Patient_agent:
    def __init__(self, id, patient_satisfaction, next_action, current_action, finished, arrived, will_arrive, arrival_time, assigned_consultant, bloods_appointment_time, consultant_1_appointment_time, consultant_2_appointment_time, time_waiting):
        #add satisafaction, and hw
        """
        id: unique id of patient
        current_day: current day count that is being modelled
        patient_satisfaction: score of patient satisfaction (similar to mood)
        next_action: the action that the patient will be doing next
        current_action: the action that the patient is currently doing
        duration: duration (in ticks) until the next action takes place (told by omnisystem)
        """
        self.id = id
        self.patient_satisfaction = patient_satisfaction
        self.next_action = next_action
        self.current_action = current_action
        self.arrived = arrived
        self.will_arrive = will_arrive
        self.arrival_time = arrival_time
        self.finished = finished
        #something to store all the actions it will do?
        self.assigned_consultant = assigned_consultant
        self.bloods_appointment_time = bloods_appointment_time
        self.consult_1_appointment_time = consultant_1_appointment_time
        self.consult_2_appointment_time = consultant_2_appointment_time
        self.time_waiting = time_waiting
        #self.hw = hw #heigght and weight
        pass


    def arrival_times(Patient_agent):#max 2 hrs early
        if_arrive = random.randint(1,100)
        if if_arrive >15: #!!!!!!!!!!!!!!!change to actual percentage:
            Patient_agent.will_arrive = True
        else:
            Patient_agent.will_arrive = False

        #if gonna arrive
        if Patient_agent.will_arrive == True:
            Patient_agent.arrival_time = random.randint(-16, 120) #-16 because can be up to 15mins late, if 16mins then classed as DNA
            if Patient_agent.arrival_time == -16:
                Patient_agent.will_arrive = False
        return(Patient_agent)


    #add later
    def leave(Patient_agent):
        if Patient_agent.current_action != "Appointed" or "Complete":
            if Patient_agent.patient_satisfaction <= 0:
                Patient_agent.current_action = "left_clinic"

        return(Patient_agent)
                

    #add later
    def update_satisfaction(patient_list):
        
        #if current action remains unchanged reduce patient_satisfaction by 0.25
        #if current action changes then patient_satisfaction increases by 10?
        print("hi")
        pass


#initialise the patient agent
def initialise_patient(counter):
    global patients
    
    patient_satisfaction = random.randint(30, 100) #(scale is 0 - 100)
    id = counter
    current_action = "Appointed"
        

    #need to give all the stuffs
    patient = Patient_agent(id, patient_satisfaction, "unknown", current_action, 0, False, False, "unknown", "unknown", "unkown", 0)
    Patient_agent.arrival_times(patient)

    return (patient)

"""
def update_patient(patient_list, id): # runs when called by omni system
    patient = patient_list[id-1] #!!!!!!cant do this because some patients might have been remove
    patient.current_action = patient.current_action
    patient.future_action = patient.future_action
    patient.duration = #
"""
    




#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~end patient stuff~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Nurse start~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

#Nurse agent (do i make this just a general nurse or specific to each)
#attributes of: type of nurse, unique identifier?, action doing/state

class Nurse_agent:
    def __init__(self, id, type, current_action, task_duration, patient_treating):
        self.id = id
        self.type = type #bloods only, h&w only, mixed
        self.current_action = current_action
        #self.next_action = next_action
        self.task_duration = task_duration
        self.patient_treating = patient_treating

    #def check_for_next_patient():
        #chooses which patient to call in next, if there is
        pass


def initialise_nurse(counter):
    global nurses

    id = counter
    type = random.choice(["Bloods", "HW"]) #rand choice from bloods, H&W (if bloods then can do both)
    current_action = "waiting" #could be calling patients, H&w, waiting, bloods - make sure matches nurse type
    nurse = Nurse_agent(id, type current_action, "unknown", "uknown")

    return (nurse)


"""
def update_nurse(nurse_list, patient_id, nurse_id): #runs when called by omni
    nurse = nurse_list[nurse_id-1]
    nurse.current_action = #omni
    nurse.task_duration = #omni
    nurse.patient_treating = patient_id
"""


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~end Nurse stuff~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Consultant start~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#


#Consultant agent 

class Consultant_agent:
    def __init__(self, id, current_action ,patient_treating, patients_seeing, duration, sick):
        self.id = id
        self.current_action = current_action
        self.patient_treating = patient_treating #current patient they're with
        self.patients_seeing = patients_seeing # patients on list to see today
        self.duration = duration #how logn with current patient
        self.sick = sick #if the consultant calls in sick or not


    #def check_for_next_patient_to_see():
        #check for which patient is here and closeset to appt time without skipping one


def initialise_consultant(counter):
    global consultants
    id = counter
    current_action = "waiting"
    sick = bool(random.choice([True, False]))
    consultant = Consultant_agent(counter, current_action, "unknown", [], "uknown", sick)

    return (consultant)


"""
def update_consultant(consultant_list, consultant_id, patient_id): # make sure not called if the consultant is sick
    consultant = consultant_list[consultant_id-1] #might not work if we remove a consutlant if theyre sick
    consultant.current_action = #omni
    consultant.patient_treating = patient_id #append to remove from list after seen
    consultant.duration = #omni
    consultant.patients_seeing = #updated to remove patient_id 
"""


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~end Consultant stuff~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

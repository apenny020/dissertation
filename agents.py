import random

#Patient agent
#attributes of: unique identifier, current state, patient satisfaction score
class Patient_agent:
    def __init__(self, id, patient_satisfaction, next_action, current_action, finished, arrived, assigned_consultant, bloods_appointment_time, first_consult_appointment_time, second_consult_appointment_time, time_waiting):
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
        #self.character = character
        #self.current_day = current_day
        self.patient_satisfaction = patient_satisfaction
        self.next_action = next_action
        self.current_action = current_action
        self.arrived = arrived
        #self.duration = duration
        self.finished = finished
        #something to store all the actions it will do?
        self.assigned_consultant = assigned_consultant
        self.bloods_appointment_time = bloods_appointment_time
        self.first_consult_appointment_time = first_consult_appointment_time
        self.second_consult_appointment_time = second_consult_appointment_time
        self.time_waiting = time_waiting
        #self.hw = hw #heigght and weight
        pass

    #def create(self):
        #creates a new agent

    #somehow need to initialise multiple patients
    
    #character = "patient"
    #anything else same to all patients

    #check below will run automatically and when they run

    #add later
    #def leave():
     #   if patient.current_action != "Appointed" or "Complete":
      #      if patient.patient_satisfaction <= 0:
       #         patient.current_action = "left_clinic"
                #update the patient in clinic to 0
                #update omni system


    #def change_action():
        #function about changing action

    #def move_on():
        #moving to next task and update the things, 
        #only if space is free, and when tick time met
        #but need to make sure not two patients advance at once





#might need to go in main
#initialise environemtal stuff
#pop_size = #GET THIS FROM PROBABILITIES - patient population size for the day
#clinic_pop_size = #GET THIS FROM PROBABILITIES - patient population inside the clinic at any one time - will this change for a day or is this a max????
#max_blood_room = 3 #this is a constant of the max patients a blood room can ever have
#PUT ANY OTHER ENVIRONMENT INSTATNTIATES HERE

#patient_list = [Patient_agent() for i in range(pop_size)]
#INSTANTIATE THE PATIENTS HERE WITH THERE INFORMATION

def initialise_patient(counter):
    global patients
    
    patient_satisfaction = random.randint(30, 100) #(scale is 0 - 100)
    id = counter
    current_action = "Appointed"

    #need to give all the stuffs
    patient = Patient_agent(id, patient_satisfaction, "unknown", current_action, 0, False, False, "unknown", "unknown", "unkown", 0)

    #add satisfaction

    #paitent.future_action = #gotten from omni system - a function
    #patient.duration = #gotten from omni system - need it?
    #(above) this way they can arrive whenever and get called accordingly
    #patient.position_in_list = #omnisystem #add later on
    #patient.arrived = #randint? or based on data, #assign later
    #below assigned in omni
    #patient.assigned_consultant = #choice between consultants on shift (omni), or none
    #patient.appointment_time = #given a time (make sure doesn't clash) or none

    #patient_list.append(patient)
    #counter += 1
    return (patient)

"""
def update_patient(patient_list, id): # runs when called by omni system
    patient = patient_list[id-1] #!!!!!!cant do this because some patients might have been remove
    patient.current_action = patient.current_action
    patient.future_action = patient.future_action
    patient.duration = #
"""
    
#add later
#def update_satisfaction(patient_list):
#    #needs to run every tick for every patient
#    for patient in patient_list():
#        #if current action remains unchanged reduce patient_satisfaction by 0.25
#        #if current action changes then patient_satisfaction increases by 10?
#        print("hi")
#    pass



#end patient stuff


#Nurse agent (do i make this just a general nurse or specific to each)
#attributes of: type of nurse, unique identifier?, action doing/state

class Nurse_agent:
    def __init__(self, id, current_action, task_duration, patient_treating):
        self.id = id
        #add later #self.type = type #bloods only, h&w only, mixed
        self.current_action = current_action
        #self.next_action = next_action
        self.task_duration = task_duration
        self.patient_treating = patient_treating

    #def create(self):
        #creates an agent
    #    pass

    #def check_for_next_patient():
        #chooses which patient to call in next, if there is
    #    pass

    #anymore functions?

#num_nurses = #randint between 1 and 3 (check number)

def initialise_nurse(counter):
    global nurses
    #nurse_list = [] #not needed?

    id = counter
    #change to make sure not all are h&w
    #add later #type = random.choice(["bloods", "H&W"]) #rand choice from bloods, H&W (if bloods then can do both)
    current_action = "waiting" #could be calling patients, H&w, waiting, bloods - make sure matches nurse type
    #task_duration = #omni system and based on current action
    #patient_treating = #omni system?
    nurse = Nurse_agent(id, current_action, "unknown", "uknown")

    #nurse_list.append(nurse)
    return (nurse)
"""
def update_nurse(nurse_list, patient_id, nurse_id): #runs when called by omni
    nurse = nurse_list[nurse_id-1]
    nurse.current_action = #omni
    nurse.task_duration = #omni
    nurse.patient_treating = patient_id
"""

#Consultant agent 
#attributes of: unique identifier, action doing/state

class Consultant_agent:
    def __init__(self, id, current_action ,patient_treating, patients_seeing, duration, sick):
        self.id = id
        self.current_action = current_action
        self.patient_treating = patient_treating #current patient they're with
        self.patients_seeing = patients_seeing # patients on list to see today
        self.duration = duration #how logn with current patient
        self.sick = sick #if the consultant calls in sick or not

    #def create(self):
        #creates agent

    #def check_for_next_patient_to_see():
        #check for which patient is here and closeset to appt time without skipping one

#num_consultants = #randint between 1 and 3 (check number)

def initialise_consultant(counter):
    global consultants
    #consultant_list = []#not needed?
    id = counter
    current_action = "waiting"
    #patient_treating = #omnisystem
    #patients_seeing = #list from omni system - needs to tell or match the patients one too
    #duration = #omni 
    #sick = #random chance between TRUE and FALSE #add later
        
    consultant = Consultant_agent(counter, current_action, "unknown", [], "uknown", False)
    

    #consultant_list.append(consultant)
    return (consultant)
"""
def update_consultant(consultant_list, consultant_id, patient_id): # make sure not called if the consultant is sick
    consultant = consultant_list[consultant_id-1] #might not work if we remove a consutlant if theyre sick
    consultant.current_action = #omni
    consultant.patient_treating = patient_id #append to remove from list after seen
    consultant.duration = #omni
    consultant.patients_seeing = #updated to remove patient_id 
"""

#Pathfinder
#Gets updated with informatin, tells nurses and consultatn who is next 

#environment
#universal 'time' measure
#ticks = 1440 #minutes in a day


#Patient agent
#attributes of: unique identifier, current state, patient satisfaction score
class Patient_agent:
    def __init__(self, id, patient_satisfaction, next_action, current_action, position_in_list, arrived, assigned_consultant, appointment_time)
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
        self.position_in_list = position_in_list
        #something to store all the actions it will do?
        self.assigned_consultant = assigned_consultant
        self.appointment_time = appointment_time
        pass

    #def create(self):
        #creates a new agent

    #somehow need to initialise multiple patients
    
    #character = "patient"
    #anything else same to all patients

    #check below will run automatically and when they run


    def leave():
        if patient.current_action != "Appointed" or "Complete":
            if patient.patient_satisfaction <= 0:
                patient.current_action = "left_clinic"
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
pop_size = #GET THIS FROM PROBABILITIES - patient population size for the day
clinic_pop_size = #GET THIS FROM PROBABILITIES - patient population inside the clinic at any one time - will this change for a day or is this a max????
max_blood_room = 3 #this is a constant of the max patients a blood room can ever have
#PUT ANY OTHER ENVIRONMENT INSTATNTIATES HERE

patient_list = [Patient_agent() for i in range(pop_size)]
#INSTANTIATE THE PATIENTS HERE WITH THERE INFORMATION

def initialise_patient():
    global patients
    patient_list = []
    counter = 0
    for i in range(pop_size):
        patient = Patient_agent()
        patient.id = counter
        patient.patient_satisfaction = #randint() from range 30 - 100 (scale is 0 - 100)
        patient.current_action = "Appointed"
        paitent.future_action = #gotten from omni system - a function
        #patient.duration = #gotten from omni system - need it?
        #(above) this way they can arrive whenever and get called accordingly
        patient.position_in_list = #omnisystem
        patient.arrived = #randint? or based on data, 
        patient.assigned_consultant = #choice between consultants on shift (omni), or none
        patient.appointment_time = #given a time (make sure doesn't clash) or none

        patient_list.append(paitent)
        counter += 1


def update_patient(patient_list, id): # runs when called by omni system
    patient = patient_list[id-1] #!!!!!!cant do this because some patients might have been remove
    patient.current_action = patient.current_action
    patient.future_action = patient.future_action
    patient.duration = #

def update_satisfaction(patient_list):
    #needs to run every tick for every patient
    for patient in patient_list():
        #if current action remains unchanged reduce patient_satisfaction by 0.25
        #if current action changes then patient_satisfaction increases by 10?
        print("hi")
    pass



#end patient stuff


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

    def create(self):
        #creates an agent
        pass

    def check_for_next_patient():
        #chooses which patient to call in next, if there is
        pass

    #anymore functions?

#num_nurses = #randint between 1 and 3 (check number)

def initialise_nurse():
    global nurses
    nurse_list = []

    nurse = Nurse_agent()
    nurse.id = counter
    nurse.type = #rand choice from bloods, H&W, mixed
    nurse.current_action = "waiting" #could be calling patients, H&w, waiting, bloods - make sure matches nurse type
    nurse.task_duration = #omni system and based on current action
    nurse.patient_treating = #omni system?

    nurse_list.append(nurse)
    return (nurse_list)

def update_nurse(nurse_list, patient_id, nurse_id): #runs when called by omni
    nurse = nurse_list[nurse_id-1]
    nurse.current_action = #omni
    nurse.task_duration = #omni
    nurse.patient_treating = patient_id


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

    def create(self):
        #creates agent

    def check_for_next_patient_to_see():
        #check for which patient is here and closeset to appt time without skipping one

#num_consultants = #randint between 1 and 3 (check number)

def initialise_consultant():
    global consultants
    consultant_list = []
    
        
    consultant = Consultant_agent()
    consultant.id = counter
    consultant.current_action = "waiting"
    consultant.patient_treating = #omnisystem
    consultant.patients_seeing = #list from omni system - needs to tell or match the patients one too
    consultant.duration = #omni 
    consultant.sick = #random chance between TRUE and FALSE

    consultant_list.append(consultant)
    

    return (consultant_list)

def update_consultant(consultant_list, consultant_id, patient_id): # make sure not called if the consultant is sick
    consultant = consultant_list[consultant_id-1] #might not work if we remove a consutlant if theyre sick
    consultant.current_action = #omni
    consultant.patient_treating = patient_id #append to remove from list after seen
    consultant.duration = #omni
    consultant.patients_seeing = #updated to remove patient_id 


#Pathfinder
#Gets updated with informatin, tells nurses and consultatn who is next 

#environment
#universal 'time' measure
ticks = 1440 #minutes in a day


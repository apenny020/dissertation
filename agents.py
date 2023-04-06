#Patient agent
#attributes of: unique identifier, current state, patient satisfaction score
class Patient_agent:
    def __init__(self, id, character, current_day, patient_satisfaction, next_action, current_action, duration)
        """
        id: unique id of patient
        current_day: current day count that is being modelled
        patient_satisfaction: score of patient satisfaction (similar to mood)
        next_action: the action that the patient will be doing next
        current_action: the action that the patient is currently doing
        duration: duration (in ticks) until the next action takes place (told by omnisystem)
        """
        self.id = id
        self.character = character
        self.current_day = current_day
        self.patient_satisfaction = patient_satisfaction
        self.next_action = next_action
        self.current_action = current_action
        self.duration = duration

    def create(self):
        #creates a new agent

    #somehow need to initialise multiple patients
    
    character = "patient"
    #anything else same to all patients

    def __init__(self, ...):
        #initialise here

    def (leave):
        #function about patient satisfaction

    def (change_action):
        #function about changing action

    def (move_on):
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












"""
def patient_set_up(todays_date, todays_patients):
    
    dict_patients = {}
    counter = 0
    for i in todays_patients:
        #attributes of patient agent
        #ID, day, patient satisfaction, next action, duration
        dict_patients["patient_" + str(counter)] = {"ID":"","day":todays_date, "patient satisfaction":"", "next action":"","duration":""}
        dict_patients["patient_" + str(counter)]["ID"] = counter
        

        counter += 1






    counter = 0
    for i in todays_patients:
        counter += 1
        a = "patient_" + str(counter)
        "patient_" + str(counter) = patient()

    return()
patient_agent.current_action


"""
#Nurse agent (do i make this just a general nurse or specific to each)
#attributes of: type of nurse, unique identifier?, action doing/state

#Consultant agent 
#attributes of: unique identifier, action doing/state

#Pathfinder
#Gets updated with informatin, tells nurses and consultatn who is next 

#environment
#universal 'time' measure
ticks = 1440 #minutes in a day


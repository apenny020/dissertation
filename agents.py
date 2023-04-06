#Patient agent
#attributes of: unique identifier, current state, patient satisfaction score


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


#Nurse agent (do i make this just a general nurse or specific to each)
#attributes of: type of nurse, unique identifier?, action doing/state

#Consultant agent 
#attributes of: unique identifier, action doing/state

#Pathfinder
#Gets updated with informatin, tells nurses and consultatn who is next 



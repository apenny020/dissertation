import time
from agents import *
import pandas as pd
import random

#Holds the state of the patients and other agents and updates their states

#has a time step that checks and executes at every timestep - main?

#environment
#universal 'time' measure
ticks = 1440 #minutes in a day



######################################################
#Pre model stuff 

#Function
#Unpacks lists of lists of data from data processing 
#and sends it to data analysis for percentage calculation and charts
#def unpackage(dict_of_lists):
#instead of unpackage we will just reference into the dataframe
        



#Function to get patients and workflow for the day

#initialise
#work out how many patients there will be today
#work out how many consultants there is supposed be today
#work out how many nurses there is supposed to be today
##clinic opening and closing times

#a list of appointment times for each consultant and for bloods
# ^ appointment times x mins apart and bloods x mins apart

#work out which consultants sick if any
#Update patients dictionary with appointments cancelled


#go through each patient and assign them a workflow
# ^ if they have an appointment, take that appointment time off the list for that consultant
# ^ write when tick they're meant to get called through

##########################

#Functions that get called every tick
#Checking to see if a patient needs to move on
#Update new patient dictionary with when they were actually called through
#Check if nurse is free
# ^if yes then call next waiting through (just the one waiting the longest)
# ^if no then ignore
#Check if consultant is free
# ^if yes then call the next closest to their appointment time (but making sure that its not ignoring the ones that have been waiting)
# ^^eg if you have a 16:00 patient waiting and 16:30 patient waiting and its 16:35 - make sure still pick the 16:00 patient
#Update patients patient satisfaction

#################################
#Fake Model






def appointment_times(start_hour, interval, end_hour):
    times = []
    num_appointments = 0
    for hour in range(start_hour, end_hour):
        for minute in range(0, 60, interval):
            times.append('{:02d}:{:02d}'.format(hour, minute))
            num_appointments += 1
    return (times, num_appointments)


def initialise():
    patient_number = 50
    dr_number = 3
    nurse_number = 3
    clinic_start = 9 #hour of day
    clinic_end = 17 #hour of day
    nurse_list = []
    consultant_list = []

    #update below to be automated and also to generate based on dr number
    appointment_times_bloods, num_bloods_appts = appointment_times(9, 15, 17) #28
    clinic_1_times, num_clinic_1_appts = appointment_times(9, 30, 12) #(6) will give appts from 9 till 12 (non inclusive) in 30min intervals
    clinic_2_times, num_clinic_2_appts = appointment_times(13, 30, 17) #8
    clinic_3_times, num_clinic_3_appts = appointment_times(9, 30, 12) #6

    consultant_1_patients = []
    consultant_2_patients = []
    consultant_3_patients = []

    bloods_patients = []
    
    #initialise patient df: Patient identifier, appointment time bloods, appointment time clinic 1, appointment time clinic 2, current action, waiting for
    patient_df = pd.DataFrame()
    patient_df.columns = ["ID", "Bloods_time", "Consultant_1_time", "Consultant_2_time", "current_action"]#add satisfaction later
    duplicate_bloods_times = appointment_times_bloods
    duplicate_consultant_1_times = clinic_1_times
    duplicate_consultant_2_times = clinic_2_times
    duplicate_consultant_3_times = clinic_3_times

    for x in range(patient_number):
        patient = initialise_patient(x)
        temp_list = [patient]
        #add bloods time (and remove time from list)
        bloods = bool(random.choice([True, False]))
        if bloods:
            bloods_appt_time = random.choice(duplicate_bloods_times)
            temp_list.append(bloods_appt_time)
            setattr(patient, "bloods_appointment_time", appt_time)
            bloods_patients.append(getattr(patient, "id"))
        else:
            temp_list.append("null")
            
        
        #add consultant time
        consultants = bool(random.choice([True, False]))
        if consultants:
            #choosing if 0, 1 or 2 consults
            consult_number = random.randint(1,2)
            if consult_number == 1:
                #check if any appts left in list
                if duplicate_consultant_1_times: #if not empty
                    appt_time = random.choice(duplicate_consultant_1_times)
                    duplicate_consultant_1_times.remove(appt_time)
                    dr = "1"
                    setattr(patient, "assigned_consultant", dr)
                    consultant_1_patients.append(getattr(patient, "id"))
                elif duplicate_consultant_2_times:
                    appt_time = random.choice(duplicate_consultant_2_times)
                    duplicate_consultant_2_times.remove(appt_time)
                    dr = "2"
                    setattr(patient, "assigned_consultant", dr)
                    consultant_2_patients.append(getattr(patient, "id"))
                elif duplicate_consultant_3_times:
                    appt_time = random.choice(duplicate_consultant_3_times)
                    duplicate_consultant_3_times.remove(appt_time)
                    dr = "3"
                    setattr(patient, "assigned_consultant", dr)
                    consultant_3_patients.append(getattr(patient, "id"))
                else:
                    print("no more appts avaliable")
                temp_list.append(appt_time)
                temp_list.append("null")
                setattr(patient, "consultant_1_appointment_time", appt_time)
                
            #2 consultations
            elif consult_number == 2:
                if duplicate_consultant_1_times: #if not empty
                    appt_time = random.choice(duplicate_consultant_1_times)
                    duplicate_consultant_1_times.remove(appt_time)
                    temp_list.append(appt_time)
                    setattr(patient, "consultant_1_appointment_time", appt_time)
                    consultant_1_patients.append(getattr(patient, "id"))
                    #get 2nd appt
                    if duplicate_consultant_2_times:
                        appt_time = random.choice(duplicate_consultant_2_times)
                        duplicate_consultant_2_times.remove(appt_time)
                        temp_list.append(appt_time)
                        setattr(patient, "consultant_2_appointment_time", appt_time)
                        dr = "1,2"
                        setattr(patient, "assigned_consultant", dr)
                        consultant_2_patients.append(getattr(patient, "id"))
                    elif duplicate_consultant_3_times:
                        appt_time = random.choice(duplicate_consultant_3_times)
                        duplicate_consultant_3_times.remove(appt_time)
                        temp_list.append(appt_time)
                        setattr(patient, "consultant_2_appointment_time", appt_time)
                        dr = "1,3"
                        setattr(patient, "assigned_consultant", dr)
                        consultant_3_patients.append(getattr(patient, "id"))
                    else:
                        temp_list.append("null")
                elif duplicate_consultant_2_times:
                    appt_time = random.choice(duplicate_consultant_2_times)
                    duplicate_consultant_2_times.remove(appt_time)
                    temp_list.append(appt_time)
                    setattr(patient, "consultant_1_appointment_time", appt_time)
                    consultant_2_patients.append(getattr(patient, "id"))
                    #get 2nd appt
                    if duplicate_consultant_3_times:
                        appt_time = random.choice(duplicate_consultant_3_times)
                        duplicate_consultant_3_times.remove(appt_time)
                        temp_list.append(appt_time)
                        setattr(patient, "consultant_2_appointment_time", appt_time)
                        dr = "2,3"
                        setattr(patient, "assigned_consultant", dr)
                        consultant_3_patients.append(getattr(patient, "id"))
                    else:
                        temp_list.append("null")
                else:
                    temp_list.append("null")
                    temp_list.append("null")

        current_action = getattr(patient, "current_action")
        temp_list.append(current_action)

        #patient_satisfaction = getattr(patient, "patient_satisfaction") 
        #temp_list.append(patient_satisfaction)
    
    for x in range(nurse_number):
        nurse = initialise_nurse(x)
        nurse_list.append(nurse)
        #need to update nurse attributes

    for x in range(dr_number):
        consultant = initialise_nurse(x)
        consultant_list.append(consultant)
        #need to update consultant attributes
        if x == 0:
            setattr(consultant, "patients_seeing", consultant_1_patients)
        elif x == 1:
            setattr(consultant, "patients_seeing", consultant_2_patients)
        elif x == 2:
            setattr(consultant, "patients_seeing", consultant_3_patients)

    return(patient_df, nurse_list, consultant_list, bloods_patients)     

    
def starts_everything():
    tick = 0 # each minute
    
    #initialise the day
    patient_df, nurse_list, consultant_list, bloods_patients = initialise()
    patients_arrived = []

    while tick <= 1440: #24 hours
        if (tick > 540 and tick < 1020): #9am & 5pm
            #check if patient has arrived (also have to develop function for when patient decides to arrive)
            #Look for who has appts (currently 1 person could have 3 9ams, gotta change this)
            #if dr is free, put through patient (if they have arrived)(need to develop function for choosign which patient to go through)
            #if nurse is free put through patient (if they have arrived)(need to develop function for choosign which patient to go through)
            #reduce durations tick left of appts
            #later do satisfaction too
            


    
    

###########################
#Recording data
#Records waiting times for each action
#Records duration for each action
#Records total number of
#^patients
#^nurses
#^consultants
#^DNA's
#^Lates
#Records total number of patients in:
#^Consultation at any one time
#^H&W&Bloods at any one time
#^Clinic at any one time
#Records total time in the clinic


####################################



#something that keeps track of all patients and 
#future durations and 
#future actions for patients in the day
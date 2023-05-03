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





"""
use when developed
def appointment_times(start_hour, interval, end_hour):
    times = []
    num_appointments = 0
    for hour in range(start_hour, end_hour):
        for minute in range(0, 60, interval):
            times.append('{:02d}:{:02d}'.format(hour, minute))
            num_appointments += 1
    return (times, num_appointments)
"""

def appointment_times(start_hour, interval, end_hour): 
    times = []
    appt = start_hour
    for minute in range(start_hour, end_hour, interval):
        appt = appt + interval
        times.append(appt)
    return(times)

def initialise(data_capture_df):
    patient_number = 32
    dr_number = 1
    nurse_number = 3
    clinic_start = 9 #hour of day (540 ticks)
    clinic_end = 17 #hour of day (1020 ticks)
    nurse_list = []
    consultant_list = []

    #update below to be automated and also to generate based on dr number
    appointment_times_bloods = appointment_times(540, 15, 1020) #28
    clinic_1_times = appointment_times(540, 30, 1020) #(6) will give appts from 9 till 12 (non inclusive) in 30min intervals
    
    #clinic_2_times, num_clinic_2_appts = appointment_times(13, 30, 17) #8
    #clinic_3_times, num_clinic_3_appts = appointment_times(9, 30, 12) #6

    consultant_1_patients = []
    consultant_2_patients = []
    consultant_3_patients = []

    bloods_patients = []
    
    all_patients = []
    
    #initialise patient df: Patient identifier, appointment time bloods, appointment time clinic 1, appointment time clinic 2, current action, waiting for
    patient_df = pd.DataFrame()
    patient_df = patient_df.assign(Patient=[], ID=[], Bloods_time=[], Consultant_1_time=[], current_action=[])#add satisfaction later and consultant 2 time
    duplicate_bloods_times = appointment_times_bloods
    duplicate_consultant_1_times = clinic_1_times
    #duplicate_consultant_2_times = clinic_2_times
    #duplicate_consultant_3_times = clinic_3_times

    for x in range(patient_number):
        patient = initialise_patient(x)
        temp_list = [patient]
        temp_list.append(getattr(patient, "id"))
        

        data_capture_df.at[x,"Patient"] = patient
        data_capture_df.at[x,"ID"] = getattr(patient, "id")

        #add bloods time (and remove time from list)
        #bloods = bool(random.choice([True, False]))
        #if bloods:
        if duplicate_bloods_times: #if its not empty
            bloods_appt_time = random.choice(duplicate_bloods_times)
            duplicate_bloods_times.remove(bloods_appt_time)
            temp_list.append(str(bloods_appt_time))
            setattr(patient, "bloods_appointment_time", bloods_appt_time)
            bloods_patients.append(patient)

            data_capture_df.at[x,"Bloods_scheduled"] = bloods_appt_time

        else:
            temp_list.append("null")
            
            data_capture_df.at[x,"Bloods_scheduled"] = "null"
            
        
        #add consultant time
        consultants = bool(random.choice([True, False]))
        if consultants:
            if duplicate_consultant_1_times: #if not empty
                appt_time = random.choice(duplicate_consultant_1_times)
                duplicate_consultant_1_times.remove(appt_time)
                dr = "1"
                setattr(patient, "assigned_consultant", dr)
                setattr(patient, "consultant_1_appointment_time", str(appt_time))
                consultant_1_patients.append(getattr(patient, "id"))
                temp_list.append(str(appt_time))
                data_capture_df.at[x,"Consultant_scheduled"] = appt_time

            else:
                temp_list.append("null")
                data_capture_df.at[x,"Consultant_scheduled"] = "null"
                setattr(patient, "consultant_1_appointment_time", "null")
        else: 
            temp_list.append("null")
            data_capture_df.at[x,"Consultant_scheduled"] = "null"
            setattr(patient, "consultant_1_appointment_time", "null")
            
            """
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
            """
        setattr(patient, "current_action", "appointed")
        current_action = getattr(patient, "current_action")
        temp_list.append(current_action)

        #patient_satisfaction = getattr(patient, "patient_satisfaction") 
        #temp_list.append(patient_satisfaction)
        
        #add temp_list to dataframe
        patient_df.loc[len(patient_df)] = temp_list


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

    print(patient_df)
    return(patient_df, nurse_list, consultant_list, bloods_patients, data_capture_df)     


def longest_waiting_patient(total_patients):
    patient_dict = {}
    for p in total_patients:
        if (getattr(p, "arrived") == True):
            patient_dict[p] = getattr(p, "time_waiting")
    patient_dict = dict(sorted(patient_dict.items(), key=lambda item: item[1]))
    return(patient_dict)


def starts_everything():
    tick = 510 # each minute, 8:30am
    
    data_capture_df = pd.DataFrame()
    data_capture_df = data_capture_df.assign(Patient=[], ID=[], Bloods_scheduled=[], Bloods_seen=[], Consultant_scheduled=[], Consultant_seen=[], arrival_time=[], exit_time=[]) #add wait time
    
    #initialise the day
    patient_df, nurse_list, consultant_list, bloods_patients, data_capture = initialise(data_capture_df)
    
    patients_arrived = []
    #hw_nurses = []
    #blood_nurses = []
    #create a list of all the patients in the dataframe (ie all patients today)
    total_patients = patient_df["Patient"]

    #create a list from dataframe for consultants
    consult_patients = pd.Series(patient_df.Consultant_1_time.values,index=patient_df.Patient).to_dict()
    consult_patients = dict(sorted(consult_patients.items(), key=lambda item: item[1]))

    while tick <= 1050: #5:30pm
        tick += 1
        print(tick)
        if (tick > 540 and tick < 1020): #9am & 5pm
            #check which patients are here
            print(tick)
            for p in total_patients:
                if getattr(p, "arrived") and (p not in patients_arrived):
                    patients_arrived.append(p)
                elif (getattr(p, "arrived") == False) and (getattr(p,"finished") == False):
                    other = ["null", "uknown", "complete"]

                    if (getattr(p, "consultant_1_appointment_time") not in other) and (getattr(p, "bloods_appointment_time") not in other):
                        print("BALHHHHHHHHH")
                        print(getattr(p, "bloods_appointment_time"))
                        print(getattr(p, "consultant_1_appointment_time"))
                        appt_time = str(max(int(getattr(p, "bloods_appointment_time")),int(getattr(p, "consultant_1_appointment_time"))))
                    elif (getattr(p, "consultant_1_appointment_time") not in other) and (getattr(p, "bloods_appointment_time") in other):
                        appt_time = getattr(p, "consultant_1_appointment_time")
                    elif (getattr(p, "consultant_1_appointment_time") in other) and (getattr(p, "bloods_appointment_time") not in other):
                        appt_time = getattr(p, "bloods_appointment_time")
                        

                    if tick+10 >= int(appt_time):
                        setattr(p, "arrived", True)
                        setattr(p, "current_action", "waiting")

                        row_num = patient_df[patient_df["Patient"] == p].index.to_numpy()
                        row_num = int(row_num)
                        patient_df.at[row_num,"current_action"] = "waiting" #row then column

                        row_num = data_capture[data_capture["Patient"] == p].index.to_numpy()
                        row_num = int(row_num)
                        data_capture.at[row_num,"arrival_time"] = tick

                        print("patient arrived")
                        print(patient_df)
            
                        
            
            #check if nurses are free
            #add later
            for n in nurse_list:
            #    if getattr(n, "type") == "H&W":
            #        hw_nurses.append(n)
            #    elif getattr(n, "type") == "bloods":
            #        blood_nurses.append(n)

                #get list of patients who have been waiting the longest
                patient_dict = longest_waiting_patient(bloods_patients)
                
                if (getattr(n, "current_action") == "waiting"):
                    for p in patient_dict:
                        if getattr(p, "current_action") == "waiting":
                            id = getattr(p, "id")
                            setattr(p, "current_action", "bloods")
                            setattr(n, "current_action", "treating")
                            setattr(n, "task_duration", 15)#minutes
                            setattr(n, "patient_treating", id)

                            #update dataframe to change bloods time of patient to complete:
                            row_num = patient_df[patient_df["Patient"] == p].index.to_numpy()
                            row_num = int(row_num)
                            patient_df.at[row_num,"current_action"] = "bloods"

                            row_num = data_capture[data_capture["Patient"] == p].index.to_numpy()
                            row_num = int(row_num)
                            data_capture.at[row_num,"Bloods_seen"] = tick

                        break #breaks out of for loop because treating patient
                elif (getattr(n, "current_action") == "treating") and (getattr(n, "task_duration") != 0):
                    duration = getattr(n, "task_duration")
                    duration -= 1
                    setattr(n, "task_duration", duration)#minutes
                
                elif (getattr(n, "current_action") == "treating") and (getattr(n, "task_duration") == 0):
                    #finished and update
                    patient_id = getattr(n, "patient_treating")
                    setattr(n, "current_action", "waiting")
                    setattr(n, "patient_treating", "unknown")
                    #update patient 
                    #loop through total_patients and match the ID
                    for p in total_patients:
                        if getattr(p, "id") == patient_id:
                            setattr(p, "current_action", "waiting")
                            setattr(p, "bloods_appointment_time", "complete")
                            row_num = patient_df[patient_df["Patient"] == p].index.to_numpy()
                            row_num = int(row_num)
                            patient_df.at[row_num,"current_action"] = "waiting" #row then column
                            patient_df.at[row_num,"Bloods_time"] = "complete" #row then column


            #check  if dr free
            #need to change to choose one closest to appointment time
            #needs to change when data used
            for c in consultant_list:
                for p in consult_patients:
                    if getattr(p, "arrived") == True:
                        if (getattr(c, "current_action") == "waiting"):
                            other = ["complete", "null", "uknown"]
                            if (getattr(p, "current_action") == "waiting" and (getattr(p, "consultant_1_appointment_time") not in other)):
                                setattr(p, "current_action", "consulting")
                                setattr(c, "current_action", "treating")
                                setattr(c, "task_duration", 30)#minutes
                                setattr(c, "patient_treating", getattr(p, "id"))

                                #update dataframe to change consult time of patient to complete:
                                row_num = patient_df[patient_df["Patient"] == p].index.to_numpy()
                                row_num = int(row_num)
                                patient_df.at[row_num,"current_action"] = "consult"
                                #print (patient_df)

                                row_num = data_capture[data_capture["Patient"] == p].index.to_numpy()
                                row_num = int(row_num)
                                data_capture.at[row_num,"Consultant_seen"] = tick

                        elif (getattr(c, "current_action") == "treating") and (getattr(c, "task_duration") != 0):
                            duration = getattr(c, "task_duration")
                            duration = duration - 1
                            setattr(c, "task_duration", duration)#minutes
                        
                        elif (getattr(c, "current_action") == "treating") and (getattr(c, "task_duration") == 0):
                            #finished and update
                            patient_id = getattr(c, "patient_treating")
                            setattr(c, "current_action", "waiting")
                            setattr(c, "patient_treating", "unknown")
                            #update patient 
                            #loop through total_patients and match the ID
                            for p in total_patients:
                                if getattr(p, "id") == patient_id:
                                    setattr(p, "current_action", "waiting")
                                    setattr(p, "consultant_1_appointment_time", "complete")
                                    row_num = patient_df[patient_df["Patient"] == p].index.to_numpy()
                                    row_num = int(row_num)
                                    patient_df.at[row_num,"Consultant_1_time"] = "complete" #row then column
                                    patient_df.at[row_num,"current_action"] = "waiting" #row then column
                                    #print(getattr(p, "current_action"))
                                    #print("hi")

            #update patients
            for p in total_patients:
                if getattr(p, "current_action") == "waiting":
                    #increase waiting
                    waiting = getattr(p, "time_waiting")
                    waiting += 1
                    setattr(p, "time_waiting", waiting)

                if (getattr(p, "bloods_appointment_time") == "complete") and (getattr(p, "consultant_1_appointment_time") == "complete"):
                    #finished
                    setattr(p, "current_action", "finished")
                    setattr(p, "arrived", False)
                    setattr(p, "finished", True)

                    if p in patients_arrived:
                        patients_arrived.remove(p)

                    row_num = patient_df[patient_df["Patient"] == p].index.to_numpy()
                    row_num = int(row_num)
                    patient_df.at[row_num,"current_action"] = "finished"

                    row_num = data_capture[data_capture["Patient"] == p].index.to_numpy()
                    row_num = int(row_num)
                    data_capture.at[row_num,"exit_time"] = tick

    print ("data capture")
    print(data_capture)



    


                    



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
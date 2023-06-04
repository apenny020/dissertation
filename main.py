from omni_system import *
from data_processor import *
from data_analyser import *
import time
from agents import *
import pandas as pd
import random


def starts_everything(untallied_dict):
    tick = 510 # each minute, 8:30am
    
    data_capture_df = pd.DataFrame(columns=["Patient", "ID", "Bloods_scheduled", "Bloods_seen", "Consultant_scheduled", "Consultant_seen", "arrival_time", "exit_time", "patient_satisfaction"])
    
    #initialise the day
    patient_df, nurse_list, consultant_list, bloods_patients, data_capture, consultant_appts_dict, clinic_start, clinic_end = initialise(data_capture_df, untallied_dict)
    print(data_capture)

    patients_arrived = []
    hw_nurses = []
    blood_nurses = []
    #create a list of all the patients in the dataframe (ie all patients today)!!!!!!!!!!!!!!!!!
    total_patients = patient_df["Patient"]

    #create a list from dataframe for consultants
    #consult_patients = pd.Series(patient_df.Consultant_1_time.values,index=patient_df.Patient).to_dict()
    #consult_patients = dict(sorted(consult_patients.items(), key=lambda item: item[1]))

    while tick <= 1050: #5:30pm
        tick += 1
        print(tick)
        other = ["null", "uknown", "complete", "incomplete"]
        if (tick > clinic_start and tick < clinic_end): #8am & 5:30pm
            #check which patients are here
            print(tick)
            #for each patient check if arrived, add to list of arrived patients
            for p in total_patients:
                if getattr(p, "arrived") and (p not in patients_arrived):
                    patients_arrived.append(p)

                    states = ["consulting", "bloods"]
                        #update satisfaction
                    if getattr(p, "current_action") not in states: 
                        satis = getattr(p, "patient_satisfaction")
                        satis = satis - 0.25
                        setattr(p, "patient_satisfaction", satis)
                        data_capture_df["patient_satisfaction"] = satis

                    #check their satisfaction
                    p, left = Patient_agent.leave(p)
                    if left == True:
                        data_capture_df["patient_satisfaction"] = 0
                        data_capture_df["exit_time"] = tick
                        setattr(p, "current_action", "incomplete")
                        setattr(p, "finished", True)

                #if not arrived and not finished
                elif (getattr(p, "arrived") == False) and (getattr(p,"finished") == False):
                    
                    #if appointment times arent null, unknown, or complete, ie they exist and havent happened yet
                    if (getattr(p, "consultant_1_appointment_time") not in other) and (getattr(p, "bloods_appointment_time") not in other):

                        #adds appt time to appt time variable
                        if (p, "consultant_2_appointment_time") not in other:
                            appt_time = str(min(int(getattr(p, "bloods_appointment_time"))),int(getattr(p, "consultant_1_appointment_time"),int(getattr(p, "consultant_2_appointment_time"))))
                        else:
                            appt_time = str(min(int(getattr(p, "bloods_appointment_time"))),int(getattr(p, "consultant_1_appointment_time")))

                    #Checking for the other situations
                    elif (getattr(p, "consultant_1_appointment_time") not in other) and (getattr(p, "bloods_appointment_time") in other):
                        if (p, "consultant_2_appointment_time") not in other:
                            appt_time = str(min(int(getattr(p, "consultant_1_appointment_time")),int(getattr(p, "consultant_2_appointment_time"))))
                        else:
                            appt_time = str(int(getattr(p, "consultant_1_appointment_time")))

                    #no consultant appointment, no need to check consultant 2
                    elif (getattr(p, "consultant_1_appointment_time") in other) and (getattr(p, "bloods_appointment_time") not in other):
                        appt_time = getattr(p, "bloods_appointment_time")
                        
                    #If patient wont turn up
                    if getattr(p, "will_arrive") == False:
                        setattr(p, "arrived", False)
                        setattr(p, "current_action", "finished")
                    
                        if getattr(p, "bloods_appointment_time") not in other:
                            setattr(p, "bloods_appointment_time", "complete")

                        if getattr(p, "consultant_1_appointment_time") not in other:
                            setattr(p, "consultant_1_appointment_time", "complete")

                        if getattr(p, "consultant_2_appointment_time") not in other:
                            setattr(p, "consultant_2_appointment_time", "complete")

                    #work out their actual arrival time
                    temp_time = getattr(p, "arrival_time")
                    temp_time = temp_time-appt_time
                    setattr(p, "arrival_time", temp_time)

                    #if patient wants to arrive before clinic starts, reset to arrive when clinic starts
                    if getattr(p, "arrival_time") < clinic_start:
                        setattr(p, "arrival_time", clinic_start)

                    #checking if arrived
                    if tick >= getattr(p, "arrival_time"):
                        setattr(p, "arrived", True)
                        setattr(p, "current_action", "waiting")

                        #update the current status df
                        row_num = patient_df[patient_df["Patient"] == p].index.to_numpy()
                        row_num = int(row_num)
                        patient_df.at[row_num,"current_action"] = "waiting" #row then column

                        #update arrival time in the data capture df
                        row_num = data_capture[data_capture["Patient"] == p].index.to_numpy()
                        row_num = int(row_num)
                        data_capture.at[row_num,"arrival_time"] = tick

                        print("patient arrived")
                        print(patient_df)

                        #update patients
                        setattr(p, "arrived", True)
                        setattr(p, "current_action", "watiting")
            
                if getattr(p, "current_action") == "waiting":
                    #increase waiting time capture
                    waiting = getattr(p, "time_waiting")
                    waiting += 1
                    setattr(p, "time_waiting", waiting)

                elif getattr(p, "current_action") in states:
                    #waiting time paused
                    waiting = 0
                    setattr(p, "time_waiting", waiting)
                

                if (getattr(p, "current_action") != "finished"):
                    if (getattr(p, "bloods_appointment_time") in other and (getattr(p, "consultant_1_appointment_time") in other) and (getattr(p, "consultant_2_appointment_time") in other) ):
                        #finished, appts are complete, update states to finished
                        print(getattr(p, "id"))
                        print(tick)
                        print(getattr(p, "current_action"))
                        
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
        
            #check  if dr free
            #need to change to choose one closest to appointment time
            #needs to change when data used
            for c in consultant_list:
                #get list of patients
                consult_patients = consultant_appts_dict[c]

                if getattr(c, "sick") == True:#consultant not in because sick
                    for p in consult_patients:
                        appt = consultant_appts_dict #!!!!!!!!!!!!!!!!!!!111111111111111111

                        if getattr(p, "consultation_2_appointment_time") in other:
                            setattr(p, "consultation_1_appointment_time", "sick")
                        else:
                            drs = getattr(p)


                for p in consult_patients:

                    #if this is true (below) means DNA so remove from list
                    if getattr(p, "consultant_1_appointment_time") in other:
                        consult_patients.remove(p)
                    if getattr(p, "consultant_2_appointment_time") in other:
                        consult_patients.remove(p)

                    if getattr(p, "arrived") == True:
                        if (getattr(c, "current_action") == "waiting"):

                            #CHANGE FOR LONGEST WAITING ETC!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!/closest to time
                            if (getattr(p, "current_action") == "waiting" and ((getattr(p, "consultant_1_appointment_time") not in other) or (getattr(p, "consultant_2_appointment_time") not in other))):
                                setattr(p, "current_action", "consulting")
                                satis = getattr(p, "patient_satisfaction")
                                satis = satis + 20
                                setattr(p, "patient_satisfaction", satis)
                                data_capture_df["patient_satisfaction"] = satis
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

                                if (getattr(p, "consultant_1_appointment_time") not in other):
                                    setattr(p, "consultant_1_appointment_time", "in_progress")
                                elif (getattr(p, "consultant_1_appointment_time") not in other):
                                    setattr(p, "consultant_2_appointment_time", "in_progress")
                                else:
                                    print("error")


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

                                    if getattr(p, "consultant_1_appointment)time") == "in_progress":
                                        setattr(p, "consultant_1_appointment_time", "complete")
                                        patient_df.at[row_num,"Consultant_1_time"] = "complete" #row then column
                                    elif getattr(p, "consultant_2_appointment)time") == "in_progress":
                                        setattr(p, "consultant_2_appointment_time", "complete")
                                        patient_df.at[row_num,"Consultant_2_time"] = "complete" #row then column
                                    else:
                                        print("error")

                                    row_num = patient_df[patient_df["Patient"] == p].index.to_numpy()
                                    row_num = int(row_num)
                                    patient_df.at[row_num,"current_action"] = "waiting" #row then column
 
            
            #check if nurses are free
            for n in nurse_list:
                if getattr(n, "type") == "H&W":
                    hw_nurses.append(n)
                elif getattr(n, "type") == "bloods":
                    blood_nurses.append(n)

                #check for DNAs
                
                for p in bloods_patients:
                    if getattr(p, "bloods_appointment_time") in other:
                        bloods_patients.remove(p)

                #get list of patients who have been waiting the longest
                patient_dict = longest_waiting_patient(bloods_patients)

            
                
                if (getattr(n, "current_action") == "waiting") and (getattr(n, "type") == "bloods"):
                    for p in patient_dict:
                        if getattr(p, "current_action") == "waiting":
                            id = getattr(p, "id")
                            setattr(p, "current_action", "bloods")
                            satis = getattr(p, "patient_satisfaction")
                            satis = satis + 20
                            setattr(p, "patient_satisfaction", satis)
                            data_capture_df["patient_satisfaction"] = satis
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
                            bloods_patients.remove(p)
                            setattr(p, "current_action", "waiting")
                            setattr(p, "bloods_appointment_time", "complete")
                            row_num = patient_df[patient_df["Patient"] == p].index.to_numpy()
                            row_num = int(row_num)
                            patient_df.at[row_num,"current_action"] = "waiting" #row then column
                            patient_df.at[row_num,"Bloods_time"] = "complete" #row then column


            

            
    data_capture.to_csv("output_data")
    print ("data capture")
    print(data_capture)

    return()


#run the model here
print("Process data")
tally_dict = process_all_data()
print(tally_dict)
print("------------------------")
print("going to start")
starts_everything(untallied_dict)
print("completed")
        
                



#NUMBER OF PATIENTS WHO LEFT BECAUSE SATISFACTION TOO LOW
#NUMBER OF PATIENTS IN CLINIC THAT DAY
#AVERAGE WAIT TIME FOR HEIGHT AND WEIGHT
#AVERAGE WAIT TIME FOR CONSULTATION 1
#AVERAGE WAIT TIME FOR CONSULTATION 2
#AVERAGE WAIT TIME FOR BLOODS
#AVERAGE TIME START TO FINISH
#AVERAGE TOTAL WAIT TIMES
#DURATIONS TOO?




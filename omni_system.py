import time
from agents import *
import pandas as pd
import random

#Holds the state of the patients and other agents and updates their states
#has a time step that checks and executes at every timestep
#environment is time
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





#function that creates a list of appointment times with a given interval between two times
def appointment_times(start_hour, interval, end_hour): 
    times = []
    appt = start_hour
    for minute in range(start_hour, end_hour, interval):
        appt = appt + interval
        times.append(appt)
    
    #appt_dict.update({key:times})
    return(times)


#~~~~Random process of picking appointments for consultations for patient~~~~~~~~~~~~~~~~#
def consult_appts(appts_df, iterations, num_consultants):
    """
    for number of drs on shift - chooses random number from this
    find the corresponding list of appointment times
    if theres still times - randomly pick one
    if there are none left, redo step 1
    """
    #NEED TO ADD SOMETHING TO MAKE SURE SECOND APPT NOT AT SAME TIME !!!!!!!!!!
    temp_list = []
    for i in iterations:
        num_dr = [] 
        dr = 0
        dr2 = 0
        finished = False

        for i in range(num_consultants):
            num_dr.append(i+1) #adds the number of todays consultants to list

        if not num_dr:
            #if empty, i.e. no consultants today
            temp_list.append("null")
            temp_list.append("null")
            if i == 2:
                return(temp_list)

        while not finished: #in loop because there might not be any appt times and they'd have to pick again from a different doctor
            if i == 2:
                #checking that not duplicate dr
                if len(num_dr) == 1: #if only 1 dr today can only have 1 appt (which wouldve been assigned when i ==1)
                    #assign null and break
                    temp_list.append("null")
                    finished = True
                    return(temp_list)

                while dr == dr2: #should never be equal as cant have 2 appointments with same dr
                    dr2 = random.randint(1, num_dr) # picking a new dr
                    column_header = ("dr" + str(dr2))
                    possible_times = appts_df.loc[column_header] # possible appt times to choose from

            if i == 1:
                #choosing a dr randomly, same with appointment
                dr = random.randint(1, num_dr)
                column_header = ("dr" + str(dr))
                possible_times = appts_df.loc[column_header]

            #if possible times (appt times) not empty
            if possible_times:
                appt_time = random.choice(possible_times)
                possible_times.remove(appt_time)
                #update df to remove the appt
                if i == 1:
                    temp_list.append(dr)
                    num_dr.remove(dr)
                elif i == 2:
                    temp_list.append(dr2)
                    num_dr.remove(dr2)
                temp_list.append(appt_time)
                finished = True

            else: #no appts left with that dr rmeove that dr from the list
                num_dr.remove(dr)
                num_dr.remove(dr2)

        temp_list.append(dr)
        if dr2 != 0: #if there are 2 drs, add both to the list
            temp_list.append(dr2)

        #temp_list.append(appt_time)
    return(temp_list)


"""
Possible workflows according to NHS contact:
- Check in, Blood test
- Check in, see consultant, Blood test
- Check in, get H&W, see consultant, blood tests
- Check in, get H&W, see consultant, see consultant, blood tests

"""


#~~~~~does the apoointment choice (random), and calls consult_appts for appointments for patients ~~~~~~~~~~~#
def appointment_choice(patient, id, appt_df, num_consultants, dr_dict, bloods_patients):
    #!!!!get the column Bloods_appts and assign to list called bloods_appt
    #Assign consultant appt first because bloods after
    """
    finds appointments for patients, 1 blood (if they have a blood one), and between 0 and 2 consult appointments
    Makes sure the appointments dont clash 
    Calls consult_appts to get the consult appointments
    Makes sure that consultant is before bloods - to make sure it flollows the workflow above
    """

    #finding out if they're going to have a bloods and/or consultant appointment
    consultants = bool(random.choice([True, False]))
    bloods = bool(random.choice([True, False]))


    #if they dont have a bloods or consultant appointment, they get assigned a bloods appointment - this is the only workflow with a singular appointment
    #if they have a consultants appointment
    if (consultants):
        #you cant have a consultant appointment without also having a bloods appointment
        bloods = True
        #choose whether one or two consultations
        consult_number = random.randint(1, 2)
        
        #If 1 appointment
        if consult_number == 1: 
            temp_list = consult_appts(appt_df, 1, num_consultants) #chooses appointment time for consultant
            dr = temp_list[0] #grabbing the consultants id from temp list
            consult_appt_time = temp_list[1] #grabibng the appt time from temp list

            #update patient agent attributes
            setattr(patient, "assigned_consultant", dr)
            setattr(patient, "first_consult_appointment_time", str(consult_appt_time))
            setattr(patient, "second_consult_appointment_time", "null")

            #add patients to drs patient list
            for dr in dr_list:
                if dr == dr_1:
                    temp = dr_dict['consultant_%s' % dr]
                    temp.append(getattr(patient,"id"))


        #If 2 consultations
        if consult_number == 2:
            temp_list = consult_appts(appt_df, 2, num_consultants)
            dr_1 = temp_list[0]
            consult_appt_time_1 = temp_list[1]
            dr_2 = temp_list[2]
            consult_appt_time_2 = temp_list[3]
            dr = (str(dr_1) + str(dr_2))

            #compare to find out which is the sooner consult
            if int(consult_appt_time_2) < int(consult_appt_time_1):
                consult_appt_time_1 = int(consult_appt_time_2)
                consult_appt_time_2 = int(consult_appt_time_1)

            #update patient attirubtes
            setattr(patient, "assigned_consultant", dr)
            setattr(patient, "first_consult_appointment_time", str(consult_appt_time_1))
            setattr(patient, "second_consult_appointment_time", str(consult_appt_time_2))

            #add patients to drs patient list
            for dr in dr_list:
                if dr == dr_2:
                    temp = dr_dict['consultant_%s' % dr]
                    temp.append(getattr(patient,"id"))
        


    #if they dont have a consultants appointment, auto get bloods appt
    if bloods or (not consultants):
        bloods = True
        possible_times = appt_df.loc["bloods"] #retrieving all the possible blood appointment times
        not_duplicate = False
        for i in possible_times:
            while not not_duplicate:
                if consult_number == 1:
                    if i < (int(consult_appt_time_1)+30):#finding an appointment that is after the consultant appointment as per workflow
                        possible_times.remove(i)
                elif consult_number == 2:
                    if i < (int(consult_appt_time_2)+30):#finding an appointment that is after the consultant appointment as per workflow
                        possible_times.remove(i)
        
        bloods_appt_time = random.choice(possible_times)#choose appt times for bloods
    
        #add patients to a list of all bloods patients 
        bloods_patients.append(getattr(patient,"id"))


    elif not bloods:
        bloods_appt_time="null"

    #update df to remove appts (consultants)
        #the dr number is first column and then the rest of row are appts

        #update df to remove the appts!!!!!!!!!!!11   
    #then for bloods
    #update df to remove the appts!!!!!!!!!!!!!


    #update dataframe on patients consultants !!!!!!!!!!!!!!!!!!!
    return(bloods_appt_time, consult_appt_time_1, consult_appt_time_2, appt_df, dr_dict, bloods_patients)


#finds which patient is waiting the longest from a list of patients
def longest_waiting_patient(total_patients):
    patient_dict = {}
    for p in total_patients:
        if (getattr(p, "arrived") == True):
            patient_dict[p] = getattr(p, "time_waiting")
    patient_dict = dict(sorted(patient_dict.items(), key=lambda item: item[1]))
    return(patient_dict)



#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#~Initialise~#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def initialise(data_capture_df):
    patient_number = #take from data
    dr_number = #take from data
    nurse_number = #take from data
    bloods_appt_length = 15 #assumption of 15mins - could get from data?
    clinic_start = 540 #minutes of day (540 ticks) could get from data?
    clinic_end = 1020 #minutes of day (1020 ticks) could get from data?
    nurse_list = []
    consultant_list = #data
    waiting_room_capacity = [] #,ax patients
    
    bloods_patients = []
    all_patients = []

    dr_list = []
    dr_dict = {}

    #create a list and then dict of drs
    for i in range(dr_number):
        dr_list.append(i+1)
        
    for i in dr_list:
        dr_dict['consultant_%s' % i] = []

    #update below to be automated and also to generate based on dr number!!!!!!!!!!!!!!!
    
    appointment_df = pd.DataFrame()
    #appointment_df = appointment_df.assign()#assign column headers
    
    #seeting the appts times of bloods appt and adding to df
    appointment_times_bloods = appointment_times(clinic_start, bloods_appt_length, clinic_end) #28
    appointment_df["bloods"]= appointment_times_bloods
    
    #initialise patient df: Patient identifier, appointment time bloods, appointment time clinic 1, appointment time clinic 2, current action, waiting for
    patient_df = pd.DataFrame()
    patient_df = patient_df.assign(Patient=[], ID=[], Bloods_time=[], Consultant_1_time=[], Consultant_2_time=[], current_action=[], patient_satisfaction=[])#add satisfaction later and consultant 2 time

    #initialising nurses by how many there are
    for x in range(nurse_number):
        nurse = initialise_nurse(x)
        nurse_list.append(nurse)
    
    HW_nurses = []
    Bloods_nurses = []

    for nurse in nurse_list:
        if getattr(nurse, "type") == "HW":
            HW_nurses.append(getattr(nurse, "id"))
        elif getattr(nurse, "type") == "Bloods":
            Bloods_nurses.append(getattr(nurse, "id"))
        else:
            print("error")
        
        #if no bloods nurses, take 1 HW nurse and change them to a bloods nurse because unfeasible to have 0
        if not Bloods_nurses:
            temp_nurse = HW_nurses[0]
            setattr(temp_nurse, "type", "Bloods")
            HW_nurses.remove(getattr(temp_nurse, "id"))
            Bloods_nurses.append(getattr(temp_nurse, "id"))

    #initialising drs by how many there are
    for x in range(dr_number):
        consultant = initialise_consultant(x)
        consultant_list.append(consultant)
        
        #take from the processed data - make sure in minutes form
        consultant_start = #take from data
        consult_length = 30 # assumption - can take from data
        consultant_end = #take from data

        clinic_times = appointment_times(consultant_start, consult_length, consultant_end) 
        #Appends to apopintment df
        appointment_df["dr" + str(x)]= clinic_times

    #initialises patients
    for x in range(patient_number):
        patient = initialise_patient(x)
        temp_list = [patient]
        temp_list.append(getattr(patient, "id"))

        data_capture_df.at[x,"Patient"] = patient
        data_capture_df.at[x,"ID"] = getattr(patient, "id")

        #calls appointment choice to have appointments assigned to students
        bloods_appt_time,  consult_appt_time_1, consult_appt_time_2, appointment_df, dr_dict, bloods_patients  =appointment_choice(patient, getattr(patient, "id"), appointment_df, dr_number, dr_dict, bloods_patients)
        #need a list of blood patietnts and consultant patients for each consultant

        data_capture_df.at[x,"Bloods_scheduled"] = bloods_appt_time
        data_capture_df.at[x,"Consultant_scheduled_1"] = consult_appt_time_1
        data_capture_df.at[x,"Consultant_scheduled_2"] = consult_appt_time_1

        temp_list.append(bloods_appt_time)
        temp_list.append(consult_appt_time_1)
        temp_list.append(consult_appt_time_2)      


        # might need to put some stuff in agents file for function !!!!!!!!!!!!!!!!!!!

            
        setattr(patient, "current_action", "appointed")
        current_action = getattr(patient, "current_action")
        temp_list.append(current_action)

        patient_satisfaction = getattr(patient, "patient_satisfaction") 
        temp_list.append(patient_satisfaction)
        
        #add temp_list to dataframe
        patient_df.loc[len(patient_df)] = temp_list

        
    #need to update consultant attributes 
    for ctant in consultant_list:
        for x in range(dr_number):
            consultant_patients = dr_dict['consultant_%s' % x]
            setattr(ctant, "patients_seeing", consultant_patients)
        

    print(patient_df)
    return(patient_df, nurse_list, consultant_list, bloods_patients, data_capture_df, dr_dict)     


#------------------continue from here -----------------

def starts_everything():
    tick = 510 # each minute, 8:30am
    
    data_capture_df = pd.DataFrame()
    data_capture_df = data_capture_df.assign(Patient=[], ID=[], Bloods_scheduled=[], Bloods_seen=[], Consultant_scheduled=[], Consultant_seen=[], arrival_time=[], exit_time=[], patient_satisfaction=[]) #add wait time
    
    #initialise the day
    patient_df, nurse_list, consultant_list, bloods_patients, data_capture, consultant_appts_dict = initialise(data_capture_df)
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
        if (tick > 540 and tick < 1020): #9am & 5pm
            #check which patients are here
            print(tick)
            #for each patient check if arrived, add to list of arrived patients
            for p in total_patients:
                if getattr(p, "arrived") and (p not in patients_arrived):
                    patients_arrived.append(p)

                #if not arrived and not finished
                elif (getattr(p, "arrived") == False) and (getattr(p,"finished") == False):
                    other = ["null", "uknown", "complete"]

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
                        
#######adjust for realistic arrival times!!!!!!!!!!!!!!!!!!!!!!!!!!! later
                    if tick+10 >= int(appt_time):
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
                
                other_states = ["complete", "null"]

                if (getattr(p, "current_action") is not "finished"):
                    if (getattr(p, "bloods_appointment_time") in other_states and (getattr(p, "consultant_1_appointment_time") in other_states) and (getattr(p, "consultant_2_appointment_time") in other_states) ):
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
                for p in consult_patients:
                    if getattr(p, "arrived") == True:
                        if (getattr(c, "current_action") == "waiting"):
                            other = ["complete", "null", "uknown"]

                            #CHANGE FOR LONGEST WAITING ETC!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!/closest to time
                            if (getattr(p, "current_action") == "waiting" and ((getattr(p, "consultant_1_appointment_time") not in other) or (getattr(p, "consultant_2_appointment_time") not in other))):
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
import time
from agents import *
import pandas as pd
import random
from data_analyser import *

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
def consult_appts(appts_df, iterations, num_consultants, dr1, dr2):
    print(appts_df)
    """
    for number of drs on shift - chooses random number from this
    find the corresponding list of appointment times
    if theres still times - randomly pick one
    if there are none left, redo step 1
    """

    if dr1 == "null" and dr2 == "null":
        temp_list.append("null")
        print("append1")
        temp_list.append("null")
        print("append2")
        print(temp_list)
        return(temp_list)

    temp_list = []
    dr_list = [] # list of consultants
    appt_list = []
    

    for i in range(num_consultants):
        dr_list.append(i)

    for i in range(iterations): #for however many drs they have
        got_appts = False
        while not got_appts and dr_list:
            if num_consultants == 0: #no consultants today
                temp_list.append("null")
                print("append1")
                temp_list.append("null")
                print("append2")
                got_appts = True
                
            
            if i+1 == 1: # first iteration
                column_header = ("dr" + str(dr1) + "_appt")
                print(appts_df)
                possible_times = list(appts_df.loc[:,column_header])
                print(possible_times)
                possible_times = [x for x in possible_times if str(x).lower() != 'nan']
                

            elif i+1 == 2: # second iteration
                column_header = ("dr" + str(dr2) + "_appt")
                print(appts_df)
                possible_times = list(appts_df.loc[:,column_header])
                print(possible_times)
                possible_times = [x for x in possible_times if str(x).lower() != 'nan']

            else:
                print("error, i")

            print(possible_times)
            if possible_times: # if not empty
                appt_time = random.choice(possible_times)
                appt_list.append(appt_time)
                temp_list.append(appt_time)
                print("append")

                if iterations == 1 or i+1 == 1:
                    #remove from df
                    temp = dr1
                    if temp == 0:
                        appts_df.loc[appts_df.dr0_appt == appt_time, column_header] = "NaN"
                    elif temp == 1:
                        appts_df.loc[appts_df.dr1_appt == appt_time, column_header] = "NaN"
                    elif temp == 2:
                        appts_df.loc[appts_df.dr2_appt == appt_time, column_header] = "NaN"
                    elif temp == 3:
                        appts_df.loc[appts_df.dr3_appt == appt_time, column_header] = "NaN"
                    elif temp == 4:
                        appts_df.loc[appts_df.dr4_appt == appt_time, column_header] = "NaN"
                    else:
                        print("problem")
                    
                    # temp_list.append(appt_time)
                    # print("append1")
                    
                    if iterations == 1:
                        
                        temp_list.append("null")#second appt time is null becuase only 1 dr assigned
                        print("append2")
                    got_appts = True
                    

                elif iterations == 2 and i+1 == 2:
                    #check that appt is after the first
                    same = True

                    while same:
                        print(appt_time)
                        print(appt_list[0])
                        if appt_time <= appt_list[0]+30: #if earlier
                            # print(appt_time)
                            # print(appt_list[0])
                            # print(temp_list)
                            
                            # temp_list.remove(appt_time)
                            possible_times.remove(appt_time)
                            appt_time = random.choice(possible_times)
                            print(appt_time)
                        else:
                            same = False
                    
                    #remove from df
                    temp = dr2
                    if temp == 0:
                        appts_df.loc[appts_df.dr0_appt == appt_time, column_header] = "NaN"
                    elif temp == 1:
                        appts_df.loc[appts_df.dr1_appt == appt_time, column_header] = "NaN"
                    elif temp == 2:
                        appts_df.loc[appts_df.dr2_appt == appt_time, column_header] = "NaN"
                    elif temp == 3:
                        appts_df.loc[appts_df.dr3_appt == appt_time, column_header] = "NaN"
                    elif temp == 4:
                        appts_df.loc[appts_df.dr4_appt == appt_time, column_header] = "NaN"
                    else:
                        print("problem")

                    temp_list.append(appt_time)
                    print("append1")
                    got_appts = True
                    
                elif iterations == 2:
                    print("stuck here")
                    
            else: # if empty (no appts left with that dr)
                print(possible_times)
                if i+1 == 1:
                    print(dr_list)
                    print(dr1)
                    dr_list.remove(dr1)
                    print(dr_list)

                    if dr_list: #if drs with appts left
                        dr1 = random.choice(dr_list)

                    else: # no drs left
                        print(dr_list)
                        dr1 = "null"
                        temp_list.append("null")
                        print("append1")
                        temp_list.append("null")
                        print("append2")
                        got_appts = True
                        
                    
                elif i+1 == 2: #on second iteration
                    #need to choose new dr
                    print(dr_list)
                    print(dr1)
                    print(dr2)
                    if dr2 in dr_list:
                        dr_list.remove(dr2)
                    print(dr_list)
                    if dr_list: # if not empty
                        same = True
                        dr2 = random.choice(dr_list)
                        while same:
                            if dr2 == dr1:
                                if dr2 in dr_list:
                                    dr_list.remove(dr2)
                                print(dr_list)
                                if dr_list:
                                    dr2 = random.choice(dr_list)
                                else:
                                    temp_list.append("null")
                                    print("append2")
                                    got_appts = True
                                    

                            else:
                                same = False
                    else:
                        temp_list.append("null")
                        print("append2")
                        got_appts = True
                        
                    
                #restart while loop to get appt
    print(temp_list)
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
    
    #you cant have a consultant appointment without also having a bloods appointment
    bloods = True
    #choose whether one or two consultations
    if num_consultants > 1:
        consult_number = random.randint(0, 2)
    elif num_consultants == 1:
        consult_number = 1
    elif num_consultants == 0:
        consult_number = 0
    print(consultants)
    print(num_consultants)
    print(consult_number)
    if (consultants):
        
        
        #If 1 appointment
        
        if consult_number == 1: 
            dr_choice = random.randint(0, num_consultants-1) # choosing dr
            temp_list = consult_appts(appt_df, 1, num_consultants, dr_choice, "null") #chooses appointment time for consultant
            #update appts_df
            temp = dr_choice
            if temp == 0:
                appt_df.loc[appt_df.dr0_appt == temp_list[0], "dr0_appt"] = "NaN"
            elif temp == 1:
                appt_df.loc[appt_df.dr1_appt == temp_list[0], "dr1_appt"] = "NaN"
            elif temp == 2:
                appt_df.loc[appt_df.dr2_appt == temp_list[0], "dr2_appt"] = "NaN"
            elif temp == 3:
                appt_df.loc[appt_df.dr3_appt == temp_list[0], "dr3_appt"] = "NaN"
            elif temp == 4:
                appt_df.loc[appt_df.dr4_appt == temp_list[0], "dr4_appt"] = "NaN"
            else:
                print("problem")

            print(num_consultants)
            print(temp_list)
            dr = temp_list[0] #grabbing the consultants id from temp list
            consult_appt_time_1 = temp_list[1] #grabibng the appt time from temp list
            consult_appt_time_2 = "null"

            #update patient agent attributes
            setattr(patient, "assigned_consultant", dr)
            setattr(patient, "first_consult_appointment_time", str(consult_appt_time_1))
            setattr(patient, "second_consult_appointment_time", "null")

            #dr_temp = []
            #add patients to drs patient list
            # for i in range(num_consultants):
            #     if dr == i:
            #         dr_temp.append(getattr(patient,"id"))
            #         dr_dict['consultant_%s' % dr] = dr_temp


        #If 2 consultations
        elif consult_number == 2:
            dr_choice1 = random.randint(0, num_consultants-1)
            dr_choice2 = random.randint(0, num_consultants-1)
            
            #checking if chose same dr, they should be different
            same = True
            while same:
                if dr_choice2 == dr_choice1:
                    dr_choice2 = random.randint(0, num_consultants-1)
                else:
                    same = False

            temp_list = consult_appts(appt_df, 2, num_consultants, dr_choice1, dr_choice2)
            #update appts_df
            for i in temp_list:
                if i == temp_list[0]:
                    temp = dr_choice1
                elif i == temp_list[1]:
                    temp = dr_choice2
                if temp == 0:
                    appt_df.loc[appt_df.dr0_appt == temp_list[0], "dr0_appt"] = "NaN"
                elif temp == 1:
                    appt_df.loc[appt_df.dr1_appt == temp_list[0], "dr1_appt"] = "NaN"
                elif temp == 2:
                    appt_df.loc[appt_df.dr2_appt == temp_list[0], "dr2_appt"] = "NaN"
                elif temp == 3:
                    appt_df.loc[appt_df.dr3_appt == temp_list[0], "dr3_appt"] = "NaN"
                elif temp == 4:
                    appt_df.loc[appt_df.dr4_appt == temp_list[0], "dr4_appt"] = "NaN"
                else:
                    print("problem")

            print(temp_list)
            
            dr_1 = dr_choice1
            consult_appt_time_1 = temp_list[0]
            dr_2 = dr_choice2
            consult_appt_time_2 = temp_list[1]
            dr = (str(dr_1) + str(dr_2))

            #compare to find out which is the sooner consult
            if consult_appt_time_1 != "null" and consult_appt_time_2 != "null":
                if int(consult_appt_time_2) < int(consult_appt_time_1):
                    temp = int(consult_appt_time_1)
                    consult_appt_time_1 = int(consult_appt_time_2)
                    consult_appt_time_2 = temp
            elif consult_appt_time_1 == "null" and consult_appt_time_2 != "null":
                consult_appt_time_1 = consult_appt_time_2
                consult_appt_time_2 == "null"

            #update patient attirubtes
            setattr(patient, "assigned_consultant", dr)
            setattr(patient, "first_consult_appointment_time", str(consult_appt_time_1))
            setattr(patient, "second_consult_appointment_time", str(consult_appt_time_2))

            # dr_temp = []
            # for i in range(num_consultants):
            #     if dr_1 == i:
            #         dr_temp.append(getattr(patient,"id"))
            #         dr_dict['consultant_%s' % dr] = dr_temp
            #     elif dr_2 == i:
            #         dr_temp.append(getattr(patient,"id"))
            #         dr_dict['consultant_%s' % dr] = dr_temp
        
        elif consult_number == 0:
            setattr(patient, "assigned_consultant", "null")
            setattr(patient, "first_consult_appointment_time", "null")
            setattr(patient, "second_consult_appointment_time", "null")
            consult_appt_time_1 = "null"
            consult_appt_time_2 = "null"
    else: # no consultant appt
        setattr(patient, "assigned_consultant", "null")
        setattr(patient, "first_consult_appointment_time", "null")
        setattr(patient, "second_consult_appointment_time", "null")
        consult_appt_time_1 = "null"
        consult_appt_time_2 = "null"


    print(num_consultants)
    print(consult_appt_time_1)
    print(consult_appt_time_2)
    #if they dont have a consultants appointment, auto get bloods appt
    if bloods or (not consultants):
        bloods = True
        possible_times = appt_df.loc[:,"bloods_appt"] #retrieving all the possible blood appointment times
        print(possible_times)
        possible_times = [x for x in possible_times if str(x).lower() != 'nan']
        
        for i in possible_times:
            if consult_number == 1 and consult_appt_time_1 != "null":
                if i < (int(consult_appt_time_1)+30):#finding an appointment that is after the consultant appointment as per workflow
                    possible_times.remove(i)
            elif consult_number == 2 and consult_appt_time_2 != "null":
                if i < (int(consult_appt_time_2)+30):#finding an appointment that is after the consultant appointment as per workflow
                    possible_times.remove(i) 
        
        if possible_times:
            bloods_appt_time = random.choice(possible_times)#choose appt times for bloods
            setattr(patient, "bloods_appointment_time", str(bloods_appt_time))
            print(bloods_appt_time)
        else:
            bloods_appt_time = "null"
            setattr(patient, "bloods_appointment_time", str(bloods_appt_time))

        #update df
        print(appt_df)
        appt_df.loc[appt_df.bloods_appt == bloods_appt_time, "bloods_appt"] = "NaN"
        print(appt_df)

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
def initialise(data_capture_df):#add tally dict back
    
    #list_x = list(tally_dict[i].keys()) #values
    #list_y = list(tally_dict[i].values()) #percentages
    #if list_x:
    #    create_graph(list_x, list_y, " ", "test_x", "test_y", True)

    #DONT NEED TO WORK OUT THE DISTRIBUTIONS FOR THESES


    # patient_number = random.randint(untallied_dict["num_patients"])#graph
    # dr_number = random.randint(untallied_dict["num_consult"])#graph
    patient_number = 30
    dr_number = random.randint(1,5)
    nurse_number = random.randint(1,3)#up to 3 blood stations
    bloods_appt_length = 15 #assumption of 15mins 
    clinic_start = 480 #minutes of day (540 ticks) assumption from what told - 8am
    clinic_end = 1050 #minutes of day (1020 ticks) assumption from what told - 5:30pm
    nurse_list = []
    consultant_list = []
    waiting_room_capacity = 15
    # waiting_room_capacity = max(untallied_dict["num_patients"])#graph
    
    bloods_patients = []
    all_patients = []

    dr_list = []
    dr_dict = {}

    #create a list and then dict of drs
    for i in range(dr_number):
        dr_list.append(i+1)
        
    for i in dr_list:
        print(dr_list)
        print(i)
        dr_dict['consultant_%s' % i] = []


    #update below to be automated and also to generate based on dr number!!!!!!!!!!!!!!!
    
    appointment_df = pd.DataFrame()
    
    #seeting the appts times of bloods appt and adding to df
    appointment_times_bloods = appointment_times(clinic_start, bloods_appt_length, clinic_end-30) #28
    #appointment_df["bloods"]= appointment_times_bloods
    
    #initialise patient df: Patient identifier, appointment time bloods, appointment time clinic 1, appointment time clinic 2, current action, waiting for
    patient_df = pd.DataFrame(columns=["Patient", "ID", "Bloods_time", "Consultant_1_time", "Consultant_2_time", "current_action", "patient_satisfaction", "arrival_time"])

    HW_nurses = []
    Bloods_nurses = []
    
    #initialising nurses by how many there are
    for x in range(nurse_number):
        nurse = initialise_nurse(x)
        nurse_list.append(nurse)
    
    

    for nurse in nurse_list:
        if getattr(nurse, "type") == "HW":
            HW_nurses.append(nurse)
        elif getattr(nurse, "type") == "Bloods":
            Bloods_nurses.append(nurse)
        else:
            print("error")
        
        #if no bloods nurses, take 1 HW nurse and change them to a bloods nurse because unfeasible to have 0
        if (not Bloods_nurses) and (HW_nurses):
            temp_nurse = HW_nurses[0] 
            setattr(temp_nurse, "type", "Bloods")
            HW_nurses.remove(temp_nurse)
            Bloods_nurses.append(getattr(temp_nurse, "id"))

    #initialising drs by how many there are
    temp_list = []
    temp_dict = {}
    temp_dict["bloods"] = appointment_times_bloods
    for x in range(dr_number):
        consultant = initialise_consultant(x)
        consultant_list.append(consultant)
        
        if getattr(consultant, "sick") == True:
            print("SICK")
            clinic_times = []
        else:
            #take from the processed data - make sure in minutes form
            consultant_start = 540 #assumption
            consult_length = 20 #20-30mins in life
            consultant_end = 1020 #assumption

            clinic_times = appointment_times(consultant_start, consult_length, consultant_end) 
            print(clinic_times)

        #Appends to apopintment df
        temp_list.append("dr" + str(x))
        temp_dict[temp_list[x]] = clinic_times
        #appointment_df["dr" + str(x)]= clinic_times

    #add to appointment_df
    c = 0
    for i in temp_dict:
        temp_length = len(temp_dict[i])
        if c == 0:
            length = temp_length
        else:
            if temp_length > length:
                length = temp_length
        c += 1

    num_list = range(length)
    c = 0
    appointment_df["num"] = num_list
    for i in temp_dict:
        if c == 0: #bloods
            bloods_dict = dict(enumerate(temp_dict[i]))
            appointment_df["bloods_appt"] = appointment_df["num"].map(bloods_dict)
        elif c == 1:
            dr0_dict = dict(enumerate(temp_dict[i]))
            appointment_df["dr0_appt"] = appointment_df["num"].map(dr0_dict)
        elif c == 2:
            dr1_dict = dict(enumerate(temp_dict[i]))
            appointment_df["dr1_appt"] = appointment_df["num"].map(dr1_dict)
        elif c == 3:
            dr2_dict = dict(enumerate(temp_dict[i]))
            appointment_df["dr2_appt"] = appointment_df["num"].map(dr2_dict)
        elif c == 4:
            dr3_dict = dict(enumerate(temp_dict[i]))
            appointment_df["dr3_appt"] = appointment_df["num"].map(dr3_dict)
        elif c == 5:
            dr4_dict = dict(enumerate(temp_dict[i]))
            appointment_df["dr4_appt"] = appointment_df["num"].map(dr4_dict)
        c += 1


    #initialises patients
    for x in range(patient_number):
        print("PATIENT NUMBER")
        print(x)
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
        data_capture_df.at[x,"Consultant_scheduled_2"] = consult_appt_time_2

        temp_list.append(bloods_appt_time)
        temp_list.append(consult_appt_time_1)
        temp_list.append(consult_appt_time_2)      
            
        setattr(patient, "current_action", "appointed")
        current_action = getattr(patient, "current_action")
        temp_list.append(current_action)

        patient_satisfaction = getattr(patient, "patient_satisfaction") 
        temp_list.append(patient_satisfaction)

        #arrival
        arrival_diff = getattr(patient, "arrival_time")
        if consult_appt_time_1 == "null" and consult_appt_time_2 == "null":
            first_appt_time = bloods_appt_time # finding earliest appt
        elif consult_appt_time_1 == "null":
            first_appt_time = min(int(bloods_appt_time), int(consult_appt_time_2)) # finding earliest appt
        elif consult_appt_time_2 == "null":
            first_appt_time = min(int(bloods_appt_time), int(consult_appt_time_1)) # finding earliest appt
        elif consult_appt_time_1 != "null" and consult_appt_time_2 != "null":
            first_appt_time = min(int(bloods_appt_time),int(consult_appt_time_1), int(consult_appt_time_2)) # finding earliest appt

        else:
            print("ISSUE")
            print(bloods_appt_time)
            print(consult_appt_time_1)
            print(consult_appt_time_2)

        
        arrival_time = first_appt_time - int(arrival_diff)
        if arrival_time < clinic_start:#If arriving before clinic opens
            setattr(patient, "arrival_time", 540)

        temp_list.append(arrival_time)

        #add temp_list to dataframe
        patient_df.loc[len(patient_df)] = temp_list

        
    #need to update consultant attributes 
    # for ctant in consultant_list:
    #         print(dr_dict)
    #         consultant_patients = dr_dict['consultant_%s' % x]
    #         setattr(ctant, "patients_seeing", consultant_patients)
        

    print(patient_df)
    return(patient_df, nurse_list, consultant_list, bloods_patients, data_capture_df, dr_dict, clinic_start, clinic_end)     


#------------------continue from here -----------------





    


                    



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
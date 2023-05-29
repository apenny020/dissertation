from read_data import *
from data_analyser import *
import pandas as pd


#this will take the data and work out the probabilities for each section
#so need to work out times between check in and either H/W, bloods, consultant, Research
"""
There is data collection for:
Waiting times; Height/Weight, Bloods, Consultation 1/1 of 2/2
Durations of; Bloods, Consultation 1/2, 
Number of DNA's
Number of Patients in a day
Number of Consults in a day
Consult start times
Blood start times
Late durations

Number of patients at clinic at any one time
How many patients in bloods at one time
How many patients in consulatation at same time

"""
#This function finds the data for the paritcular given day
def collecting_days_data (all_data_df, current_day, num_rows):
    todays_data = []
    todays_patients = []
    #num_patients_in_day = len(todays_patients)
    for i in range(num_rows):
        date = all_data_df.iloc[i]["DateTime"]
        while date == current_day:
            temp_list = []
            id = all_data_df.iloc[i]["Patient_id"]
            state_enter = all_data_df.iloc[i]["State_Enter"]
            state =  all_data_df.iloc[i]["State"]
            temp_list.append(id)
            temp_list.append(date)
            temp_list.append(state_enter)
            temp_list.append(state)

            #add to lists
            todays_data.append(temp_list)
            if id not in todays_patients:
                todays_patients.append(id)

    return(todays_data, todays_patients)


#Calculates the durations, waiting times and other data needed to be found
def calculating_times (current_days_data , current_days_patients, waiting_df, number_df, duration_df, starts_df, wait_for_Height_and_weight, wait_for_Bloods, wait_for_consultation_1, wait_for_consultation_1_of_2, wait_for_consultation_2, bloods_duration, consultation_duration_1, consultation_duration_1_of_2, consultation_duration_2, late_duration, bloods_starts, consultation_starts, arrival_time, num_of_consultations, num_of_did_not_attends, num_of_lates, num_patients, final, first):
    
    if first == True:
        #Instantiating 
        arrival_time = []

        #To collect a list of waiting times in minutes
        wait_for_Height_and_weight = []
        wait_for_Bloods = []
        wait_for_consultation_1 = []
        wait_for_consultation_1_of_2 = []
        wait_for_consultation_2 = []

        #To collect appointment times approximation
        consultation_starts = []
        bloods_starts = []

        #To collect a list of duration times in minutes
        consultation_duration_1 = []
        consultation_duration_1_of_2 = []
        consultation_duration_2 = []
        bloods_duration = []
        late_duration = []

        num_of_consultations = [] 
        num_of_did_not_attends = []
        num_of_lates = []
        num_patients = []

    #To collect a list of number of patients to the particular event
    number_of_did_not_attends = 0
    number_of_lates = 0 #not including DNA's
    number_of_consultations = 0
    number_of_patients = len(current_days_patients)

    #re-sort the list by unique identifier (patient)
    sorted_current_days_data = sorted(current_days_data, key=lambda d: d['unique_identifier'])
    sorted_current_days_patients = current_days_patients.sort()

    #go through each item in the new sorted list and match it to particular situations and add the value to the above waiting time lists
    for i in sorted_current_days_data:
        c = 0 #counter to keep track of patient
        while i == current_days_patients[c].get("unique_identifier"): #while the patient is the same
            current_action = i.self[c].get("action").str().lower()
            previous_action = i.self[c-1].get("action").str().lower()
            future_action = i.self[c+1].get("action").str().lower() # need a fail safe here and above just incase at first or last action !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            
            if current_action == "patient identified by kiosk":
                arrival_time = i[c].get("date_time")[10:].time()
            
            elif current_action == "appointed" or "late arrival" or "patient identified by kiosk":
                #ignore
                print("hi")
            
            elif previous_action == "waiting height and weight": # you cant tell what is wait and and what is duration so duration will be fixed
                time_start = i[c-1].get("date_time")[8:].time()
                time_end = i[c].get("date_time")[8:].time()
                duration = time_end - time_start
                wait_for_Height_and_weight.append(round(duration))

            elif current_action == "in consultation 1 of 1"  and previous_action == "waiting consultation 1 of 1":
                time_start = i[c-1].get("date_time")[8:].time()
                time_end = i[c].get("date_time")[8:].time()
                duration = time_end - time_start
                wait_for_consultation_1.append(round(duration))
                consultation_starts.append(time_start)

            elif current_action == "in consultation 1 of 2" and previous_action == "waiting consultation 1 of 2":
                time_start = i[c-1].get("date_time")[8:].time()
                time_end = i[c].get("date_time")[8:].time()
                duration = time_end - time_start
                wait_for_consultation_1_of_2.append(round(duration))
                consultation_starts.append(time_start)

            elif current_action == "in consultation 2 of 2" and previous_action == "waiting consultation 2 of 2":
                time_start = i[c-1].get("date_time")[8:].time()
                time_end = i[c].get("date_time")[8:].time()
                duration = time_end - time_start
                wait_for_consultation_2.append(round(duration))  
                consultation_starts.append(time_start)

            elif current_action == "in blood room" and previous_action == "waiting blood room":
                time_start = i[c-1].get("date_time")[8:].time()
                time_end = i[c].get("date_time")[8:].time()
                duration = time_end - time_start
                wait_for_Bloods.append(round(duration))
                bloods_starts.append(time_start)

            elif current_action == "late arrival" and future_action != "did not attend":
                number_of_lates += 1
                time_start = i[c].get("date_time")[8:].time()
                time_end = i[c+1].get("date_time")[8:].time()
                duration = time_end - time_start
                late_duration.append(round(duration))

            else:
                #x
                print ("hi")
            
            #Same as above but looking for durations now and numbers of patients to add to the lists
            if current_action == "appointed" or "late arrival" or "patient identified by kiosk":
                #ignore
                print ("hi")
            
            elif current_action == "did not attend":
                number_of_did_not_attends =+ 1

            elif previous_action == "in consultation 1 of 1":
                time_start = i[c-1].get("date_time")[8:].time()
                time_end = i[c].get("date_time")[8:].time()
                duration = time_end - time_start
                consultation_duration_1.append(round(duration))

            elif previous_action == "in consultation 1 of 2":
                time_start = i[c-1].get("date_time")[8:].time()
                time_end = i[c].get("date_time")[8:].time()
                duration = time_end - time_start
                consultation_duration_1_of_2.append(round(duration))

            elif previous_action == "in consultation 2 of 2":
                time_start = i[c-1].get("date_time")[8:].time()
                time_end = i[c].get("date_time")[8:].time()
                duration = time_end - time_start
                consultation_duration_2.append(round(duration))

            elif previous_action == "in blood room":
                time_start = i[c-1].get("date_time")[8:].time()
                time_end = i[c].get("date_time")[8:].time()
                duration = time_end - time_start
                bloods_duration.append(round(duration))

            else:
                #x
                print("hi")

            #can make above more efficient by having a function that takes in what its looking for and produces the value/time

            c =+ 1 #counter


    num_of_consultations.append((number_of_consultations/number_of_patients)*100)
    num_of_did_not_attends.append((number_of_did_not_attends/number_of_patients)*100)
    num_of_lates.append((number_of_lates/number_of_patients)*100)
    num_patients.append(number_of_patients)

    if final == True:
        #adding lists to dataframes above - could turn more efficient !!!!!!!!!!!!!
        waiting_df ["wait_h&w"] = wait_for_Height_and_weight
        waiting_df ["wait_bloods"] = wait_for_Bloods
        waiting_df ["wait_consult_1"] = wait_for_consultation_1
        waiting_df ["wait_consult_1/2"] = wait_for_consultation_1_of_2
        waiting_df ["wait_consult_2"] = wait_for_consultation_2
        #waiting_df_headers = ["wait_h&w","wait_bloods","wait_consult_1","wait_consult_1/2"]

        duration_df ["duration_bloods"] = bloods_duration
        duration_df ["duration_consult_1"] = consultation_duration_1
        duration_df ["duration_consult_1/2"] = consultation_duration_1_of_2
        duration_df ["duration_consult_2"] = consultation_duration_2
        duration_df ["duration_lates"] = late_duration

        starts_df ["starts_bloods"] = bloods_starts
        starts_df ["starts_consult"] = consultation_starts
        starts_df ["starts_arrival"] = arrival_time

        number_df ["num_consult"] = num_of_consultations
        number_df ["num_dna"] = num_of_did_not_attends
        number_df ["num_lates"] = num_of_lates
        number_df ["num_patients"] = num_patients

        return (waiting_df, number_df, duration_df, starts_df)
    
    return(wait_for_Height_and_weight, wait_for_Bloods, wait_for_consultation_1, wait_for_consultation_1_of_2, wait_for_consultation_2, bloods_duration, consultation_duration_1, consultation_duration_1of_2, consultation_duration_2, late_duration, bloods_starts, consultation_starts, arrival_time, num_of_consultations, num_of_did_not_attends, num_of_lates, num_patients)


        

#Calculates the number of patients in certain situations
def calculating_patient_numbers (todays_data, todays_patients, number_list, counter_list, first, final):#!!!!!!!!!!!!unfinished function in the elifs etc !!!!!!!!!!!!!!!!!
    length = len(todays_data)
    start_time = todays_data.self[0].get("date_time")
    end_time = todays_data.self[length-1].get("date_time")

    counter = 0

    if first == True:
        patients_in_clinic = []
        patients_in_bloods = []
        patients_in_consultation = []

        clinic_counter = 0#number of patients in clinic at any time
        bloods_counter = 0#number of patients in bloods at one time
        consult_counter = 0#number of patients in consultation at one time


    while (start_time <= end_time):
        for i in todays_data:
            current_action = i.self[counter].get("action").str().lower()
            previous_action = i.self[counter-1].get("action").str().lower()
            current_patient = i.self[counter].get("unique_identifier").str().lower()

            #checking for patients arriving and adding to list
            if current_action == "patient identified by kiosk":
                patients_in_clinic = current_patient

            elif current_action == "in blood room":
                patients_in_bloods = current_patient

            elif current_action == "in consultation 1 of 1" or "in consultation 1 of 2" of "in consultation 2 of 2":
                patients_in_consultation = current_patient

            #checking for patients leaving and taking a count
            elif previous_action == "in blood room":
                if current_patient in patients_in_bloods:
                    patients_in_bloods.remove(current_patient)
                
                temp = len(patients_in_bloods)
                if bloods_counter < temp:
                    bloods_counter = temp

            elif previous_action == "in consultation 1 of 1" or "in consultation 1 of 2" of "in consultation 2 of 2":
                if current_patient in patients_in_consultation:
                    patients_in_consultation.remove(current_patient)
                
                temp = len(patients_in_clinic)
                if consult_counter < temp:
                    consult_counter = temp

            elif current_action[8:] == "complete":
                if current_patient in patients_in_clinic:
                    patients_in_clinic.remove(current_patient)
                
                temp = len(patients_in_clinic)
                if clinic_counter < temp:
                    clinic_counter = temp
            
            counter += 1

    if final == True:
        return_dict = {"number_list":number_list, "counter_list":counter_list}
        return(return_dict)
    
    return(number_list, counter_list)




#finds the current date and calls a function with that information -
#^recieves back the data and patients for only that day - 
#^calls the function to work out data and gets it back
#calls all above functions

# def give_date(data_list): #need to edit the function to take in the date when requested !!!!!!!!!1
#     temp_val = []
#     temp_val.append(data_list[0])
#     current_day = temp_val[0].get("date_time")      
#     current_day = current_day[:10] #should cut it to just be date
#     return (data_list) # add here!!!!!!!!!!! also could maybe have the function calling taken out !!!!!!!!!!!



def get_data():
    with open("data_input_file_2018", "r") as data_file:
        Lines = data_file.readlines()
        data_file.close()

    #get all the data
    for line in range(Lines):
        temp_list = line
        all_data_df = pd.DataFrame()
        all_data_df = all_data_df.assign(Patient_id=[], DateTime=[], State_Enter=[], State=[])
        all_data_df.loc[len(all_data_df)] = temp_list

    #work out number of dates
    list_days = []
    num_rows = len(all_data_df.index)
    for i in range(num_rows):
        temp = all_data_df.iloc[i]["DateTime"]
        if temp not in list_days:
            temp = temp[:10]
            list_days.append(i)
    
    num_days = len(list_days)
    return(all_data_df, num_days, list_days, num_rows)



#calls all the functions
def process_all_data():

    all_data_df, num_days, list_days, num_rows = get_data()

    waiting_df = pd.DataFrame()
    number_df = pd.DataFrame()
    duration_df = pd.DataFrame()
    starts_df = pd.DataFrame()

    number_list = []
    counter_list = []

    final = False
    first = False
    counter = 0
    for day in list_days:
        current_days_data, current_days_patients = collecting_days_data(all_data_df, day, num_rows)

        counter =+ 1
        if counter == num_days:
            final = True
            waiting_df, number_df, duration_df, starts_df = calculating_times (current_days_data, current_days_patients, waiting_df, number_df, duration_df, starts_df, wait_for_Height_and_weight, wait_for_Bloods, wait_for_consultation_1, wait_for_consultation_1_of_2, wait_for_consultation_2, bloods_duration, consultation_duration_1, consultation_duration_1_of_2, consultation_duration_2, late_duration, bloods_starts, consultation_starts, arrival_time, num_of_consultations, num_of_did_not_attends, num_of_lates, num_patients, final, first)
            return_dict = calculating_patient_numbers(current_days_data, current_days_patients, number_list, counter_list, final, first) 

        elif counter == 1:
            first = True
            wait_for_Height_and_weight, wait_for_Bloods, wait_for_consultation_1, wait_for_consultation_1_of_2, wait_for_consultation_2, bloods_duration, consultation_duration_1, consultation_duration_1_of_2, consultation_duration_2, late_duration, bloods_starts, consultation_starts, arrival_time, num_of_consultations, num_of_did_not_attends, num_of_lates, num_patients = calculating_times (current_days_data , current_days_patients, waiting_df, number_df, duration_df, starts_df, wait_for_Height_and_weight, wait_for_Bloods, wait_for_consultation_1, wait_for_consultation_1_of_2, wait_for_consultation_2, bloods_duration, consultation_duration_1, consultation_duration_1_of_2, consultation_duration_2, late_duration, bloods_starts, consultation_starts, arrival_time, num_of_consultations, num_of_did_not_attends, num_of_lates, num_patients, final, first)
            number_list, counter_list = calculating_patient_numbers(current_days_data, current_days_patients, number_list, counter_list, final, first) 

        else:
            first = False
            wait_for_Height_and_weight, wait_for_Bloods, wait_for_consultation_1, wait_for_consultation_1_of_2, wait_for_consultation_2, bloods_duration, consultation_duration_1, consultation_duration_1_of_2, consultation_duration_2, late_duration, bloods_starts, consultation_starts, arrival_time, num_of_consultations, num_of_did_not_attends, num_of_lates, num_patients = calculating_times (current_days_data , current_days_patients, waiting_df, number_df, duration_df, starts_df, wait_for_Height_and_weight, wait_for_Bloods, wait_for_consultation_1, wait_for_consultation_1_of_2, wait_for_consultation_2, bloods_duration, consultation_duration_1, consultation_duration_1_of_2, consultation_duration_2, late_duration, bloods_starts, consultation_starts, arrival_time, num_of_consultations, num_of_did_not_attends, num_of_lates, num_patients, final, first)
            number_list, counter_list = calculating_patient_numbers(current_days_data, current_days_patients, number_list, counter_list, final, first) 



    list_of_df = [waiting_df, duration_df, starts_df]
    num_df = [number_df]

    tally_dict = {}
    list_names = []
    list_tallys = []


    #get the lists out of the df
    df_dict = {}
    num_dict = {}
    column_headers = []
    temp_col = []

    c = 0 # counter
    for i in list_of_df:
        column_headers.append(list(i.columns.values))
        temp_col.append(i[column_headers[c]].tolist())
        c =+ 1

    for header, col in zip(column_headers, temp_col):
        df_dict[header] = col


    #for number_df
    for i in num_df:
        column_headers.append(list(i.columns.values))
        temp_col.append(i[column_headers[c]].tolist())
        c =+ 1

    for header, col in zip(column_headers, temp_col):
        num_dict[header] = col



    #getting the tallys
    for i in df_dict:
        name, tally = (get_probabilities_time(df_dict[i]))
        list_names.append(str(name))
        list_tallys.append(tally)

    for i in return_dict:
        name, tally = (get_probabilities_time(return_dict[i])) #gives the values as a list
        list_names.append(str(name))
        list_tallys.append(tally)

    for name, tally in zip(list_names, list_tallys):
        tally_dict[name] = tally

    
    #raw, untallied dict of lists
    untallied_dict = {}

    for i in df_dict:
        temp_list = df_dict[i]
        temp_list = sorted(temp_list)
        untallied_dict[i]=temp_list
    
    for i in return_dict:
        temp_list = df_dict[i]
        temp_list = sorted(temp_list)
        untallied_dict[i]=temp_list
    
    for i in num_dict:
        temp_list = df_dict[i]
        temp_list = sorted(temp_list)
        untallied_dict[i]=temp_list

    return(tally_dict, untallied_dict, num_dict)


#running here !!!!!!!!!!!!!

#a = give_date(date_sorted_data_list, 0)
#print("hi")

#NEEDS something that analyses the flow of events

#Cancelled <-- need to add in !!!!!!!!!!!!!!!!!

#Exclusions !!!!!!!!!!!!!!!!!!!!!
#If does not complete - ignore data, 
#if more than 10 hours, ignore


#!!!!further work - different days could have different waiting times because of different number of staff - so adjust to this
# ^ would play into changing number of staff
#there is 1 blood room and up to 3 blood stations at one time (but rare that all 3 would be up)
#!!!! remember that a patient is connected to a consultant
#if consultation is longer than 2 hours, throw away


#2 - extension see if you can work out how many staff working by how many patients in which area at the same time

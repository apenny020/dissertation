from read_data import *
from data_analyser import *
import pandas as pd
from datetime import datetime, date



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
    print(num_rows)
    print(current_day)
    todays_data = []
    todays_patients = []
    #num_patients_in_day = len(todays_patients)
    for i in range(num_rows):
        date = (all_data_df.iloc[i]["DateTime"])[:10]
        while date == current_day:
            print(i)
            temp_dict = {}
            id = all_data_df.iloc[i]["Patient_id"]
            state_enter = all_data_df.iloc[i]["State_Enter"]
            state =  all_data_df.iloc[i]["State"]
            time =(all_data_df.iloc[i]["DateTime"])[11:19]
            temp_dict["id"] = id
            temp_dict["time"] = time
            temp_dict["state_enter"] = state_enter
            temp_dict["action"] = state
            print(temp_dict)

            #add to lists
            todays_data.append(temp_dict)
            if id not in todays_patients:
                print(id)
                print(todays_patients)
                todays_patients.append(id)
                break
            else:
                break

    return(todays_data, todays_patients)


#Calculates the durations, waiting times and other data needed to be found
def calculating_times (current_days_data , current_days_patients, waiting_df, number_df, duration_df, starts_df, wait_for_Height_and_weight, wait_for_Bloods, wait_for_consultation_1, wait_for_consultation_1_of_2, wait_for_consultation_2, bloods_duration, consultation_duration_1, consultation_duration_1_of_2, consultation_duration_2, late_duration, bloods_starts, consultation_starts, arrival_time, num_of_consultations, num_of_did_not_attends, num_of_lates, num_patients, final, first):
    
    #To collect a list of number of patients to the particular event
    number_of_did_not_attends = 0
    number_of_lates = 0 #not including DNA's
    number_of_consultations = 0
    number_of_patients = len(current_days_patients)
    print(current_days_patients)

    #re-sort the list by unique identifier (patient)
    #sorted_current_days_data = sorted(current_days_data, key=lambda d: d['unique_identifier'])
    #sorted_current_days_patients = current_days_patients.sort()

    #go through each item in the new sorted list and match it to particular situations and add the value to the above waiting time lists
    c=0
    patient_exists = True
    next_patient_exists = True
    while patient_exists:
        for i in current_days_data:
            

            #incase it will go past list range
            try:
                current_days_data[c+1]
            except IndexError:
                next_patient_exists = False
                #raise Exception("no more patients after this one in list")
            else:
                next_patient_exists = True
            

            print(current_days_data[c]["id"])
            print(i["id"])
            print("----------------------") 

            #c = 0 #counter to keep track of patient
            
            while ((str(i["id"])) is (str(current_days_data[c]["id"]))): #while the patient is the same
                
                current_action = str(i["action"]).lower()
                print(current_action)
                if c > 0 and i["id"] == current_days_data[c]["id"]:
                    previous_action = str(current_days_data[c-1]["action"]).lower()
                    print (previous_action)
                if next_patient_exists:
                    if i["id"] is current_days_data[c+1]["id"]:
                        future_action = str(current_days_data[c+1].get("action")).lower() # need a fail safe here and above just incase at first or last action !!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                        print(future_action)
                else:
                    future_action = "invalid"

                if c > 0 and i["id"] == current_days_data[c-1]["id"]:
                    time_start = datetime.strptime(current_days_data[c-1]["time"], '%H:%M:%S').time()
                time_end = datetime.strptime(i["time"], '%H:%M:%S').time()
                print(time_end)

                print(current_action)
                if current_action == "patient identified by kiosk":
                    arrival_time = datetime.strptime(i["time"], '%H:%M:%S').time()
                
                elif current_action == "appointed" or current_action == "late arrival" or current_action == "patient identified by kiosk":
                    #ignore
                    print("ignore")
                
                elif previous_action == "waiting height and weight": # you cant tell what is wait and and what is duration so duration will be fixed
                    duration = datetime.combine(date.today(), time_end) - datetime.combine(date.today(), time_start)
                    duration = str(duration)[:4]
                    print(duration)
                    duration = datetime.strptime(duration, '%H:%M').time()
                    wait_for_Height_and_weight.append(duration)
                    print("~~~~~~~~~~~~~~~~")
                    print (wait_for_Height_and_weight)

                elif current_action == "in consultation 1 of 1"  and previous_action == "waiting consultation 1 of 1":
                    duration = datetime.combine(date.today(), time_end) - datetime.combine(date.today(), time_start)
                    duration = str(duration)[:4]
                    duration = datetime.strptime(duration, '%H:%M').time()
                    wait_for_consultation_1.append(duration)
                    consultation_starts.append(time_start)
                    print("~~~~~~~~~~~~~~~~")
                    print (wait_for_consultation_1)

                elif current_action == "in consultation 1 of 2" and previous_action == "waiting consultation 1 of 2":
                    duration = datetime.combine(date.today(), time_end) - datetime.combine(date.today(), time_start)
                    duration = str(duration)[:4]
                    duration = datetime.strptime(duration, '%H:%M').time()
                    wait_for_consultation_1_of_2.append(duration)
                    consultation_starts.append(time_start)
                    print("~~~~~~~~~~~~~~~~")
                    print(wait_for_consultation_1_of_2)

                elif current_action == "in consultation 2 of 2" and previous_action == "waiting consultation 2 of 2":
                    duration = datetime.combine(date.today(), time_end) - datetime.combine(date.today(), time_start)
                    duration = str(duration)[:4]
                    duration = datetime.strptime(duration, '%H:%M').time()
                    wait_for_consultation_2.append(duration)  
                    consultation_starts.append(time_start)
                    print("~~~~~~~~~~~~~~~~")
                    print (wait_for_consultation_2)

                elif current_action == "in blood room" and previous_action == "waiting blood room":
                    duration = datetime.combine(date.today(), time_end) - datetime.combine(date.today(), time_start)
                    duration = str(duration)[:4]
                    duration = datetime.strptime(duration, '%H:%M').time()
                    wait_for_Bloods.append(duration)
                    bloods_starts.append(time_start)
                    print("~~~~~~~~~~~~~~~~")
                    print (wait_for_Bloods)

                elif current_action == "late arrival" and future_action != "did not attend":
                    time_start = datetime.strptime(i["date_time"], '%H:%M:%S').time()
                    if next_patient_exists:
                        if i["id"] == current_days_data[c+1]["id"]:
                            time_end = datetime.strptime(current_days_data[c+1]["date_time"], '%H:%M:%S').time()
                    
                        number_of_lates += 1
                        duration = datetime.combine(date.today(), time_end) - datetime.combine(date.today(), time_start)
                        duration = str(duration)[:4]
                        duration = datetime.strptime(duration, '%H:%M').time()
                        late_duration.append(duration)

                else:
                    #x
                    print ("ignore2")
                
                
                if c > 0 and i["id"] == current_days_data[c-1]["id"]:
                    time_start = datetime.strptime(current_days_data[c-1]["time"], '%H:%M:%S').time()
                time_end = datetime.strptime(i["time"], '%H:%M:%S').time()

                #Same as above but looking for durations now and numbers of patients to add to the lists
                if current_action == "appointed" or current_action == "late arrival" or current_action == "patient identified by kiosk":
                    #ignore
                    print ("hi")
                
                elif current_action == "did not attend":
                    number_of_did_not_attends += 1

                elif previous_action == "in consultation 1 of 1":
                    duration = datetime.combine(date.today(), time_end) - datetime.combine(date.today(), time_start)
                    duration = str(duration)[:4]
                    duration = datetime.strptime(duration, '%H:%M').time()
                    consultation_duration_1.append(duration)

                elif previous_action == "in consultation 1 of 2":
                    duration = datetime.combine(date.today(), time_end) - datetime.combine(date.today(), time_start)
                    duration = str(duration)[:4]
                    duration = datetime.strptime(duration, '%H:%M').time()
                    consultation_duration_1_of_2.append(duration)

                elif previous_action == "in consultation 2 of 2":
                    duration = datetime.combine(date.today(), time_end) - datetime.combine(date.today(), time_start)
                    duration = str(duration)[:4]
                    duration = datetime.strptime(duration, '%H:%M').time()
                    consultation_duration_2.append(duration)

                elif previous_action == "in blood room":
                    duration = datetime.combine(date.today(), time_end) - datetime.combine(date.today(), time_start)
                    duration = str(duration)[:4]
                    duration = datetime.strptime(duration, '%H:%M').time()
                    bloods_duration.append(duration)

                else:
                    #x
                    print("hi")

                #can make above more efficient by having a function that takes in what its looking for and produces the value/time

                c += 1 #counter

                #incase gone past list range
                try:
                    current_days_data[c]
                except IndexError:
                    patient_exists = False
                    #raise Exception("finished list")
                    break
                else:
                    patient_exists = True
                
                if not patient_exists:
                    break


    num_of_consultations.append((number_of_consultations/number_of_patients)*100)
    num_of_did_not_attends.append((number_of_did_not_attends/number_of_patients)*100)
    num_of_lates.append((number_of_lates/number_of_patients)*100)
    num_patients.append(number_of_patients)

    if final == True:
        #adding lists to dataframes above - could turn more efficient !!!!!!!!!!!!!
        print (wait_for_Bloods)
        print (wait_for_consultation_1)
        print (wait_for_consultation_1_of_2)
        print (wait_for_consultation_2)
        print (wait_for_Height_and_weight)
    
        bloods = len(wait_for_Bloods)
        consult1 = len(wait_for_consultation_1)
        #consult12 = len(wait_for_consultation_1_of_2)
        #consult2 = len(wait_for_consultation_2)
        hw = len(wait_for_Height_and_weight)
        
        counter = [bloods, consult1, hw]
        counter = sorted(counter)
        print(counter)
        print(waiting_df)
        for i in counter:
            #SORT NUMBER OF ROWS/COLUMNS ISSUE
            if i:
                if i == bloods:
                    waiting_df ["wait_bloods"] = wait_for_Bloods
                elif i == consult1:
                    waiting_df ["wait_consult_1"] = wait_for_consultation_1
                #elif i == consult12:
                #    waiting_df ["wait_consult_1/2"] = wait_for_consultation_1_of_2
                #elif i == consult2:
                #    waiting_df ["wait_consult_2"] = wait_for_consultation_2
                elif i == hw:
                    waiting_df ["wait_h&w"] = wait_for_Height_and_weight
        print(waiting_df)
        print("______________________")

        
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
    
    return(wait_for_Height_and_weight, wait_for_Bloods, wait_for_consultation_1, wait_for_consultation_1_of_2, wait_for_consultation_2, bloods_duration, consultation_duration_1, consultation_duration_1_of_2, consultation_duration_2, late_duration, bloods_starts, consultation_starts, arrival_time, num_of_consultations, num_of_did_not_attends, num_of_lates, num_patients)


        

#Calculates the number of patients in certain situations
def calculating_patient_numbers (todays_data, todays_patients, counter_list, first, final):#!!!!!!!!!!!!unfinished function in the elifs etc !!!!!!!!!!!!!!!!!
    length = len(todays_data)

    print (todays_data)
    todays_data = sorted(todays_data, key=lambda d: d["time"])
    print (todays_data)

    start_time = todays_data[0]["time"]
    end_time = todays_data[length-1]["time"]

    counter = 0
    
    patients_in_clinic = []
    patients_in_bloods = []
    patients_in_consultation = []

    clinic_counter = 0#number of patients in clinic at any time
    bloods_counter = 0#number of patients in bloods at one time
    consult_counter = 0#number of patients in consultation at one time

    patient_exists = True

    while patient_exists:
        while (start_time <= end_time):
            
            #incase gone past list range
            try:
                todays_data[counter]
            except IndexError:
                patient_exists = False
                break
            else:
                patient_exists = True

            for i in todays_data:
                current_action = str(i["action"]).lower()
                if counter > 0 and i["id"] == todays_data[counter]["id"]:
                    previous_action = str(todays_data[counter-1]["action"]).lower()
                else: 
                    previous_action = "invalid"
                current_patient = str(i["id"]).lower()

                #checking for patients arriving and adding to list
                if current_action == "patient identified by kiosk":
                    patients_in_clinic.append(current_patient)

                elif current_action == "in blood room":
                    patients_in_bloods.append(current_patient)

                elif current_action == "in consultation 1 of 1" or current_action == "in consultation 1 of 2" or current_action == "in consultation 2 of 2":
                    patients_in_consultation.append(current_patient)

                #checking for patients leaving and taking a count
                elif previous_action == "in blood room":
                    if current_patient in patients_in_bloods:
                        patients_in_bloods.remove(current_patient)
                    
                    temp = len(patients_in_bloods)
                    if bloods_counter < temp:
                        bloods_counter = temp

                elif previous_action == "in consultation 1 of 1" or previous_action =="in consultation 1 of 2" or previous_action == "in consultation 2 of 2":
                    if current_patient in patients_in_consultation:
                        print(current_patient)
                        print(patients_in_consultation)
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

    
    counter_list.append(consult_counter)
    counter_list.append(bloods_counter)
    counter_list.append(clinic_counter)

    return(counter_list)




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
    with open("data_input_file_2018.txt", "r") as data_file:
        Lines = data_file.readlines()
        data_file.close()

    #get all the data
    c = 0
    all_data_df = pd.DataFrame()
    all_data_df = all_data_df.assign(Patient_id=[], DateTime=[], State_Enter=[], State=[])
        
    
    

    for line in Lines:
        #turn into list
        line = list(line.split("\t"))
        line[3] = line[3].replace("\n", "")
        line[0] = line[0].replace("ï»¿", "")


        print (len(Lines))
        c += 1
        print(c)
        if c == 200:
            break
        all_data_df.loc[len(all_data_df)] = line
        print(all_data_df)
        all_data_df.to_csv("all_data")

    #work out number of dates
    list_days = []
    num_rows = len(all_data_df.index)
    print(num_rows)
    for i in range(num_rows):
        temp = all_data_df.iloc[i]["DateTime"]
        print(temp)
        if temp[:10] not in list_days:
            print(list_days)
            print(temp)
            temp = temp[:10]
            list_days.append(temp)

    print(list_days)
    
    num_days = len(list_days)
    return(all_data_df, num_days, list_days, num_rows)



#calls all the functions
def process_all_data():

    all_data_df, num_days, list_days, num_rows = get_data()

    waiting_df = pd.DataFrame()
    number_df = pd.DataFrame()
    duration_df = pd.DataFrame()
    starts_df = pd.DataFrame()

    counter_list = []

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


    final = False
    first = False
    counter = 0
    for day in list_days:
        current_days_data, current_days_patients = collecting_days_data(all_data_df, day, num_rows)
        print(current_days_data)
        print(current_days_patients)

        counter += 1
        if counter == num_days:
            final = True
            waiting_df, number_df, duration_df, starts_df = calculating_times (current_days_data, current_days_patients, waiting_df, number_df, duration_df, starts_df, wait_for_Height_and_weight, wait_for_Bloods, wait_for_consultation_1, wait_for_consultation_1_of_2, wait_for_consultation_2, bloods_duration, consultation_duration_1, consultation_duration_1_of_2, consultation_duration_2, late_duration, bloods_starts, consultation_starts, arrival_time, num_of_consultations, num_of_did_not_attends, num_of_lates, num_patients, final, first)
            return_dict = calculating_patient_numbers(current_days_data, current_days_patients, counter_list, final, first) 

        elif counter == 1:
            first = True
            wait_for_Height_and_weight, wait_for_Bloods, wait_for_consultation_1, wait_for_consultation_1_of_2, wait_for_consultation_2, bloods_duration, consultation_duration_1, consultation_duration_1_of_2, consultation_duration_2, late_duration, bloods_starts, consultation_starts, arrival_time, num_of_consultations, num_of_did_not_attends, num_of_lates, num_patients = calculating_times (current_days_data , current_days_patients, waiting_df, number_df, duration_df, starts_df, wait_for_Height_and_weight, wait_for_Bloods, wait_for_consultation_1, wait_for_consultation_1_of_2, wait_for_consultation_2, bloods_duration, consultation_duration_1, consultation_duration_1_of_2, consultation_duration_2, late_duration, bloods_starts, consultation_starts, arrival_time, num_of_consultations, num_of_did_not_attends, num_of_lates, num_patients, final, first)
            counter_list = calculating_patient_numbers(current_days_data, current_days_patients, counter_list, final, first) 

        else:
            first = False
            wait_for_Height_and_weight, wait_for_Bloods, wait_for_consultation_1, wait_for_consultation_1_of_2, wait_for_consultation_2, bloods_duration, consultation_duration_1, consultation_duration_1_of_2, consultation_duration_2, late_duration, bloods_starts, consultation_starts, arrival_time, num_of_consultations, num_of_did_not_attends, num_of_lates, num_patients = calculating_times (current_days_data , current_days_patients, waiting_df, number_df, duration_df, starts_df, wait_for_Height_and_weight, wait_for_Bloods, wait_for_consultation_1, wait_for_consultation_1_of_2, wait_for_consultation_2, bloods_duration, consultation_duration_1, consultation_duration_1_of_2, consultation_duration_2, late_duration, bloods_starts, consultation_starts, arrival_time, num_of_consultations, num_of_did_not_attends, num_of_lates, num_patients, final, first)
            counter_list = calculating_patient_numbers(current_days_data, current_days_patients,  counter_list, final, first) 



    list_of_df = [waiting_df, duration_df, starts_df]
    print(waiting_df)
    print(duration_df)
    print(starts_df)
    print("-----------")
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
        print(i)
        print(column_headers)
        print("----------")
        for col in column_headers:
            temp = i[col].values.tolist()
            temp_col.append(temp)
        

    for header, col in zip(column_headers, temp_col):
        df_dict[header] = col


    #for number_df
    for i in num_df:
        column_headers.append(list(i.columns.values))
        temp_col.append(i[column_headers[c]].tolist())
        c += 1

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

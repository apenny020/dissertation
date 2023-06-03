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
    # print(num_rows)
    # print(current_day)
    todays_data = []
    todays_patients = []
    #num_patients_in_day = len(todays_patients)
    for i in range(num_rows):
        date = (all_data_df.iloc[i]["DateTime"])[:10]
        while date == current_day:
            #print(i)
            temp_dict = {}
            id = all_data_df.iloc[i]["Patient_id"]
            state_enter = all_data_df.iloc[i]["State_Enter"]
            state =  all_data_df.iloc[i]["State"]
            time =(all_data_df.iloc[i]["DateTime"])[11:19]
            temp_dict["id"] = id
            temp_dict["time"] = time
            temp_dict["state_enter"] = state_enter
            temp_dict["action"] = state
            #print(temp_dict)

            #add to lists
            todays_data.append(temp_dict)
            if id not in todays_patients:
                #print(id)
                #print(todays_patients)
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
    #print(current_days_patients)

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
            

            #print(current_days_data[c]["id"])
            #print(i["id"])
            #print("----------------------") 

            #c = 0 #counter to keep track of patient
            
            while ((str(i["id"])) is (str(current_days_data[c]["id"]))): #while the patient is the same
                
                current_action = str(i["action"]).lower()
                #print(current_action)
                if c > 0 and i["id"] == current_days_data[c]["id"]:
                    previous_action = str(current_days_data[c-1]["action"]).lower()
                    #print (previous_action)
                if next_patient_exists:
                    if i["id"] is current_days_data[c+1]["id"]:
                        future_action = str(current_days_data[c+1].get("action")).lower() # need a fail safe here and above just incase at first or last action !!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                        #print(future_action)
                else:
                    future_action = "invalid"

                if c > 0 and i["id"] == current_days_data[c-1]["id"]:
                    time_start = datetime.strptime(current_days_data[c-1]["time"], '%H:%M:%S').time()
                time_end = datetime.strptime(i["time"], '%H:%M:%S').time()
                #print(time_end)

                #print(current_action)
                if current_action == "patient identified by kiosk":
                    arrival_time.append(datetime.strptime(i["time"], '%H:%M:%S').time())
                
                elif current_action == "appointed" or current_action == "late arrival" or current_action == "patient identified by kiosk":
                    #ignore
                    print("ignore")
                
                elif previous_action == "waiting height and weight": # you cant tell what is wait and and what is duration so duration will be fixed
                    duration = datetime.combine(date.today(), time_end) - datetime.combine(date.today(), time_start)
                    duration = str(duration)[:4]
                    #print(duration)
                    duration = datetime.strptime(duration, '%H:%M').time()
                    wait_for_Height_and_weight.append(duration)
                    #print("~~~~~~~~~~~~~~~~")
                    #print (wait_for_Height_and_weight)

                elif current_action == "in consultation 1 of 1"  and previous_action == "waiting consultation 1 of 1":
                    duration = datetime.combine(date.today(), time_end) - datetime.combine(date.today(), time_start)
                    duration = str(duration)[:4]
                    duration = datetime.strptime(duration, '%H:%M').time()
                    wait_for_consultation_1.append(duration)
                    consultation_starts.append(time_start)
                    #print("~~~~~~~~~~~~~~~~")
                    #print (wait_for_consultation_1)

                elif current_action == "in consultation 1 of 2" and previous_action == "waiting consultation 1 of 2":
                    duration = datetime.combine(date.today(), time_end) - datetime.combine(date.today(), time_start)
                    duration = str(duration)[:4]
                    duration = datetime.strptime(duration, '%H:%M').time()
                    wait_for_consultation_1_of_2.append(duration)
                    consultation_starts.append(time_start)
                    #print("~~~~~~~~~~~~~~~~")
                    #print(wait_for_consultation_1_of_2)

                elif current_action == "in consultation 2 of 2" and previous_action == "waiting consultation 2 of 2":
                    duration = datetime.combine(date.today(), time_end) - datetime.combine(date.today(), time_start)
                    duration = str(duration)[:4]
                    duration = datetime.strptime(duration, '%H:%M').time()
                    wait_for_consultation_2.append(duration)  
                    consultation_starts.append(time_start)
                    #print("~~~~~~~~~~~~~~~~")
                    #print (wait_for_consultation_2)

                elif current_action == "in blood room" and previous_action == "waiting blood room":
                    duration = datetime.combine(date.today(), time_end) - datetime.combine(date.today(), time_start)
                    duration = str(duration)[:4]
                    duration = datetime.strptime(duration, '%H:%M').time()
                    wait_for_Bloods.append(duration)
                    bloods_starts.append(time_start)
                    #print("~~~~~~~~~~~~~~~~")
                    #print (wait_for_Bloods)

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
        #adding lists to dataframes above - could turn more efficient - could be turned into a function for sure 
        #adding waits
        #DO THE SAME FOR ANYWHERE ELSE ADDING TO DF AND ALSO MAKE SURE NaN ARE EXCLUDED FOR TALLYING AND PICKING!!!!!!!!!!!!!
        #print (wait_for_Bloods)
        #print (wait_for_consultation_1)
        #print (wait_for_consultation_1_of_2)
        #print (wait_for_consultation_2)
        #print (wait_for_Height_and_weight)
    
        bloods = len(wait_for_Bloods)
        consult1 = len(wait_for_consultation_1)
        consult12 = len(wait_for_consultation_1_of_2)
        consult2 = len(wait_for_consultation_2)
        hw = len(wait_for_Height_and_weight)
        
        counter = [bloods, consult1, consult12, consult2, hw]
        biggest = max(counter)

        #print(counter)
        #print(waiting_df)

        num_list = range(biggest)

        wait_bloods_dict = dict(enumerate(wait_for_Bloods))
        wait_consult1_dict = dict(enumerate(wait_for_consultation_1))
        wait_contsult12_dict = dict(enumerate(wait_for_consultation_1_of_2))
        wait_consult2_dict = dict(enumerate(wait_for_consultation_2))
        wait_hw_dict = dict(enumerate(wait_for_Height_and_weight))

        waiting_df["num"] = num_list
        waiting_df["wait_bloods"] = waiting_df["num"].map(wait_bloods_dict)
        waiting_df["wait_consult_1"] = waiting_df["num"].map(wait_consult1_dict)
        waiting_df["wait_consult_1/2"] = waiting_df["num"].map(wait_contsult12_dict)
        waiting_df["wait_consult_2"] = waiting_df["num"].map(wait_consult2_dict)
        waiting_df["wait_h&w"] = waiting_df["num"].map(wait_hw_dict)

        #print(waiting_df)
        #print("______________________")


        #adding durations
        bloods = len(bloods_duration)
        consult1 = len(consultation_duration_1)
        consult12 = len(consultation_duration_1_of_2)
        consult2 = len(consultation_duration_2)
        late = len(late_duration)
        
        counter = [bloods, consult1, consult12, consult2, late]
        biggest = max(counter)

        num_list = range(biggest)

        dur_bloods_dict = dict(enumerate(bloods_duration))
        dur_consult1_dict = dict(enumerate(consultation_duration_1))
        dur_contsult12_dict = dict(enumerate(consultation_duration_1_of_2))
        dur_consult2_dict = dict(enumerate(consultation_duration_2))
        dur_late_dict = dict(enumerate(late_duration))

        duration_df["num"] = num_list
        duration_df["duration_bloods"] = duration_df["num"].map(dur_bloods_dict)
        duration_df["duration_consult_1"] = duration_df["num"].map(dur_consult1_dict)
        duration_df["duration_consult_1/2"] = duration_df["num"].map(dur_contsult12_dict)
        duration_df["duration_consult_2"] = duration_df["num"].map(dur_consult2_dict)
        duration_df["duration_lates"] = duration_df["num"].map(dur_late_dict)


        #adding starts
        bloods = len(bloods_starts)
        consult = len(consultation_starts)
        arrival = len(arrival_time)
        
        counter = [bloods, consult, arrival]
        biggest = max(counter)

        num_list = range(biggest)

        bloods_starts_dict = dict(enumerate(bloods_starts))
        consultation_starts_dict = dict(enumerate(consultation_starts))
        arrival_time_dict = dict(enumerate(arrival_time))
        
        starts_df["num"] = num_list
        starts_df["starts_bloods"] = starts_df["num"].map(bloods_starts_dict)
        starts_df["starts_consult"] = starts_df["num"].map(consultation_starts_dict)
        starts_df["starts_arrival"] = starts_df["num"].map(arrival_time_dict)


        #adding numbers
        consult = len(num_of_consultations)
        dna = len(num_of_did_not_attends)
        lates = len(num_of_lates)
        patients = len(num_patients)
        
        counter = [consult, dna, lates, patients]
        biggest = max(counter)

        num_list = range(biggest)

        num_consult_dict = dict(enumerate(num_of_consultations))
        num_dna_dict = dict(enumerate(num_of_did_not_attends))
        num_lates_dict = dict(enumerate(num_of_lates))
        num_patients_dict = dict(enumerate(num_patients))

        number_df["num"] = num_list
        number_df["num_consult"] = number_df["num"].map(num_consult_dict)
        number_df["num_dna"] = number_df["num"].map(num_dna_dict)
        number_df["num_lates"] = number_df["num"].map(num_lates_dict)
        number_df["num_patients"] = number_df["num"].map(num_patients_dict)
        

        return (waiting_df, number_df, duration_df, starts_df)
    
    return(wait_for_Height_and_weight, wait_for_Bloods, wait_for_consultation_1, wait_for_consultation_1_of_2, wait_for_consultation_2, bloods_duration, consultation_duration_1, consultation_duration_1_of_2, consultation_duration_2, late_duration, bloods_starts, consultation_starts, arrival_time, num_of_consultations, num_of_did_not_attends, num_of_lates, num_patients)


        

#Calculates the number of patients in certain situations
def calculating_patient_numbers (todays_data, first, final, consult_counter_list, bloods_counter_list, clinic_counter_list):#!!!!!!!!!!!!unfinished function in the elifs etc !!!!!!!!!!!!!!!!!
    length = len(todays_data)

    if final:
        counter_dict = {}

    #print (todays_data)
    todays_data = sorted(todays_data, key=lambda d: d["time"])
    #print (todays_data)

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
                        #print(current_patient)
                        #print(patients_in_consultation)
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

    consult_counter_list.append(consult_counter)
    bloods_counter_list.append(bloods_counter)
    clinic_counter_list.append(clinic_counter)

    if final:
        counter_dict["consult_counter"] = (consult_counter_list)
        counter_dict["bloods_counter"] = (bloods_counter_list)
        counter_dict["clinic_counter"] = (clinic_counter_list)
        return(counter_dict)
    
    return(consult_counter_list, bloods_counter_list, clinic_counter_list)




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


        #print (len(Lines))
        c += 1
        #print(c)
        if c == 200:
            break
        all_data_df.loc[len(all_data_df)] = line
        #print(all_data_df)
        all_data_df.to_csv("all_data")

    #work out number of dates
    list_days = []
    num_rows = len(all_data_df.index)
    #print(num_rows)
    for i in range(num_rows):
        temp = all_data_df.iloc[i]["DateTime"]
        #print(temp)
        if temp[:10] not in list_days:
            #print(list_days)
            #print(temp)
            temp = temp[:10]
            list_days.append(temp)

    #print(list_days)
    
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

    consult_counter_list = []
    bloods_counter_list = []
    clinic_counter_list = []

    final = False
    first = False
    counter = 0
    for day in list_days:
        current_days_data, current_days_patients = collecting_days_data(all_data_df, day, num_rows)
        #print(current_days_data)
        #print(current_days_patients)

        counter += 1
        if counter == num_days:
            final = True
            waiting_df, number_df, duration_df, starts_df = calculating_times (current_days_data, current_days_patients, waiting_df, number_df, duration_df, starts_df, wait_for_Height_and_weight, wait_for_Bloods, wait_for_consultation_1, wait_for_consultation_1_of_2, wait_for_consultation_2, bloods_duration, consultation_duration_1, consultation_duration_1_of_2, consultation_duration_2, late_duration, bloods_starts, consultation_starts, arrival_time, num_of_consultations, num_of_did_not_attends, num_of_lates, num_patients, final, first)
            return_dict = calculating_patient_numbers(current_days_data, first, final, consult_counter_list, bloods_counter_list, clinic_counter_list) 

        elif counter == 1:
            first = True
            wait_for_Height_and_weight, wait_for_Bloods, wait_for_consultation_1, wait_for_consultation_1_of_2, wait_for_consultation_2, bloods_duration, consultation_duration_1, consultation_duration_1_of_2, consultation_duration_2, late_duration, bloods_starts, consultation_starts, arrival_time, num_of_consultations, num_of_did_not_attends, num_of_lates, num_patients = calculating_times (current_days_data , current_days_patients, waiting_df, number_df, duration_df, starts_df, wait_for_Height_and_weight, wait_for_Bloods, wait_for_consultation_1, wait_for_consultation_1_of_2, wait_for_consultation_2, bloods_duration, consultation_duration_1, consultation_duration_1_of_2, consultation_duration_2, late_duration, bloods_starts, consultation_starts, arrival_time, num_of_consultations, num_of_did_not_attends, num_of_lates, num_patients, final, first)
            consult_counter_list, bloods_counter_list, clinic_counter_list = calculating_patient_numbers(current_days_data, first, final, consult_counter_list, bloods_counter_list, clinic_counter_list) 

        else:
            first = False
            wait_for_Height_and_weight, wait_for_Bloods, wait_for_consultation_1, wait_for_consultation_1_of_2, wait_for_consultation_2, bloods_duration, consultation_duration_1, consultation_duration_1_of_2, consultation_duration_2, late_duration, bloods_starts, consultation_starts, arrival_time, num_of_consultations, num_of_did_not_attends, num_of_lates, num_patients = calculating_times (current_days_data , current_days_patients, waiting_df, number_df, duration_df, starts_df, wait_for_Height_and_weight, wait_for_Bloods, wait_for_consultation_1, wait_for_consultation_1_of_2, wait_for_consultation_2, bloods_duration, consultation_duration_1, consultation_duration_1_of_2, consultation_duration_2, late_duration, bloods_starts, consultation_starts, arrival_time, num_of_consultations, num_of_did_not_attends, num_of_lates, num_patients, final, first)
            consult_counter_list, bloods_counter_list, clinic_counter_list = calculating_patient_numbers(current_days_data, first, final, consult_counter_list, bloods_counter_list, clinic_counter_list) 



    list_of_df = [waiting_df, duration_df, starts_df]
    df_names = ["waiting_df", "duration_df", "starts_df"]
    #print(waiting_df)
    #print(duration_df)
    #print(starts_df)
    #print("-----------")

    tally_dict = {}
    list_names = []
    list_tallys = []


    #get the lists out of the df
    df_dict = {}
    num_dict = {}
    column_headers = []
    temp_col = []
    temp_dict = {}
    print(return_dict)
    c = 0
    for i in list_of_df: # i is now a df
        column_headers = []
        temp_col = []

        column_headers = (list(i.columns.values))#ALSO remove NaNs
        #print(i)
        #print(column_headers)
        #print("----------")
        for col in column_headers:
            temp = i.loc[:,col].tolist()
            temp_col.append(temp)
            #print(temp_col)
        

        for header, col in zip(column_headers, temp_col):
            #print("hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh")
            #print(header)
            #print(col)
            temp_dict[header] = col
            #print("diiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiictr")
            #print(temp_dict)

        df_dict[df_names[c]] = temp_dict
        c += 1

    #for number_df
    temp_col = []
    #print(number_df)
    for i in number_df:
        column_headers.append(i)
        #print("iiiiiiiii")
        #print(i)
        temp = number_df[i].tolist()
        temp_col.append(temp)
        
    for header, col in zip(column_headers, temp_col):
        num_dict[header] = col


    final_tally_dict = {}
    list_tallys = []
    #getting the tallys
    c= 0
    for i in df_dict:
        print("dfdfdffdfdfdfdfdfdf")
        print(df_dict)
        tally_dict, names = (get_probabilities_time(df_dict[i]))
        #df_names.append(df_dict[c])
        print(names)
        print(tally_dict)

        list_names.append(names)
        list_tallys.append(tally_dict)
        c += 1

    
    tally_dict2, names2 = (get_probabilities_time(return_dict)) #gives the values as a list
    #df_names.append(df_dict[c])
    tally_dict.update(tally_dict2)
    names.extend(names2)
    # for name, tally in zip(list_names, list_tallys):
    #     final_tally_dict[name] = tally

    #raw, untallied dict of lists
    untallied_dict = {}
    print(df_dict)
    print(return_dict)
    print(num_dict)

    for i in df_dict:
        print(i)
        print(df_dict[i])
        for j in df_dict[i]:
            temp = df_dict[i]
            print(j)
            print(temp)
            print(temp[j])
            temp_list = [temp[j]]
            temp_list = [x for x in temp_list if str(x) != 'nan']
            temp_list = sorted(temp_list)
            untallied_dict[j]=temp_list
    
    for i in return_dict:
        temp_list = return_dict[i]
        temp_list = [x for x in temp_list if str(x) != 'nan']
        temp_list = sorted(temp_list)
        untallied_dict[i]=temp_list
    
    for i in num_dict:
        temp_list = num_dict[i]
        temp_list = [x for x in temp_list if str(x) != 'nan']
        temp_list = sorted(temp_list)
        untallied_dict[i]=temp_list

    return(tally_dict, untallied_dict)


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

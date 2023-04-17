from read_data import *


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

def collecting_days_data (sorted_data_list, current_day):
    todays_data = []
    todays_patients = []
    num_patients_in_day = len(todays_patients)
    for i in sorted_data_list:
        while i.get("date_time") == current_day:
            todays_data.append(i)
            patient = i.get("unique_identifier")
            if todays_patients.count(i.get("unique_identifier")):
                print("exists")
            else: 
                todays_patients.append(i.get("unique_identifier"))

    return(todays_data, todays_patients)


#Calculates the durations, waiting times and other data needed to be found
def calculating_times (sorted_data_list, current_days_data , current_days_patients):
    #Instantiating 
    arrival_time = []

    #To collect a list of waiting times in minutes
    wait_for_Height_and_weight = []
    wait_for_Bloods = []
    wait_for_consultation_1 = []
    wait_for_consultation_1_of_2 = []
    wait_for_consultation_2 = []

    #To collect a list of number of patients to the particular event
    number_of_did_not_attends = 0
    number_of_lates = 0 #not including DNA's
    number_of_consultations = 0

    #To collect appointment times approximation
    consultation_starts = []
    bloods_starts = []

    #To collect a list of duration times in minutes
    consultation_duration_1 = []
    consultation_duration_1_of_2 = []
    consultation_duration_2 = []
    bloods_duration = []
    late_duration = []

    #To be an overall list of the above lists
    waiting_list = [] 
    number_list = []
    duration_list = []
    starts_list = []


    #re-sort the list by unique identifier (patient)
    sorted_current_days_data = sorted(current_days_data, key=lambda d: d['unique_identifier'])
    sorted_current_days_patients = current_days_patients.sort()

    #go through each item in the new sorted list and match it to particular situations and add the value to the above waiting time lists
    for i in sorted_current_days_data:
        c = 0 #counter to keep track of patient
        while i == current_days_patients[c].get("unique_identifier"): #while the patient is the same
            current_action = i.[c].get("action").str().lower()
            previous_action = i.[c-1].get("action").str().lower()
            future_action = i.[c+1].get("action").str().lower() # need a fail safe here and above just incase at first or last action !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            
            if current_action = "patient identified by kiosk":
                arrival_time = i[c].get("date_time")[10:].time()
            
            elif current_action == "appointed" or "late arrival" or "patient identified by kiosk":
                #ignore
            
            elif previous_action == "waiting height and weight": # you cant tell what is wait and and what is duration so duration will be fixed
                time_start = i[c-1].get("date_time")[10:].time()
                time_end = i[c].get("date_time")[10:].time()
                duration = time_end - time_start
                wait_for_Height_and_weight.append(duration)

            elif current_action == "in consultation 1 of 1"  and previous_action == "waiting consultation 1 of 1":
                time_start = i[c-1].get("date_time")[10:].time()
                time_end = i[c].get("date_time")[10:].time()
                duration = time_end - time_start
                wait_for_consultation_1.append(duration)
                consultation_starts.append(time_start)

            elif current_action == "in consultation 1 of 2" and previous_action == "waiting consultation 1 of 2":
                time_start = i[c-1].get("date_time")[10:].time()
                time_end = i[c].get("date_time")[10:].time()
                duration = time_end - time_start
                wait_for_consultation_1_of_2.append(duration)
                consultation_starts.append(time_start)

            elif current_action == "in consultation 2 of 2" and previous_action == "waiting consultation 2 of 2":
                time_start = i[c-1].get("date_time")[10:].time()
                time_end = i[c].get("date_time")[10:].time()
                duration = time_end - time_start
                wait_for_consultation_2.append(duration)  
                consultation_starts.append(time_start)

            elif current_action == "in blood room" and previous_action == "waiting blood room":
                time_start = i[c-1].get("date_time")[10:].time()
                time_end = i[c].get("date_time")[10:].time()
                duration = time_end - time_start
                wait_for_Bloods.append(duration)
                bloods_starts.append(time_start)

            elif current_action == "late arrival" and future_action != "did not attend":
                number_of_lates += 1
                time_start = i[c].get("date_time")[10:].time()
                time_end = i[c+1].get("date_time")[10:].time()
                duration = time_end - time_start
                late_duration.append(duration)

            else:
                #x
            
            #Same as above but looking for durations now and numbers of patients to add to the lists
            if current_action == "appointed" or "late arrival" or "patient identified by kiosk":
                #ignore
            
            elif current_action == "did not attend":
                number_of_did_not_attends =+ 1

            elif previous_action == "in consultation 1 of 1":
                time_start = i[c-1].get("date_time")[10:].time()
                time_end = i[c].get("date_time")[10:].time()
                duration = time_end - time_start
                consultation_duration_1.append(duration)

            elif previous_action == "in consultation 1 of 2":
                time_start = i[c-1].get("date_time")[10:].time()
                time_end = i[c].get("date_time")[10:].time()
                duration = time_end - time_start
                consultation_duration_1_of_2.append(duration)

            elif previous_action == "in consultation 2 of 2":
                time_start = i[c-1].get("date_time")[10:].time()
                time_end = i[c].get("date_time")[10:].time()
                duration = time_end - time_start
                consultation_duration_2.append(duration)

            elif previous_action == "in blood room":
                time_start = i[c-1].get("date_time")[10:].time()
                time_end = i[c].get("date_time")[10:].time()
                duration = time_end - time_start
                bloods_duration.append(duration)

            else:
                #x

            #can make above more efficient by having a function that takes in what its looking for and produces the value/time

            c =+ 1 #counter

    #calls function - repeats for every day
    give_date(date_sorted_data_list) #need to put in a loop to only call until end of list !!!!!!!!!!1111

    #adding lists to an overall list
    waiting_list.extend(wait_for_Height_and_weight, wait_for_Bloods, wait_for_consultation_1, wait_for_consultation_1_of_2, wait_for_consultation_2)
    number_list.extend(number_of_consultations, number_of_did_not_attends, number_of_lates)
    duration_list.extend(bloods_duration, consultation_duration_1, consultation_duration_1_of_2, consultation_duration_2, late_duration)
    starts_list.extend(bloods_starts, consultation_starts, arrival_time)

    return (waiting_list, number_list, duration_list, starts_list)

#Calculates the number of patients in certain situations
def calculating_patient_numbers (todays_data, todays_patients):#!!!!!!!!!!!!unfinished function in the elifs etc !!!!!!!!!!!!!!!!!
    length = len(todays_data)
    start_time = todays_data.[0].get("date_time")
    end_time = todays_data.[length-1].get("date_time")

    counter = 0

    patients_in_clinic = []
    patients_in_bloods = []
    patients_in_consultation = []

    clinic_counter = 0#number of patients in clinic at any time
    bloods_counter = 0#number of patients in bloods at one time
    consult_counter = 0#number of patients in consultation at one time

    #lists to contain the above
    number_list = []
    counter_list = []


        while (start_time <= end_time):
            for i in todays_data:
                current_action = i.[counter].get("action").str().lower()
                previous_action = i.[counter-1].get("action").str().lower()
                current_patient = i.[counter].get("unique_identifier").str().lower()

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

    return(number_list, counter_list)




#finds the current date and calls a function with that information -
#^recieves back the data and patients for only that day - 
#^calls the function to work out data and gets it back
def give_date(date_sorted_data_list): #need to edit the function to take in the date when requested !!!!!!!!!1
    temp_val = []
    temp_val.append(sorted_data_list[0])
    current_day = temp_val[0].get("date_time")      
    current_day = current_day[:10] #should cut it to just be date

    #get the days data by using the day function
    current_days_data , current_days_patients = collecting_days_data(sorted_data_list, current_day)
    waiting_list, number_list, duration_list, starts_list = calculating_times (date_sorted_data_list, current_days_data , current_days_patients)
    number_list, counter_list = calculating_patient_numbers(current_days_data, current_days_data) 
return () # add here!!!!!!!!!!! also could maybe have the function calling taken out !!!!!!!!!!!



#running here !!!!!!!!!!!!!

a = give_date(date_sorted_data_list, 0)
print("hi")



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

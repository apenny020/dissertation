from read_data import *


#this will take the data and work out the probabilities for each section
#so need to work out times between check in and either H/W, bloods, consultant, Research
#maybe workout from check in to check out
#but need to check between each section - collect the data and use numpy - workout how long the like quickest 10% were on average
#then 20%, 30% etc, find the longest and if reaches this time then called basically.

#also be good to know how many people go on each pathway


#for each day
#multiple patients to keep track of

#could do average of times, but i think a distribution would be more accurate
#for distribution - record all times and then order them, then you can take length divided by x to get a certain proportion of the distribution



#need a temp collector
#for each day
#for each patient
#work out waiting times

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
    #needs to do a loop, while date_time == current_day
    #store the dictionaries into a new temp list - not sure if needed 
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

    calculating_patient_numbers()


    return(todays_data, todays_patients)


def calculating_wait_times (sorted_data_list, current_days_data , current_days_patients):
    #Instantiating 
    arrival_time = []

    #List of waiting times in minutes
    wait_for_Height_and_weight = []
    wait_for_Bloods = []
    wait_for_consultation_1 = []
    wait_for_consultation_1_of_2 = []
    wait_for_consultation_2 = []

    number_of_did_not_attends = 0
    number_of_lates = 0 #not including DNA's
    number_of_consultations = 0#

    consultation_starts = []
    bloods_starts = []

    consultation_duration_1 = []
    consultation_duration_1_of_2 = []
    consultaiton_duration_2 = []
    bloods_duration = []
    late_duration = []
    waiting_dictionary = {} # CREATE A DICT 

    #re-sort by unique identifier
    sorted_current_days_data = sorted(current_days_data, key=lambda d: d['unique_identifier'])
    sorted_current_days_patients = current_days_patients.sort()

    print("HELLO")

    
    #go through each item in the new sorted list
    for i in sorted_current_days_data:
        c = 0
        while i == current_days_patients[c].get("unique_identifier"): #while the patient is the same
            current_action = i.[c].get("action").str().lower()
            previous_action = i.[c-1].get("action").str().lower()
            future_action = i.[c+1].get("action").str().lower() # need a fail safe here and above just incase at first or last action
            
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
            
            #looking for durations
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

            #can probably make above code more efficient

            c =+ 1
    give_date(date_sorted_data_list, )

    return (wait_for_Bloods, wait_for_consultation_1, wait_for_consultation_1_of_2, wait_for_consultation_2, wait_for_Height_and_weight, number_of_did_not_attends, bloods_duration, consultation_duration_1, consultation_duration_1_of_2, consultaiton_duration_2)


def give_date(date_sorted_data_list, counter):
    temp_val = []
    temp_val.append(sorted_data_list[0])
    current_day = temp_val[0].get("date_time")      
    current_day = current_day[:10] #should cut it to just be date

    #get the days data by using the day function
    current_days_data , current_days_patients = collecting_days_data(sorted_data_list, current_day)
    calculating_wait_times (date_sorted_data_list, current_days_data , current_days_patients)
return ()

def calculating_patient_numbers (todays_data, todays_patients):
    length = len(todays_data)
    start_time = todays_data.[0].get("date_time")
    end_time = todays_data.[length-1].get("date_time")

    counter = 0

    patients_in_clinic = []
    patients_in_bloods = []
    patients_in_consultation = []

    clinic_counter = 0
    bloods_counter = 0
    consult_counter = 0
    #number of patients in clinic at any time
    #number of patients in bloods at one time
    #number of patients in consultation at one time

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

    pass








a = give_date(date_sorted_data_list, 0)
print("hi")

#NEED SOMETHING THAT WORKS OUT THE ORDER OF WHAT PATIENTS DO< AND THE LIKELIHOOD



#!!!do i need to work out probability of a patient not showing up


#!!!!further work - different days could have different waiting times because of different number of staff - so adjust to this
# ^ would play into changing number of staff
#there is 1 blood room and up to 3 blood stations at one time (but rare that all 3 would be up)
#!!!! remember that a patient is connected to a consultant
#if consultation is longer than 2 hours, throw away

#need to access the sorted list from data processor
#then seperate the information into dates (each day is 1 list of dictionary<-- double think this data structure)
#then 2 tasks

#1 reorder data by patient number
#work out how long they waited for each thing
#store this in the main data structure

#2 - extension see if you can work out how many staff working by how many patients in which area at the same time

#also need a main data structure in here that is maybe a dictionary...
#how likely to use kiosk or reception
#how likely to DNA
#how likely to be late - and by how much
#time from check in to weight and height 
#time from check in to other if identified?
#time from 

#Possible states are
#Appointed
#Patient Identified by Kiosk
#Waiting Height and Weight
#Waiting Consultation 1 of 1
#In Consultation 1 of 1
#Waiting Consultation 1 of 2
#In Consultation 2 of 2
#Waiting Blood Room
#In Blood Room
#Complete
#Complete, Bloods Done
#Cancelled
#Late Arrival
#DNA

#Patients can come in for
#Height weight, consultation (1or2)
#Height weight, consultation (1or2), Bloods
#Bloods
#Cancelled
#Late arrival, DNA


#Exclusions
#If does not complete - ignore data, 
#if more than 10 hours, ignore

#make sure you change to all upper or all lower case

#need to reread the data and look at how its set for this ^
#need to read about how to make probablilities - are they going to be purely from the data, how work out - write it more


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

def collecting_days_data (sorted_data_list, current_day):
    #needs to do a loop, while date_time == current_day
    #store the dictionaries into a new temp list - not sure if needed 
    todays_data = []
    todays_patients = []
    for i in sorted_data_list:
        while i.get("date_time") == current_day:
            todays_data.append(i)
            patient = i.get("unique_identifier")
            if todays_patients.count(i.get("unique_identifier")):
                print("exists")
            else: 
                todays_patients.append(i.get("unique_identifier"))
    return(todays_data, todays_patients)


def calculating_wait_times (sorted_data_list):
    #List of waiting times in minutes
    wait_for_Height_and_weight = []
    wait_for_Bloods = []
    wait_for_consultation = [] #for consultation 1 and 2

    number_of_did_not_attends = []

    consultation_duration = []
    bloods_duration = []
    waiting_dictionary = {} # CREATE A DICT 

    temp_val = []
    temp_val.append(sorted_data_list[0])
    current_day = temp_val[0].get("date_time")      
    current_day = current_day[:10] #should cut it to just be date

    #get the days data by using the day function
    current_days_data , current_days_patients = collecting_days_data(sorted_data_list, current_day)

    #re-sort by unique identifier
    sorted_current_days_data = sorted(current_days_data, key=lambda d: d['unique_identifier'])
    sorted_current_days_patients = current_days_patients.sort()

    print("HELLO")

    #go through each item in the new sorted list
    for i in sorted_current_days_data:
        while i == current_days_patients[c].get("unique_identifier"): #while the patient is the same
            current_action = i.[c].get("action").str().lower()
            previous_action = i.[c-1].get("action").str().lower()
            #looking for wait times
            if current_action == "appointed" or "late arrival" or "patient identified by kiosk":
                #ignore
            elif current_action == "did not attend":
                number_of_did_not_attends =+ 1
            elif previous_action == "waiting height and weight": # you cant tell what is wait and and what is duration so duration will be fixed
                time_start = i[c-1].get("date_time")[10:].time()
                time_end = i[c].get("date_time")[10:].time()
                duration = time_end - time_start
                wait_for_Height_and_weight.append(duration)
            elif current_action == "in consultation 1 of 1" or "in consultation 1 of 2" or "in consultation 2 of 2" and previous_action == "waiting consultation 1 of 1" or "waiting consultation 1 of 2" or "waiting consultation 2 of 2":
                time_start = i[c-1].get("date_time")[10:].time()
                time_end = i[c].get("date_time")[10:].time()
                duration = time_end - time_start
                wait_for_consultation.append(duration)
            elif current_action == "in blood room" and previous_action == "waiting blood room":
                time_start = i[c-1].get("date_time")[10:].time()
                time_end = i[c].get("date_time")[10:].time()
                duration = time_end - time_start
                wait_for_Bloods.append(duration)
            else:
                #x
            
            #looking for durations
            if current_action == "appointed" or "late arrival" or "patient identified by kiosk":
                #ignore
            elif current_action == "did not attend":
                number_of_did_not_attends =+ 1
            elif previous_action == "in consultation 1 of 1" or "in consultation 1 of 2" or "in consultation 2 of 2":
                time_start = i[c-1].get("date_time")[10:].time()
                time_end = i[c].get("date_time")[10:].time()
                duration = time_end - time_start
                consultation_duration.append(duration)
            elif previous_action == "in blood room":
                time_start = i[c-1].get("date_time")[10:].time()
                time_end = i[c].get("date_time")[10:].time()
                duration = time_end - time_start
                bloods_duration.append(duration)
            else:
                #x


            #can probably make above code more efficient
            #check over above that it covers everything!!!!!!!!!! TO DO 

            c =+ 1


    return (wait_for_Bloods, wait_for_consultation, wait_for_Height_and_weight, number_of_did_not_attends, bloods_duration, consultation_duration)

#this bit doesnt work
#    for i in current_days_patients:
 #       for j in sorted_current_days_data:
  #          while i == j['unique identifier']: # fix this
   #             if j['action'].str.lower() == "cancelled" or "late arrival" or "appointed" or "cancelled":
    #                #ignore
     #           elif j['action'].str.lower() == patient identified by kiosk:
      #              start_time = j['date_time'][10:]
       #         elif  j['action'].str.lower() == Waiting height weight:
        #            start_time = j['date_time'][10:]
                    #change above to work with a dictionary



# waiting consultant is always followed by in consult
#waiting for bloods is always followed by in bloods
#Height and weight is not always followed by the same thing



    #then grab timestamp

    #eventually has to loop round and find the next day somehow
    




a = calculating_wait_times(date_sorted_data_list)
print("hi")



#loop through day function for each day (which calls the wait time functino)

#do i need to work out probability of a patient not showing up


#further work - different days could have different waiting times because of different number of staff - so adjust to this
# ^ would play into changing number of staff


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


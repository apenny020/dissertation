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

def calculating_wait_times (data_list):
    #List of waiting times in minutes
    wait_for_Height_and_weight = ()
    wait_for_Bloods = ()
    wait_for_consultation_1 = ()
    wait_for_consultation_2 = () #combine with above?


    temp_val = []
    temp_val.append(data_list(0))
    current_day = temp_val.get("date_time")      
    current_day = current_day[:10] #should cut it to just be date
    
    #needs to do a loop, while date_time == current_day
    #store patient in patient dict
    todays_patients = []
        #this occurs when appointed
        todays_patients.append(unique_identifier)

    #then grab timestamp

    #eventually has to loop round and find the next day somehow
    
    pass







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


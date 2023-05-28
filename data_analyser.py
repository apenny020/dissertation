#visualise and analyse data
import csv

"""
Data we've got to work with:
Waiting times; Height/Weight, Bloods, Consultation 1/1 of 2/2
Durations of; Bloods, Consultation 1/2, 
Number of DNA's
Number of Patients in a day
Number of Consults in a day
Consult start times
Blood start times
Late durations

Number of patients at clinic at any one time
How many patients in bloods at one time == number of blood nurses
How many patients in consulatation at same time == number of consultants

Want to order some and create a distribution
Visualise data and output CSV

"""

#order list and output to CSV
def order_list(to_order_list, file_name):
    ordered_list = sorted(to_order_list)

    #write to new CSV
    with open(file_name, "w") as f:
        for i in ordered_list:
            writer.writerow(i)
    f.close()
    
    return(ordered_list)

#create distributions to be used (for one day)
#first for time based data - waiting times/durations/lates
#also
#second for number of patients 
#the list should be a number over multiple dates
def get_probabilities_time(data_list):

    tally_dict = {}
    
    ordered_list = sorted(data_list)
    for i in ordered_list:
        if i in tally_dict:
            #increase by value 1 -creates a dictionary with each value and a tally for it 
            temp_val = tally_dict[i]
            temp_val += 1
            tally_dict.update({i:temp_val})
        else:
            #add to dict
            tally_dict[i] = 1
        
    #creating percentage
    total = len(ordered_list)
    for i in tally_dict:
        #get value and put in probability
        #update value to this
        temp_val = tally_dict[i]
        temp_val = temp_val/total
        tally_dict.update({i:temp_val})
    
    #a dictionary that returns the collected data value and its probability chance of existing
    return (tally_dict)
    




#plot the data so that it can be visualised


#NEED SOMETHING THAT WORKS OUT THE ORDER OF WHAT PATIENTS DO< AND THE LIKELIHOOD

#but need to check between each section - collect the data and use numpy - workout how long the like quickest 10% were on average
#then 20%, 30% etc, find the longest and if reaches this time then called basically.
#for distribution - record all times and then order them, then you can take length divided by x to get a certain proportion of the distribution

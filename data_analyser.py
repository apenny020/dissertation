#visualise and analyse data
import csv
import numpy as np 
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline
from datetime import datetime, date
import pandas as pd
import random

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

#create a smooth line graph
#x and y to be an array
def create_graph(x, y, title, x_axis, y_axis, get_value):
    if title == "starts_bloods" or title == "starts_consult" or title == "starts_arrival":
        return()
    changed_x = []
    for i in x:
        if type(i) == datetime:
            temp_hour = i.hour
            temp_minute = i.minute
            temp_minute = temp_minute + (temp_hour*60)
            i = temp_minute
            changed_x.append(i)
        else:
            changed_x.append(i)

    x = np.array(changed_x)
    y = np.array(y)

    title_dict = {"title":title, "x_axis":x_axis, "y_axis":y_axis}
    print("------------------------------")
    print(x)
    print(y)
    xy_spline = make_interp_spline(x,y)

    new_x = np.linspace(x.min(), x.max(), 500)
    new_y = xy_spline(new_x)

    plt.plot(new_x, new_y)
    #plt.plot(x,y)
    plt.title(title_dict["title"])
    plt.xlabel(title_dict["x_axis"])
    plt.ylabel(title_dict["y_axis"])
    plt.show()

    if not get_value:
        plt.savefig(title + '.png')
        plt.close()
        return()
    else: # need to get a value for model
        max_num = max(x)
        temp_val = random.randint(0, max_num)
        #value = np.interp()
        plt.close()
        #return(value)
        return()
    


#create distributions to be used (for one day)
#first for time based data - waiting times/durations/lates
#also
#second for number of patients 
#the list should be a number over multiple dates
def get_probabilities_time(data_dict):

    tally_dict = {}#CHANGE SO THAT IT GETS THE NAME OF THE LIST AND RETURNS ON IT AND FIX CODE IN PROCESSOR TO MATCH
    column_headers = []
    c=0

    if data_dict == [] or data_dict == 0:
        return (tally_dict, column_headers)

    column_headers = (list(data_dict.keys()))
    final_dict = {}

    for i in data_dict:
        tally_dict = {}        
        
        temp_list = data_dict[i]
        temp_list = [x for x in temp_list if str(x) != 'nan']

        ordered_list = sorted(temp_list)   

        length = len(ordered_list)
        c = 0
        for k in range(length):
            j = ordered_list[c]
            if str(j) == "NaT":
                ordered_list.remove(j)
            else:
                c +=1

        for j in ordered_list:
            if type(j) != int:
                j = j.to_pydatetime()          
        
            if j in tally_dict:
                #increase by value 1 -creates a dictionary with each value and a tally for it 
                temp_val = tally_dict[j]
                temp_val += 1
                tally_dict.update({j:temp_val})
            else:
                #add to dict
                tally_dict[j] = 1
            
        #creating percentage
        total = len(ordered_list)
        for j in tally_dict:
            #get value and put in probability
            #update value to this
            temp_val = tally_dict[j]
            temp_val = temp_val/total
            tally_dict.update({j:temp_val})
            c += 1
        final_dict[i] = tally_dict
            
    
    #a dictionary that returns the collected data value and its probability chance of existing
    return (final_dict, column_headers)
    




#plot the data so that it can be visualised


#NEED SOMETHING THAT WORKS OUT THE ORDER OF WHAT PATIENTS DO< AND THE LIKELIHOOD

#but need to check between each section - collect the data and use numpy - workout how long the like quickest 10% were on average
#then 20%, 30% etc, find the longest and if reaches this time then called basically.
#for distribution - record all times and then order them, then you can take length divided by x to get a certain proportion of the distribution

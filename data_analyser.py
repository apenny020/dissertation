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
    return (ordered_list)

#create distributions to be used


#workout appointment times?


#plot the data so that it can be visualised




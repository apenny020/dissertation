#read in
#first part to be assigned to individual
#second part to be assigned to date
#third part to be ignored
#4th part to assign state to a patient
#store all in a data structure - maybe a class that requires inputs and stores into a dictionary into an array

#think about how youre going to use data actually
import re


def read_in_data(): # could change parameter to take in x text file
  #read in data and put it into a list with lines being seperated by commas
  input_data_list = [] # the list of all the lines
  dataFile = open("data_input_file_2018.txt", "r", encoding='utf-8-sig')
  for line in dataFile:
    whole_line = line
    input_data_list.append(whole_line)
  dataFile.close()
  print (input_data_list[0])


  data_list = []
  #test_item = [] #for testing - just using the first line - replace to loop through each line later, use data_list
  #test_item.append(data_list[0])

  for i in input_data_list: #CHANGE TO ACTUAL LIST, this is where it will loop through each line
    item = i
    item = item.split("\t") # now a list in list

    #adding the names of keys
    dictionary_names_list = ["unique_identifier", "date_time", "state_enter_ignore", "action"]
    
    data_list.append(dict(zip(dictionary_names_list, item))) # should create a dictionary zipped up
  
  
  return (data_list)


#next function - the stuff needs to be organised by date
#this is so that we can track the actions in order and then can measure time and work day by day
#later we will cater for exception cases of if the data is abonormal or x

#function to sort list by date 
def sort_data_by_date(unsorted_list):
  sorted_list = sorted(unsorted_list, key=lambda d: d['date_time'])
  print("done")
  return (sorted_list)

#next, move data to data_processor


data_lsit = []
data_list = read_in_data() #get list of data
date_sorted_data_list = sort_data_by_date(data_list) #sort data by date
print(date_sorted_data_list)
  

#IMPORTANT NOTE   
#above has sorted but does not keep the same patient together - keep that in mind
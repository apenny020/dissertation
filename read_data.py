#read in
#first part to be assigned to individual
#second part to be assigned to date
#third part to be ignored
#4th part to assign state to a patient
#store all in a data structure - maybe a class that requires inputs and stores into a dictionary into an array

#think about how youre going to use data actually
import re

class read_data:
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

data_lsit = []
data_list = read_data()
print(data_list)


  

    

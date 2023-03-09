#read in
#first part to be assigned to individual
#second part to be assigned to date
#third part to be ignored
#4th part to assign state to a patient
#store all in a data structure - maybe a class that requires inputs and stores into a dictionary into an array

#think about how youre going to use data actually
import re


#alternate idea
#read in lines into list
#have a dictionary of the 4 words
#create a list that contains multiple valueless dictionaries for the length of the first list
#append into the dictionary with the values



#read in data and put it into a list with lines being seperated by commas
data_list = [] # the list of all the lines
dataFile = open("data_input_file_2018.txt", "r", encoding='utf-8-sig')
for line in dataFile:
  whole_line = line
  data_list.append(whole_line)
dataFile.close()
print (data_list[0])


patient_list = [] #??????
data_list_new = []
c = 0 # counter
test_item = [] #for testing - just using the first line - replace to loop through each line later, use data_list
test_item.append(data_list[0])
#test_item.append(data_list[1])
#test_item.append(data_list[2])

for i in test_item: #CHANGE TO ACTUAL LIST, this is where it will loop through each line
  item = i
  item = item.split("\t") # now a list in list
  print(item)
  print("PRINT C")
  print(c)

  #adding the names of keys
  dictionary_names_list = ["unique_identifier", "date_time", "state_enter_ignore", "action"]
  
  data_list_new.append(dict(zip(dictionary_names_list, item))) # should create a dictionary zipped up
  print(data_list_new)

  c = 1 #change to incremental, if its event needed anymore?

  


  

    

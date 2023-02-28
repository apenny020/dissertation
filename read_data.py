#read in
#first part to be assigned to individual
#second part to be assigned to date
#third part to be ignored
#4th part to assign state to a patient
#store all in a data structure - maybe a class that requires inputs and stores into a dictionary into an array

#think about how youre going to use data actually
import re

#read in data and put it into a list with lines being seperated by commas
data_list = []
dataFile = open("data_input_file_2018.txt", "r")
for line in dataFile:
  whole_line = line
  data_list.append(whole_line)
dataFile.close()
print (data_list[0])


patient_list = []
c = 0 # counter
test_item = []
test_item.append(data_list[0])

for i in test_item: #CHANGE TO ACTUAL LIST
  
  item = i
  item = item.split("\t") # now a list in list
  print("PRINT C")
  print(c)
  c = 1

  #adding the names of keys
  dictionary_names_list = ["unique_identifier", "date_time", "state_enter_ignore", "action"]
  index_counter = 0 # counts through the index at which point to add the string
  list_counter = 0 # counts for index in dictionary_names_list
  for i in dictionary_names_list:
    item.insert(index_counter, dictionary_names_list[list_counter]) #inserts the dictionary key name evey other item
    index_counter += 2
    list_counter += 1
    print(item)
    print(list_counter)
    print(i)



  #convert to tuples
  print("HERE")
  #it = iter(item)
  #it(zip(it, it))

  # list of vowels
  #phones = ['apple', 'samsung', 'oneplus']
  #phones_iter = iter(item)

  #print(next(phones_iter))   
  #print(next(phones_iter)) 
  #print(next(phones_iter))    


  

  #patient_list.append(item) #line now in the list

  #converting to dictionary

  #patient_list[c] = {}
  #c2 = 0 # second counter
  #for i in item:
  #  patient_list.update({c2:i})
  #  unique_identifier = patient_list[c2] 
  #  c2 += 1
    

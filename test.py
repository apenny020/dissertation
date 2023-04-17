#tests

############ Data #################
#Checking if data collected is reasonable

#Test to check Number consultants/nurses/patients in at any one time 
# -doesn't exceed the max possible (based off data collected)
# -not below 0

#Test to check number of patients in consultants/H&W&Bloods at any one time
# -doesn't exceed number of consultants/nurses
# -not below 0

########## Durations ##################

#Test to check that durations are 
# -greater than 5minutes
# -less than the max from the data

#Test to check that waiting times are
# -greater than 1minute
# -less than the length of the clinic minus the time the patient started waiting

#Test to check the % of patients leaving due to unsatisfaction
#If >25%, might want to change the conditions

######## workflow ##############

#Test to make sure patients are following their given workflow

#Test to check model only runs for < 14441 ticks

#Test to make sure actions are only happening within opening times

#Test to make sure that patients that had consultant appt if cancelled gets updated

#Test to make sure only one patient called through when nurse/consultant is free
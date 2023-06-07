To change any initialisation variables, see the initialise() function in 'omni_system.py'

NOTE: time is measured in minutes, if you wish to update a time, make sure it is in the minutes of the day format

(How it runs:
within main, 
process_all_data() from data_processor.py is called to process the input file (the input file can be changed providing it is of the same format),
then starts_everything() in main.py is called which within it calls
initialise() from omni_system.py is called which also calls other relevant smaller functions within itself, including initialising the agents.
starts_everything() then continues and runs through each tick, sometimes calling external functions and runs through the day)

To run the system, navigate to line 367 in Main.py
Follow the instructions there, you can choose to just run the model or the data processing and the model


def run_model(env, agents, ticks=1440):
    
    #env = environment project
    #agents = a list of agents
    #ticks = minutes in a day

    for tick in range(ticks):

        #here we check every minute and update agents and the system

        #update patients of the day and action
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
        #extra
            #waiting to start
            #finished

def get_agents_counted(record):
    #returns number of agents
    return()
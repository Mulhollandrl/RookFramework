import numpy as np
import random



# The statespace
states = ["Sleep","Icecream","Run"]

# Possible sequences of events
state_transitions = [["SS","SR","SI"],["RS","RR","RI"],["IS","IR","II"]]

# Probabilities matrix (transition matrix)
transition_probabilities = [[0.2,0.6,0.2],[0.1,0.6,0.3],[0.2,0.7,0.1]]

def reward(s, s_prime):
    pass


def probability_of_transition(s, s_prime):
    pass


def play_highest_point():
    pass


def play_trump():
    pass


def play_rook():
    pass


def lead_trump():
    pass


def lead_highest_number():
    pass


def get_state_space():
    strategies = [play_highest_point, play_trump, play_rook, lead_trump, lead_highest_number]
    return strategies


def get_current_strategy():
    strategies = get_state_space


def estimate_opponent_strategy():
    pass


def simulate(days):
    # Choose the starting state
    current_state = "Sleep"
    states_used = [current_state]
    i = 0
    prob = 1
    while i != days:
        if current_state == "Sleep":
            change = np.random.choice(state_transitions[0],replace=True,p=transition_probabilities[0])
            if change == "SS":
                prob = prob * 0.2
                states_used.append("Sleep")
                pass
            elif change == "SR":
                prob = prob * 0.6
                current_state = "Run"
                states_used.append("Run")
            else:
                prob = prob * 0.2
                current_state = "Icecream"
                states_used.append("Icecream")
        elif current_state == "Run":
            change = np.random.choice(state_transitions[1],replace=True,p=transition_probabilities[1])
            if change == "RR":
                prob = prob * 0.5
                states_used.append("Run")
                pass
            elif change == "RS":
                prob = prob * 0.2
                current_state = "Sleep"
                states_used.append("Sleep")
            else:
                prob = prob * 0.3
                current_state = "Icecream"
                states_used.append("Icecream")
        elif current_state == "Icecream":
            change = np.random.choice(state_transitions[2],replace=True,p=transition_probabilities[2])
            if change == "II":
                prob = prob * 0.1
                states_used.append("Icecream")
                pass
            elif change == "IS":
                prob = prob * 0.2
                current_state = "Sleep"
                states_used.append("Sleep")
            else:
                prob = prob * 0.7
                current_state = "Run"
                states_used.append("Run")
        i += 1    
    return states_used

# To save every activityList
list_activity = []
count = 0

# `Range` starts from the first count up until but excluding the last count
for iterations in range(1,10000):
        list_activity.append(simulate(2))

# Check out all the `activityList` we collected    
#print(list_activity)

# Iterate through the list to get a count of all activities ending in state:'Run'
for smaller_list in list_activity:
    if(smaller_list[2] == "Run"):
        count += 1

# Calculate the probability of starting from state:'Sleep' and ending at state:'Run'
percentage = (count/10000) * 100
print("The probability of starting at state:'Sleep' and ending at state:'Run'= " + str(percentage) + "%")

action_space = []
state_space = get_state_space()




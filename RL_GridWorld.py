
# define all states
states = [ i for i in range(16) ]
# 0   1   2   3
# 4   5   6   7
# 8   9   10  11
# 12  13  14  15


# Initial values of states
values = [ 0 for _ in range(16) ]

# Action
actions = ['n', 'e', 's', 'w']

# how states change by action
ds_action = {'n':-4, 's':4, 'w':-1, 'e':1}

# discount factor
gamma = 1.00

# according to current state and your action, calculate next state and immediate reward
def nextState(s, a):
    next_state = s

    # if at the edges, and next step will step outside the grid, then do nothing
    if(s%4 == 0 and a == 'w') or ((s+1)%4 == 0 and a == 'e') or (s<4 and a == 'n') or (s>11 and a == 's'):
        pass
    else:
        ds = ds_action[a]
        next_state = s+ds

    return next_state

# reward of a state
# if get to 1 or 15, return 0, else return -1
def rewardOf(s):
    return 0 if s in [0,15] else -1

# a = rewardOf(1)
# print(a)

# check if a state is terminate state
def isTerminateState(s):
    return s in [0, 15]

# get successor of a given state s
def getSuccessors(s):
    successors = []
    if isTerminateState(s):
        return successors
    for a in actions:
        next_state = nextState(s, a)
        successors.append(next_state)
    return successors


# update the value of state s
def updateValue(s):
    successors = getSuccessors(s)
    newValue = 0  # values[s]
    num = 4       # len(successors)
    reward = rewardOf(s)
    for next_state in successors:
        newValue += 1.00/num * (reward + gamma * values[next_state])
    return newValue


# perform one-step iteration
def performOneIteration():
    newValues = [0 for _ in range(16)]
    for s in states:
        newValues[s] = updateValue(s)
    global values
    values = newValues
    printValue(values)


# show some array info of the small grid world
def printValue(v):
    for i in range(16):
        print('{0:>6.2f}'.format(v[i]), end="")
        if (i+1)%4 == 0:
            print("")
    print()


# test function
def test():
    printValue(states)
    printValue(values)
    for s in states:
        reward = rewardOf(s)
        for a in actions:
            next_state = nextState(s,a)
            print("({0}, {1}) -> {2}, with reward {3}".format(s, a, next_state, reward))

    for i in range(200):
        performOneIteration()
        printValue(values)

def main():
    max_iterate_times = 160
    cur_iterate_times = 0
    while cur_iterate_times <= max_iterate_times:
        print("Iterate No.{0}".format(cur_iterate_times))
        performOneIteration()
        cur_iterate_times += 1
    printValue(values)

if __name__ == '__main__':
    main()

import copy

#Node class
class Node:

    def __init__(self, state, parent, action, path_cost, heuristic):

        self.state = state #State of the node (pancakes)
        self.parent = parent #Parent of the current node
        self.action = action #Action of the parent node
        self.path_cost = path_cost #Cost (only for A*)
        self.heuristic = heuristic #Heuristic (only for A*)


#BFS Printer##########################################################
def print_path(solution_child):

    sequence = []
    node = solution_child
    action = node.action
    sequence = ["".join(node.state)]
    node = solution_child.parent
    #Iterating through all children on the path
    while(True):
         
        #Creating the required output
        if(node.parent != None):
            node_state = node.state
            node_state.insert(action+1, "|")
            node_state = "".join(node_state)
            sequence.append(node_state)
            action = node.action
            node = node.parent
          
        else:
            node_state = node.state
            node_state.insert(action+1, "|")
            node_state = "".join(node_state)
            sequence.append(node_state)
            break

    #Printing the sequence in reverse
    length = len(sequence)-1
    while length >= 0:
        print(sequence[length])
        length -= 1


#A* Printer
def print_path_astar(solution_child):

    sequence = []
    node = solution_child
    action = node.action
    sequence = ["".join(node.state)+" g:" + str(node.path_cost) + ", " + "h:" + str(node.heuristic)]
    node = solution_child.parent
    #Iterating through all children on the path
    while(True):
         
        #Creating the required output
        if(node.parent != None):
            node_state = node.state
            node_state.insert(action+1, "|")
            node_state = "".join(node_state)
            node_state = node_state + " g:" + str(node.path_cost) + ", " + "h:" + str(node.heuristic)
            sequence.append(node_state)
            action = node.action
            node = node.parent
          
        else:
            node_state = node.state
            node_state.insert(action+1, "|")
            node_state = "".join(node_state)
            node_state = node_state + " g:" + str(node.path_cost) + ", " + "h:" + str(node.heuristic)
            sequence.append(node_state)
            break

    #Printing the sequence in reverse
    length = len(sequence)-1
    while length >= 0:
        print(sequence[length])
        length -= 1

#####################################################################


#BFS Flipper##########################################################
def flip(node, index):

    #Simply flip the pancakes by the current index
    copy_node = copy.deepcopy(node)
    pancakes = copy_node.state
    pancakes[0:index+1] = pancakes[0:index+1][::-1]

    for i in range(index+1):

        if(pancakes[i][1] == 'w'):
            pancake = pancakes[i]
            pancake = pancake.replace("w", "b")
            pancakes[i] = pancake
        
        else:
            pancake = pancakes[i]
            pancake = pancake.replace("b", "w")
            pancakes[i] = pancake
    
    #Create the flipped node (child)
    child = Node(pancakes, node, index, None, None)
    
    return child

#A* Flipper
def flip_astar(node, index):
    #Simply flip the pancakes by the current index
    copy_node = copy.deepcopy(node)
    pancakes = copy_node.state
    pancakes[0:index+1] = pancakes[0:index+1][::-1]

    for i in range(index+1):

        if(pancakes[i][1] == 'w'):
            pancake = pancakes[i]
            pancake = pancake.replace("w", "b")
            pancakes[i] = pancake
        
        else:
            pancake = pancakes[i]
            pancake = pancake.replace("b", "w")
            pancakes[i] = pancake

    node_heursistic = get_heuristic(pancakes)
    #Create the flipped node (child)
    child = Node(pancakes, node, index, index+1+node.path_cost, node_heursistic)

    return child

##################################################################################



#BFS Expander######################################################################
def expand(node, problems):

    children = []
    action = node.action

    #Get each child that isnt already in the closed set or isnt the same as the parent
    for i in range(4):
        flipped_node = flip(node, i)
        flipped_state = flipped_node.state
        if(i != action and flipped_state not in problems):
            children.append(flip(node, i))
        
        else:
            continue
    
    return children

#A* Expander
def expand_astar(node, problems):

    children = []
    action = node.action

    #Get each child that isnt already in the closed set or isnt the same as the parent
    for i in range(4):
        flipped_node = flip_astar(node, i)
        flipped_state = flipped_node.state
        if(i != action and flipped_state not in problems):
            children.append(flip_astar(node, i))
        
        else:
            continue
    
    return children

##################################################################################

def get_heuristic(pancakes):

    out_of_place = []
    for i in range(len(pancakes)):
        if(pancakes[i][0] != str(i+1)):
            out_of_place.append(pancakes[i][0])

    if(out_of_place == []):
        return 0
    else:
        return int(max(out_of_place))

def get_fn(node):

    return node.path_cost + node.heuristic

def get_tiebreak_val(node):

    tie_break_vals = []
    state = node.state
    for i in range(len(state)):
        val = state[i]
        if(val[1] == "w"):
            tie_break_vals.append(val[0] + "1")
        else:
            tie_break_vals.append(val[0] + "0")
    
    tie_val = "".join(tie_break_vals)
    tie_val = int(tie_val)

    return tie_val

def sort_fringe(fringe):

    fringe = sorted(fringe, key=lambda x: [get_fn(x), get_tiebreak_val(x)],reverse=False)
    return fringe

#Checking the conditions of the goal state    
def is_goal(node_state):
    
    if(node_state == ['1w','2w','3w','4w']):
        return True
    
    else:
        return False

#BFS Algorithm
def bfs(root_node, goal_state):

    #Checking to see if Root (initial state) is the Goal State
    if(is_goal(root_node.state)):
        print("".join(root_node.state))
        
    
    #The Fringe (FIFO queue)
    frontier = [root_node]

    #Reached States (Keeping track of the states we reach --> closed set)
    reached = [root_node.state]

    #BFS
    while(frontier != []):

        #FIFO Behavior
        current_node = frontier.pop(0)

        #Expanding the current node
        children = expand(current_node,reached)

        #Checking if either of the children is the goal - if one child is the goal, print its path
        for child in children:
            s = child.state
            if(is_goal(s)):
                print_path(child)
                return
                
            
            #If the child is not a goal, add to fringe and closed set
            else:
                if(s not in reached):
                    reached.append(s)
                    frontier.append(child)
    
    
    #If no solution is found, print failure
    failure = "Failed to find a solution."
    return failure

def a_star(root_node, goal_state):

    #Checking to see if Root (initial state) is the Goal State
    if(is_goal(root_node.state)):
        print("".join(root_node.state)+" g:0, h:0")
        
    
    #The Fringe
    frontier = [root_node]

    #Reached States (Keeping track of the states we reach --> closed set)
    reached = [root_node.state]

    #A*
    while(frontier != []):

        current_node = frontier.pop(0)

        #Expanding the current node
        children = expand_astar(current_node,reached)

        #Checking if either of the children is the goal - if one child is the goal, print its path
        for child in children:
            s = child.state
            if(is_goal(s)):
                print_path_astar(child)
                return
            
            
            #If the child is not a goal, add to fringe and closed set
            else:
                if(s not in reached):
                    reached.append(s)
                    frontier.append(child)
        
        frontier = sort_fringe(frontier)
    
    
    #If no solution is found, print failure
    failure = "Failed to find a solution."
    return failure


def get_algorithm(input_string):
    
    #returning the input algorithm
    return input_string[-1]

def get_input_state(input_string):

    #Getting rid of last two characters
    string = input_string[:-2]
    #Generating the state as a list
    state = []
    for i in range(len(string)):
        if(i%2==0):
            state.append(string[i]+string[i+1])

    #returning the cleaned state
    return state

def get_solution(state, algo, goal):

    if(algo == "b"):
        bfs(state, goal)
    
    else:
        a_star(state,goal)

if __name__ == "__main__":
    goal = ["1w", "2w", "3w", "4w"]
    user_input = input("Enter initial state\n")
    initial_state = Node(get_input_state(user_input), None, None, 0, 0)
    algorithm = get_algorithm(user_input)
    get_solution(initial_state, algorithm, goal)

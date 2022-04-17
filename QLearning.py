import random
random.seed(1)

class Cell:

    def __init__(self, reward, q_values, index, cell_type):

        self.reward = reward #Cell Reward
        self.q_values = q_values #Q-values, all initialized to 0
        self.index = index #Cell Index, 1-16
        self.cell_type = cell_type #Type of cell to make sure it is not a forbidden, goal or wall cell

class Environment:

    def __init__(self, user_input):

        self.learning_rate = 0.3 #Environment Learning Rate
        self.discount = 0.1 #Environment Discount
        self.greedy_rate = 0.5 #Environment Greedy Rate
        self.living_reward = -0.1 #Environment Living Reward
        self.user_input = user_input #Environment Input by the user
        self.board = self.create_board() #Creating a board with 16 cells as a list
    
    def create_board(self):

        cells = [] #cell list

        for i in range(16): #Creating 16 cells as the board

            cells.append(Cell(self.living_reward, {"up": 0.00, "right": 0.00, "down": 0.00, "left": 0.00}, i, "normal"))
        
        #Assigning User Input to the cells
        goal_one = self.user_input[0] - 1
        goal_two = self.user_input[1] - 1
        forbidden = self.user_input[2] - 1
        wall = self.user_input[3] - 1

        #Assigning new values to the cells based on user input
        cells[goal_one].reward, cells[goal_one].cell_type = 100, "goal"
        cells[goal_two].reward, cells[goal_two].cell_type = 100, "goal"
        cells[forbidden].reward, cells[forbidden].cell_type = -100, "forbid"
        cells[wall].reward, cells[wall].cell_type = 0, "wall-square"

        return cells

class QLearning:

    def __init__(self, user_sequence):

        self.user_sequence = user_sequence #Input user gives
        self.user_input = self.get_input() #Parsed input the user gives
        self.environment = self.get_environment() #creating an environment object
        self.board = self.environment.board #getting the created board
        self.learned_values = self.q_learning() #getting the final learned state from q_learning
        

    #Parser Function
    def get_input(self):
        
        sequence_list = self.user_sequence.split()
        for i in range(len(sequence_list)):
            if(sequence_list[i] != 'q' and sequence_list[i]!= 'p'):
                sequence_list[i] = int(sequence_list[i])
        
        return sequence_list

    #Getter for enviroment
    def get_environment(self):

        return Environment(self.user_input)

    #Update agent position in the gridworld
    def update_position(self, current_cell, action):

        cell_index = current_cell.index
        

        if(action == "up"):
            
            if(cell_index > 11):
                return current_cell.index
            
            else:
                cell_index += 4
        
        elif(action == "right"):

            if(cell_index in [3,7,11,15]):
                return current_cell.index
            
            else:
                cell_index += 1

        elif(action == "down"):
            if(cell_index < 4):
                return current_cell.index
            
            else:
                cell_index -= 4

        else:
            if(cell_index in [0,4,8,12]):
                return current_cell.index
            
            else:
                cell_index -= 1

        if(self.board[cell_index].cell_type == "wall-square"):
            return current_cell.index
        
        return cell_index

    #Getting a random action 
    def random_action(self):

        rand_action = random.choice(["up", "right", "down", "left"])

        return rand_action

    #Getting the best action based on Q-value
    def best_action(self, current_cell):

        q_vals = current_cell.q_values
        return max(q_vals, key=q_vals.get)
        

    #Moving the agent
    def move(self, current_cell):

        if(self.environment.greedy_rate > random.random()):

            #Take a random action
            action = self.random_action()
            return action, self.board[self.update_position(current_cell, action)]
        
        else: #Use the best action instead
            action = self.best_action(current_cell)
            return action, self.board[self.update_position(current_cell, action)]
    
    def q_learning(self):

        #Iteration
        iteration = 0

        while(iteration <= 120000):
            
            if(iteration > 100000):
                self.environment.greedy_rate = 0

            #Setting agent back at the start of the board
            current_cell = self.board[1]
            
            while(current_cell.cell_type not in ['forbid', 'goal']): #Computing an iteration until the agent receives a goal or the forbidden reward

                action, updated_cell = self.move(current_cell) #Moving the agent
                q_value = current_cell.q_values[action] #Getting the q-value
                new_reward = updated_cell.reward #Receiving the reward
                current_cell.q_values[action] = ((1-self.environment.learning_rate)*q_value) + (self.environment.learning_rate * (new_reward + self.environment.discount * max(updated_cell.q_values.values())))
                self.board[current_cell.index].q_values = current_cell.q_values #setting the new q-value
                current_cell = updated_cell #updating the new cell

            iteration += 1

def main():

    user_input = input() #getting user input
    result = QLearning(user_input) #learning
    
    if("p" in user_input): #print policy
        for i in range(16):
            if(result.board[i].cell_type == "normal"):
                print(str(i+1) + " ", str(result.best_action(result.board[i]))) 
            else:
                print(str(i+1) + " ", result.board[i].cell_type)
    
    else: #print q-values
        cell = result.board[result.user_input[-1] - 1].q_values
        print("up", round(cell["up"],2))
        print("right", round(cell["right"], 2))
        print("down", round(cell["down"], 2))
        print("left", round(cell["left"],2))

if __name__ == "__main__":
    
    main()
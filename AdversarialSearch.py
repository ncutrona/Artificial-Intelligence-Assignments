class TreeNode:

    def __init__(self, children, value, index, eval_type):

        self.children = children #Node Children
        self.value = value #Value of the terminal Node
        self.index = index #Index of the terminal Node
        self.eval_type = eval_type #Evaluation Type (Max or Min)

class MiniMaxTree:

    def __init__(self, input_sequence, visited_nodes):

        self.input_sequence = input_sequence #User Input Sequence
        self.terminal_children = self.get_terminals() #Getting Terminal Children cleaned and in a list of ints
        self.visited_nodes = visited_nodes #Keeping track of visited nodes in order to prune unvisited nodes
        self.tree = self.construct_tree() #Building the tree (hardcoded as per the problem)

    #Getting user input data formated 
    def get_terminals(self):

        sequence = self.input_sequence
        sequence_list = sequence.split()
        map_sequence = map(int, sequence_list)
        terminal_children = list(map_sequence)

        return terminal_children #Returns a list of children in int form

    #Hardcoding the tree with respect to the problem
    def construct_tree(self):

        term = self.terminal_children
        #Terminal Nodes
        term_nodes = []
        for i in range(len(term)):
            term_nodes.append(TreeNode(None,term[i], i, "Min")) #Level 4 --> Terminal children
            
        #Level Three
        level_three_nodes = []
        for i in range(len(term_nodes)):

            if(i%2 == 0): #Building two children per node
                level_three_node = TreeNode([],None, None, "Max")
                level_three_node.children.append(term_nodes[i])
                level_three_node.children.append(term_nodes[i+1])

                level_three_nodes.append(level_three_node)
        
        #Level Two
        level_two_nodes = []
        for i in range(len(level_three_nodes)):

                if(i%2 == 0): #Building two children per node
                    level_two_node = TreeNode([],None, None, "Min")
                    level_two_node.children.append(level_three_nodes[i])
                    level_two_node.children.append(level_three_nodes[i+1])

                    level_two_nodes.append(level_two_node)
        
        #Root Node
        root = TreeNode([], None, None, "Max")

        for i in range(len(level_two_nodes)): #Adding all the min children to the root node
            root.children.append(level_two_nodes[i])

        return root #Returning the root (tree)

    #Checking if Alpha >= Beta for the stopping condition in the minimax prune function
    def explore_check(self, alpha, beta):

        if(alpha >= beta): #If this condition, do not explore children
            return True
        
        else:
            return False

    #Recursive Call function to repeatedly call the alphabeta pruning as we go down a path of a tree
    def recursive_call(self, current, child, alpha, beta):

        updated_alpha, updated_beta = self.alpha_beta_prune(child, alpha, beta) #Recursive Call
        if current.eval_type == "Min":
            beta = min(beta, updated_alpha, updated_beta)
        else:
            alpha = max(alpha, updated_alpha, updated_beta)

        return alpha, beta #Returning the Best case values for both alpha and beta

    #Main Pruning Function
    def alpha_beta_prune(self, current_node, alpha, beta):
        
        if(self.explore_check(alpha, beta)): #Checking our stopping condition
            return alpha, beta
        
        self.visited_nodes.append(current_node.index) #Keeping track of visited Nodes
        
        if current_node.children == None: #Reached the bottom (terminal values, stop because we cant expland further down the tree on this path)
            return current_node.value, current_node.value #Return the value twice (for beta/alpha)
        
        #Recursively iterating through each child as we move down a path on the tree 
        for child_node in current_node.children:
            
            #Setting alpha and beta equal to the recursive call helper function output 
            alpha, beta = self.recursive_call(current_node, child_node, alpha, beta)
        
        return alpha, beta #Returning the updated alpha and beta once we reach a node in the recursion
    
    #Display Function for Pruned Nodes
    def display_pruned(self):

        visited = [] #Creating a new list of visited nodes without None in the list

        for i in range(len(self.visited_nodes)):
            if(self.visited_nodes[i] != None):
                visited.append(self.visited_nodes[i]) #Adding to the new visited list
        
        pruned = [] #Creating a pruned list

        for i in range(12): #Getting the pruned nodes that are not in visited
            if(i not in visited):
                pruned.append(i)
        
        print(" ".join(list(map(str, pruned)))) #Displaying pruned Nodes

    def main(self):
        
        root = self.tree #Building the tree

        alpha, beta = self.alpha_beta_prune(root, -1e+20, 1e+20) #pruning
        
        self.display_pruned() #display results

if __name__ == "__main__":
    sequence = input("Please enter terminal nodes:\n")
    MiniMaxTree(sequence, []).main()
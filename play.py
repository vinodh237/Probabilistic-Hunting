import numpy as np
from numpy import unravel_index
import copy
from helper import generate_board,Target_not_found_given_Target_in_cell,generate_intial_belief_matrix,choose_target,get_prob_found_matrix,update_belief_matrix
from helper import ManhattanDistance,Target_of_Type,get_dis
import random

def get_max_index(prob_mat):
    """
    :param prob_mat: probability matrix
    :return: returns index which has maximum probability
    """
    max_value = np.ndarray.max(prob_mat)
    l = []
    for i in range(len(prob_mat)):
        for j in range(len(prob_mat)):
            if prob_mat[i,j] == max_value:
                l.append((i,j))
    a = random.randint(1,len(l))-1
    #return unravel_index(prob_mat.argmax(),prob_mat.shape)
    return l[a]

## rule 1
def rule_1(board,belief_matrix_,target):
    num_searches = 0
    next_step = get_max_index(belief_matrix_)
    while (target[0],target[1]) != next_step:
        belief_matrix_ = update_belief_matrix(board=board,belief=belief_matrix_,i=next_step[0],j=next_step[1])
        num_searches+=1
        next_step = get_max_index(belief_matrix_)
    return num_searches

## rule-1 with distance factor
def rule_1_dis(board,belief_matrix_,target,simple = True):
    num_searches = 0
    next_step = get_max_index(belief_matrix_)
    dim = len(board)
    dis_matrix = np.zeros_like(board)
    while (target[0],target[1]) != next_step:
        belief_matrix_ = update_belief_matrix(board=board,belief=belief_matrix_,i=next_step[0],j=next_step[1])
        num_searches+= dis_matrix[next_step[0],next_step[1]]
        dis_matrix = get_dis(dim,i=next_step[0],j=next_step[1])
        if simple == False:
            log_dis_matrix = 1+np.log(1+dis_matrix)
            next_step = get_max_index(belief_matrix_/log_dis_matrix)
        else:
            next_step = get_max_index(belief_matrix_)
    return num_searches

## rule 2 with distance
def rule_2_dis(board,belief_matrix_,target,simple = True):
    num_searches = 0
    prob_found_matrix_ = get_prob_found_matrix(board=board,belief=belief_matrix_)
    next_step = get_max_index(prob_found_matrix_)
    dim = len(board)
    dis_matrix = np.zeros_like(board)
    while (target[0],target[1]) != next_step:
        belief_matrix_ = update_belief_matrix(board=board, belief=belief_matrix_,i = next_step[0],j = next_step[1])
        num_searches += dis_matrix[next_step[0],next_step[1]]
        prob_found_matrix_ = get_prob_found_matrix(board=board,belief=belief_matrix_)
        dis_matrix = get_dis(dim, i=next_step[0], j=next_step[1])
        log_dis_matrix = 1+np.log(1 + dis_matrix)
        if simple == False:
            next_step = get_max_index(prob_found_matrix_/log_dis_matrix)
        else:
            next_step = get_max_index(prob_found_matrix_)

    return num_searches

# rule 2
def rule_2(board,belief_matrix_,target):
    num_searches = 0
    prob_found_matrix_ = get_prob_found_matrix(board=board,belief=belief_matrix_)
    next_step = get_max_index(prob_found_matrix_)
    while (target[0],target[1]) != next_step:
        belief_matrix_ = update_belief_matrix(board=board, belief=belief_matrix_,i = next_step[0],j = next_step[1])
        num_searches += 1
        prob_found_matrix_ = get_prob_found_matrix(board=board,belief=belief_matrix_)
        next_step = get_max_index(prob_found_matrix_)
    return num_searches


# def ques_4(board,belief_matrix_,target):
#     num_searches = 0
#     prob_found_matrix_ = get_prob_found_matrix(board=board, belief=belief_matrix_)
#     next_step = get_max_index(prob_found_matrix_)
#     while target != next_step:
#         belief_matrix_ = update_belief_matrix(board=board, belief=belief_matrix_, i=next_step[0], j=next_step[1])
#         num_searches += 1
#         prob_found_matrix_ = get_prob_found_matrix(board=board, belief=belief_matrix_)
#         next_step = get_max_index(prob_found_matrix_)
#     return num_searches

def ques_3():
    for type in [0, 1, 2, 3]:
        searches_rule_1 = 0
        searches_rule_2 = 0
        iterations = 100
        dim = 50

        for i in range(iterations):
            # searches_rule_1 = 0
            # searches_rule_2 = 0
            if i%10 == 0:
                print(i)
            # generate board
            board = generate_board(dim)
            # Choose target
            target = Target_of_Type(copy.deepcopy(board),type)
            # print("target type  "+str(board[target[0],target[1]]))
            belief_matrix = generate_intial_belief_matrix(dim)
            searches_rule_1 += rule_1(copy.deepcopy(board),copy.deepcopy(belief_matrix),copy.copy(target))
            searches_rule_2 += rule_2(copy.deepcopy(board),copy.deepcopy(belief_matrix),copy.copy(target))
            # print("rule-1 --- "+str(searches_rule_1) +"rule-2 --- "+str(searches_rule_2))
        print("type :: "+str(type))
        print("Average number of searches rule-1 and rule-2 respectively: ",str(searches_rule_1/iterations)+"  ,  "+str(searches_rule_2/iterations)+"\n")

# ques_3()
def ques_4():
    for type in [0, 1, 2, 3]:
        searches_rule_1 = 0
        searches_rule_2 = 0
        searches_rule_1_ = 0
        searches_rule_2_ = 0
        iterations = 10
        dim = 50

        for i in range(iterations):
            # searches_rule_1 = 0
            # searches_rule_2 = 0
            if i%10 == 0:
                print(i)
            # generate board
            board = generate_board(dim)
            # Choose target
            target = Target_of_Type(copy.deepcopy(board),type)
            # print("target type  "+str(board[target[0],target[1]]))
            belief_matrix = generate_intial_belief_matrix(dim)
            searches_rule_1 += rule_1_dis(copy.deepcopy(board),copy.deepcopy(belief_matrix),copy.copy(target),simple=False)
            searches_rule_1_ += rule_1_dis(copy.deepcopy(board), copy.deepcopy(belief_matrix), copy.copy(target),
                                          simple=True)
            searches_rule_2 += rule_2_dis(copy.deepcopy(board),copy.deepcopy(belief_matrix),copy.copy(target),simple=False)
            searches_rule_2_ += rule_2_dis(copy.deepcopy(board), copy.deepcopy(belief_matrix), copy.copy(target),
                                          simple=True)
            # print("rule-1 --- "+str(searches_rule_1) +"rule-2 --- "+str(searches_rule_2))
        print("type :: "+str(type))
        print("Average number of searches rule-1 and rule-2 respectively: ",str(searches_rule_1/iterations)+"  ,  "+str(searches_rule_2/iterations)+"\n")
        print("Average number of searches rule-1 and rule-2 respectively: ",
              str(searches_rule_1_ / iterations) + "  ,  " + str(searches_rule_2_ / iterations) + "\n")
ques_4()
# QUESTION - 2

def move_target(dim,target,board):
    a = target[0]
    b = target[1]
    type1 = board[a,b]
    L = []
    new_L = []
    ## adding all possible neighbours to a list
    L.append([a - 1, b])
    L.append([a + 1, b])
    L.append([a, b - 1])
    L.append([a, b + 1])
    for l in L:
        if IsvalidPoint(dim,l[0],l[1]):
            new_L.append(l)
    pick = random.randint(1,len(new_L)) - 1
    type2 = board[new_L[pick][0],new_L[pick][1]]
    return new_L[pick],(type1,type2)

def get_neighbs(dim,a,b):
    L = []
    new_L = []
    L.append([a - 1, b])
    L.append([a + 1, b])
    L.append([a, b - 1])
    L.append([a, b + 1])
    for l in L:
        if IsvalidPoint(dim, l[0], l[1]):
            new_L.append(l)
    return new_L

def IsvalidPoint(dim,m,n):
    ## return False if point is not in maze limit
    if  m < 0 or n < 0 or m >= dim or n >= dim :
        return False
    return True

def update_found_matrix_by_evidence(board,prob_found_matrix_,evidence):
    type1,type2 = evidence
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i,j] == type1 or board[i,j] == type2:
                # update prob found matrix
                prob_found_matrix_[i, j] = 0
            else:
                # update prob found matrix
                prob_found_matrix_[i, j] = 0
    return prob_found_matrix_

def list_contains_type(board,l,type):
    for i,j in l:
        if board[i,j] == type:
            return True
    return False

def neigh_sum(matrix):
    dim = len(matrix)
    sum_matrix = np.zeros_like(matrix)
    for i in range(dim):
        for j in range(dim):
            if i > 0 and j >0 and i < dim-1 and j < dim -1 :
                sum_matrix[i,j] = matrix[i-1,j] + matrix[i,j-1] + matrix[i+1,j] + matrix[i,j+1]

            elif i==0 and j==0:
                sum_matrix[i, j] = matrix[i + 1, j] + matrix[i, j + 1]
            elif i==dim-1 and j == dim -1:
                sum_matrix[i, j] = matrix[i-1,j] + matrix[i,j-1]
            elif i==0 and j == dim -1:
                sum_matrix[i, j] =  matrix[i,j-1] + matrix[i+1,j]
            elif i==dim-1 and j == 0:
                sum_matrix[i, j] = matrix[i-1,j]  + matrix[i,j+1]

            elif i == 0:
                sum_matrix[i,j] = matrix[i,j-1] + matrix[i+1,j] + matrix[i,j+1]
            elif i == dim-1:
                sum_matrix[i,j] = matrix[i-1,j] + matrix[i,j-1] + matrix[i,j+1]
            elif j == 0:
                sum_matrix[i,j] = matrix[i-1,j] + matrix[i+1,j] + matrix[i,j+1]
            elif j == dim-1:
                sum_matrix[i,j] = matrix[i-1,j] + matrix[i,j-1] + matrix[i+1,j]
    return sum_matrix


def update_belief_matrix_by_evidence(board,prob_found_matrix_,evidence):
    type1,type2 = evidence
    new_prob_found_matrix_ = np.zeros_like(prob_found_matrix_)
    for i in range(len(board)):
        for j in range(len(board)):
            current_type = board[i,j]
            if current_type == type1:
                # update prob found matrix
                l = get_neighbs(dim=len(board),a=i,b=j)
                if list_contains_type(board,l,type2):
                    new_prob_found_matrix_[i,j] = 1

            elif current_type == type2:
                l = get_neighbs(dim=len(board),a=i,b=j)
                list_contains_type(board,l,type2)
                if list_contains_type(board,l,type2):
                    new_prob_found_matrix_[i,j] = 1
            else:
                # update prob found matrix
                new_prob_found_matrix_[i, j] = 0
    sum_matrix = neigh_sum(new_prob_found_matrix_)
    #Zeros for all cells of other types
    a = prob_found_matrix_*new_prob_found_matrix_
    # b = a/sum_matrix
    b = np.zeros_like(a)
    for i in range(len(a)):
        for j in range(len(a)):
            if sum_matrix[i,j] > 0.0:
                b[i,j] = a[i,j] / sum_matrix[i,j]
    f = neigh_sum(b)
    return f

def part2_rule_1(board,belief_matrix_,target):
    """
    :param board: board
    :param belief_matrix: belief matrix
    :return: number of searches
    """
    num_searches = 0
    dim = len(board)
    prob_found_matrix_ = get_prob_found_matrix(board=board, belief=belief_matrix_)
    next_step = get_max_index(prob_found_matrix_)

    while (target[0],target[1]) != next_step:
        belief_matrix_ = update_belief_matrix(board=board, belief=belief_matrix_, i=next_step[0], j=next_step[1])
        num_searches += 1
        # target moved
        target,evidence = move_target(dim,target,board)
        prob_belief_matrix_ = update_belief_matrix_by_evidence(board,prob_found_matrix_,evidence)
        next_step = get_max_index(prob_belief_matrix_)

    return num_searches



def part2_rule_2(board,belief_matrix_,target):
    """
    :param board: board
    :param belief_matrix: belief matrix
    :return: number of searches
    """
    num_searches = 0
    dim = len(board)
    prob_found_matrix_ = get_prob_found_matrix(board=board, belief=belief_matrix_)
    next_step = get_max_index(prob_found_matrix_)
    while (target[0],target[1]) != next_step:
        belief_matrix_ = update_belief_matrix(board=board, belief=belief_matrix_, i=next_step[0], j=next_step[1])
        num_searches += 1
        prob_found_matrix_ = get_prob_found_matrix(board=board, belief=belief_matrix_)
        # target moved
        target,evidence = move_target(dim,target,board)
        prob_found_matrix_ = update_found_matrix_by_evidence(board,prob_found_matrix_,evidence)
        next_step = get_max_index(prob_found_matrix_)
    return num_searches

def last_question():
    for type in [0, 1, 2, 3]:
        searches_rule_1 = 0
        searches_rule_2 = 0
        iterations = 100
        dim = 50

        for i in range(iterations):
            # searches_rule_1 = 0
            # searches_rule_2 = 0
            if i%10 == 0:
                print(i)
            # generate board
            board = generate_board(dim)
            # Choose target
            target = Target_of_Type(copy.deepcopy(board),type)
            # print("target type  "+str(board[target[0],target[1]]))
            belief_matrix = generate_intial_belief_matrix(dim)
            searches_rule_1 += part2_rule_1(copy.deepcopy(board),copy.deepcopy(belief_matrix),copy.copy(target))
            searches_rule_2 += part2_rule_2(copy.deepcopy(board),copy.deepcopy(belief_matrix),copy.copy(target))
            # print("rule-1 --- "+str(searches_rule_1) +"rule-2 --- "+str(searches_rule_2))
        print("type :: "+str(type))
        print("Average number of searches rule-1 and rule-2 respectively: ",str(searches_rule_1/iterations)+"  ,  "+str(searches_rule_2/iterations)+"\n")

# last_question()
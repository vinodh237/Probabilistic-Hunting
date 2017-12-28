import numpy as np
import random
def generate_board(dim):
    """

    :param dim: board size
    #0 ----> Flat
    #1 ----> Hilly
    #2 ----> Forest
    #3 ----> Caves
    :return:
    """
    m = np.zeros([dim,dim],dtype=int)
    for i in range(dim):
        for j in range(dim):
            m[i,j] = get_surface()
    return m

def get_surface():
    """

    :return:  a surface at random
    """
    p = np.random.rand()
    ## flat with probability
    if p <= 0.2:
        return 0
    if p <= 0.5:
        return 1
    if p <= 0.8:
        return 2
    if p <= 1.0:
        return 3
Target_not_found_given_Target_in_cell_map = {}
Target_not_found_given_Target_in_cell_map[0] = 0.1
Target_not_found_given_Target_in_cell_map[1] = 0.3
Target_not_found_given_Target_in_cell_map[2] = 0.7
Target_not_found_given_Target_in_cell_map[3] = 0.9

Target_found_given_Target_in_cell_map = {}
Target_found_given_Target_in_cell_map[0] = 0.9
Target_found_given_Target_in_cell_map[1] = 0.7
Target_found_given_Target_in_cell_map[2] = 0.3
Target_found_given_Target_in_cell_map[3] = 0.1


def Target_not_found_given_Target_in_cell(cell_type):
    """
    :param cell_type: type of surface
    :return: probability that target not found give Target in cell
    """
    #0 ----> Flat   ----> 0.1
    #1 ----> Hilly  ----> 0.3
    #2 ----> Forest ----> 0.7
    #3 ----> Caves  ----> 0.9

    return Target_not_found_given_Target_in_cell_map[cell_type]

def Target_of_Type(board,type):
    """
    :param board: board
    :param type: type of surface
    :return: target in this type of surface
    """
    dim = len(board)
    a = random.randint(0,dim-1)
    b = random.randint(0,dim-1)
    while board[a,b] != type:
        a = random.randint(0, dim - 1)
        b = random.randint(0, dim - 1)
    return (a,b)

def mod(x):
    """
    :param x: any number
    :return: |x|
    """
    if x >= 0:
        return x
    else:
        return -x

def ManhattanDistance(x1,y1,x2,y2):
    """
    :param x1: x coordinate of point-1
    :param y1: y coordinate of point-1
    :param x2: x coordinate of point-2
    :param y2: y coordinate of point-2
    :return: Manhattan distance between the points (integer)
    """
    return mod(x1-x2) + mod(y1-y2)

def get_dis(dim,i,j):
    dis_mat = np.zeros([dim,dim])
    for l in range(dim):
        for m in range(dim):
            dis_mat[l,m] = ManhattanDistance(l,m,i,j)
    return dis_mat

def generate_intial_belief_matrix(dim):
    """
    :param dim: size of board
    :return: initial belief matrix
    """
    matrix = np.zeros([dim,dim]) + (1/(dim*dim))
    return matrix

def choose_target(dim):
    pos = np.random.randint(1,dim*dim)
    i = pos%dim
    j = int(pos/dim)%dim
    return (i,j)


# def update_belief_matrix(board,belief,i,j):
#     """
#     :param board: board which contains type of terrain
#     :param belief: belief matrix
#     :param j: Failure in cell j
#     :return: updated belief matrix
#     """
#
#     belief_i_j = belief[i,j]*(Target_not_found_given_Target_in_cell(board[i,j]))
#
#     diff = (belief[i,j] - belief_i_j)/(1-belief[i,j])
#
#     # normalization = np.sum(belief) - belief[i,j]
#     # belief = belief/normalization
#     new_belief = belief + diff*belief
#     new_belief[i,j] = belief[i,j]
#
#     return new_belief

def update_belief_matrix(board,belief,i,j):
    """
    :param board: board which contains type of terrain
    :param belief: belief matrix
    :param j: Failure in cell j
    :return: updated belief matrix
    """

    belief[i,j] = belief[i,j]*(Target_not_found_given_Target_in_cell(board[i,j]))

    # diff = (belief[i,j] - belief_i_j)/(1-belief[i,j])

    normalization = np.sum(belief)
    belief = belief/normalization

    return belief

# def get_prob_found_matrix(board,belief):
#     dim = len(board)
#     prob_not_found_matrix = np.zeros([dim,dim])
#
#     for i in range(dim):
#         for j in range(dim):
#             prob_not_found_matrix[i,j] = 1 - belief[i,j] + Target_not_found_given_Target_in_cell(board[i,j])*belief[i,j]
#     prob_found_matrix = 1- prob_not_found_matrix
#     # print("normalize  " + str(normalize) + "\n")
#     return prob_found_matrix

def get_prob_found_matrix(board,belief):
    dim = len(board)
    prob_found_matrix = np.zeros([dim, dim])

    for i in range(dim):
        for j in range(dim):
            prob_found_matrix[i,j] = belief[i,j]*Target_found_given_Target_in_cell_map[board[i,j]]

    return prob_found_matrix
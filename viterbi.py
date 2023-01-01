import sys
import numpy as np
import math

def Viterbi(map_data,state_space,start_prob,obs_data,transition,emission):
    trellis = []
    # first ob
    temp = np.zeros(np.shape(map_data),dtype=float)
    for i in range(len(state_space)):
        x,y = state_space[i]
        temp[x][y] = start_prob[i] * emission[0][i]
    prev = temp
    trellis.append(temp)

    # next obs
    for j in range(1,len(obs_data)):
        temp = np.zeros(np.shape(map_data),dtype=float)
        for i in range(len(state_space)):
            maxprob = 0
            x,y = state_space[i]
            for k in range(len(state_space)):
                a,b = state_space[k]
                maxprob = max(maxprob, prev[a][b] * transition[k][i] * emission[j][i])
                temp[x][y] = maxprob
        prev = temp
        trellis.append(temp)

    return trellis

if __name__ == '__main__':
    input_file = open(sys.argv[1])

    size = input_file.readline().strip().split()

    map_data = []
    for i in range(int(size[0])):
        line = input_file.readline().strip().split()
        map_data.append(line)

    obs = int(input_file.readline().strip())

    obs_data = []
    for i in range(obs):
        line = input_file.readline().strip().split()
        obs_data.append(line)

    error = float(input_file.readline().strip())

    K = []
    for row in range(int(size[0])):
        for col in range(int(size[1])):
            if map_data[row][col] == '0':
                K.append((row,col))

    start_prob = []
    for row in range(len(K)):
        start_prob.append(float(1/len(K)))

    transition = []
    for pos in K:
        adj = 0
        row = np.zeros(len(K), dtype = float)
        temp = []
        if (pos[0]-1,pos[1]) in K:  # N
            adj += 1
            temp.append((pos[0]-1,pos[1]))
        if (pos[0],pos[1]+1) in K:  # E
            adj += 1
            temp.append((pos[0],pos[1]+1))
        if (pos[0]+1,pos[1]) in K:  # S
            adj += 1
            temp.append((pos[0]+1,pos[1]))
        if (pos[0],pos[1]-1) in K:  # W
            adj += 1
            temp.append((pos[0],pos[1]-1))
        if adj > 0:
            for pair in temp:
                for i in range(len(K)):
                    if pair == K[i]:
                        row[i] = float(1/adj)
            transition.append(row)
        elif adj == 0:  # landlocked
            transition.append(row)

    emission = []
    for ob in obs_data:
        row = []
        for x,y in K:
            observation = ""# np.zeros(4,dtype = str)

            if x == 0:  # N
                observation += "1"
            elif map_data[x-1][y] == "X":
                observation += "1"
            else:
                observation += "0"
            
            if y+1 == int(size[1]):  # E
                observation += "1"
            elif map_data[x][y+1] == "X":
                observation += "1"
            else:
                observation += "0"

            if x+1 == int(size[0]):  # S
                observation += "1"
            elif map_data[x+1][y] == "X":
                observation += "1"
            else:
                observation += "0"

            if y == 0:  # W
                observation += "1"
            elif map_data[x][y-1] == "X":
                observation += "1"
            else:
                observation += "0"

            diff = 0
            observation = [observation]
            if ob[0][0] != observation[0][0]:
                diff += 1
            if ob[0][1] != observation[0][1]:
                diff += 1
            if ob[0][2] != observation[0][2]:
                diff += 1
            if ob[0][3] != observation[0][3]:
                diff += 1
            prob = pow((1-error),4-diff)*pow(error,diff)
            row.append(prob)
        emission.append(row)

    trellis = Viterbi(map_data,K,start_prob,obs_data,transition,emission)

    # print(trellis)
    # print(np.shape(trellis))

    np.savez('output.npz', *trellis)

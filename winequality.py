import sys
import math

class Node:
    def __init__(self,leaf=False):
        self.splitval = None
        self.leaf = leaf
        self.left = None
        self.right = None
        if leaf:
            self.label = None

def unique_labels(data):
    labels = [val[1] for val in data]
    unique = {}
    for i in labels:
        unique[i] = unique.get(i, 0) + 1
    return unique

def get_info(data):
    info = 0.0
    N = len(data)
    labels = unique_labels(data)
    for label,frequency in labels.items():
        prob = frequency/N
        info += -(prob * math.log(prob, 2))
        if prob == 0:
            info = 0.0
    return info

def DTL(data, minleaf):
    N = len(data)
    X = [tuple(val[0]) for val in data]
    X = set(X)
    Y = [val[1] for val in data]
    Y = set(Y)
    if N <= minleaf or len(X) == 1 or len(Y) == 1:
        n = Node(leaf=True)
        unique = unique_labels(data)
        max = 0
        unique_mode = True
        label = float(0)
        for lab, count in unique.items():
            # print(lab,count)
            if count == max:
                unique_mode = False
            elif count > max:
                max = count
                label = lab
                unique_mode = True
        if unique_mode:
            n.label = label
        return n

    attr, splitval = ChooseSplit(data)
    n = Node()
    n.attr = attr
    n.splitval = splitval
    left, right = [],[]
    for val in data:
        x = val[0]
        if x[attr] <= splitval:
            left.append(val)
        else:
            right.append(val)
    n.left = DTL(left, minleaf)
    n.right = DTL(right, minleaf)
    return n

def ChooseSplit(data):
    N = len(data)
    bestgain = 0
    bestattr = 0
    bestsplitval = 0
    for attr in range(len(data[0][0])):
        data.sort(key = lambda sort:sort[0][attr])
        for row in range(len(data)-1):
            splitval = 0.5 * (data[row][0][attr] + data[row + 1][0][attr])
            left, right = [], []
            for val in data:
                x = val[0]
                if x[attr] <= splitval:
                    left.append(val)
                else:
                    right.append(val)
            if len(left) == 0 or len(right) == 0:
                continue

            gain = 0

            rootinfo = get_info(data)
            leftinfo = get_info(left)
            rightinfo = get_info(right)

            remainder = (len(left)/len(data))*leftinfo + (len(right)/len(data))*rightinfo

            gain = rootinfo - remainder

            if (len(left) == 0 or len(right) == 0):
                gain = 0

            if gain > bestgain:
                bestattr = attr
                bestgain = gain
                bestsplitval = splitval

    return (bestattr,bestsplitval)


def Predict_DTL(node, data):
    while not node.leaf:
        if data[node.attr] <= node.splitval:
            node = node.left
        else:
            node = node.right

    return node.label

if __name__ == '__main__':
    train_path = sys.argv[1]
    test_path = sys.argv[2]
    minleaf = int(sys.argv[3])

    train_file = open(train_path)
    test_file = open(test_path)

    # headers = train_file.readline().strip().split()
    train_file.readline()

    train_data = []
    for line in train_file.readlines():
        data = [float(val) for val in line.strip().split()]
        # print(data)
        label = data[-1]
        data.pop()
        train_data.append((data, label))
        # print(data,quality)

    test_data = []
    test_file.readline()
    for line in test_file.readlines():
        entry = [float(val) for val in line.strip().split()]
        # print(entry)
        test_data.append(entry)

    dt = DTL(train_data, minleaf)

    for line in test_data:
        print(int(Predict_DTL(dt, line)))
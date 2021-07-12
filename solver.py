# Richard Cruikshank V00844041

# your program must
# function correctly with an LP provided via standard input and generate its output to standard
# output, with no command line parameters required for basic operation

import sys
import re

class Node:
    def __init__(self, row, col, mag, number):
        self.row = row
        self.col = col
        self.mag = mag
        self.number = number

    def __str__(self):
        return str(self.number) + ":" + str(self.mag)

    def __repr__(self):
        return str(self.number) + ":" + str(self.mag)

    def __lt__(self, other):
        return self.number < other.number

    def __add__(self, other):
        self.mag += other
        return self

    def __sub__(self, other):
        self.mag -= other
        return self

    def __mul__(self, other):
        self.mag *= other
        return self

    def __truediv__(self, other):
        self.mag /= other
        return self

    def isBasic(self):
        return self.col == 0

    def isNonbasic(self):
        return self.row == 0

    def isPrimalCandidate(self):
        return self.isNonbasic() and self.mag > 0

    def isDualCandidate(self):
        return self.isBasic() and self.mag < 0

class LP:
    def __init__(self, matrix):
        self.matrix = matrix
        self.num_opt_vars = len(self.matrix[0]) - 1
        self.num_constraints = len(self.matrix) - 1
        self.objective_val = self.matrix[0][0]
        self.objective_row = self.matrix[0]
        self.basis = self.matrix[1:]
        self.opt_var_indices = [(0,col) for col in range(1, len(self.matrix[0]))]
        self.slack_var_indices = [(row,0) for row in range(1,len(self.matrix))]

        self.opt_var_numbering = [i for i in range(self.num_opt_vars)]
        self.slack_var_numbering = [i for i in range(self.num_opt_vars, self.num_opt_vars+self.num_constraints)]
        # will not change - used to test optimalitcol
        self.nonbasic_var_indices = [(0,col) for col in range(1, len(self.matrix[0]))]
        self.basic_var_indices = [(row,0) for row in range(1,len(self.matrix))]

        # use nodes to represent variables so we have more information about them??
        self.dictionary = [[val for val in row] for row in self.matrix]
        for row in range(len(self.matrix)):
            for col in range(len(self.matrix[0])):
                if row == 0 and col > 0:
                    self.dictionary[row][col] = Node(row, col, self.matrix[row][col], col)
                elif row > 0 and col == 0:
                    self.dictionary[row][col] = Node(row, col, self.matrix[row][col], self.num_opt_vars+row)

    def getOptVarVals(self):
        return [self.matrix[row][col] for row,col in self.opt_var_indices]

    def getSlackVarVals(self):
        return [self.matrix[row][col] for row,col in self.slack_var_indices]

    def getNonBasicVarVals(self):
        return [self.matrix[row][col] for row,col in self.nonbasic_var_indices]

    def getBasicVarVals(self):
        return [self.matrix[row][col] for row,col in self.basic_var_indices]

    def chooseEnteringPrimal(self):
        # get lowest numbered nonbasic primal candidate
        candidates = [node for node in self.dictionary[0][1:] if node.mag > 0]
        if len(candidates) == 0:
            return None
        else:
            candidate = min(candidates)
            print("Entering primal: " + str(candidate))
            return candidate

    def chooseEnteringDual(self):
        # get lowest numbered basic dual candidate
        candidates = [node for node in [row[0] for row in self.dictionary[1:]] if node.mag < 0]
        if len(candidates) == 0:
            return None
        else:
            candidate = min(candidates)
            print("Entering dual: " + str(candidate))
            return candidate

    def chooseLeavingPrimal(self, enteringNode):
        # compute the bounds on the candidate leaving variables
        candidates = (
            [
                (i, self.dictionary[i][0].mag / (-1 * self.dictionary[i][enteringNode.col]))
                for i in range(1, len(self.dictionary))
                if self.dictionary[i][0].mag >= 0
                and self.dictionary[i][enteringNode.col] < 0
            ]
        )
        minimum = min(pair[1] for pair in candidates)
        print(minimum)
        candidates = [pair for pair in candidates if pair[1] == minimum]
        if len(candidates) == 1:
            return self.dictionary[candidates[0][0]][0]
        elif len(candidates > 1):
            candidates = [self.dictionary[candidate[0]] for candidate in candidates]
            return min(candidates)
        return

    def chooseLeavingDual(self, enteringNode):
        # compute the bounds on the candidate leaving variables
        candidates = (
            [
                (i, (-1 * self.dictionary[0][i].mag) / self.dictionary[enteringNode.row][i])
                for i in range(1, len(self.dictionary[0]))
                if self.dictionary[0][i].mag <= 0
                and self.dictionary[enteringNode.row][i] > 0
            ]
        )
        minimum = min(pair[1] for pair in candidates)
        print(minimum)
        candidates = [pair for pair in candidates if pair[1] == minimum]
        if len(candidates) == 1:
            return self.dictionary[0][candidates[0][0]]
        elif len(candidates > 1):
            candidates = [self.dictionary[0][candidate[0]] for candidate in candidates]
            return min(candidates)
        return

    def primalPivot(self):
        entering = self.chooseEnteringPrimal()
        print("Entering: " + str(entering))
        leaving = self.chooseLeavingPrimal(entering)
        print("Leaving: " + str(leaving))
        # solve leaving var row for entering var
        leaving_row = self.dictionary[leaving.row]
        leaving_coeff = leaving_row[entering.col] * -1
        print("leaving coeff: " + str(leaving_coeff))
        self.printDictionary()
        leaving_row[entering.col] = float(-1)
        self.printDictionary()

        print("leaving coeff: " + str(leaving_coeff))
        # for i in range(1, len(leaving_row)):
            # leaving_row[i] = leaving_row[i] / leaving_coeff
        leaving_row = [val/leaving_coeff for val in leaving_row]
        print(leaving_row)
        self.dictionary[leaving.row] = leaving_row
        self.printDictionary()
        return

    def dualPivot(self):
        entering = chooseEnteringDual()
        leaving = chooseLeavingDual()
        return

    def generateAuxMatrix(self):
        return

    def isPrimalFeasible(self):
        neg_basic_vals = [i for i in self.getBasicVarVals() if i < 0]
        return len(neg_basic_vals) == 0

    def isDualFeasible(self):
        pos_nonbasic_vals = [i for i in self.getNonBasicVarVals() if i >= 0]
        return len(pos_nonbasic_vals) == 0

    def isOptimal(self):
        return self.isPrimalFeasible() and self.isDualFeasible()

    def isUnbounded(self):
        return

    def solve(self):
        if self.isOptimal():
            print("optimal")
            print(self.objective_val)
            for entry in self.getOptVarVals():
                print("{:.7g} ".format(entry), end="")
        elif self.isPrimalFeasible():
            print("primal feasible")
            self.primalPivot()
        elif self.isDualFeasible():
            print("dual feasible")

        # if (initially_primal_feasible):
        #     print("INITIALLY PRIMAL FEASIBLE")
        # elif (initially_dual_feasible):
        #     print("INITIALLY DUAL FEASIBLE")
        # else:
        #     print("man fuck I don't wanna solve this")
        return

    def printMatrix(self):
        for row in self.matrix:
            for entry in row:
                print("{:^13.7g} ".format(entry), end="")
            print()

    def printDictionary(self):
        print("{:^13} ".format(" "), end="")
        print("{:^13} ".format(" "), end="")
        for i in range(1, len(self.dictionary[0])):
            print("{:^13} ".format(self.dictionary[0][i].number), end="")
        print()
        print("{:^13} ".format(" "), end="")
        print("{:^13.7g} ".format(self.dictionary[0][0]), end="") # objective val
        for i in range(1, len(self.dictionary[0])):
            print("{:^13.7g} ".format(self.dictionary[0][i].mag), end="")
        print()
        for i in range(1,len(self.dictionary)):
            print("{:^13} ".format(self.dictionary[i][0].number), end="")
            print("{:^13.7g} ".format(self.dictionary[i][0].mag), end="")
            for j in range(1,len(self.dictionary[i])):
                print("{:^13.7g} ".format(self.dictionary[i][j]), end="")
            print()

def printInput(input):
    for row in input:
        for entry in row:
            print("{:^13.7g} ".format(entry), end="")
        print()

def parseInput():
    input = ""
    if len(sys.argv) == 1:
        input = sys.stdin.readlines()

    elif len(sys.argv) == 2:
        fileName = sys.argv[1]
        with open(fileName, 'r') as fp:
            input = fp.readlines()

    # strip out lines that contain no numbers
    input = [line for line in input if bool(re.findall(r'\d+', line))]
    # extract a list of lists of coefficients
    input = [re.findall(r'-?\d+\.?\d*', line) for line in input]
    # cast string values to float
    input = [[float(i) for i in line] for line in input]
    # add objective value of zero
    input[0].insert(0, 0)
    # create matrix formatted as dictionary for the encoded LP
    matrix = [input[0]]
    # move last column to front and negate basic coefficients
    for i in range(1, len(input)):
        new_basic_row = [input[i][-1]] + input[i][0:-1]
        for j in range(1, len(new_basic_row)):
            new_basic_row[j] *= -1
        matrix.append(new_basic_row)

    return matrix

def main():
    A = LP(parseInput())
    A.printMatrix()
    print()
    A.printDictionary()
    print("solving")
    A.solve()
    # print("\nmatrix: {}".format(A.matrix))
    # print("num_opt_vars: {}".format(A.num_opt_vars))
    # print("\nobjective_val: {}".format(A.objective_val))
    # print("\nobjective_row: {}".format(A.objective_row))
    # print("\nbasis: {}".format(A.basis))
    # print("\nopt_var_indices: {}".format(A.opt_var_indices))
    # print("\nopt var vals: {}".format(A.getOptVarVals()))
    # print("\nslack_var_indices: {}".format(A.slack_var_indices))
    # print("\nslack var vals: {}".format(A.getSlackVarVals()))
    return

if __name__ == "__main__":
    main()

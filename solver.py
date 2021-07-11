# Richard Cruikshank V00844041

# your program must
# function correctly with an LP provided via standard input and generate its output to standard
# output, with no command line parameters required for basic operation

import sys
import re

class LP:
    def __init__(self, matrix):
        self.matrix = matrix
        self.num_opt_vars = len(matrix[0]) - 1
        self.objective_val = matrix[0][0]
        self.objective_row = matrix[0]
        self.basis = matrix[1:]
        self.opt_var_indices = [(0,y) for y in range(1, len(matrix[0]))]

    def getOptVarVals(self):
        return [self.matrix[x][y] for x,y in self.opt_var_indices]

    def primalPivot(self):
        return

    def dualPivot(self):
        return

    def generateAuxMatrix(self):
        return

    def isFeasible(self):
        return

    def isOptimal(self):
        return

    def isUnbounded(self):
        return

def isInitiallyFeasible(lp):
    return

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
    input = [re.findall(r'\d+\.?\d*', line) for line in input]

    return input

def main():
    A = LP(parseInput())
    print("matrix: {}".format(A.matrix))
    print("\nnum_opt_vars: {}".format(A.num_opt_vars))
    print("\nobjective_val: {}".format(A.objective_val))
    print("\nobjective_row: {}".format(A.objective_row))
    print("\nbasis: {}".format(A.basis))
    print("\nopt_var_indices: {}".format(A.opt_var_indices))
    print("\nopt var vals: {}".format(A.getOptVarVals()))
    return

if __name__ == "__main__":
    main()

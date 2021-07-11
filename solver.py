# Richard Cruikshank V00844041

# your program must
# function correctly with an LP provided via standard input and generate its output to standard
# output, with no command line parameters required for basic operation

import sys
import re

class LP:
    def __init__(self, matrix):
        self.matrix = matrix
        self.num_opt_vars = len(self.matrix[0]) - 1
        self.num_constraints = len(self.matrix) - 1
        self.objective_val = self.matrix[0][0]
        self.objective_row = self.matrix[0]
        self.basis = self.matrix[1:]
        self.opt_var_indices = [(0,y) for y in range(1, len(self.matrix[0]))]
        self.slack_var_indices = [(x,0) for x in range(1,len(self.matrix))]
        self.nonbasic_var_indices = [(0,y) for y in range(1, len(self.matrix[0]))]
        self.basic_var_indices = [(x,0) for x in range(1,len(self.matrix))]

    def printMatrix(self):
        for row in self.matrix:
            for entry in row:
                print("{:^13.7g} ".format(entry), end="")
            print()

    def getOptVarVals(self):
        return [self.matrix[x][y] for x,y in self.opt_var_indices]

    def getSlackVarVals(self):
        return [self.matrix[x][y] for x,y in self.slack_var_indices]

    def getNonBasicVarVals(self):
        return [self.matrix[x][y] for x,y in self.nonbasic_var_indices]

    def getBasicVarVals(self):
        return [self.matrix[x][y] for x,y in self.basic_var_indices]

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

    def chooseEnteringPrimal(self):
        return

    def chooseEnteringDual(self):
        return

    def chooseLeavingPrimal(self):
        return

    def chooseLeavingDual(self):
        return

    def solve(self):
        # initial feasibility
        # pos_basic_vals = [x for x in self.getBasicVarVals() if x > 0]
        neg_basic_vals = [x for x in self.getBasicVarVals() if x < 0]
        pos_nonbasic_vals = [x for x in self.getNonBasicVarVals() if x > 0]
        # neg_nonbasic_vals = [x for x in self.getNonBasicVarVals() if x < 0]

        initially_primal_feasible = (
            len(neg_basic_vals) == 0 and
            len(pos_nonbasic_vals) > 0
        )

        initially_dual_feasible = (
            len(pos_nonbasic_vals) == 0 and
            len(neg_basic_vals) > 0
        )

        if (initially_primal_feasible):
            print("INITIALLY PRIMAL FEASIBLE")
        elif (initially_dual_feasible):
            print("INITIALLY DUAL FEASIBLE")
        else
            print("man fuck I don't wanna solve this")
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
    input = [re.findall(r'-?\d+\.?\d*', line) for line in input]
    # cast string values to float
    input = [[float(x) for x in line] for line in input]

    return input

def main():
    A = LP(parseInput())
    A.printMatrix()
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

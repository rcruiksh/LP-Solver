# Richard Cruikshank V00844041

# your program must
# function correctly with an LP provided via standard input and generate its output to standard
# output, with no command line parameters required for basic operation

import sys
import re

class Node:
    def __init__(self, row, col, mag, number, dual_number):
        self.row = row
        self.col = col
        self.mag = mag
        self.number = number
        self.dual_number = dual_number

    def __str__(self):
        return str(self.number) + ":" + str(self.mag)

    def __repr__(self):
        return str(self.number) + ":" + str(self.mag)

    def __lt__(self, other):
        return self.number < other.number

    def __add__(self, other):
        if (isinstance(other, Node)):
            self.mag += other.mag
        else:
            self.mag += other
        return self

    def __sub__(self, other):
        if (isinstance(other, Node)):
            self.mag -= other.mag
        else:
            self.mag -= other
        return self

    def __mul__(self, other):
        if (isinstance(other, Node)):
            self.mag *= other.mag
        else:
            self.mag *= other
        return self

    def __truediv__(self, other):
        if (isinstance(other, Node)):
            self.mag /= other.mag
        else:
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
        self.num_vars = self.num_opt_vars + self.num_constraints
        self.num_rows = len(self.matrix)
        self.num_cols = len(self.matrix[0])

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
                    self.dictionary[row][col] = Node(row, col, self.matrix[row][col], col, self.num_constraints+col)
                elif row > 0 and col == 0:
                    self.dictionary[row][col] = Node(row, col, self.matrix[row][col], self.num_opt_vars+row, row)
                else:
                    self.dictionary[row][col] = Node(row, col, self.matrix[row][col], float('inf'), float('inf'))

    def getObjectiveVal(self):
        return self.dictionary[0][0].mag

    def getOptVarVals(self):
        opt_vars = []
        for row in self.dictionary:
            opt_vars += [node for node in row if node.number <= self.num_opt_vars and node.number > 0]
        opt_vars.sort(key=lambda var: var.number)
        return [0 if var.isNonbasic() else var.mag for var in opt_vars]

    def getNonBasicVarVals(self):
        return [self.dictionary[row][col].mag for row,col in self.nonbasic_var_indices]

    def getBasicVarVals(self):
        return [self.dictionary[row][col].mag for row,col in self.basic_var_indices]

    def getNonBasicVars(self):
        return [self.dictionary[row][col] for row,col in self.nonbasic_var_indices]

    def getBasicVars(self):
        return [self.dictionary[row][col] for row,col in self.basic_var_indices]

    def chooseEnteringPrimal(self):
        # get lowest numbered nonbasic primal candidate
        candidates = [node for node in self.dictionary[0][1:] if node.mag > 0]
        if len(candidates) == 0:
            candidates = [node for node in self.dictionary[0][1:] if node.mag >= 0]
        #     print("RETURNING NONE")
        #     return None
        # else:
        print("ENTERING CANDIDATES: ", candidates)
        candidate = min(candidates)
        # print("Entering primal: " + str(candidate))
        return candidate

    def chooseEnteringDual(self):
        # get lowest numbered basic dual candidate
        candidates = [node for node in [row[0] for row in self.dictionary[1:]] if node.mag < 0]
        print("DUAL CANDIDATES: ", candidates)
        if len(candidates) == 0:
            candidates = [node for node in [row[0] for row in self.dictionary[1:]] if node.mag <= 0]
        else:
            candidate = min(candidates)
            # print("Entering dual: " + str(candidate))
            return candidate

    def chooseLeavingPrimal(self, enteringNode):

        # candidates = (
        #     [
        #         (self.dictionary[i][0], self.dictionary[i][0].mag / (-1 * self.dictionary[i][enteringNode.col].mag))
        #         for i in range(1, len(self.dictionary))
        #         if self.dictionary[i][0].mag > 0
        #         and self.dictionary[i][enteringNode.col].mag < 0
        #     ]
        # )

        # compute the bounds on the candidate leaving variables
        candidates = (
            [
                (i, self.dictionary[i][0].mag / (-1 * self.dictionary[i][enteringNode.col].mag))
                for i in range(1, len(self.dictionary))
                if self.dictionary[i][0].mag >= 0
                and self.dictionary[i][enteringNode.col].mag < 0
            ]
        )
        if len(candidates) == 0:
            # print("LENGTH ZERO")
            candidates = (
                [
                    (i, self.dictionary[i][0].mag / (-1 * self.dictionary[i][enteringNode.col].mag))
                    for i in range(1, len(self.dictionary))
                    if self.dictionary[i][0].mag >= 0
                    and self.dictionary[i][enteringNode.col].mag < 0
                ]
            )
        print("CANDIDATES: ", candidates)
        minimum = min(pair[1] for pair in candidates)
        # print("minimum: ", minimum)
        candidates = [pair for pair in candidates if pair[1] == minimum]
        # print("CANDIDATES2: ", candidates)
        print("LEAVING CANDIDATES: ", candidates)
        if len(candidates) == 1:
            # print("len 1: ", self.dictionary[candidates[0][0]][0])
            return self.dictionary[candidates[0][0]][0]
        elif len(candidates) > 1:
            candidates = [self.dictionary[candidate[0]][0] for candidate in candidates]
            candidates.sort()
            # print(candidates)
            # print("len > 1: ", candidates[0])
            return candidates[0]
        return

    def chooseLeavingDual(self, enteringNode):
        # compute the bounds on the candidate leaving variables
        candidates = (
            [
                (i, (-1 * self.dictionary[0][i].mag) / self.dictionary[enteringNode.row][i].mag)
                for i in range(1, len(self.dictionary[0]))
                if self.dictionary[0][i].mag <= 0
                and self.dictionary[enteringNode.row][i].mag > 0
            ]
        )
        minimum = min(pair[1] for pair in candidates)
        print(minimum)
        candidates = [pair for pair in candidates if pair[1] == minimum]
        if len(candidates) == 1:
            return self.dictionary[0][candidates[0][0]]
        elif len(candidates) > 1:
            candidates = [self.dictionary[0][candidate[0]] for candidate in candidates]
            return min(candidates)
        return

    def primalPivot(self):
        entering = self.chooseEnteringPrimal()
        print("Entering: " + str(entering))
        if (self.isPrimalUnbounded(entering)):
            print("unbounded")
            return "unbounded"
        leaving = self.chooseLeavingPrimal(entering)
        print("Leaving: " + str(leaving))

        entering_number = entering.number
        leaving_number = leaving.number
        entering_dual_number = entering.dual_number
        leaving_dual_number = leaving.dual_number
        # solve leaving var row for entering var
        leaving_row = self.dictionary[leaving.row]
        leaving_coeff = leaving_row[entering.col] * -1
        leaving_row[entering.col] = Node(leaving.row, entering.col, -1, float('inf'), float('inf'))
        leaving_row = [val/leaving_coeff for val in leaving_row]
        self.dictionary[leaving.row] = leaving_row

        for row in range(len(self.dictionary)):
            if row != leaving.row:
                coeff = self.dictionary[row][entering.col].mag
                expansion = [coeff * val.mag for val in leaving_row]
                new_row = []
                for col in range(len(self.dictionary[row])):
                    if col == entering.col:
                        new_row.append(Node(row, col, expansion[col], self.dictionary[row][col].number, self.dictionary[row][col].dual_number))
                    else:
                        new_row.append(self.dictionary[row][col] + expansion[col])
                self.dictionary[row] = new_row
        self.dictionary[entering.row][entering.col].number = leaving_number
        self.dictionary[leaving.row][leaving.col].number = entering_number
        self.dictionary[entering.row][entering.col].dual_number = leaving_dual_number
        self.dictionary[leaving.row][leaving.col].dual_number = entering_dual_number
        # self.printDictionary()
        return ""

    def dualPivot(self):
        entering = self.chooseEnteringDual()
        print("Entering: " + str(entering))
        if (self.isPrimalUnbounded(entering)):
            print("unbounded")
            return "unbounded"
        leaving = self.chooseLeavingDual(entering)
        print("Leaving: " + str(leaving))

        entering_number = entering.number
        leaving_number = leaving.number
        entering_dual_number = entering.dual_number
        leaving_dual_number = leaving.dual_number
        # solve leaving var row for entering var
        leaving_col = [row[leaving.col] for row in self.dictionary]
        leaving_coeff = leaving_col[entering.row]
        # print("leaving coeff: " + str(leaving_coeff))
        # self.printDictionary()
        leaving_col[entering.row] = Node(leaving.col, entering.row, 1, float('inf'), float('inf'))
        # self.printDictionary()

        # print("leaving coeff: " + str(leaving_coeff))
        # for i in range(1, len(leaving_row)):
            # leaving_row[i] = leaving_row[i] / leaving_coeff
        leaving_col = [val/leaving_coeff for val in leaving_col]
        # print("LEAVING ROW")
        # print(leaving_row)
        for row in range(len(self.dictionary)):
            self.dictionary[row][leaving.col] = leaving_col[row]
        # self.printDictionary()
        # objective row:
        # coeff = self.dictionary[row][entering.col].mag
        # expansion = [coeff * val.mag for val in leaving_row]

        for col in range(self.num_cols):
            if col != leaving.col:
                coeff = self.dictionary[entering.row][col].mag * -1
                expansion = [coeff * val.mag for val in leaving_col]

                new_col = []
                for row in range(self.num_rows):
                    if row == entering.row:
                        new_col.append(Node(row, col, expansion[row], self.dictionary[row][col].number, self.dictionary[row][col].dual_number))
                    else:
                        new_col.append(self.dictionary[row][col] + expansion[row])
                for row in range(self.num_rows):
                    self.dictionary[row][col] = new_col[row]

        self.dictionary[entering.row][entering.col].number = leaving_number
        self.dictionary[leaving.row][leaving.col].number = entering_number
        self.dictionary[entering.row][entering.col].dual_number = leaving_dual_number
        self.dictionary[leaving.row][leaving.col].dual_number = entering_dual_number
        # self.printDictionary()
        return ""

    def generateAuxMatrix(self):
        return

    def isPrimalFeasible(self):
        neg_basic_vals = [i for i in self.getBasicVarVals() if i < 0]
        # print("PRIMAL_VARS: ", neg_basic_vals)
        return len(neg_basic_vals) == 0

    def isDualFeasible(self):
        pos_nonbasic_vals = [i for i in self.getNonBasicVarVals() if i > 0]
        # print("DUAL_VARS: ", pos_nonbasic_vals)
        return len(pos_nonbasic_vals) == 0

    def isOptimal(self):
        # print("primal feasible: ", self.isPrimalFeasible())
        # print("dual feasible: ", self.isDualFeasible())
        return self.isPrimalFeasible() and self.isDualFeasible()

    def isPrimalUnbounded(self, entering):
        # one or moreone or more possible entering variables has
        # no upper bound (that is, if the coefficient for that variable
        # in every basis row is positive or zero)
        leaving_coeffs = [row[entering.col] for row in self.dictionary[1:] if row[entering.col].mag < 0]
        return len(leaving_coeffs) == 0

    def isDualUnbounded(self):
        leaving_coeffs = [col for col in self.dictionary[entering.row] if col.mag > 0]
        return len(leaving_coeffs) == 0

    def isInfeasible(self):
        # run dual simplex, if unbounded then infeasible.
        # otherwise, use optimal basis with primal simplex to solve
        return

    def solve(self):
        res = ""
        if self.isOptimal():
            print("optimal")
            print("{:.7g} ".format(self.getObjectiveVal()))
            for entry in self.getOptVarVals():
                print("{:.7g} ".format(entry), end="")
            print()
        elif self.isPrimalFeasible():
            print("primal feasible")
            while not self.isOptimal() and res != "unbounded":
                res = self.primalPivot()
                print("OBJECTIVE: ", self.getObjectiveVal())
                # self.printDictionary()
                # print("nonbasic vars: ", self.getNonBasicVars())
                # print("basic vars: ", self.getBasicVars())
            # self.printDictionary()
        elif self.isDualFeasible():
            print("dual feasible")
            while not self.isOptimal() and res != "unbounded":
                res = self.dualPivot()
                print("OBJECTIVE: ", self.getObjectiveVal())
                # print("nonbasic vars: ", self.getNonBasicVars())
                # print("basic vars: ", self.getBasicVars())
        else: # initially infeasible
            print("Initially infeasible")
            og_objective = [Node(col.row, col.col, col.mag, col.number, col.dual_number) for col in self.dictionary[0]]
            print("OG", og_objective)

            for col in self.dictionary[0]:
                col.mag = 0

            print("OG", og_objective)
            self.printDictionary()

            print("dual_feas? ", self.isDualFeasible())
            print("primal_feas? ", self.isPrimalFeasible())

            while not self.isOptimal() and res != "unbounded":
                res = self.dualPivot()
                print("OBJECTIVE: ", self.getObjectiveVal())
                self.printDictionary()
            if res == "unbounded":
                res = "infeasible"
            else:
                print("OPTIMAL")
                self.printDictionary()
                new_objective = []
                # basic vars
                for node in og_objective:
                    for row in self.dictionary:
                        if row[0].number == node.number:
                            print("wawaweewa")
                            new_objective.append([Node(col.row, col.col, col.mag * node.mag, col.number, col.dual_number) for col in row])
                n_o = new_objective[0]
                print("new_objective:", new_objective)
                if len(new_objective) > 1:
                    print("new_objective:", new_objective[1:])
                    for row in new_objective[1:]:
                        for i in range(len(row)):
                            print("BRO")
                            n_o[i] += row[i]
                # nonbasic vars
                for node in og_objective:
                    if node.number in [col.number for col in self.dictionary[0][1:]]:
                        for col in range(1, len(self.dictionary[0])):
                            if node.number == self.dictionary[0][col].number:
                                n_o[col] += node

                print("n_o: ", n_o)
                self.dictionary[0] = n_o
                self.printDictionary()
                res = self.solve()
                self.printDictionary()

            print("RESULT: ", res)


        if self.isOptimal():
            print("optimal")
            print("{:.7g} ".format(self.getObjectiveVal()))
            for entry in self.getOptVarVals():
                print("{:.7g} ".format(entry), end="")
            print()

        # if (initially_primal_feasible):
        #     print("INITIALLY PRIMAL FEASIBLE")
        # elif (initially_dual_feasible):
        #     print("INITIALLY DUAL FEASIBLE")
        # else:
        #     print("man fuck I don't wanna solve this")
        return res

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
        print("{:^13.7g} ".format(self.dictionary[0][0].mag), end="") # objective val
        for i in range(1, len(self.dictionary[0])):
            print("{:^13.7g} ".format(self.dictionary[0][i].mag), end="")
        print()
        for i in range(1,len(self.dictionary)):
            print("{:^13} ".format(self.dictionary[i][0].number), end="")
            print("{:^13.7g} ".format(self.dictionary[i][0].mag), end="")
            for j in range(1,len(self.dictionary[i])):
                print("{:^13.7g} ".format(self.dictionary[i][j].mag), end="")
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
    # A.printMatrix()
    print()
    # A.printDictionary()
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

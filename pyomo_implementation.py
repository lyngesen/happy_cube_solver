# Private library imports
from classes import FigureSpace, Face, Brick
# Public library imports
import math
import matplotlib.pyplot as plt
import matplotlib
import pyomo.environ as pyomo
from pyomo.opt import SolverStatus, TerminationCondition
from itertools import product
import logging
import re



# The following lines use the logging module to ignore the wanings: 
# WARNING: Loading a SolverResults object with a warning status into
# model.name="unknown";
#   - termination condition: infeasible
#    - message from solver: <undefined>

# Define a custom filter class
class IgnoreWarningsFilter(logging.Filter):
    def __init__(self, pattern):
        self.pattern = re.compile(pattern)
        super().__init__()

    def filter(self, record):
        return not self.pattern.search(record.getMessage())

# Create a filter for the specific warning message
ignore_filter = IgnoreWarningsFilter(r"SolverResults object with a warning status into")
# Get the Pyomo logger and add the filter
pyomo_logger = logging.getLogger('pyomo.core')
pyomo_logger.addFilter(ignore_filter)


def build_happy_model(F: FigureSpace, B):

    def setup_A_matrix(A,B):
        C = set()
        A = dict()
        for f_id, f in enumerate(F.faces):
            f.cubegrid_coord_dir()
            for b_id, b in enumerate(B):
            # TODO: maybe create deepcopy <30-07-24> #
                for r_id, br in enumerate(b.or_list):
                    br_ir = set()
                    f_br_cubits = set()
                    for i in range(5):
                        for j in range(5):
                            if br.cubegrid[i][j] == 1:
                                # print(f"{i,j=}")
                                br_ir.add((i,j))
                                cubit_id = f.ij_to_cube_center[(i,j)]
                                C.add(cubit_id)
                                f_br_cubits.add(cubit_id)
                    A[(f_id, b_id, r_id)] = f_br_cubits

        return A, C


    A, C = setup_A_matrix(F, B)

    F_set = list(range(len(F.faces)))
    B_set = list(range(len(B)))
    R_set = list(range(8))
    C_set = list(range(len(C)))

    model = pyomo.ConcreteModel()
    # Define your sets
    model.F_set = pyomo.Set(initialize=F_set)
    model.B_set = pyomo.Set(initialize=B_set)
    model.R_set = pyomo.Set(initialize=R_set)
    model.C_set = pyomo.Set(initialize=C_set)

    # Create an intermediate set of valid combinations of f,b,r
    def fbr_rule(model):
        return [(f_id,b_id,r_id) for f_id in model.F_set for b_id in model.B_set for r_id in range(len(B[b_id].or_list))]

    valid_fbr = set(fbr_rule(model))
    
    model.fbr_set = pyomo.Set(within=model.F_set*model.B_set*model.R_set, initialize=fbr_rule)

    # Define continous variables
    # model.x = pyomo.Var(model.fbr_set, within=pyomo.NonNegativeReals, bounds= (0,1))
    # Define binary variables
    model.x = pyomo.Var(model.fbr_set, within=pyomo.Binary)


    # Define constraints
    model.cons = pyomo.ConstraintList()

    # add constraints
    for f in model.F_set:
        model.cons.add(sum(model.x[f,b,r] for b in model.B_set for r in model.R_set if (f,b,r) in A.keys()) == 1)

    # add constraints
    for b in model.B_set:
        model.cons.add(sum(model.x[f,b,r] for f in model.F_set for r in model.R_set if (f,b,r) in A.keys()) <= 1)

    for c_id, c in enumerate(C):
        model.cons.add(sum(model.x[f,b,r] for f,b,r in valid_fbr if c in A[(f,b,r)]) == 1)

    # Define objective
    def objective_rule(model):
        return 0
        

    model.obj = pyomo.Objective(rule=objective_rule, sense=pyomo.minimize)

    return model




def solve_model(model:pyomo.ConcreteModel(), solver_str = "cplex_direct"):
    assert solver_str in ["cbc", "cplex_direct", "plpk"]
    # Solve model
    solver = pyomo.SolverFactory(solver_str)
    # check if feasible
    result = solver.solve(model) # Solving a model instance - This line will throw an error which we ignore in the start of the file

    if result.solver.termination_condition == TerminationCondition.infeasible:
        return False
    else:
        return True


def retrieve_solution(model:pyomo.ConcreteModel, F: FigureSpace, B: Brick):
    for f,b,r in model.fbr_set:
        if math.isclose(pyomo.value(model.x[f,b,r]),1):
        # if not math.isclose(pyomo.value(model.x[f,b,r]),0):
        # if pyomo.value(model.x[f,b,r]) > 0:
            br = B[b].or_list[r]
            br.color = B[b].color
            F.faces[f].set_face(br)
    return F

def solve_happy_problem(F, B):

    if len(B) < len(F.faces):
        # print(f"not enough bricks {len(F.faces)}")
        return False

    model = build_happy_model(F,B)
    if not solve_model(model):
        return False 
    F = retrieve_solution(model, F,B)
    return F


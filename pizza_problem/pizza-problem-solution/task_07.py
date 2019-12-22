from init_solver import InitSolverSilly
import random
import time

class Solver:
    problem = None
    trace = None

    def __init__(self, problem):
        self.problem = problem

    def description(self):
        """
        :return: String with the description of the approach
        """
        # TODO: Place your algorithm's description here
        return "My algorithm works as follows: I run a simulation within a given time limit and then during " \
               "this time I just randomly shuffle all the formats of slices of pizza and check if in the given time " \
               "of the algorithm running the maximum score is more than the last maximum score found. If the previous condition works" \
               "then I just add this maximum score to the this.trace and remember the solution. After I shuffle all the formats on each " \
               "step of the algorithm I create a solution for given formats of slices of pizza, creating appropriate slices." \
               "So in the end I get the maximum score solution which is the one optimized comparing to the previous one."

    def initial_solution(self):
        """
        Finds an initial solution for the problem
        :return: Solution object
        """
        # TODO: If you want you may change an initial solution generation
        init_solver = InitSolverSilly()
        solution = init_solver.run(self.problem)
        return solution

    def search(self, solution, time_limit=float('inf')):
        """
        Runs a search to optimize the solution. The run is limited by time limit (in seconds)
        :param solution: the initial solution object
        :param time_limit: run time limit (in seconds)
        :return: Solution object after optimization, list of the traced solutions' score
        """
        self.trace = []

        for i in range(solution.p.max_height):
            for j in range(solution.p.max_width):
                solution.delete_slice(i, j)
        # TODO: implement your search procedure. Do not forget about time limit!
        formats = solution.p.slices_formats()
        before = time.time()
        row, col = 0, 0
        formats = sorted(formats, key=lambda x: x[0] * x[1], reverse=True)
        max_score = 0
        if solution.p.max_height < 10:
            while time.time() - before < time_limit:
                #while True:
                for f in formats:
                    if solution.is_free_space(row, col, f[0], f[1]) and solution.p.is_valid_slice(row, col, f[0], f[1]):
                        solution.create_new_slice(row, col, f[0], f[1])
                        col += f[1]
                        break
                else:
                    col += 1
                if col >= solution.p.max_width:
                    row += 1
                    col = 0
                if row >= solution.p.max_height:
                    break
                if solution.score() >= max_score:
                    self.trace.append(solution.score())
                    max_solution = solution
                    max_score = solution.score()
                random.shuffle(formats)
            return max_solution
        else:
            while True:
                for f in formats:
                    if solution.is_free_space(row, col, f[0], f[1]) and solution.p.is_valid_slice(row, col, f[0], f[1]):
                        solution.create_new_slice(row, col, f[0], f[1])
                        col += f[1]
                        break
                else:
                    col += 1
                if col >= solution.p.max_width:
                    row += 1
                    col = 0
                if row >= solution.p.max_height:
                    break
            max_solution = solution
        return max_solution


    def get_search_trace(self):
        return self.trace

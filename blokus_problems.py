import math

from board import Board
from search import SearchProblem, ucs
import util


class BlokusFillProblem(SearchProblem):
    """
    A one-player Blokus game as a search problem.
    This problem is implemented for you. You should NOT change it!
    """

    def __init__(self, board_w, board_h, piece_list, starting_point=(0, 0)):
        self.board = Board(board_w, board_h, 1, piece_list, starting_point)
        self.expanded = 0

    def get_start_state(self):
        """
        Returns the start state for the search problem
        """
        return self.board

    def is_goal_state(self, state):
        """
        state: Search state
        Returns True if and only if the state is a valid goal state
        """
        return not any(state.pieces[0])

    def get_successors(self, state):
        """
        state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        # Note that for the search problem, there is only one player - #0
        self.expanded = self.expanded + 1
        return [(state.do_move(0, move), move, 1) for move in state.get_legal_moves(0)]

    def get_cost_of_actions(self, actions):
        """
        actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        return len(actions)


#####################################################
# This portion is incomplete.  Time to write code!  #
#####################################################
class BlokusCornersProblem(SearchProblem):
    def __init__(self, board_w, board_h, piece_list, starting_point=(0, 0)):
        self.expanded = 0
        self.board = Board(board_w, board_h, 1, piece_list, starting_point)
        self.board_w = board_w
        self.board_h = board_h

    def get_start_state(self):
        """
        Returns the start state for the search problem
        """
        return self.board

    def is_goal_state(self, state):
        # return the corners are filled
        return (state.get_position(0, 0) != -1 and
                state.get_position(0, self.board_h - 1) != -1
                and state.get_position(self.board_w - 1, 0) != -1 and
                state.get_position(self.board_w - 1, self.board_h - 1) != -1)

    def get_successors(self, state):
        """
        state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        # Note that for the search problem, there is only one player - #0
        self.expanded = self.expanded + 1
        return [(state.do_move(0, move), move, move.piece.get_num_tiles()) for
                move in state.get_legal_moves(0)]

    def get_cost_of_actions(self, actions):
        """
        actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        # The cost of actions is the number of tiles placed on the board
        cost = 0
        for move in actions:
            cost += move.piece.get_num_tiles()
        return cost


def blokus_corners_heuristic(state, problem):
    """
    Your heuristic for the BlokusCornersProblem goes here.

    This heuristic must be consistent to ensure correctness.  First, try to come up
    with an admissible heuristic; almost all admissible heuristics will be consistent
    as well.

    If using A* ever finds a solution that is worse uniform cost search finds,
    your heuristic is *not* consistent, and probably not admissible!  On the other hand,
    inadmissible or inconsistent heuristics may find optimal solutions, so be careful.
    """
    "*** YOUR CODE HERE ***"
    occupied = []
    dist = 0
    targets = [(0, 0), (0, problem.board_h - 1), (problem.board_w - 1, 0), (problem.board_w - 1, problem.board_h - 1)]
    for i in range(problem.board_h):
        for j in range(problem.board_w):
            if state.get_position(i, j) != -1:
                occupied.append((j, i))
    for target in targets:
        dist += min([max(abs(target[0] - x), abs(target[1] - y)) for x, y in occupied])
    return abs(dist)


def blokus_corners_heuristic_2(state, problem):
    occupied = []
    dist = 0
    targets = [(0, 0), (0, problem.board_h - 1), (problem.board_w - 1, 0), (problem.board_w - 1, problem.board_h - 1)]
    for i in range(problem.board_h):
        for j in range(problem.board_w):
            if state.get_position(i, j) != -1:
                occupied.append((j, i))
    for target in targets:
        dist += min([max(abs(target[0] - x), abs(target[1] - y)) for x, y in occupied])
    return abs(dist)

class BlokusCoverProblem(SearchProblem):
    def __init__(self, board_w, board_h, piece_list, starting_point=(0, 0), targets=[(0, 0)]):
        self.targets = targets.copy()
        self.expanded = 0
        self.board = Board(board_w, board_h, 1, piece_list, starting_point)
        self.board_w = board_w
        self.board_h = board_h

    def get_start_state(self):
        """
        Returns the start state for the search problem
        """
        return self.board

    def is_goal_state(self, state):
        for target in self.targets:
            row, col = target
            if state.get_position(col, row) == -1:
                return False
        return True

    def get_successors(self, state):
        """
        state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        # Note that for the search problem, there is only one player - #0
        self.expanded = self.expanded + 1
        return [(state.do_move(0, move), move, move.piece.get_num_tiles()) for move in state.get_legal_moves(0)]

    def get_cost_of_actions(self, actions):
        """
        actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        "*** YOUR CODE HERE ***"
        cost = 0
        for move in actions:
            cost += move.piece.get_num_tiles()
        return cost


def blokus_cover_heuristic(state, problem):
    "*** YOUR CODE HERE ***"
    dist = 0
    occupied = []
    for i in range(problem.board_h):
        for j in range(problem.board_w):
            if state.get_position(i, j) != -1:
                occupied.append((j, i))
    for target in problem.targets:
        dist += min([max(abs(target[0] - x), abs(target[1] - y)) for x, y in occupied])
    return abs(dist)


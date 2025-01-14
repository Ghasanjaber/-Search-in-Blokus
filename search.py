"""
In search.py, you will implement generic search algorithms
"""

import util


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def get_start_state(self):
        """
        Returns the start state for the search problem
        """
        util.raiseNotDefined()

    def is_goal_state(self, state):
        """
        state: Search state

        Returns True if and only if the state is a valid goal state
        """
        util.raiseNotDefined()

    def get_successors(self, state):
        """
        state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        util.raiseNotDefined()

    def get_cost_of_actions(self, actions):
        """
        actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        util.raiseNotDefined()


def depth_first_search(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches
    the goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    return depth_first_search_helper(problem, problem.get_start_state(), [], set())


def depth_first_search_helper(problem, state, path, visited):
    if problem.is_goal_state(state):
        return path
    visited.add(state)
    for successor, action, stepCost in problem.get_successors(state):
        if successor not in visited:
            path.append(action)
            result = depth_first_search_helper(problem, successor, path, visited)
            if result:
                return result
            path.pop()
    return None


def breadth_first_search(problem):
    """
    Search the shallowest nodes in the search tree first.
    """
    "*** YOUR CODE HERE ***"

    return breath_first_search_helper(problem, problem.get_start_state(), [], set())


def breath_first_search_helper(problem, state, path, visited):
    queue = util.Queue()
    queue.push((state, path))
    visited.add(state)
    while not queue.isEmpty():
        state, path = queue.pop()
        if problem.is_goal_state(state):
            return path
        for successor, action, stepCost in problem.get_successors(state):
            if successor not in visited:
                queue.push((successor, path + [action]))
                visited.add(successor)
    return None


def uniform_cost_search(problem):
    """
    Search the node of least total cost first.
    """
    "*** YOUR CODE HERE ***"
    return uniform_cost_search_helper(problem, problem.get_start_state(), [], set(), {})


def uniform_cost_search_helper(problem, state, path, visited, path_state_dict):
    queue = util.PriorityQueue()
    queue.push(state, 0)
    path_state_dict.update({state: path})
    visited.add(state)
    while not queue.isEmpty():
        state = queue.pop()
        path = path_state_dict[state]
        if problem.is_goal_state(state):
            return path
        for successor, action, stepCost in problem.get_successors(state):
            if successor not in visited:
                queue.push(successor, problem.get_cost_of_actions(path + [action]))
                path_state_dict.update({successor: path + [action]})
                visited.add(successor)
    return None


def null_heuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def a_star_search(problem, heuristic=null_heuristic):
    """
    Search the node that has the lowest combined cost and heuristic first.
    """
    "*** YOUR CODE HERE ***"
    return a_star_search_helper(problem, problem.get_start_state(), [], set(), {}, heuristic)


def a_star_search_helper(problem, state, path, visited, path_state_dict, heuristic):
    queue = util.PriorityQueue()
    queue.push(state, 0)
    path_state_dict.update({state: path})
    visited.add(state)
    while not queue.isEmpty():
        state = queue.pop()
        path = path_state_dict[state]
        if problem.is_goal_state(state):
            return path
        for successor, action, stepCost in problem.get_successors(state):
            if successor not in visited:
                queue.push(successor, problem.get_cost_of_actions(path + [action]) + heuristic(successor, problem))
                path_state_dict.update({successor: path + [action]})
                visited.add(successor)
    return None

# Abbreviations
bfs = breadth_first_search
dfs = depth_first_search
astar = a_star_search
ucs = uniform_cost_search

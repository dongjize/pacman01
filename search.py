# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         get_actions: A list of get_actions to take

        This method returns the total cost of a particular sequence of get_actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]


def execute(problem, start, expand):
    """
    The generic search method executing dfs, bfs, ucs and A* search

    :param problem: the generic search problem
    :param start: the method handle for initializing the first node
    :param expand: the method handle for expanding the fringe
    :return: returns a list of get_actions to go when reaching the goal state
    """
    fringe = start()
    closed = set()
    while not fringe.isEmpty():
        node = fringe.pop()
        if problem.isGoalState(node.state):
            return get_actions(node)
        if node.state not in closed:
            closed.add(node.state)
            expand(node, fringe)


def get_actions(node):
    """
    Iteratively get the get_actions to reach the current node
    :param node: the current node
    :return: the action list to reach the current node
    """
    actions = []
    while node.prev:
        actions.insert(0, node.action)
        node = node.prev
    return actions


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of get_actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())

    - Start: (5, 5)
    - Is the start a goal? False
    - Start 's successors: [((5, 4), ' South ', 1), ((4, 5), ' West ', 1)]

    """

    """*** Q1 ***"""

    def start():
        node0 = Node(problem.getStartState(), None, 0, None)
        stack = util.Stack()
        stack.push(node0)
        return stack

    def expand(curr_node, stack):
        for s in problem.getSuccessors(curr_node.state):
            successor = Node(s[0], curr_node, s[2], s[1])
            stack.push(successor)

    return execute(problem, start, expand)


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""

    """*** Q2 ***"""

    def start():
        node0 = Node(problem.getStartState(), None, 0, None)
        queue = util.Queue()
        queue.push(node0)
        return queue

    def expand(curr_node, queue):
        for s in problem.getSuccessors(curr_node.state):
            successor = Node(s[0], curr_node, s[2], s[1])
            queue.push(successor)

    return execute(problem, start, expand)


def uniformCostSearch(problem):
    """Search the node of least total cost first."""

    """*** Q3 ***"""

    def start():
        node0 = Node(problem.getStartState(), None, 0, None)
        pq = util.PriorityQueue()
        pq.push(node0, node0.cost)
        return pq

    def expand(curr_node, pq):
        for s in problem.getSuccessors(curr_node.state):
            successor = Node(s[0], curr_node, s[2], s[1])
            actions = get_actions(successor)
            cost = problem.getCostOfActions(actions)
            pq.update(successor, cost)

    return execute(problem, start, expand)


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""

    """*** Q4 ***"""

    def start():
        node0 = Node(problem.getStartState(), None, 0, None)
        pq = util.PriorityQueue()
        pq.push(node0, 0)
        return pq

    def expand(curr_node, pq):
        for s in problem.getSuccessors(curr_node.state):
            successor = Node(s[0], curr_node, s[2], s[1])
            actions = get_actions(successor)
            g = problem.getCostOfActions(actions)  # the total cost of visited nodes
            h = heuristic(successor.state, problem)  # the heuristic of unvisited nodes
            pq.update(successor, g + h)

    return execute(problem, start, expand)


class Node:

    def __init__(self, state, prev, cost, action):
        """
        :param state: contains all necessary information of the node (e.g. coordinates, whether reaches the goal)
        :param prev: the previous node
        :param action: the required action to reach from the previous node
        :param cost: the cost for reaching from the previous node (always 1 in the project)
        """
        self.state = state
        self.prev = prev
        self.action = action
        self.cost = cost


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch

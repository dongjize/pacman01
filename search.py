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
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
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


class Node:
    def __init__(self, state, action, cost, prev):
        self.state = state
        self.action = action
        self.cost = cost
        self.prev = prev


def init_node(state):
    return Node(state, None, 0, None)


def make_successor_node(current_node, successor):
    return Node(successor[0], successor[1], successor[2], current_node)


def get_actions(node):
    actions = []
    while node.prev:
        actions.append(node.action)
        node = node.prev
    return actions[::-1]


def search(problem, init, expand):
    closed = set()
    opened = init()
    while not opened.isEmpty():
        node = opened.pop()
        if problem.isGoalState(node.state):
            return get_actions(node)
        if node.state not in closed:
            closed.add(node.state)
            expand(node, opened)
    return None


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())

    Start: (5, 5)
    Is the start a goal? False
    Start 's successors: [((5, 4), ' South ', 1), ((4, 5), ' West ', 1)]

    """

    def init():
        initial_node = Node(problem.getStartState(), None, 0, None)
        stack = util.Stack()
        stack.push(initial_node)
        return stack

    def expand(curr_node, pushed):
        for s in problem.getSuccessors(curr_node.state):
            pushed.push(make_successor_node(curr_node, s))

    return search(problem, init, expand)


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""

    def init():
        initial_node = Node(problem.getStartState(), None, 0, None)
        queue = util.Queue()
        queue.push(initial_node)
        return queue

    def expand(curr_node, pushed):
        for s in problem.getSuccessors(curr_node.state):
            pushed.push(make_successor_node(curr_node, s))

    return search(problem, init, expand)


def uniformCostSearch(problem):
    """Search the node of least total cost first."""

    def init():
        initial_node = init_node(problem.getStartState())
        pq = util.PriorityQueue()
        pq.push(initial_node, initial_node.cost)
        return pq

    def expand(curr_node, pq):
        for s in problem.getSuccessors(curr_node.state):
            node = make_successor_node(curr_node, s)
            cost = problem.getCostOfActions(get_actions(node))
            pq.update(node, cost)

    return search(problem, init, expand)


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""

    def init():
        initial_node = init_node(problem.getStartState())
        opened = util.PriorityQueue()
        opened.push(initial_node, 0)
        return opened

    def expand(curr_node, opened):
        for s in problem.getSuccessors(curr_node.state):
            node = make_successor_node(curr_node, s)
            g = problem.getCostOfActions(get_actions(node))
            h = heuristic(node.state, problem)
            opened.update(node, g + h)

    return search(problem, init, expand)


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch

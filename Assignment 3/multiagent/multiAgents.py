# multiAgents.py
# --------------
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


from numpy import Infinity
from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        return successorGameState.getScore()

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        
#forsøk 3
        numGhost = gameState.getNumAgents()-1
        
        # maxEval for pacman
        # agentNum = 0
        
        def maxEvaluation(gameState, depth, player = 0):
            """
            beregner beste evalueringen for pacman
            player/agentindex er satt til 0 for default, men er egentlig unødvendig parameter
            omg ingenting skal endres

            Args:
                gameState (state): state for the game
                depth (int): depth of the game, updates only on pacman move
                player (int, optional): agentindex. Defaults to 0.

            Returns:
                int: the highest evaluation
            """
            newDepth = depth + 1
            if gameState.isWin() or gameState.isLose() or newDepth == self.depth:
                return self.evaluationFunction(gameState)
            maxEval = -float('inf')
            for action in gameState.getLegalActions():
                eval = gameState.generateSuccessor(player, action)
                maxEval = max(maxEval, minEvaluation(eval, newDepth, player + 1))
            return maxEval
        
        def minEvaluation(gameState, depth, player):
            """
            eval function for ghosts

            Args:
                gameState (state): state of the game
                depth (int): depth of the game, does not update for ghost moves
                player (int): agent index, incremented by one unless its the last ghost 

            Returns:
                int: minimum evaluation for the given state
            """
            minEval = float('inf')
            if gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState)
            for action in gameState.getLegalActions(player):
                eval = gameState.generateSuccessor(player, action)
                if player == numGhost:
                    minEval = min(minEval, maxEvaluation(eval, depth, 0))
                else:
                    minEval = min(minEval, minEvaluation(eval, depth, player+1))
            return minEval
        
        bestEval = -float('inf')
        move = Directions.STOP
        for action in gameState.getLegalActions():
            eval = minEvaluation(gameState.generateSuccessor(0,action), 0, 1)
            if eval > bestEval:
                move = action
                bestEval = eval
        return move
                                  
        
    
    
#forsøk 2
    # må oversette pseudokoden til å gjelde for n ulike spillere
    # pacman = 0, ghosts = n > 0
    # max for pacman, min for ghost
    # må ta vare på både move og verdi, men kun returnere move
    # mye inspirasjon og pseudokode fra Sebastian Lague på youtube
    
    
        #return self.minimax(gameState,0,0)[1]
    
    # def minimax(self, state, depth, player):
    #     if state.isWin() or state.isLose() or depth == self.depth:
    #         None, self.evaluationFunction(state)
        
    #     if player == 0:
    #         # max for pacman
    #         maxEval = -9999999
    #         maxMove = None
    #         for action in state.getLegalActions(player):
    #             eval = self.minimax(state.generateSuccessor(player, action),depth+1, player+1)[0]
    #             if eval > maxEval:
    #                 maxEval = eval
    #                 maxMove = action
    #         return maxEval, maxMove
        
    #     else:
    #         minEval = 999999999
    #         minMove = Directions.STOP
    #         for action in state.getLegalActions(player):
    #             if player == state.getNumAgents():
    #                 player = 0
    #             else:
    #                 player += 1
    #             eval = self.minimax(state.generateSuccessor(player, action),depth, player)[0]
    #             if eval < minEval:
    #                 minEval = eval
    #                 minMove = action
    #         return minEval, minMove
                    


# forsøk 1

    # def max_eval(self, state, depth):

    #     maxEval = None, -float('inf')
    #     for action in state.getLegalActions():
    #         next_state = state.generateSuccessor(0,action)
            

    # def minimax(self, state, depth):
    #     if state.isLose() or state.isWin():
    #         return self.evaluationFunction(), None
    #     numAgents = state.getNumAgents()
    #     if player == numAgents-1:
    #         player = 0
    #     if player == 0:        
    #         maxEval = -float('inf'), None
    #         depth =- 1
    #         for action in state.getLegalActions(player):
    #             eval = self.minimax(action,depth, player+1)
    #             maxEval = max(maxEval[0], eval[0])
    #         return maxEval
        
    #     else:
    #         minEval = +float('inf'), None
    #         for action in state.getLegalActions(player):
    #             eval = self.minimax(action, depth, player+1)
    #             minEval = min(minEval[0], eval[0])
    #         return minEval
            
""" def max_value(game,state, depth):
    if state.isLose() or state.isWin() or depth == 0:
        return game.scoreEvaluationFunction(state), None
    v = -float('inf')
    action = Directions.STOP
    for action in game.getLegalActions(0):
        v2 = min_value(game, game.generateSuccessor(0, action), depth-1)
        if v2 > v:
            v = v2
            move = action
    return v, move

def min_value(game,state,depth):
    if game.isLose() or game.isWin() or depth == 0:
        return game.scoreEvaluationFunction(state), None
    v, move = -Infinity
    for action in game.getLegalActions(0):
        v2, a2 = max_value(game, game.generateSuccessor(0, action), depth-1)
        if v2 > v:
            v, move = v2, action
    return v, move
 """
    
        
                    
class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        
        numGhost = gameState.getNumAgents()-1
        
        # maxEval for pacman
        # agentNum = 0
        
        def maxEvaluation(gameState, depth, player, alpha, beta):
            """
            beregner beste evalueringen for pacman.
            player/agentindex er satt til 0 for default, men er egentlig unødvendig parameter
            omg ingenting skal endres.

            Args:
                gameState (state): state for the game.
                depth (int): depth of the game, updates only on pacman move.
                player (int): agentindex.
                alpha, beta (int): pruning values.

            Returns:
                int: the highest evaluation.
            """
            newDepth = depth + 1
            if gameState.isWin() or gameState.isLose() or newDepth == self.depth:
                return self.evaluationFunction(gameState)
            maxEval = -float('inf')
            for action in gameState.getLegalActions():
                eval = gameState.generateSuccessor(player, action)
                maxEval = max(maxEval, minEvaluation(eval, newDepth, player + 1, alpha, beta))
                alpha = max (alpha,maxEval)
                if beta < alpha:
                    break
            return maxEval
        
        def minEvaluation(gameState, depth, player, alpha, beta):
            """
            eval function for ghosts.

            Args:
                gameState (state): state of the game.
                depth (int): depth of the game, does not update for ghost moves.
                player (int): agent index, incremented by one unless its the last ghost .

            Returns:
                int: minimum evaluation for the given state.
            """
            minEval = float('inf')
            if gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState)
            for action in gameState.getLegalActions(player):
                eval = gameState.generateSuccessor(player, action)
                if player == numGhost:
                    minEval = min(minEval, maxEvaluation(eval, depth, 0, alpha, beta))
                else:
                    minEval = min(minEval, minEvaluation(eval, depth, player+1, alpha, beta))
                beta = min(beta, minEval)
                if beta < alpha:
                    break
            return minEval
        
        bestEval = -float('inf')
        move = Directions.STOP
        alpha = -float('inf')
        beta = float('inf')
        for action in gameState.getLegalActions():
            eval = minEvaluation(gameState.generateSuccessor(0,action), 0, 1, alpha, beta)
            if eval > bestEval:
                move = action
                bestEval = eval
            if eval > beta:
                return move
            alpha = max(alpha, eval)
        return move

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

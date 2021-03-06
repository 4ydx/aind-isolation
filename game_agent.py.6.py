"""This file contains all the classes you must complete for this project.

You can use the test cases in agent_test.py to help during development, and
augment the test suite with your own test cases to further test your code.

You must test your agent's strength against a set of agents with known
relative strength using tournament.py and include the results in your report.
"""
import random


class Timeout(Exception):
    """Subclass base exception for code clarity."""
    pass

def board_center(game):
    """ Find the center of the board.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    Returns
    -------
    (int, int)
        Coordinates of the center of the board
    """
    return (game.height//2, game.width//2)

def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """

    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("+inf")

    """ not available """
    """ favor moves where the player has more moves than the opponent
    return float(len(game.get_legal_moves(player))-len(game.get_legal_moves(game.get_opponent(player))))
    """

    """ 1 """
    """ favor moves where the player encroaches on the opponents moves
    favored = float(0)
    playerMoves = game.get_legal_moves(player)
    opponentMoves = game.get_legal_moves(game.get_opponent(player))
    for o in opponentMoves:
        for p in playerMoves:
            if o == p:
                favored += 1
            else:
                favored -= 1
    return favored
    """

    """ 2 """
    """ favor moves where the player encroaches on the opponents final move 
        otherwise follow the opponent around the board
    playerMoves = game.get_legal_moves(player)
    opponentMoves = game.get_legal_moves(game.get_opponent(player))
    if len(opponentMoves) == 1:
        for o in opponentMoves:
            for p in playerMoves:
                if o == p:
                    return float("+inf")

    playerAt = game.get_player_location(player)
    opponentAt = game.get_player_location(game.get_opponent(player))

    xDiff = playerAt[0] - opponentAt[0]
    yDiff = playerAt[1] - opponentAt[1]
    denom = float(xDiff*xDiff + yDiff*yDiff)
    if denom == 0:
        return float("+inf")
    return float(1.0/denom)
    """

    """ 3 """
    """ favor moves where the player encroaches on the opponents final move 
        moves that encroach on the other players moves are favored
        otherwise follow the opponent around the board waiting to pounce
    playerMoves = game.get_legal_moves(player)
    opponentMoves = game.get_legal_moves(game.get_opponent(player))
    if len(opponentMoves) == 1:
        for o in opponentMoves:
            for p in playerMoves:
                if o == p:
                    return float("+inf")

    matchedMoves = 0
    centerAt = board_center(game)
    for o in opponentMoves:
        for p in playerMoves:
            if o == p:
                matchedMoves += 10
    if matchedMoves > 0:
        return float(matchedMoves)

    playerAt = game.get_player_location(player)
    opponentAt = game.get_player_location(game.get_opponent(player))

    xDiff = playerAt[0] - opponentAt[0]
    yDiff = playerAt[1] - opponentAt[1]
    denom = float(xDiff*xDiff + yDiff*yDiff)
    if denom == 0:
        return float("+inf")
    return float(1.0/denom)
    """

    """ 4 """
    """ favor moves that position the player closer to the opponent
    playerAt = game.get_player_location(player)
    opponentAt = game.get_player_location(game.get_opponent(player))

    xDiff = playerAt[0] - opponentAt[0]
    yDiff = playerAt[1] - opponentAt[1]
    denom = float(xDiff*xDiff + yDiff*yDiff)
    if denom == 0:
        return float("+inf")
    return float(1.0/denom)
    """

    """ 5 """
    """ favor moves that position the player closer to the center of the board
    centerAt = board_center(game)
    playerAt = game.get_player_location(player)

    xDiff = playerAt[0] - centerAt[0]
    yDiff = playerAt[1] - centerAt[1]
    denom = float(xDiff*xDiff + yDiff*yDiff)
    if denom == 0:
        return float("+inf")
    return float(1.0/denom)
    """

    """ 6 """
    """ favor moves that position the player closer to the center of the board until the game board >= %60 empty
        if a set of moves can pinch an opponent, weight it heavily
        otherwise, simply move with most available
    """
    blanks = game.get_blank_spaces()
    if len(blanks) > (3*game.width*game.height/5):
        centerAt = board_center(game)
        playerAt = game.get_player_location(player)
        xDiff = playerAt[0] - centerAt[0]
        yDiff = playerAt[1] - centerAt[1]
        denom = float(xDiff*xDiff + yDiff*yDiff)
        if denom == 0:
            return float("+inf")
        return float(1.0/denom)

    playerMoves = game.get_legal_moves(player)
    opponentMoves = game.get_legal_moves(game.get_opponent(player))
    if len(opponentMoves) == 1:
        for o in opponentMoves:
            for p in playerMoves:
                if o == p:
                    return float("+inf")

    return float(len(game.get_legal_moves(player))-len(game.get_legal_moves(game.get_opponent(player))))

class CustomPlayer:
    """Game-playing agent that chooses a move using your evaluation function
    and a depth-limited minimax algorithm with alpha-beta pruning. You must
    finish and test this player to make sure it properly uses minimax and
    alpha-beta to return a good move before the search time limit expires.

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    iterative : boolean (optional)
        Flag indicating whether to perform fixed-depth search (False) or
        iterative deepening search (True).

    method : {'minimax', 'alphabeta'} (optional)
        The name of the search method to use in get_move().

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """

    def __init__(self, search_depth=3, score_fn=custom_score,
                 iterative=True, method='minimax', timeout=10.):
        self.search_depth = search_depth
        self.iterative = iterative
        self.score = score_fn
        self.method = method
        self.time_left = None
        self.TIMER_THRESHOLD = timeout

    def get_move(self, game, legal_moves, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        This function must perform iterative deepening if self.iterative=True,
        and it must use the search method (minimax or alphabeta) corresponding
        to the self.method value.

        **********************************************************************
        NOTE: If time_left < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        legal_moves : list<(int, int)>
            A list containing legal moves. Moves are encoded as tuples of pairs
            of ints defining the next (row, col) for the agent to occupy.

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """

        # Perform any required initializations, including selecting an initial
        # move from the game board (i.e., an opening book), or returning
        # immediately if there are no legal moves

        self.time_left = time_left

        if not legal_moves:
            return (-1, -1)
        
        # open book selection - center or nearest
        if game.get_player_location(self) == game.NOT_MOVED:
            center = board_center(game) # depending on width and height exact center may not exist
            if center in legal_moves:
                return center
            else:
                return (center[0]-1, center[1]-1) # just offset from the center

        depth = 1
        move = (-1, -1)
        try:
            # The search method call (alpha beta or minimax) should happen in
            # here in order to avoid timeout. The try/except block will
            # automatically catch the exception raised by the search method
            # when the timer gets close to expiring
            if self.method == "minimax":
                if self.iterative:
                    # consider tracking the score and the move to see if quiescence is reached
                    # depth = 1
                    while True:
                        _, move = self.minimax(game, depth)
                        depth = depth + 1
                else:
                    _, move = self.minimax(game, self.search_depth)
            else:
                if self.iterative:
                    # depth = 1
                    while True:
                        _, move = self.alphabeta(game, depth)
                        depth = depth + 1
                else:
                    _, move = self.alphabeta(game, self.search_depth)

        except Timeout:
            # print("depth", depth, self.method)
            pass

        return move

    def minimax(self, game, depth, maximizing_player=True):
        """Implement the minimax search algorithm as described in the lectures.

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        maximizing_player : bool
            Flag indicating whether the current search depth corresponds to a
            maximizing layer (True) or a minimizing layer (False)

        Returns
        -------
        float
            The score for the current search branch

        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project unit tests; you cannot call any other
                evaluation function directly.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()

        # calculate the scores for all possible moves and return the best move
        legal_moves = game.get_legal_moves()

        if not legal_moves:
            if maximizing_player:
                return (float("-inf"), (-1, -1))
            else :
                return (float("+inf"), (-1, -1))

        if depth == 1:
            if maximizing_player:
                return max([(self.score(game.forecast_move(m), self), m) for m in legal_moves])
            else:
                return min([(self.score(game.forecast_move(m), self), m) for m in legal_moves])

        # evaluate all branches and return the highest/lowest scoring tuple
        branches = [(game.forecast_move(m), m) for m in legal_moves]
        if maximizing_player:
            # maximizing player node: return the best branch(the max score)
            scores = []
            for branch, move in branches:
                score, _ = self.minimax(branch, depth-1, not maximizing_player)
                scores.append((score, move))
            return max(scores)
        else:
            # minimizing player node: expect that the opponent will choose the worst branch(the min score)
            scores = []
            for branch, move in branches:
                score, _ = self.minimax(branch, depth-1, not maximizing_player)
                scores.append((score, move))
            return min(scores)

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf"), maximizing_player=True):
        """Implement minimax search with alpha-beta pruning as described in the
        lectures.

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        maximizing_player : bool
            Flag indicating whether the current search depth corresponds to a
            maximizing layer (True) or a minimizing layer (False)

        Returns
        -------
        float
            The score for the current search branch

        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project unit tests; you cannot call any other
                evaluation function directly.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()

        # calculate the scores for all possible moves and return the best move
        legal_moves = game.get_legal_moves()

        if not legal_moves:
            if maximizing_player:
                return (float("-inf"), (-1, -1))
            else :
                return (float("+inf"), (-1, -1))

        current_move = (-1, -1)
        current_score = 0
        if maximizing_player:
            current_score = float("-inf")
        else:
            current_score = float("+inf")

        if depth == 1:
            if maximizing_player:
                for m in legal_moves:
                    score = self.score(game.forecast_move(m), self)
                    if score >= beta:
                        return (score, m)
                    if score > current_score:
                        current_score = score
                        current_move = m
                return (current_score, current_move)
            else:
                for m in legal_moves:
                    score = self.score(game.forecast_move(m), self)
                    if score <= alpha:
                        return (score, m)
                    if score < current_score:
                        current_score = score
                        current_move = m
                return (current_score, current_move)

        # evaluate all branches and return the highest/lowest scoring tuple
        for m in legal_moves:
            if current_move == (-1, -1):
                current_move = m

            if maximizing_player:
                branch = game.forecast_move(m)
                score, _ = self.alphabeta(branch, depth-1, alpha, beta, not maximizing_player)
                if score >= beta:
                    return (score, m)
                if score > alpha:
                    alpha = score
                if score > current_score:
                    current_score = score
                    current_move = m
            else:
                branch = game.forecast_move(m)
                score, _ = self.alphabeta(branch, depth-1, alpha, beta, not maximizing_player)
                if score <= alpha:
                    return (score, m)
                if score < beta:
                    beta = score
                if score < current_score:
                    current_score = score
                    current_move = m

        return (current_score, current_move)

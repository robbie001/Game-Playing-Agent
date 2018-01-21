"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
import random


class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass


def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    This should be the best heuristic function for your project submission.

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
    # TODO: finish this function!
    
    # Return inf if player has won or -inf if player has lost the game  
    if game.is_loser(player) or game.is_winner(player):
        return game.utility(player)
    
    # Reward the center position as the first move if game agent is the first player
    center_reward = 0
    my_pos = game.get_player_location(player)
    if game.move_count == 0 and my_pos == (game.width//2, game.height//2):
        center_reward += 5
        
    # Reward a position one legal move away from opponent's position
    block_reward = 0
    opp_pos = game.get_player_location(game.get_opponent(player))
    jumps = [(1, -2), (1, 2), (-1, 2), (-1, -2), (2, -1), (2, 1), (-2, -1), (-2, 1)]

    for jump in jumps:
        if (jump[0] + opp_pos[0], jump[1] + opp_pos[1]) == my_pos:
            block_reward += 1
            break            
    
    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    
    # Create an aggressive game beginning:
    if game.move_count <= 6:
        return float(own_moves - 2 * opp_moves + center_reward + block_reward)
    else:
        return float(own_moves - opp_moves + block_reward)
    


def custom_score_2(game, player):
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
    # TODO: finish this function!

    # Return inf if player has won or -inf if player has lost the game  
    if game.is_loser(player) or game.is_winner(player):
        return game.utility(player)
    
    # Reward a position that would block one of the opponent's moves
    block_reward = 0
    my_pos = game.get_player_location(player)
    jumps = [(1, -2), (1, 2), (-1, 2), (-1, -2), (2, -1), (2, 1), (-2, -1), (-2, 1)]
    
    opp_legal_moves = game.get_legal_moves(game.get_opponent(player))

    for jump in jumps:
        if (jump[0] + my_pos[0], jump[1] + my_pos[1]) in opp_legal_moves:
            block_reward += 1
            # Create a more aggressive block for early games of 4 or less
            #block_reward += 2 if game.move_count <= 4 else 1
            #break
    
    #own_moves = len(game.get_legal_moves(player))
    #opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    
    #return float(own_moves - opp_moves + block_reward)
    return block_reward


def custom_score_3(game, player):
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
    # TODO: finish this function!
    
    # Return inf if player has won or -inf if player has lost the game  
    if game.is_loser(player) or game.is_winner(player):
        return game.utility(player)
    
    # Get the positions and legal moves of the agent and the opponent
    opp_pos = game.get_player_location(game.get_opponent(player))
    my_pos = game.get_player_location(player)

    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    
    # Reward if the game agent is the second player and stays away from opponent
    #far_reward = 0
    #if game.move_count % 2 == 1:
    #    if opp_pos[0] + 2 < my_pos[0] < game.width or opp_pos[0] - 2 > my_pos[0] >= 0 or opp_pos[1] + 2 < my_pos[1] < game.height or opp_pos[1] - 2 > my_pos[1] >= 0:
    #        far_reward += 1

    # Reward if the game agent is the first player and sticks close to opponent
    close_reward = 0        
    if game.move_count % 2 == 0:
        close_moves = [(1, -1), (1, 0), (1, 1), (0, 1), (0, -1), (-1, 1), (-1, 0), (-1, -1)]
        for move in close_moves:
            if (opp_pos[0] + move[0], opp_pos[1] + move[1]) == my_pos:
                close_reward += 1
                break
                
    # Reward if the second player and blocks one of the opponent's moves
    block_reward = 0
    if game.move_count % 2 == 1:
        my_pos = game.get_player_location(player)
        jumps = [(1, -2), (1, 2), (-1, 2), (-1, -2), (2, -1), (2, 1), (-2, -1), (-2, 1)]
        opp_legal_moves = game.get_legal_moves(game.get_opponent(player))

        for jump in jumps:
            if (jump[0] + my_pos[0], jump[1] + my_pos[1]) in opp_legal_moves:
                block_reward += 1
                break
    
    # Return the difference of remaining moves if there are no close or far moves.
    return float(own_moves - opp_moves + close_reward + block_reward)

class IsolationPlayer:
    """Base class for minimax and alphabeta agents -- this class is never
    constructed or tested directly.

    ********************  DO NOT MODIFY THIS CLASS  ********************

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """
    def __init__(self, search_depth=3, score_fn=custom_score, timeout=10.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout


class MinimaxPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using depth-limited minimax
    search. You must finish and test this player to make sure it properly uses
    minimax to return a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        **************  YOU DO NOT NEED TO MODIFY THIS FUNCTION  *************

        For fixed-depth search, this function simply wraps the call to the
        minimax method, but this method provides a common interface for all
        Isolation agents, and you will replace it in the AlphaBetaPlayer with
        iterative deepening search.

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

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
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            return self.minimax(game, self.search_depth)

        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move

    def minimax(self, game, depth):
        """Implement depth-limited minimax search algorithm as described in
        the lectures.

        This should be a modified version of MINIMAX-DECISION in the AIMA text.
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Minimax-Decision.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        # TODO: finish this function!   
        
        def min_value(game_state, depth):
            """ Return the value for a win (the self.score heuristic) if the game is over or
            if the depth of the search is reached. Otherwise return the minimum value over all
            legal child nodes.
            Parameters
            -----------
            game_state: a copy of the game board
            depth_counter: int variable for counting search depth
            """
            if self.time_left() < self.TIMER_THRESHOLD:
                raise SearchTimeout()
            
            # Return the score heuristic if there are no legal moves or the search depth is reached
            if depth == 0:
                return self.score(game_state, self)
            
            value = float("inf")            
            for m in game_state.get_legal_moves():
                value = min(value, max_value(game_state.forecast_move(m), depth-1))
            return value
        
        def max_value(game_state, depth):
            """ Return the value for a loss (the self.score heuristic) if the game is over or
            if the depth of the search is reached. Otherwise return the maximum value over all
            legal child nodes.
            Parameters
            -----------
            game_state: a copy of the game board
            depth_counter: int variable for counting search depth
            """
            if self.time_left() < self.TIMER_THRESHOLD:
                raise SearchTimeout()
            
            # Return the score heuristic if the active player losses or the search depth reached                
            if depth == 0:
                return self.score(game_state, self)            
            
            value = float("-inf")            
            for m in game_state.get_legal_moves():
                value = max(value, min_value(game_state.forecast_move(m), depth-1))
            return value

        # Return (-1, -1) if there are no legal moves 
        if not game.get_legal_moves():
            return (-1, -1)
        
        # Set best move to first legal move in case of timeout
        best_move = game.get_legal_moves()[0]
        
        try:
            best_move = max(game.get_legal_moves(), key=lambda m: min_value(game.forecast_move(m), depth-1))
            return best_move
        except SearchTimeout:
            return best_move  


class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        Modify the get_move() method from the MinimaxPlayer class to implement
        iterative deepening search instead of fixed-depth search.

        **********************************************************************
        NOTE: If time_left() < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

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
        self.time_left = time_left       
        
        # TODO: finish this function!
        # Set best_move to (-1, -1) if no moves are available, or to the first move if moves are available
        best_move = (-1, -1) if not game.get_legal_moves() else game.get_legal_moves()[0]

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            # Create counter d and search alphabeta one level at a time
            d = 1
            while d < float("inf"):
                best_move = self.alphabeta(game, d)
                d += 1  
            #return self.alphabeta(game, self.search_depth)

        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration            
        return best_move
    

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        """Implement depth-limited minimax search with alpha-beta pruning as
        described in the lectures.

        This should be a modified version of ALPHA-BETA-SEARCH in the AIMA text
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Alpha-Beta-Search.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

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

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        # TODO: finish this function!

        
        def max_value(game_state, depth, alpha, beta):
            """ Return the value for a loss (the self.score heuristic) if the game is over or
            if the depth of the search is reached. Otherwise return the maximum value over all
            legal child nodes.
            Parameters
            -----------
            game_state: a copy of the game board
            depth_counter: int variable for counting search depth
            """
            if self.time_left() < self.TIMER_THRESHOLD:
                raise SearchTimeout()
            
            # Return the score heuristic if there are no legal moves or the search depth reached                
            if depth == 0:
                return self.score(game_state, self)            
            
            value = float("-inf")            
            for m in game_state.get_legal_moves():
                value = max(value, min_value(game_state.forecast_move(m), depth-1, alpha, beta))
                if value >= beta:
                    return value
                alpha = max(alpha, value)
            return value
        
        def min_value(game_state, depth, alpha, beta):
            """ Return the value for a win (the self.score heuristic) if the game is over or
            if the depth of the search is reached. Otherwise return the minimum value over all
            legal child nodes.
            Parameters
            -----------
            game_state: a copy of the game board
            depth_counter: int variable for counting search depth
            """
            if self.time_left() < self.TIMER_THRESHOLD:
                raise SearchTimeout()
            
            # Return the score heuristic if there are no legal moves or the search depth is reached
            if depth == 0:
                return self.score(game_state, self)
            
            value = float("inf")                        
            for m in game_state.get_legal_moves():
                value = min(value, max_value(game_state.forecast_move(m), depth-1, alpha, beta))
                if value <= alpha:
                    return value
                beta = min(beta, value)
            return value        
        
        # Return (-1, -1) if there are no legal moves
        if not game.get_legal_moves():
            return (-1, -1)
        
        # Set the best move to the first legal move in case of timeout
        best_move = game.get_legal_moves()[0]
        
        # Forecast the best move
        best_score = float("-inf")
        for move in game.get_legal_moves():
            value = min_value(game.forecast_move(move), depth-1, alpha, beta)
            if value > best_score:
                best_score = value
                best_move = move
            alpha = max(alpha, best_score)
        return best_move


from collections import namedtuple

from bobbot.search_node import GameAdapter


# Types, constants and helpers


GameState = namedtuple('GameState', ['board', 'active_player'])

PLAYER_X = 1
PLAYER_O = 2

def player_symbol(state):
    return {PLAYER_X: "X",
            PLAYER_O: "O",
            None: " "}[state]


def textual_repr(game_state):
    b = game_state.board
    if not is_finished(game_state):
        m = "Move: {}".format(player_symbol(game_state.active_player))
    else:
        m = "Winner: {}".format(player_symbol(winner(game_state)))
    return (" {} | {} | {}\n"
            "---+---+---\n"
            " {} | {} | {}\n"
            "---+---+---\n"
            " {} | {} | {}\n"
            "{}".format(player_symbol(b[(0,0)]),
                        player_symbol(b[(1,0)]),
                        player_symbol(b[(2,0)]),
                        player_symbol(b[(0,1)]),
                        player_symbol(b[(1,1)]),
                        player_symbol(b[(2,1)]),
                        player_symbol(b[(0,2)]),
                        player_symbol(b[(1,2)]),
                        player_symbol(b[(2,2)]),
                        m))

# Functional implementation of game rules


def starting_state():
    board = {(x,y): None for x in range(3) for y in range(3)}
    active_player = PLAYER_X
    return GameState(board=board, active_player=active_player)


def is_winner(game_state, player):
    row = any([all([game_state.board[(b_column, b_row)] == player
                    for b_column in range(3)])
               for b_row in range(3)])
    column = any([all([game_state.board[(b_column, b_row)] == player
                       for b_row in range(3)])
                  for b_column in range(3)])
    diagonal_a = all([game_state.board[(b, b)] == player for b in range(3)])
    diagonal_b = all([game_state.board[(b, 2-b)] == player for b in range(3)])

    return any([row, column, diagonal_a, diagonal_b])


def is_finished(game_state):
    player_won = is_winner(game_state, PLAYER_X) or is_winner(game_state, PLAYER_O)
    board_full = all([field is not None for field in game_state.board.values()])
    return player_won or board_full


def winner(game_state):
    if is_winner(game_state, PLAYER_X):
        return PLAYER_X
    elif is_winner(game_state, PLAYER_O):
        return PLAYER_O
    elif not is_finished(game_state):
        raise ValueError
    else:
        return None


def is_legal_move(game_state, coord):
    assert len(coord) == 2, "Not a coord tuple"
    assert (0 <= coord[0] <= 2) and (0 <= coord[1] <= 2), "Value out of range"
    return not is_finished(game_state) and game_state.board[coord] is None


def make_move(game_state, coord):
    if not is_legal_move(game_state, coord):
        raise ValueError("Illegal move")

    successor_board = {c: s for c, s in game_state.board.items()}
    successor_board[coord] = game_state.active_player
    tentative_successor_game_state = GameState(board=successor_board,
                                               active_player=None)
    if is_finished(tentative_successor_game_state):
        successor_active_player = None
    elif game_state.active_player == PLAYER_X:
        successor_active_player = PLAYER_O
    else:
        successor_active_player = PLAYER_X
    return GameState(board=successor_board,
                     active_player=successor_active_player)


def all_legal_moves(game_state):
    return [coord
            for coord in [(x,y) for x in range(3) for y in range(3)]
            if is_legal_move(game_state, coord)]


def evaluate(game_state):
    if not is_finished(game_state):
        return {PLAYER_X: 0,
                PLAYER_O: 0}
    elif is_winner(game_state, PLAYER_X):
        return {PLAYER_X: 1,
                PLAYER_O: -1}
    elif is_winner(game_state, PLAYER_O):
        return {PLAYER_X: -1,
                PLAYER_O: 1}
    else:
        return {PLAYER_X: -0.5,
                PLAYER_O: -0.5}


def node_key(game_state):
    return ''.join([player_symbol(game_state.board[(x,y)])
                    for x in range(3)
                    for y in range(3)])


# TODO: GameAdapter needs to pass the state in the first place.
class TicTacToeAdapter(GameAdapter):
    def starting_state(self):
        return starting_state()

    def evaluate(self, game_state):
        return evaluate(game_state)

    def active_player(self, game_state):
        return game_state.active_player

    def is_finished(self, game_state):
        return is_finished(game_state)

    def all_legal_moves(self, game_state):
        return all_legal_moves(game_state)

    def make_move(self, game_state, move):
        return make_move(game_state, move)

    def winner(self, game_state):
        return winner(game_state)

    def node_key(self, game_state):
        return node_key(game_state)

    def __repr__(self):
        return textual_repr(self.state)

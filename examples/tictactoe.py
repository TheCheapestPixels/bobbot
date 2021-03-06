#!/usr/bin/env python3

from bobbot.search_tree import BaseAI
from bobbot.search_tree import FullExpansionMixin, BoundedExpansionMixin
from bobbot.search_tree import OneStepSearchMixin
from bobbot.search_tree import ForwardSweepingMixin
from bobbot.search_tree import NaivePruningMixin
from bobbot.search_node import MinMaxScoringMixin
from bobbot.search_node import (ChooseFirstMoveMixin, ChooseRandomMoveMixin,
    ChooseRandomMoveFromBestMixin)
from bobbot.games.tictactoe import TicTacToeAdapter


TicTacToe = type('TicTacToe',
                 (MinMaxScoringMixin,
                  ChooseRandomMoveFromBestMixin,
                  TicTacToeAdapter,
                 ),
                 {})
AI = type('AI',
          (BoundedExpansionMixin,
           ForwardSweepingMixin,
           NaivePruningMixin,
           BaseAI,
          ),
          {})
ai = AI(TicTacToe(), debug=True, search_depth=5, node_limit=100)


if __name__ == '__main__':
    ai.play()

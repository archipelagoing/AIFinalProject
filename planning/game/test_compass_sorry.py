import random
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from compass_sorry import CHECKPOINTS, Game


class CompassSorryTests(unittest.TestCase):
    def test_issue_requires_unique_identifier(self):
        game = Game()
        game.complete_issue("A", "CMP-1", random.Random(1))
        with self.assertRaises(ValueError):
            game.complete_issue("A", "CMP-1", random.Random(1))

    def test_unpassed_gate_stops_movement(self):
        game = Game()
        player = game.player("A")
        game.move(player, 12)
        self.assertEqual(player.position, 8)
        self.assertIn(8, CHECKPOINTS)

    def test_finish_requires_all_gates(self):
        game = Game()
        player = game.player("A")
        game.passed_gates = list(CHECKPOINTS)
        game.move(player, 40)
        self.assertEqual(player.position, 40)


if __name__ == "__main__":
    unittest.main()

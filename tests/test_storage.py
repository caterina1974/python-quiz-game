"""Tests for JSON backup, atomic saving, and recovery choices."""

import json
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from unittest.mock import patch

from main import QuizGame


class TestQuizStorage(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.state_file = Path(self.temp_dir.name) / "state.json"
        self.backup_file = Path(self.temp_dir.name) / "state.backup.json"

    def tearDown(self):
        self.temp_dir.cleanup()

    def make_game(self):
        with redirect_stdout(StringIO()):
            return QuizGame(state_file=self.state_file)

    def test_first_run_creates_default_state_file(self):
        game = self.make_game()

        self.assertTrue(self.state_file.exists())
        self.assertEqual(len(game.quizzes), 7)
        self.assertFalse(self.backup_file.exists())

    def test_saving_creates_backup_of_previous_valid_state(self):
        game = self.make_game()

        game.best_score = 71
        game.best_correct = 5
        game.best_total = 7
        game.has_played = True
        self.assertTrue(game.save_data(show_message=False))

        game.best_score = 85
        game.best_correct = 6
        game.best_total = 7
        self.assertTrue(game.save_data(show_message=False))

        with self.backup_file.open("r", encoding="utf-8") as file:
            backup_data = json.load(file)

        self.assertEqual(backup_data["best_score"], 71)
        self.assertEqual(backup_data["best_correct"], 5)

    def test_corrupt_state_can_be_restored_from_backup(self):
        game = self.make_game()
        game.best_score = 71
        game.best_correct = 5
        game.best_total = 7
        game.has_played = True
        game.save_data(show_message=False)

        game.best_score = 85
        game.best_correct = 6
        game.save_data(show_message=False)

        self.state_file.write_text("{ broken json", encoding="utf-8")

        with patch("builtins.input", return_value="1"):
            with redirect_stdout(StringIO()):
                restored_game = QuizGame(state_file=self.state_file)

        self.assertEqual(restored_game.best_score, 71)
        self.assertEqual(restored_game.best_correct, 5)
        self.assertTrue(restored_game.has_played)
        self.assertEqual(len(restored_game.quizzes), 7)

        # The repaired main file must itself be valid JSON.
        with self.state_file.open("r", encoding="utf-8") as file:
            saved_state = json.load(file)
        self.assertEqual(saved_state["best_score"], 71)

    def test_user_can_choose_default_reset(self):
        game = self.make_game()
        game.best_score = 71
        game.best_correct = 5
        game.best_total = 7
        game.has_played = True
        game.save_data(show_message=False)

        self.state_file.write_text("{ broken json", encoding="utf-8")

        with patch("builtins.input", return_value="2"):
            with redirect_stdout(StringIO()):
                reset_game = QuizGame(state_file=self.state_file)

        self.assertEqual(len(reset_game.quizzes), 7)
        self.assertEqual(reset_game.best_score, 0)
        self.assertEqual(reset_game.best_correct, 0)
        self.assertFalse(reset_game.has_played)

    def test_user_can_exit_without_overwriting_damaged_file(self):
        game = self.make_game()
        damaged_content = "{ broken json"
        self.state_file.write_text(damaged_content, encoding="utf-8")

        with patch("builtins.input", return_value="2"):
            with redirect_stdout(StringIO()):
                with self.assertRaises(SystemExit):
                    QuizGame(state_file=self.state_file)

        self.assertEqual(
            self.state_file.read_text(encoding="utf-8"),
            damaged_content,
        )

    def test_temporary_files_are_removed_after_successful_save(self):
        game = self.make_game()
        self.assertTrue(game.save_data(show_message=False))

        self.assertFalse(
            self.state_file.with_name("state.json.tmp").exists()
        )
        self.assertFalse(
            self.backup_file.with_name("state.backup.json.tmp").exists()
        )


if __name__ == "__main__":
    unittest.main()

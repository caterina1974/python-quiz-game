import unittest
from main import Quiz


class TestQuiz(unittest.TestCase):

	def setUp(self):
		self.quiz = Quiz(
			"Python에서 출력하는 함수는?",
			["input()", "print()", "len()", "type()"],
			2
		)

	def test_question_is_saved(self):
		self.assertEqual(
			self.quiz.question,
			"Python에서 출력하는 함수는?"
		)

	def test_four_choices_are_saved(self):
		self.assertEqual(len(self.quiz.choices), 4)

	def test_correct_answer(self):
		self.assertTrue(self.quiz.is_correct(2))

	def test_wrong_answer(self):
		self.assertFalse(self.quiz.is_correct(1))

	def test_quiz_to_dict(self):
		data = self.quiz.to_dict()
		self.assertEqual(data["answer"], 2)
		self.assertEqual(data["question"], self.quiz.question)

	def test_invalid_answer_is_rejected(self):
		with self.assertRaises(ValueError):
			Quiz("문제", ["A", "B", "C", "D"], 5)

	def test_invalid_choice_count_is_rejected(self):
		with self.assertRaises(ValueError):
			Quiz("문제", ["A", "B", "C"], 1)

	def test_empty_question_is_rejected(self):
		with self.assertRaises(ValueError):
			Quiz("", ["A", "B", "C", "D"], 1)


if __name__ == "__main__":
	unittest.main()

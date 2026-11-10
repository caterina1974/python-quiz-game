"""Windows 11 beginner Python quiz game.

Run with: py -X utf8 main.py
"""

import json
from pathlib import Path


# state.json is always stored beside this main.py file (project root).
STATE_FILE = Path(__file__).resolve().parent / "state.json"


class Quiz:
    """One quiz question, its four choices, and its correct answer number."""

    def __init__(self, question, choices, answer):
        question = str(question).strip()
        if not question:
            raise ValueError("문제 내용이 비어 있습니다.")
        if not isinstance(choices, list) or len(choices) != 4:
            raise ValueError("선택지는 반드시 4개여야 합니다.")
        cleaned_choices = [str(choice).strip() for choice in choices]
        if any(not choice for choice in cleaned_choices):
            raise ValueError("선택지 내용은 비어 있을 수 없습니다.")
        if isinstance(answer, bool) or not isinstance(answer, int) or answer not in range(1, 5):
            raise ValueError("정답 번호는 1부터 4까지여야 합니다.")

        self.question = question
        self.choices = cleaned_choices
        self.answer = answer

    def display(self, number=None):
        print("\n" + "-" * 48)
        if number is not None:
            print(f"[문제 {number}]")
        print(self.question)
        for index, choice in enumerate(self.choices, start=1):
            print(f"{index}. {choice}")

    def is_correct(self, user_answer):
        return user_answer == self.answer

    def to_dict(self):
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer,
        }

    @classmethod
    def from_dict(cls, data):
        if not isinstance(data, dict):
            raise ValueError("퀴즈 데이터 형식이 올바르지 않습니다.")
        return cls(
            question=data["question"],
            choices=data["choices"],
            answer=data["answer"],
        )


class QuizGame:
    """Manage the quiz list, menu, scores, and JSON file."""

    def __init__(self):
        self.quizzes = []
        self.best_score = 0  # percentage, from 0 to 100
        self.best_correct = 0
        self.best_total = 0
        self.has_played = False
        self.load_data()

    @staticmethod
    def make_default_quizzes():
        """Seven beginner questions about Python."""
        return [
            Quiz(
                "Python에서 화면에 글자를 출력할 때 사용하는 함수는?",
                ["input()", "print()", "len()", "type()"], 2,
            ),
            Quiz(
                "문자열 자료형을 나타내는 것은?",
                ["int", "bool", "str", "list"], 3,
            ),
            Quiz(
                "숫자를 정수로 바꾸는 함수는?",
                ["str()", "list()", "int()", "print()"], 3,
            ),
            Quiz(
                "조건에 따라 실행할 코드를 나눌 때 사용하는 문법은?",
                ["if", "for", "import", "class"], 1,
            ),
            Quiz(
                "반복해서 코드를 실행할 때 사용하는 문법이 아닌 것은?",
                ["for", "while", "if", "반복문"], 3,
            ),
            Quiz(
                "여러 값을 순서대로 저장하는 자료형은?",
                ["bool", "list", "int", "None"], 2,
            ),
            Quiz(
                "키(key)와 값(value)을 짝으로 저장하는 자료형은?",
                ["dict", "str", "int", "float"], 1,
            ),
        ]

    @staticmethod
    def read_non_empty(prompt):
        """Ask again until the user enters non-empty text."""
        while True:
            value = input(prompt).strip()
            if value:
                return value
            print("⚠️ 빈칸으로 둘 수 없습니다. 다시 입력해 주세요.")

    @staticmethod
    def read_number(prompt, minimum, maximum):
        """Read an integer within the requested range."""
        while True:
            raw = input(prompt).strip()
            if not raw:
                print("⚠️ 입력이 비어 있습니다. 숫자를 입력해 주세요.")
                continue
            try:
                number = int(raw)
            except ValueError:
                print("⚠️ 숫자로 입력해 주세요. 예: 1")
                continue
            if not minimum <= number <= maximum:
                print(f"⚠️ {minimum}부터 {maximum} 사이의 숫자를 입력해 주세요.")
                continue
            return number

    def load_data(self):
        """Load saved questions and score, or recover with default questions."""
        if not STATE_FILE.exists():
            print("📂 state.json이 없습니다. 기본 퀴즈로 시작합니다.")
            self.quizzes = self.make_default_quizzes()
            self.save_data(show_message=False)
            return

        try:
            with STATE_FILE.open("r", encoding="utf-8") as file:
                data = json.load(file)

            if not isinstance(data, dict):
                raise ValueError("저장 파일의 최상위 구조가 올바르지 않습니다.")
            raw_quizzes = data.get("quizzes")
            if not isinstance(raw_quizzes, list):
                raise ValueError("quizzes 항목이 목록 형식이 아닙니다.")

            loaded_quizzes = [Quiz.from_dict(item) for item in raw_quizzes]
            best_score = data.get("best_score", 0)
            best_correct = data.get("best_correct", 0)
            best_total = data.get("best_total", 0)
            has_played = data.get("has_played", False)

            if isinstance(best_score, bool) or not isinstance(best_score, (int, float)) or not 0 <= best_score <= 100:
                raise ValueError("최고 점수 데이터가 올바르지 않습니다.")
            for value in (best_correct, best_total):
                if isinstance(value, bool) or not isinstance(value, int) or value < 0:
                    raise ValueError("최고 점수 상세 데이터가 올바르지 않습니다.")
            if not isinstance(has_played, bool):
                raise ValueError("게임 기록 여부가 올바르지 않습니다.")

            self.quizzes = loaded_quizzes
            self.best_score = int(best_score)
            self.best_correct = best_correct
            self.best_total = best_total
            self.has_played = has_played
            print(f"📂 저장된 데이터를 불러왔습니다. (퀴즈 {len(self.quizzes)}개)")

        except (OSError, json.JSONDecodeError, ValueError, TypeError, KeyError) as error:
            print(f"⚠️ 저장 파일을 읽을 수 없습니다: {error}")
            print("기본 퀴즈 데이터로 초기화합니다.")
            self.quizzes = self.make_default_quizzes()
            self.best_score = 0
            self.best_correct = 0
            self.best_total = 0
            self.has_played = False
            self.save_data(show_message=False)

    def save_data(self, show_message=True):
        """Save quiz questions and best score as UTF-8 JSON."""
        data = {
            "quizzes": [quiz.to_dict() for quiz in self.quizzes],
            "best_score": self.best_score,
            "best_correct": self.best_correct,
            "best_total": self.best_total,
            "has_played": self.has_played,
        }
        try:
            with STATE_FILE.open("w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
            if show_message:
                print("💾 데이터가 state.json에 저장되었습니다.")
            return True
        except OSError as error:
            print(f"⚠️ 파일 저장 중 오류가 발생했습니다: {error}")
            return False

    @staticmethod
    def show_menu():
        print("\n" + "=" * 48)
        print("             🎯 나만의 퀴즈 게임 🎯")
        print("=" * 48)
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록")
        print("4. 점수 확인")
        print("5. 종료")
        print("=" * 48)

    def play_quiz(self):
        if not self.quizzes:
            print("등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가해 주세요.")
            return

        print(f"\n📝 퀴즈를 시작합니다! (총 {len(self.quizzes)}문제)")
        correct_count = 0

        for index, quiz in enumerate(self.quizzes, start=1):
            quiz.display(index)
            user_answer = self.read_number("정답 입력 (1-4): ", 1, 4)
            if quiz.is_correct(user_answer):
                print("✅ 정답입니다!")
                correct_count += 1
            else:
                print(f"❌ 오답입니다. 정답은 {quiz.answer}번입니다.")

        total = len(self.quizzes)
        score = round(correct_count / total * 100)
        print("\n" + "=" * 48)
        print(f"🏆 결과: {total}문제 중 {correct_count}문제 정답! ({score}점)")

        if not self.has_played or score > self.best_score:
            self.best_score = score
            self.best_correct = correct_count
            self.best_total = total
            self.has_played = True
            print("🎉 새로운 최고 점수입니다!")
        else:
            print(f"현재 최고 점수는 {self.best_score}점입니다.")
        print("=" * 48)
        self.save_data()

    def add_quiz(self):
        print("\n📌 새로운 퀴즈를 추가합니다.")
        question = self.read_non_empty("문제를 입력하세요: ")
        choices = []
        for index in range(1, 5):
            choices.append(self.read_non_empty(f"선택지 {index}: "))
        answer = self.read_number("정답 번호 (1-4): ", 1, 4)

        self.quizzes.append(Quiz(question, choices, answer))
        print("✅ 퀴즈가 추가되었습니다!")
        self.save_data()

    def show_quizzes(self):
        print("\n📋 등록된 퀴즈 목록")
        if not self.quizzes:
            print("등록된 퀴즈가 없습니다.")
            return
        print(f"총 {len(self.quizzes)}개")
        for index, quiz in enumerate(self.quizzes, start=1):
            print(f"[{index}] {quiz.question}")
            for choice_index, choice in enumerate(quiz.choices, start=1):
                print(f"    {choice_index}. {choice}")

    def show_score(self):
        print("\n🏆 점수 확인")
        if not self.has_played:
            print("아직 퀴즈를 푼 기록이 없습니다.")
            return
        print(f"최고 점수: {self.best_score}점")
        print(f"정답 수: {self.best_correct}/{self.best_total}문제")

    def run(self):
        while True:
            self.show_menu()
            choice = self.read_number("메뉴 번호를 입력하세요 (1-5): ", 1, 5)

            if choice == 1:
                self.play_quiz()
            elif choice == 2:
                self.add_quiz()
            elif choice == 3:
                self.show_quizzes()
            elif choice == 4:
                self.show_score()
            elif choice == 5:
                self.save_data()
                print("👋 퀴즈 게임을 종료합니다. 다음에 또 만나요!")
                break


def main():
    game = QuizGame()
    try:
        game.run()
    except (KeyboardInterrupt, EOFError):
        print("\n\n⚠️ 입력이 중단되었습니다. 안전하게 종료합니다.")
        game.save_data()
        print("프로그램을 종료했습니다.")


if __name__ == "__main__":
    main()

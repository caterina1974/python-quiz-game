# 나만의 파이썬 기초 퀴즈 게임

Python 기초 문법을 퀴즈로 복습하고, 문제와 최고 점수를 JSON 파일에 저장하는 콘솔 프로그램입니다.

- **GitHub 저장소:** https://github.com/caterina1974/python-quiz-game
- **개발 환경:** Windows 11, Python 3.10 이상
- **외부 패키지:** 없음 (Python 표준 라이브러리 사용)

## 1. 프로젝트 개요

이 프로젝트는 Python을 처음 배우는 학습자가 기본 문법을 직접 문제로 풀어보며 복습할 수 있도록 만든 콘솔 퀴즈 게임입니다. 메뉴에서 퀴즈 풀기, 퀴즈 추가, 퀴즈 목록 확인, 최고 점수 확인 기능을 선택할 수 있습니다.

프로그램은 객체 지향 구조로 작성했으며, 퀴즈 데이터와 점수를 프로젝트 루트의 `state.json` 파일에 저장합니다. 따라서 프로그램을 종료한 뒤 다시 실행해도 저장된 퀴즈와 점수를 불러올 수 있습니다.

## 2. 퀴즈 주제와 선정 이유

퀴즈 주제는 **Python 기초 문법**입니다. 개발 입문 과정에서 자주 사용하는 출력 함수, 자료형, 형 변환, 조건문, 반복문, 리스트와 딕셔너리 등을 문제로 구성했습니다. 문법을 읽는 데서 끝나지 않고 직접 답을 선택하면서 배운 내용을 확인할 수 있어 이 주제를 선택했습니다.

기본 퀴즈 7개가 제공되며, 프로그램 메뉴에서 학습자가 새로운 문제를 추가할 수 있습니다.

## 3. 개발 환경 및 실행 방법

### 필요한 환경

- Windows 11
- Python 3.10 이상
- Visual Studio Code (선택 사항)
- Git (소스 코드 버전 관리 및 GitHub 업로드용)

외부 Python 패키지를 설치할 필요는 없습니다.

### 실행 방법

1. 저장소를 내려받거나 복제합니다.

   ```powershell
   git clone https://github.com/caterina1974/python-quiz-game.git
   cd python-quiz-game
   ```

2. 프로젝트 폴더에서 다음 명령어를 실행합니다.

   ```powershell
   py -X utf8 main.py
   ```

3. 화면에 표시되는 메뉴에서 원하는 번호를 입력합니다.

   ```text
   1. 퀴즈 풀기
   2. 퀴즈 추가
   3. 퀴즈 목록
   4. 점수 확인
   5. 종료
   ```

`-X utf8` 옵션은 Windows 터미널에서 한글 입출력을 일관되게 처리하는 데 도움이 됩니다.

## 4. 주요 기능

| 기능 | 설명 |
|---|---|
| 퀴즈 풀기 | 저장된 문제를 순서대로 출제하고 정답 여부를 알려줍니다. 모든 문제를 푼 뒤 정답 개수와 점수를 표시합니다. |
| 퀴즈 추가 | 문제, 선택지 4개, 정답 번호(1~4)를 입력하여 새 문제를 등록합니다. |
| 퀴즈 목록 | 저장된 퀴즈의 문제와 선택지를 확인합니다. |
| 점수 확인 | 지금까지 기록한 최고 점수와 해당 기록의 정답 수를 보여줍니다. |
| 자동 저장 | 퀴즈 추가와 게임 결과를 `state.json`에 저장합니다. |
| 입력값 검사 | 빈 입력, 숫자가 아닌 입력, 허용 범위 밖의 숫자를 안내하고 다시 입력받습니다. |
| 안전한 종료 | `Ctrl+C` 또는 입력 스트림 종료(`EOFError`) 상황에서 저장을 시도한 뒤 종료합니다. |
| 데이터 복구 | `state.json`이 없거나 읽을 수 없는 형식이면 기본 퀴즈 데이터로 초기화합니다. |

## 5. 코드 구조

```text
python-quiz-game/
├── main.py                 # Quiz와 QuizGame 클래스 및 프로그램 실행 코드
├── state.json              # 퀴즈와 최고 점수 저장 데이터
├── README.md               # 프로젝트 설명서
├── .gitignore              # Git에서 제외할 파일 및 폴더 설정
├── tests/
│   └── test_quiz.py        # Quiz 클래스 자동 테스트
└── docs/
    └── screenshots/        # 개발·실행·Git 실습 캡처 이미지
```

### 클래스 구성

- **`Quiz`**: 퀴즈 한 문제를 표현합니다. 문제(`question`), 선택지(`choices`), 정답 번호(`answer`)를 관리하고, 문제 출력·정답 확인·딕셔너리 변환 기능을 제공합니다.
- **`QuizGame`**: 게임 전체를 관리합니다. 메뉴 표시, 퀴즈 풀이, 퀴즈 추가, 목록 표시, 점수 확인, JSON 데이터 불러오기와 저장을 담당합니다.

## 6. 데이터 파일 설명: `state.json`

`state.json`은 `main.py`와 같은 프로젝트 최상위 폴더에 생성되는 UTF-8 JSON 파일입니다.

| 키 | 설명 |
|---|---|
| `quizzes` | 퀴즈 목록입니다. 각 항목에는 `question`, `choices`, `answer`가 들어갑니다. |
| `best_score` | 최고 점수(0~100)입니다. |
| `best_correct` | 최고 기록에서 맞힌 문제 수입니다. |
| `best_total` | 최고 기록에서 푼 전체 문제 수입니다. |
| `has_played` | 게임을 한 번이라도 진행했는지 나타내는 값입니다. |

데이터 형태 예시:

```json
{
  "quizzes": [
    {
      "question": "Python에서 화면에 글자를 출력할 때 사용하는 함수는?",
      "choices": ["input()", "print()", "len()", "type()"],
      "answer": 2
    }
  ],
  "best_score": 71,
  "best_correct": 5,
  "best_total": 7,
  "has_played": true
}
```

위 JSON은 데이터 구조를 설명하기 위한 예시입니다. 실제 파일에는 사용자가 추가한 퀴즈와 실제 최고 점수가 저장됩니다.

- 파일이 없으면 기본 퀴즈 데이터로 시작하고 `state.json`을 생성합니다.
- JSON 문법이 잘못되었거나 데이터 구조가 유효하지 않으면 안내 메시지를 표시하고 기본 데이터로 복구합니다.
- 파일 읽기·쓰기 오류는 예외 처리하여 프로그램이 오류 원인을 안내하도록 합니다.

## 7. 자동 테스트

Python 표준 라이브러리인 `unittest`로 `Quiz` 클래스의 동작을 검사합니다. 별도 패키지 설치는 필요하지 않습니다.

프로젝트 최상위 폴더에서 다음 명령어를 실행합니다.

```powershell
py -X utf8 -m unittest discover -s tests -v
```

현재 작성된 테스트는 다음 항목을 확인합니다.

1. 문제 내용 저장
2. 선택지 4개 저장
3. 정답 판정
4. 오답 판정
5. 퀴즈 데이터를 딕셔너리로 변환
6. 잘못된 정답 번호 거부
7. 선택지 개수가 4개가 아닌 경우 거부
8. 빈 문제 내용 거부
9. 딕셔너리 데이터에서 Quiz 객체 복원

테스트 실행 결과는 `Ran 9 tests`와 `OK`로 확인했습니다.

## 8. Git 및 GitHub 실습

개발 과정에서 다음 Git 명령어를 사용했습니다.

| 명령어 | 사용 목적 |
|---|---|
| `git init` | 로컬 프로젝트를 Git 저장소로 초기화 |
| `git add` | 커밋할 파일 선택 |
| `git commit` | 변경 내용을 기록 |
| `git push` | 로컬 커밋을 GitHub에 업로드 |
| `git pull` | GitHub의 변경 내용을 로컬 저장소로 가져오기 |
| `git checkout` | 브랜치 생성 및 전환 |
| `git clone` | GitHub 저장소를 별도 폴더에 복제 |

퀴즈 풀이 안내 문서를 별도 브랜치(`feature/quiz-play-guide`)에서 수정한 후 `main` 브랜치에 병합했습니다. 또한 저장소를 별도 폴더에 `clone`하고, 복제한 폴더에서 README를 수정해 `push`한 다음 원래 작업 폴더에서 `pull`하여 변경사항이 반영되는 것을 확인했습니다.

커밋 그래프 확인 명령어:

```powershell
git log --oneline --graph --decorate --all
```

## 9. 실행 및 개발 화면

아래 이미지는 `docs/screenshots/` 폴더에 저장한 실제 실행·개발 과정 캡처입니다.

### 개발 환경 및 프로그램 실행

![개발 환경](docs/screenshots/environment.png)

![메뉴 화면](docs/screenshots/menu.png)

![퀴즈 풀이 결과](docs/screenshots/play.png)

![퀴즈 추가](docs/screenshots/add_quiz.png)

### 퀴즈 목록

목록은 화면 길이에 따라 두 장으로 나누어 캡처했습니다.

![퀴즈 목록 앞부분](docs/screenshots/list-1.png)

![퀴즈 목록 뒷부분](docs/screenshots/list-2.png)

![최고 점수](docs/screenshots/score.png)

![저장 데이터](docs/screenshots/state.json.png)

### Git 및 GitHub 실습

![Git 저장소 초기화](docs/screenshots/git-init.png)

![GitHub 저장소](docs/screenshots/github-repo.png)

![브랜치 병합 앞부분](docs/screenshots/branch-merge-1.png)

![브랜치 병합 뒷부분](docs/screenshots/branch-merge-2.png)

![Git clone 실습](docs/screenshots/clone.png)

![Git pull 실습](docs/screenshots/pull.png)

![Git 커밋 그래프](docs/screenshots/git-log.png)

> 이미지가 GitHub README에 표시되지 않는 경우, 해당 파일이 실제로 `docs/screenshots/` 폴더에 저장되어 있고 GitHub에 push되었는지 확인합니다.

## 10. 저장소

GitHub: https://github.com/caterina1974/python-quiz-game

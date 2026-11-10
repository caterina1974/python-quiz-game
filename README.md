# 나만의 파이썬 기초 퀴즈 게임

## 1. 프로젝트 개요
Python 기초 문법을 연습하기 위해 만든 Windows 11용 콘솔 퀴즈 게임입니다. 메뉴에서 퀴즈 풀기, 퀴즈 추가, 퀴즈 목록, 최고 점수 확인을 할 수 있습니다.

## 2. 퀴즈 주제와 선정 이유
주제는 Python 기초 문법입니다. 개발 입문 과제에서 배우는 변수, 자료형, 조건문, 반복문, 함수와 자료구조를 퀴즈로 복습할 수 있어 선택했습니다.

## 3. 실행 방법
1. Python 3.10 이상을 설치합니다.
2. PowerShell 또는 VS Code 터미널에서 프로젝트 폴더로 이동합니다.
3. 다음 명령어를 실행합니다.

```powershell
py -X utf8 main.py
```

외부 패키지는 필요하지 않습니다. Python 표준 라이브러리만 사용합니다.

## 4. 기능 목록
- 퀴즈 풀기: 등록된 문제에 답하고 정답 수와 점수를 확인합니다.
- 퀴즈 추가: 문제, 선택지 4개, 정답 번호를 입력합니다.
- 퀴즈 목록: 저장된 문제를 확인합니다.
- 점수 확인: 최고 점수와 정답 수를 확인합니다.
- 입력 검사: 빈 입력, 숫자가 아닌 입력, 범위를 벗어난 숫자를 다시 입력하도록 안내합니다.
- 안전한 종료: Ctrl+C 또는 입력 종료(EOFError)를 처리하고 저장을 시도합니다.
- 데이터 복구: state.json이 없거나 손상된 경우 기본 퀴즈로 시작합니다.

## 5. 코드 구조
```text
python-quiz-game/
├── main.py
├── state.json
├── README.md
├── .gitignore
└── docs/
    └── screenshots/
        └── (실행 화면 캡처 이미지)
```

## 6. 데이터 파일 설명
- 파일 경로: 프로젝트 최상위 폴더의 `state.json`
- 인코딩: UTF-8
- `quizzes`: 문제, 선택지 4개, 정답 번호를 저장하는 목록
- `best_score`: 최고 점수(0~100점)
- `best_correct`: 최고 기록에서 맞힌 문제 수
- `best_total`: 최고 기록에서 푼 문제 수
- `has_played`: 퀴즈를 한 번이라도 풀었는지 여부

프로그램을 실행하거나 퀴즈·점수를 변경하면 JSON 파일에 저장됩니다. `state.json`은 프로그램이 처음 실행될 때 없으면 자동 생성됩니다.

## 7. 스크린샷
실제 실행 후 아래 경로에 화면 캡처를 저장합니다.

- `docs/screenshots/environment.png` — Python 및 Git 버전과 VS Code
- `docs/screenshots/menu.png` — 시작 메뉴
- `docs/screenshots/add_quiz.png` — 퀴즈 추가 완료
- `docs/screenshots/list.png` — 퀴즈 목록
- `docs/screenshots/play.png` — 퀴즈 풀이 및 결과
- `docs/screenshots/score.png` — 최고 점수
- `docs/screenshots/state.json.png` — 저장된 JSON 데이터
- `docs/screenshots/git-log.png` — Git 커밋 그래프

실제 캡처를 저장한 뒤 GitHub에 커밋하고 푸시합니다.

## 퀴즈 풀이 사용 방법

1. 터미널에서 `py -X utf8 main.py`를 실행합니다.
2. 메인 메뉴에서 숫자 1을 입력합니다.
3. 화면에 출제되는 문제를 확인합니다.
4. 정답 번호 1~4 중 하나를 입력합니다.
5. 모든 문제를 풀면 최종 점수와 정답 개수를 확인합니다.
6. 게임 결과는 `state.json`에 저장됩니다.

## Clone/Pull 실습
GitHub 저장소를 별도 폴더에 복제하고 README 수정 실습을 진행했습니다.

## 자동 테스트 실행

Python에 기본으로 포함된 unittest를 사용하여
퀴즈 클래스의 기능을 검사할 수 있습니다.

### 테스트 실행 명령어

```powershell
py -X utf8 -m unittest discover -s tests -v
```

### 테스트 항목

- 퀴즈 문제 저장 확인
- 선택지 4개 확인
- 정답 판정 확인
- 오답 판정 확인
- 퀴즈 데이터 변환 확인
- 잘못된 정답 번호 검사
- 잘못된 선택지 개수 검사
- 빈 문제 입력 검사

외부 라이브러리 설치 없이 실행할 수 있습니다.

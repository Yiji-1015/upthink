# upthink

[Upstage AI Ambassador] 개인 지식 관리 with Upstage Solar pro 2

## 환경 설정

### 1. uv 설치

> Installing uv : https://docs.astral.sh/uv/getting-started/installation/

#### macOS / Linux
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

#### Homebrew
```bash
brew install uv
```

#### Windows
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

또는 pip를 통해 설치:
```bash
pip install uv
```

### 2. 프로젝트 설정
```bash
# git clone
git clone https://github.com/geminii01/upthink.git && cd upthink

# Python 3.13과 의존성 자동 설치
uv sync
```

추가할 dependency가 있는 경우: `uv add {XXX}`
### 1. 프론트 서버 실행
node serve.mjs

### 2. 가상환경 활성화
python -m venv venv
source venv/scripts/activate (윈도우 .venv\Scripts\activate)

### 3. 패키지 설치
pip install -r requirements.txt

### 4. 백엔드 서버 실행
uvicorn main:app --reload --port 8000

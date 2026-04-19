### 1. 프론트 서버 실행
<code>node serve.mjs</code> --> localhost:3000

### 2. 가상환경 활성화
<code>python -m venv venv</code>

<code>source venv/scripts/activate</code> (윈도우 .venv\Scripts\activate)

### 3. 패키지 설치
<code>pip install -r requirements.txt</code>

### 4. 백엔드 서버 실행
<code>uvicorn main:app --reload --port 8000</code> --> localhost:8000

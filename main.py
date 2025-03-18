from fastapi import FastAPI, HTTPException
import csv
import sqlite3

app = FastAPI()
DB_FILE = "quiz_records.db"
QUESTIONS_FILE = "questions.csv"

# for 前端測試
from fastapi.staticfiles import StaticFiles
app.mount("/static", StaticFiles(directory="static"), name="static")

# 初始化 SQLite 資料庫
def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT,
        question_id INTEGER,
        user_answer TEXT,
        is_correct BOOLEAN
    )
    """)
    conn.commit()
    conn.close()

init_db()

# 讀取 CSV 題庫
def load_questions():
    questions = []
    with open(QUESTIONS_FILE, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            questions.append(row)
    return questions

questions_data = load_questions()

@app.get("/questions")
def get_questions():
    return {"questions": questions_data}

@app.get("/questions/{question_id}")
def get_question(question_id: int):
    for q in questions_data:
        if int(q["id"]) == question_id:
            return q
    raise HTTPException(status_code=404, detail="Question not found")

@app.post("/answer")
def submit_answer(user_id: str, question_id: int, user_answer: str):
    for q in questions_data:
        if int(q["id"]) == question_id:
            correct = q["correct_answer"].strip().upper() == user_answer.strip().upper()
            
            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO records (user_id, question_id, user_answer, is_correct) VALUES (?, ?, ?, ?)",
                           (user_id, question_id, user_answer, correct))
            conn.commit()
            conn.close()
            
            return {"question_id": question_id, "correct": correct}
    raise HTTPException(status_code=404, detail="Question not found")

@app.get("/records/{user_id}")
def get_user_records(user_id: str):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT question_id, user_answer, is_correct FROM records WHERE user_id = ?", (user_id,))
    records = cursor.fetchall()
    conn.close()
    return {"user_id": user_id, "records": records}

from fastapi import FastAPI, Request, HTTPException, UploadFile, File
from pydantic import BaseModel
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import pandas as pd
import numpy as np
import os
import sqlite3
import io
from datetime import datetime

app = FastAPI()

# --- Khởi tạo thư mục ---
for folder in ["static", "exports", "templates"]:
    if not os.path.exists(folder):
        os.makedirs(folder)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# --- DATABASE SETUP ---
DB_NAME = "history_data.db"
def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS validation_history 
                     (id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp TEXT, total REAL, count INTEGER, status TEXT)''')
init_db()

class NumberListData(BaseModel):
    numbers: str

# --- HÀM XỬ LÝ LOGIC AI (Z-SCORE) ---
def process_validation_logic(valid_numbers):
    if not valid_numbers:
        return {"status": "Reject", "errors": ["Dữ liệu trống"]}

    arr = np.array(valid_numbers)
    total_sum = float(np.sum(arr))
    mean_val = float(np.mean(arr))
    std_val = float(np.std(arr))
    count = len(valid_numbers)

    # Thuật toán Z-Score phát hiện dị thường
    anomalies = []
    ai_score = 100
    if count >= 3 and std_val > 0:
        z_scores = np.abs((arr - mean_val) / std_val)
        anomalies = arr[z_scores > 2.0].tolist()
        ai_score = int(((count - len(anomalies)) / count) * 100)

    status = "Accept" if ai_score >= 70 else "Reject"
    
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("INSERT INTO validation_history (timestamp, total, count, status) VALUES (?, ?, ?, ?)",
                     (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), round(total_sum, 2), count, status))

    return {
        "status": status,
        "sum": total_sum,
        "average": round(mean_val, 2),
        "count": count,
        "ai_score": ai_score,
        "anomalies": anomalies[:10],
        "results": valid_numbers
    }

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/validate")
async def validate_numbers(data: NumberListData):
    try:
        raw_items = data.numbers.replace('\n', ',').split(',')
        numbers = [float(i.strip()) for i in raw_items if i.strip()]
        return process_validation_logic(numbers)
    except:
        return {"status": "Reject", "errors": ["Định dạng số không hợp lệ"]}

@app.post("/upload-excel")
async def upload_excel(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        df = pd.read_excel(io.BytesIO(contents), engine='openpyxl')
        numeric_cols = df.select_dtypes(include=[np.number])
        if numeric_cols.empty:
            return {"status": "Reject", "errors": ["File không có cột số"]}
        all_numbers = numeric_cols.values.flatten()
        cleaned_numbers = all_numbers[~np.isnan(all_numbers)].tolist()
        if not cleaned_numbers:
            return {"status": "Reject", "errors": ["Không tìm thấy dữ liệu số"]}
        return process_validation_logic(cleaned_numbers)
    except Exception as e:
        return {"status": "Reject", "errors": [str(e)]}

@app.post("/export-report")
async def export_report(data: dict):
    try:
        results = data.get('results', [])
        df = pd.DataFrame(results, columns=["Gia_tri"])
        file_path = f"exports/Report_{datetime.now().strftime('%H%M%S')}.xlsx"
        df.to_excel(file_path, index=False)
        return FileResponse(file_path, filename="Bao_cao_AI.xlsx")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/get-history")
async def get_history():
    with sqlite3.connect(DB_NAME) as conn:
        rows = conn.execute("SELECT timestamp, total, status FROM validation_history ORDER BY id DESC LIMIT 5").fetchall()
    return [{"time": r[0], "sum": r[1], "status": r[2]} for r in rows]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
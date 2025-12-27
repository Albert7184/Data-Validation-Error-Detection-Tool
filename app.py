from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel, EmailStr, Field
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import pandas as pd
from fastapi import UploadFile, File
# 1. Khởi tạo ứng dụng
app = FastAPI()

class NumberListData(BaseModel):
    numbers: str

@app.post("/upload-excel")
async def upload_excel(file: UploadFile = File(...)):
    try:
        # Đọc file Excel hoặc CSV
        df = pd.read_excel(file.file) if file.filename.endswith('.xlsx') else pd.read_csv(file.file)
        
        # Giả sử file có cột tên là 'data'
        if 'data' not in df.columns:
            return {"errors": ["File cần có cột tên là 'data'"]}
        
        # Chuyển cột data thành chuỗi để dùng lại logic cũ của bạn
        data_str = ",".join(df['data'].astype(str).tolist())
        
        # Gọi lại logic validate của bạn (hoặc tách logic đó ra hàm riêng để dùng chung)
        # Ở đây mình demo trả về số dòng đã đọc được
        return {
            "message": f"Đã đọc thành công {len(df)} dòng",
            "preview": df.head().to_dict() # Gửi 5 dòng đầu lên web để xem trước
        }
    except Exception as e:
        return {"errors": [f"Lỗi đọc file: {str(e)}"]}

@app.post("/validate")
async def validate_numbers(data: NumberListData):
    # Ghi nhật ký đầu vào để theo dõi (Phần bổ sung)
    print(f"📥 Nhận dữ liệu kiểm tra: {data.numbers}")
    
    raw_list = data.numbers.split(',')
    errors = []
    valid_numbers = []
    duplicates = set()
    seen = set()

    for item in raw_list:
        clean_item = item.strip()
        if clean_item == "": continue
            
        try:
            num = float(clean_item)
            if num < 0 or num > 100:
                errors.append(f"Số {num} nằm ngoài dải cho phép (0-100).")
            else:
                if num in seen:
                    duplicates.add(num)
                else:
                    seen.add(num)
                    valid_numbers.append(num)
        except ValueError:
            errors.append(f"'{clean_item}' không phải là số hợp lệ.")

    stats = {}
    if valid_numbers:
        stats = {
            "total": sum(valid_numbers),
            "average": round(sum(valid_numbers) / len(valid_numbers), 2),
            "count": len(valid_numbers)
        }

    # Ghi nhật ký kết quả phân tích (Phần bổ sung)
    print(f"✅ Kết quả: {len(valid_numbers)} số hợp lệ, {len(errors)} lỗi.")
    
    return {
        "errors": errors,
        "duplicates": list(duplicates),
        "stats": stats
    }

# Cấu hình Static và Templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# --- Giữ nguyên các Logic Validation của bạn ở bên dưới ---

class Product(BaseModel):
    name: str
    price: float = Field(gt=0)
    quantity: int = Field(ge=0)

@app.post("/validate-product/")
async def validate_product(product: Product):
    return {"status": "Hợp lệ", "message": f"Sản phẩm {product.name} đã được kiểm tra!"}

class UserRegistration(BaseModel):
    username: str = Field(min_length=3, max_length=20)
    email: EmailStr
    age: int = Field(ge=18, le=100)

@app.post("/verify-user/")
async def verify_user(user: UserRegistration):
    return {"status": "Thành công", "message": f"Người dùng {user.username} hợp lệ!"}

# API: Kiểm tra Logic thời gian
@app.post("/check-logic/")
async def check_logic(start_year: int, end_year: int):
    if end_year < start_year:
        raise HTTPException(
            status_code=400, 
            detail=f"Lỗi logic: Năm kết thúc ({end_year}) không thể trước năm bắt đầu ({start_year})!"
        )
    duration = end_year - start_year
    return {"status": "Hợp lệ", "duration": duration}
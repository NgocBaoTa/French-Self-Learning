# Mon français — Phase 1

Website học tiếng Pháp cho người học Việt Nam, chạy local trên Windows.

## Yêu cầu

- Windows PowerShell
- Python 3.10+ (đã kiểm tra với Python 3.10.11)
- Node.js 20+ và npm

Không cần Docker, WSL, API key hay dịch vụ trả phí.

## Cài đặt backend

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
python seed.py
```

Nếu PowerShell chặn activate: `Set-ExecutionPolicy -Scope Process Bypass`.

Tạo admin bằng lệnh an toàn, không có password mặc định:

```powershell
python create_admin.py --username admin --password "ThayMatKhauManh"
```

## Cài đặt frontend

Mở PowerShell thứ hai tại thư mục dự án:

```powershell
cd frontend
npm install
```

## Chạy local

PowerShell 1:

```powershell
cd backend
.\.venv\Scripts\Activate.ps1
python app.py
```

PowerShell 2:

```powershell
cd frontend
npm run dev
```

Mở <http://localhost:5173>. Vite proxy `/api` sang Flask ở `http://127.0.0.1:5000`.

## Build và test

```powershell
cd frontend
npm run build

cd ..\backend
.\.venv\Scripts\Activate.ps1
python -m unittest discover tests -v
```

## Dữ liệu, backup và khôi phục

Database nằm ở `backend/instance/monfrancais.sqlite3`; media tương lai sẽ ở `backend/instance/media/`. Dừng Flask trước khi backup:

```powershell
Copy-Item backend\instance\monfrancais.sqlite3 .\backup-monfrancais.sqlite3
```

Khôi phục sau khi dừng Flask bằng cách copy file backup về đúng vị trí. Không xóa database khi khởi động; seed có thể chạy lại mà không xóa tiến độ.

## Kiến trúc và giới hạn Phase 1

- `frontend/`: React UI.
- `backend/app.py`: Flask API và session auth.
- `backend/schema.sql`: schema version 1.
- `backend/seed.py`: seed idempotent nội dung demo.
- `backend/instance/`: dữ liệu local, không commit Git.

Nội dung demo là nội dung gốc, chưa teacher-reviewed, không phải giáo trình đầy đủ hay ngân hàng câu hỏi chính thức. Phase 1 chưa xử lý PDF/OCR/Google Drive/audio và chưa có chấm phát âm AI. TCF/TEF exact simulation chưa được triển khai.

## Troubleshooting

- `python` không nhận: cài Python và bật “Add Python to PATH”, sau đó mở PowerShell mới.
- Lỗi activate: dùng `Set-ExecutionPolicy -Scope Process Bypass`.
- Port 5000 bận: đặt `FLASK_PORT=5001` trong `.env`, rồi đổi proxy trong `frontend/vite.config.js`.
- Muốn xóa dữ liệu local để bắt đầu lại: dừng app, xóa riêng `backend/instance/monfrancais.sqlite3`, sau đó chạy `python seed.py`.


# Mon français — Phase 1

## Mục tiêu

Xây nền tảng học tiếng Pháp A1–A2 cho người học Việt Nam, chạy local trên Windows. Giao diện tiếng Việt; ví dụ và nội dung học bằng tiếng Pháp, có nghĩa tiếng Việt.

## Phạm vi Phase 1

- Tài khoản learner/admin, đăng ký, đăng nhập, đăng xuất và session cookie HttpOnly.
- SQLite với schema versioned đơn giản, dữ liệu tách theo user.
- Dashboard responsive, learning path và navigation khung cho các phase sau.
- Vocabulary cards có tìm kiếm, lọc chủ đề, lật thẻ và tự đánh giá nhớ.
- Quiz trắc nghiệm; đáp án đúng chỉ được chấm ở backend.
- Lưu attempt, review schedule và tiến độ bài học trên backend.
- Seed nội dung gốc: 3 chủ đề, 15 từ, 3 quiz.

## Ngoài phạm vi

Nhập Google Drive/PDF/OCR, audio thật, dictation, recording, spaced repetition nâng cao, admin CRUD UI, TCF/TEF simulation, deployment online.

## Quyết định kỹ thuật

- Frontend: React 18 + Vite + JavaScript, CSS riêng, không dùng CDN/font ngoài.
- Backend: Flask 3 + sqlite3 chuẩn thư viện + Werkzeug password hashing.
- Auth: session server-side lưu token hash trong SQLite; cookie HttpOnly, SameSite=Lax.
- Chấm điểm: server giữ answer_key, frontend chỉ nhận prompt/options.
- Thời gian lưu UTC; timezone mặc định của sản phẩm là America/Toronto.


# Trạng thái

## Phase 1 — hoàn thành local foundation

- [x] React/Vite shell responsive.
- [x] Flask API và SQLite schema.
- [x] Register/login/logout, learner/admin role guard.
- [x] Seed 3 topics, 15 vocabulary items, 3 quiz questions.
- [x] Vocabulary reveal + self-rating lưu vào database.
- [x] Quiz submit chấm ở backend và lưu attempt.
- [x] Dashboard chỉ hiển thị số liệu của user hiện tại.
- [x] Test cô lập account và grading.
- [x] Grammar activities A1–A2, grading backend và lưu attempts.
- [x] Content batch mở rộng: 30 vocabulary items và 9 grammar activities A1–A2.
- [x] Roadmap A0–B2: 95 grammar/vocabulary topics with per-user completed status.
- [x] Vocabulary and grammar tabs list all roadmap topics and roadmap items link to the matching tab.
- [x] Added lesson content for all 95 roadmap topics: overview, objectives, examples and practice prompt.
- [x] Topic lesson view with detailed explanation, notes, key takeaway, exercises and expandable answers.
- [x] Vocabulary lesson now includes searchable list, Vietnamese/English meanings, IPA-style pronunciation, examples and flashcards below.
- [x] Added URL routes: `/vocabulary`, `/vocabulary/<lesson>`, `/grammar`, `/grammar/<lesson>` with browser back/forward support and detail-page back buttons.
- [x] README tiếng Việt và `.env.example`.

## Kiểm tra đã chạy

- `python -m compileall .` trong `backend/` — pass.
- `python -m unittest discover tests -v` trong `backend/` — 5 tests pass.
- `python seed.py` — pass, tạo 3 topics / 15 vocabulary / 3 quizzes.
- `npm run build` trong `frontend/` — pass với Vite 5.4.10.

## Giới hạn còn lại

Chưa có OCR, Drive import, audio, admin content editor, grammar editor, charts nâng cao và deployment online. Không có audio demo giả; các bài nghe sẽ chờ asset người dùng cung cấp.


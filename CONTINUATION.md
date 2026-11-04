# Mon français continuation handoff

Updated: 2026-11-03

## Project

Local Windows French-learning website for Vietnamese learners.

- Backend: Flask + SQLite in `backend/`
- Frontend: React 18 + Vite in `frontend/`
- Database: `backend/instance/monfrancais.sqlite3`
- Run backend: `cd backend; python app.py`
- Run frontend: `cd frontend; npm run dev`
- URL: `http://localhost:5173`

## Implemented

- Imported the supplied French_A0_A1_Vocabulary_REDOWNLOAD.docx: 445 A0-A1 vocabulary entries across 16 roadmap topics, including three newly added A0-A1 topics.
- Imported Tu_vung_tieng_Phap_A1_A2_Mo_rong.docx: 848 A1-A2 vocabulary entries across all 20 topics, with missing roadmap topics added in the A1-A2 section.
- A0-A1 and A1-A2 source vocabulary is linked to exact roadmap lessons through `roadmap_topic_id`; legacy duplicate A1-A2 roadmap entries were removed.
- Added explicit A0-A1 roadmap lessons for housing/interiors, question words/connectors, and months/possessives, with the DOCX vocabulary linked to each lesson.

- Registration, login, logout and learner/admin role structure.
- Dashboard with user-specific review and quiz statistics.
- Vocabulary flashcards with self-rating and review dates.
- Quiz activities with server-side grading.
- Grammar activities with server-side grading and attempts.
- 30 vocabulary words with Vietnamese meaning, English meaning, IPA-style pronunciation and examples.
- 9 grammar activities.
- 95 A0–B2 roadmap topics from the supplied 360-day Word document.
- Per-user roadmap completion state.
- Detailed lesson records for all 95 topics: explanation, objectives, examples, notes, takeaway, exercises and answer guidance.
- URL routing:
  - `/vocabulary` = vocabulary lesson list only.
  - `/vocabulary/<lesson-slug>` = one vocabulary lesson with its word list and flashcards.
  - `/grammar` = grammar lesson list.
  - `/grammar/<lesson-slug>` = one grammar lesson detail page.
  - `/path` = A0–B2 roadmap with completion controls.
- Browser back/forward support and back buttons on lesson pages.

## Important files

- `backend/app.py`: API routes and authentication.
- `backend/schema.sql`: SQLite schema.
- `backend/seed.py`: all demo vocabulary, grammar, roadmap and lesson content.
- `backend/vocabulary_sources/`: all imported vocabulary source files for A0-A1, A1-A2, and future curriculum files.
- `backend/vocabulary_sources/a0_a1_vocabulary.py`: imported A0-A1 source vocabulary.
- `backend/vocabulary_sources/a1_a2_vocabulary.py`: imported A1-A2 source vocabulary.
- `backend/tests/test_app.py`: backend tests.
- `frontend/src/main.jsx`: React UI, routing and lesson pages.
- `frontend/src/styles.css`: UI styling.
- `SOURCES.md`: source inventory and curriculum map.
- `STATUS.md`: project status.
- `PLAN.md`: next planned phases.

## Database tables added for Phase 2

- `grammar_activities`, `grammar_attempts`
- `roadmap_topics`, `roadmap_progress`
- `roadmap_lessons`, `roadmap_lesson_details`
- `vocabulary_details`

## Validation

Last successful checks:

- `python seed.py` — successful.
- `python -m unittest discover tests -v` from `backend/` — 5 tests passed.
- `npm run build` from `frontend/` — successful.

Run `python seed.py` after changing seed content. It is idempotent and preserves user progress.

## Source status

Inspected and used for topic planning:

- Fabulang French reading pages.
- FrancoHub lessons.
- TV5MONDE grammar, vocabulary and exercise pages.
- France Éducation international CEFR/DELF descriptors.
- `C:\Users\baong\Downloads\Lo_trinh_tieng_Phap_A0_den_B2_360_ngay.docx`.

The supplied Google Drive/Docs links were not accessible to the web connector. The large local TENDANCES PDFs and `Sách giao tiếp tiếng Pháp.pdf` were found locally but have not been fully extracted into the app. Do not claim their content has been incorporated until they are successfully read.

## Current vocabulary behavior

The parent `/vocabulary` page intentionally shows only lesson cards. A vocabulary lesson URL shows the lesson detail, vocabulary table, meanings, pronunciation, examples and flashcards. Current seeded words are grouped into the existing broad demo groups: `Chào hỏi & giới thiệu`, `Đời sống hàng ngày`, and `Cuộc sống ở Canada`. Future work should add a precise vocabulary-to-roadmap-topic relation and expand words for every roadmap vocabulary topic.

## Recommended next work

1. Add a `roadmap_topic_id` relation for vocabulary records so each lesson has an exact word set instead of broad demo-group filtering.
2. Expand vocabulary to every A0–B2 vocabulary topic with teacher-reviewed words, meanings, pronunciation and examples.
3. Improve grammar exercises from generic open prompts to several answer-checked exercises per lesson.
4. Add audio/pronunciation assets only when real licensed/user-provided assets are available.
5. Add progress charts and daily study goals.

## Working rule

Before changing content or structure, read this file first, then inspect only the specific files needed. Do not reread the full chat unless a requirement is missing here.

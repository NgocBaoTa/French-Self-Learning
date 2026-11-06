import hashlib, json, os, secrets, sqlite3
from datetime import datetime, timedelta, timezone
from functools import wraps
from pathlib import Path
from flask import Flask, jsonify, request, session, g
from dotenv import load_dotenv
from werkzeug.security import check_password_hash, generate_password_hash

BASE = Path(__file__).resolve().parent
load_dotenv(BASE / '.env')
DB_PATH = Path(os.getenv('DATABASE_PATH', 'instance/monfrancais.sqlite3'))
if not DB_PATH.is_absolute(): DB_PATH = BASE / DB_PATH
DB_PATH.parent.mkdir(parents=True, exist_ok=True)
app = Flask(__name__)
app.config.update(SECRET_KEY=os.getenv('SECRET_KEY','dev-only-change-me'), SESSION_COOKIE_HTTPONLY=True, SESSION_COOKIE_SAMESITE='Lax')

def now(): return datetime.now(timezone.utc)
def iso(dt=None): return (dt or now()).isoformat()
def db():
    if 'db' not in g:
        g.db=sqlite3.connect(DB_PATH); g.db.row_factory=sqlite3.Row; g.db.execute('PRAGMA foreign_keys=ON')
    return g.db
@app.teardown_appcontext
def close_db(_):
    conn=g.pop('db',None)
    if conn: conn.close()
def init_db():
    with app.app_context():
        db().executescript((BASE/'schema.sql').read_text(encoding='utf-8'))
        columns={row['name'] for row in db().execute('PRAGMA table_info(vocabulary)').fetchall()}
        if 'roadmap_topic_id' not in columns:
            db().execute('ALTER TABLE vocabulary ADD COLUMN roadmap_topic_id INTEGER REFERENCES roadmap_topics(id) ON DELETE SET NULL')
        lesson_columns={row['name'] for row in db().execute('PRAGMA table_info(roadmap_lessons)').fetchall()}
        if 'tables_json' not in lesson_columns:
            db().execute("ALTER TABLE roadmap_lessons ADD COLUMN tables_json TEXT NOT NULL DEFAULT '[]'")
        if 'source_content' not in lesson_columns:
            db().execute("ALTER TABLE roadmap_lessons ADD COLUMN source_content TEXT NOT NULL DEFAULT ''")
        db().commit()
def current_user():
    token=session.get('auth_token')
    if not token: return None
    row=db().execute('SELECT u.* FROM users u JOIN sessions s ON s.user_id=u.id WHERE s.token_hash=? AND s.expires_at>?',[hashlib.sha256(token.encode()).hexdigest(),iso()]).fetchone()
    return dict(row) if row else None
def safe_user(u): return {'id':u['id'],'username':u['username'],'role':u['role']}
def login_required(fn):
    @wraps(fn)
    def wrapped(*args,**kwargs):
        user=current_user()
        if not user: return jsonify(error='Bạn cần đăng nhập.'),401
        g.user=user; return fn(*args,**kwargs)
    return wrapped
def admin_required(fn):
    @wraps(fn)
    @login_required
    def wrapped(*args,**kwargs):
        if g.user['role']!='admin': return jsonify(error='Chỉ admin mới có quyền này.'),403
        return fn(*args,**kwargs)
    return wrapped

@app.get('/api/health')
def health(): return jsonify(ok=True)
@app.post('/api/auth/register')
def register():
    data=request.get_json(silent=True) or {}; username=str(data.get('username','')).strip(); password=str(data.get('password',''))
    if len(username)<3 or len(username)>40 or len(password)<8: return jsonify(error='Tên đăng nhập tối thiểu 3 ký tự và mật khẩu tối thiểu 8 ký tự.'),400
    try:
        cur=db().execute('INSERT INTO users(username,password_hash,created_at) VALUES(?,?,?)',[username,generate_password_hash(password),iso()]); db().commit()
    except sqlite3.IntegrityError: return jsonify(error='Tên đăng nhập đã tồn tại.'),409
    return jsonify(user={'id':cur.lastrowid,'username':username,'role':'learner'}),201
@app.post('/api/auth/login')
def login():
    data=request.get_json(silent=True) or {}; user=db().execute('SELECT * FROM users WHERE username=?',[str(data.get('username','')).strip()]).fetchone()
    if not user or not check_password_hash(user['password_hash'],str(data.get('password',''))): return jsonify(error='Sai tên đăng nhập hoặc mật khẩu.'),401
    token=secrets.token_urlsafe(32); db().execute('INSERT INTO sessions VALUES(?,?,?,?)',[hashlib.sha256(token.encode()).hexdigest(),user['id'],iso(),iso(now()+timedelta(days=7))]); db().commit(); session['auth_token']=token
    return jsonify(user=safe_user(user))
@app.post('/api/auth/logout')
def logout(): session.clear(); return jsonify(ok=True)
@app.get('/api/auth/me')
def me():
    user=current_user(); return jsonify(user=safe_user(user) if user else None)

@app.get('/api/dashboard')
@login_required
def dashboard():
    uid=g.user['id']; reviews=db().execute('SELECT COUNT(*) c FROM reviews WHERE user_id=?',[uid]).fetchone()['c']; due=db().execute('SELECT COUNT(*) c FROM reviews WHERE user_id=? AND due_at<=?',[uid,iso()]).fetchone()['c']; attempts=db().execute('SELECT COUNT(*) c,COALESCE(SUM(is_correct),0) correct FROM quiz_attempts WHERE user_id=?',[uid]).fetchone(); topics=db().execute('SELECT id,name,level,description FROM topics ORDER BY id').fetchall()
    return jsonify(stats={'reviewed_words':reviews,'due_words':due,'quiz_attempts':attempts['c'],'quiz_correct':attempts['correct']},topics=[dict(t) for t in topics])
@app.get('/api/roadmap')
@login_required
def roadmap():
    rows=db().execute('SELECT r.*,l.overview,l.objectives_json,l.examples_json,l.tables_json,l.practice_prompt,l.answer_hint,l.source_note,l.source_content,d.detailed_explanation,d.notes,d.takeaway,d.exercises_json,COALESCE(p.completed,0) completed FROM roadmap_topics r JOIN roadmap_lessons l ON l.topic_id=r.id JOIN roadmap_lesson_details d ON d.topic_id=r.id LEFT JOIN roadmap_progress p ON p.topic_id=r.id AND p.user_id=? ORDER BY r.sort_order',[g.user['id']]).fetchall()
    items=[]
    for row in rows:
        item=dict(row); item['objectives']=json.loads(item.pop('objectives_json')); item['examples']=json.loads(item.pop('examples_json')); item['tables']=json.loads(item.pop('tables_json')); item['exercises']=json.loads(item.pop('exercises_json')); items.append(item)
    return jsonify(items=items)
@app.post('/api/roadmap/<int:topic_id>/complete')
@login_required
def complete_roadmap(topic_id):
    topic=db().execute('SELECT id FROM roadmap_topics WHERE id=?',[topic_id]).fetchone()
    if not topic:return jsonify(error='Khong tim thay chu de.'),404
    completed=int(bool((request.get_json(silent=True) or {}).get('completed',False)))
    db().execute('INSERT INTO roadmap_progress(user_id,topic_id,completed,completed_at) VALUES(?,?,?,?) ON CONFLICT(user_id,topic_id) DO UPDATE SET completed=excluded.completed,completed_at=excluded.completed_at',[g.user['id'],topic_id,completed,iso() if completed else None]);db().commit()
    return jsonify(ok=True,completed=completed)
@app.get('/api/vocabulary')
@login_required
def vocabulary():
    rows=db().execute('SELECT v.*,t.name topic_name,t.level,d.pronunciation,r.title roadmap_topic_title FROM vocabulary v JOIN topics t ON t.id=v.topic_id LEFT JOIN vocabulary_details d ON d.vocabulary_id=v.id LEFT JOIN roadmap_topics r ON r.id=v.roadmap_topic_id ORDER BY v.id').fetchall(); return jsonify(items=[dict(r) for r in rows])
@app.post('/api/vocabulary/<int:vid>/review')
@login_required
def review(vid):
    rating=int((request.get_json(silent=True) or {}).get('rating',0))
    if rating not in (1,2,3): return jsonify(error='Rating phải từ 1 đến 3.'),400
    if not db().execute('SELECT id FROM vocabulary WHERE id=?',[vid]).fetchone(): return jsonify(error='Không tìm thấy từ.'),404
    due=now()+timedelta(days={1:1,2:3,3:7}[rating]); db().execute('INSERT INTO reviews(user_id,vocabulary_id,rating,review_count,last_reviewed_at,due_at) VALUES(?,?,?,?,?,?) ON CONFLICT(user_id,vocabulary_id) DO UPDATE SET rating=excluded.rating,review_count=reviews.review_count+1,last_reviewed_at=excluded.last_reviewed_at,due_at=excluded.due_at',[g.user['id'],vid,rating,1,iso(),iso(due)]); db().commit(); return jsonify(ok=True,due_at=iso(due))
@app.get('/api/quizzes')
@login_required
def quizzes():
    rows=db().execute('SELECT id,topic_id,prompt,options_json FROM quizzes ORDER BY id').fetchall(); return jsonify(items=[{'id':r['id'],'topic_id':r['topic_id'],'prompt':r['prompt'],'options':json.loads(r['options_json'])} for r in rows])
@app.post('/api/quizzes/<int:qid>/submit')
@login_required
def submit_quiz(qid):
    answer=str((request.get_json(silent=True) or {}).get('answer','')); q=db().execute('SELECT * FROM quizzes WHERE id=?',[qid]).fetchone()
    if not q: return jsonify(error='Không tìm thấy câu hỏi.'),404
    correct=answer==q['answer_key']; db().execute('INSERT INTO quiz_attempts(user_id,quiz_id,answer,is_correct,created_at) VALUES(?,?,?,?,?)',[g.user['id'],qid,answer,int(correct),iso()]); db().commit(); return jsonify(correct=correct,explanation=q['explanation'])

@app.get('/api/grammar')
@login_required
def grammar():
    rows=db().execute('SELECT id,topic_id,title,level,instruction,prompt,options_json FROM grammar_activities ORDER BY id').fetchall()
    return jsonify(items=[{'id':r['id'],'topic_id':r['topic_id'],'title':r['title'],'level':r['level'],'instruction':r['instruction'],'prompt':r['prompt'],'options':json.loads(r['options_json'])} for r in rows])

@app.post('/api/grammar/<int:aid>/submit')
@login_required
def submit_grammar(aid):
    answer=str((request.get_json(silent=True) or {}).get('answer','')); activity=db().execute('SELECT * FROM grammar_activities WHERE id=?',[aid]).fetchone()
    if not activity: return jsonify(error='Khong tim thay hoat dong ngu phap.'),404
    correct=answer==activity['answer_key']; db().execute('INSERT INTO grammar_attempts(user_id,activity_id,answer,is_correct,created_at) VALUES(?,?,?,?,?)',[g.user['id'],aid,answer,int(correct),iso()]); db().commit()
    return jsonify(correct=correct,explanation=activity['explanation'])

if __name__=='__main__':
    init_db(); app.run(host=os.getenv('FLASK_HOST','127.0.0.1'),port=int(os.getenv('FLASK_PORT','5000')),debug=True)


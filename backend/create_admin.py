import argparse
from app import app,db,init_db,iso
from werkzeug.security import generate_password_hash
p=argparse.ArgumentParser(); p.add_argument('--username',required=True); p.add_argument('--password',required=True); a=p.parse_args()
with app.app_context():
    init_db(); db().execute('INSERT INTO users(username,password_hash,role,created_at) VALUES(?,?,?,?) ON CONFLICT(username) DO UPDATE SET password_hash=excluded.password_hash,role="admin"',(a.username,generate_password_hash(a.password),'admin',iso())); db().commit(); print('Đã tạo/cập nhật admin:',a.username)


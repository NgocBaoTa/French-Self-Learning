import tempfile,unittest
from pathlib import Path
import app as m
class Phase1Tests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory(); m.DB_PATH=Path(self.tmp.name)/'test.sqlite3'; m.init_db(); self.c=m.app.test_client()
  with m.app.app_context():
   m.db().execute("INSERT INTO topics(slug,name,level,description) VALUES('t','Test','A1','test')"); m.db().execute("INSERT INTO vocabulary(topic_id,french,part_of_speech,gender,vietnamese,english,example_fr,example_vi) VALUES(1,'bonjour','x','','xin chào','hello','Bonjour','Xin chào')"); m.db().execute("INSERT INTO quizzes(topic_id,prompt,options_json,answer_key,explanation) VALUES(1,'q','[\"a\",\"b\"]','a','ok')"); m.db().commit()
 def tearDown(self): self.tmp.cleanup()
 def login(self,n): self.c.post('/api/auth/register',json={'username':n,'password':'password123'}); return self.c.post('/api/auth/login',json={'username':n,'password':'password123'})
 def test_isolation(self): self.login('alice'); self.c.post('/api/vocabulary/1/review',json={'rating':3}); self.c.post('/api/auth/logout'); self.login('bob'); self.assertEqual(self.c.get('/api/dashboard').json['stats']['reviewed_words'],0)
 def test_quiz_persists(self): self.login('alice'); self.assertTrue(self.c.post('/api/quizzes/1/submit',json={'answer':'a'}).json['correct']); self.assertEqual(self.c.get('/api/dashboard').json['stats']['quiz_correct'],1)
 def test_auth_required(self): self.assertEqual(self.c.get('/api/vocabulary').status_code,401)
 def test_grammar_grading_and_persistence(self):
  with m.app.app_context(): m.db().execute("INSERT INTO grammar_activities(topic_id,title,level,instruction,prompt,options_json,answer_key,explanation) VALUES(1,'Articles','A1','Choose','___ famille','[\"Un\",\"Une\"]','Une','Famille is feminine')"); m.db().commit()
  self.login('alice'); self.assertEqual(self.c.get('/api/grammar').json['items'][0]['options'],['Un','Une']); result=self.c.post('/api/grammar/1/submit',json={'answer':'Une'}).json; self.assertTrue(result['correct'])
 def test_roadmap_completion_is_user_scoped(self):
  with m.app.app_context(): m.db().execute("INSERT INTO roadmap_topics(kind,level,stage,day_start,day_end,title,description,sort_order) VALUES('grammar','A0-A1','A0-A1',1,3,'Test topic','test',1)"); m.db().execute("INSERT INTO roadmap_lessons(topic_id,overview,objectives_json,examples_json,practice_prompt,answer_hint,source_note) VALUES(1,'overview','[\"goal\"]','[\"example\"]','practice','hint','source')"); m.db().execute("INSERT INTO roadmap_lesson_details(topic_id,detailed_explanation,notes,takeaway,exercises_json) VALUES(1,'detail','note','takeaway','[{\"prompt\":\"exercise\",\"answer\":\"answer\"}]')"); m.db().commit()
  self.login('alice'); self.assertFalse(self.c.get('/api/roadmap').json['items'][0]['completed']); self.assertTrue(self.c.post('/api/roadmap/1/complete',json={'completed':True}).json['completed']); self.assertTrue(self.c.get('/api/roadmap').json['items'][0]['completed']); self.c.post('/api/auth/logout'); self.login('bob'); self.assertFalse(self.c.get('/api/roadmap').json['items'][0]['completed'])
if __name__=='__main__': unittest.main()


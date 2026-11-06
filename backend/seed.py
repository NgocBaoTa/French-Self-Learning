import json
from app import app,db,init_db
from pathlib import Path
import zipfile
from xml.etree import ElementTree as ET
from vocabulary_sources.a0_a1_vocabulary import A0_A1_VOCABULARY
from vocabulary_sources.a1_a2_vocabulary import A1_A2_VOCABULARY
from vocabulary_sources.b1_vocabulary import B1_VOCABULARY
from vocabulary_sources.b2_vocabulary import B2_VOCABULARY
TOPICS=[('premiers-pas','Chào hỏi & giới thiệu','A1','Bắt đầu một cuộc trò chuyện tự nhiên.'),('vie-quotidienne','Đời sống hằng ngày','A1','Những từ dùng khi mua sắm và đi lại.'),('canada','Cuộc sống ở Canada','A2','Giao tiếp trong học tập và công việc.')]
WORDS=[('premiers-pas','bonjour','interjection','', 'xin chào','hello','Bonjour, comment allez-vous ?','Xin chào, bạn khỏe không?'),('premiers-pas','s’appeler','verbe','', 'tên là','to be called','Je m’appelle Linh.','Tôi tên là Linh.'),('premiers-pas','enchanté','adjectif','', 'rất vui được gặp','delighted','Enchanté de faire votre connaissance.','Rất vui được làm quen với bạn.'),('premiers-pas','la famille','nom','f', 'gia đình','family','Ma famille habite à Toronto.','Gia đình tôi sống ở Toronto.'),('premiers-pas','travailler','verbe','', 'làm việc','to work','Je travaille dans une école.','Tôi làm việc ở một trường học.'),('vie-quotidienne','le marché','nom','m', 'chợ','market','Je vais au marché samedi.','Tôi đi chợ vào thứ bảy.'),('vie-quotidienne','acheter','verbe','', 'mua','to buy','Je voudrais acheter du pain.','Tôi muốn mua bánh mì.'),('vie-quotidienne','combien','adverbe','', 'bao nhiêu','how much','Combien coûte ce livre ?','Cuốn sách này giá bao nhiêu?'),('vie-quotidienne','à gauche','locution','', 'bên trái','on the left','La banque est à gauche.','Ngân hàng ở bên trái.'),('vie-quotidienne','le billet','nom','m', 'vé','ticket','Un billet pour Montréal, s’il vous plaît.','Cho tôi một vé đi Montréal.'),('canada','le quartier','nom','m', 'khu phố','neighborhood','Mon quartier est calme.','Khu phố của tôi yên tĩnh.'),('canada','un rendez-vous','nom','m', 'cuộc hẹn','appointment','J’ai un rendez-vous demain.','Tôi có cuộc hẹn ngày mai.'),('canada','le travail','nom','m', 'công việc','work','Le travail commence à neuf heures.','Công việc bắt đầu lúc chín giờ.'),('canada','la neige','nom','f', 'tuyết','snow','La neige tombe en hiver.','Tuyết rơi vào mùa đông.'),('canada','bienvenue','nom','', 'chào mừng','welcome','Bienvenue au Canada !','Chào mừng đến Canada!')]
QUIZZES=[('premiers-pas','“Bonjour” có nghĩa là gì?',['Xin chào','Tạm biệt','Cảm ơn'],'Xin chào','Bonjour là lời chào.'),('vie-quotidienne','Chọn câu có nghĩa “Tôi muốn mua bánh mì”.',['Je vais au marché.','Je voudrais acheter du pain.','La banque est à gauche.'],'Je voudrais acheter du pain.','“Je voudrais acheter” nghĩa là “Tôi muốn mua”.'),('canada','“La neige” là gì?',['mưa','tuyết','gió'],'tuyết','Neige là tuyết.')]
GRAMMAR=[('premiers-pas','Articles: un, une, des','A1',"Choisissez l'article correct.",'___ famille habite a Toronto.',['Un','Une','Des'],'Une','Famille est un nom feminin.'),('vie-quotidienne','Le present des verbes en -er','A1','Choisissez la bonne forme du verbe.','Je ___ au marche le samedi.',['vais','va','allez'],'vais','Avec je, le verbe aller devient vais.'),('canada','La negation avec ne...pas','A2','Completez la phrase negative.','Je ___ travaille ___ dimanche.',['ne / pas','pas / ne','ne / jamais'],'ne / pas','La negation standard encadre le verbe: ne ... pas.')]
EXTRA_WORDS=[('premiers-pas','salut','interjection','', 'xin chào thân mật','hi','Salut, ça va ?','Chào, bạn khỏe không?'),('premiers-pas','au revoir','locution','', 'tạm biệt','goodbye','Au revoir et à demain.','Tạm biệt và hẹn gặp ngày mai.'),('premiers-pas','habiter','verbe','', 'sống ở','to live','J’habite à Toronto.','Tôi sống ở Toronto.'),('premiers-pas','aimer','verbe','', 'thích','to like','J’aime lire en français.','Tôi thích đọc bằng tiếng Pháp.'),('premiers-pas','aujourd’hui','adverbe','', 'hôm nay','today','Aujourd’hui, je travaille.','Hôm nay tôi làm việc.'),('vie-quotidienne','la boulangerie','nom','f', 'tiệm bánh','bakery','La boulangerie est près du marché.','Tiệm bánh gần khu chợ.'),('vie-quotidienne','le prix','nom','m', 'giá','price','Quel est le prix de ce livre ?','Giá của quyển sách này là bao nhiêu?'),('vie-quotidienne','prendre','verbe','', 'đi/bắt/dùng','to take','Je prends le métro.','Tôi đi tàu điện ngầm.'),('vie-quotidienne','tout droit','locution','', 'thẳng về phía trước','straight ahead','Allez tout droit, puis tournez à gauche.','Đi thẳng, sau đó rẽ trái.'),('vie-quotidienne','la réservation','nom','f', 'đặt chỗ','reservation','J’ai une réservation pour deux personnes.','Tôi có đặt chỗ cho hai người.'),('canada','le logement','nom','m', 'chỗ ở','housing','Je cherche un logement calme.','Tôi đang tìm chỗ ở yên tĩnh.'),('canada','le voisin','nom','m', 'hàng xóm nam','neighbour','Mon voisin parle français.','Hàng xóm của tôi nói tiếng Pháp.'),('canada','la réunion','nom','f', 'cuộc họp','meeting','La réunion commence à neuf heures.','Cuộc họp bắt đầu lúc chín giờ.'),('canada','postuler','verbe','', 'nộp đơn ứng tuyển','to apply','Je voudrais postuler à ce poste.','Tôi muốn ứng tuyển vị trí này.'),('canada','l’hiver','nom','m', 'mùa đông','winter','L’hiver est froid au Canada.','Mùa đông ở Canada lạnh.')]
PRONUNCIATIONS=['/bɔ̃.ʒuʁ/','/s‿a.pe.le/','/ɑ̃.ʃɑ̃.te/','/la fa.mij/','/tʁa.va.je/','/lə maʁ.ʃe/','/aʃ.te/','/kɔ̃.bjɛ̃/','/a ɡoʃ/','/lə bi.jɛ/','/lə kaʁ.tje/','/œ̃ ʁɑ̃.de.vu/','/lə tʁa.vaj/','/la nɛʒ/','/bjɛ̃.və.ny/','/sa.ly/','/o ʁə.vwaʁ/','/a.bi.te/','/e.me/','/o.ʒuʁ.dɥi/','/la bu.lɑ̃.ʒə.ʁi/','/lə pʁi/','/pʁɑ̃dʁ/','/tu dʁwa/','/la ʁe.zɛʁ.va.sjɔ̃/','/lə lɔʒ.mɑ̃/','/lə vwɛ.zɛ̃/','/la ʁe.y.njɔ̃/','/pɔʁ.ty.le/','/li.vɛʁ/']
EXTRA_GRAMMAR=[('premiers-pas','Les pronoms sujets','A1','Choisissez le pronom correct.','___ habite à Montréal.',['Je','Nous','Vous'],'Je','Le verbe habite correspond à je.'),('premiers-pas','La question avec est-ce que','A1','Choisissez la question correcte.','___ vous aimez le café ?',['Est-ce que','Pourquoi est-ce','Comment est-ce'],'Est-ce que','Est-ce que introduit une question oui/non.'),('vie-quotidienne','Les adjectifs possessifs','A1','Choisissez le possessif correct.','C’est ___ billet.',['mon','ma','mes'],'mon','Billet est masculin singulier: mon billet.'),('vie-quotidienne','Les prépositions de lieu','A1','Choisissez la préposition correcte.','La banque est ___ gauche.',['à','en','au'],'à','On dit à gauche et à droite.'),('canada','Le passé composé','A2','Choisissez la bonne forme.','Hier, j’___ travaillé.',['ai','as','suis'],'ai','Avec travailler, on utilise avoir: j’ai travaillé.'),('canada','Le futur proche','A2','Choisissez la bonne structure.','Nous ___ visiter Montréal demain.',['allons','avons','sommes'],'allons','Le futur proche se forme avec aller + infinitif.')]
def load_grammar_source():
    source_path=Path(__file__).resolve().parent.parent/'docs'/'sources'/'French_Grammar_A1.docx'
    with zipfile.ZipFile(source_path) as archive:
        root=ET.fromstring(archive.read('word/document.xml'))
    ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    blocks=[]
    for node in root.find('w:body',ns):
        if node.tag.endswith('}p'):
            text=''.join(node.itertext()).strip()
            if not text: continue
            kind='paragraph'
            if text.startswith('CHƯƠNG '): kind='chapter'
            elif text.startswith('Tổng kết chương') or text.startswith('BẢNG TRA CỨU NHANH'): kind='summary'
            elif text[:1].isdigit() and '.' in text[:4]: kind='section'
            elif text.startswith('Mục tiêu học tập'): kind='intro'
            blocks.append({'type':kind,'text':text})
        elif node.tag.endswith('}tbl'):
            rows=[]
            for row in node.findall('w:tr',ns):
                cells=[]
                for cell in row.findall('w:tc',ns):
                    cells.append(' '.join(''.join(p.itertext()) for p in cell.findall('.//w:p',ns)).strip())
                rows.append(cells)
            if rows: blocks.append({'type':'table','rows':rows})
    starts=[index for index,block in enumerate(blocks) if block['type']=='chapter']
    return [blocks[start:end] for start,end in zip(starts,starts[1:]+[len(blocks)])]

GRAMMAR_SOURCE_CONTENTS=load_grammar_source()[:5]
VOCABULARY_ROADMAP_INDEXES=[1,1,1,4,5, 9,9,9,10,14, 17,19,19,12,1, 1,1,5,13,7, 9,9,14,10,15, 17,17,19,19,12]
ROADMAP=[
('grammar','A0-A1','A0-A1',1,30,'Phát âm nền tảng','Bảng chữ cái, dấu phụ, âm mũi, liaison, enchaînement, âm câm và ngữ điệu.'),
('grammar','A0-A1','A0-A1',1,30,'Cấu trúc câu cơ bản','Trật tự chủ ngữ - động từ - bổ ngữ; c’est, ce sont và il y a.'),
('grammar','A0-A1','A0-A1',1,30,'Đại từ chủ ngữ','Je, tu, il, elle, on, nous, vous, ils, elles.'),
('grammar','A0-A1','A0-A1',1,30,'Giống và số','Giống, số của danh từ và hòa hợp cơ bản của tính từ.'),
('grammar','A0-A1','A0-A1',1,30,'Mạo từ','Le, la, l’, les; un, une, des; du, de la, de l’.'),
('grammar','A0-A1','A0-A1',1,30,'Động từ hiện tại','Être, avoir, aller, faire, động từ -er và -ir thông dụng.'),
('grammar','A0-A1','A0-A1',1,30,'Động từ phản thân và phủ định','Các động từ phản thân; ne...pas và ne...jamais cơ bản.'),
('grammar','A0-A1','A0-A1',1,30,'Câu hỏi','Ngữ điệu, est-ce que, đảo ngữ và từ hỏi thông dụng.'),
('grammar','A0-A1','A0-A1',1,30,'Sở hữu và chỉ định','Mon/ma/mes và ce/cet/cette/ces.'),
('grammar','A0-A1','A0-A1',1,30,'Giới từ và co rút','À, de, en, au, aux, chez, dans, sur, sous và các dạng co rút.'),
('grammar','A0-A1','A0-A1',1,30,'Tương lai gần và mệnh lệnh','Aller + infinitif và impératif cơ bản.'),
('grammar','A0-A1','A0-A1',1,30,'Số và thời gian','Số đếm, số thứ tự, giờ, ngày tháng và lịch.'),
('grammar','A0-A1','A0-A1',1,30,'So sánh cơ bản','Plus, moins, aussi...que trong tình huống quen thuộc.'),
('grammar','A1-A2','A1-A2',46,120,'Passé composé','Passé composé với avoir và être, participe passé và động từ phản thân.'),
('grammar','A1-A2','A1-A2',46,120,'Hòa hợp participe passé','Hòa hợp với être và nguyên tắc cơ bản với avoir.'),
('grammar','A1-A2','A1-A2',46,120,'Imparfait','Hình thành, thói quen và bối cảnh; đối chiếu với passé composé.'),
('grammar','A1-A2','A1-A2',46,120,'Tương lai đơn','Futur simple và so sánh với futur proche.'),
('grammar','A1-A2','A1-A2',46,120,'COD và COI','Me, te, le, la, nous, vous, les, lui, leur và vị trí đại từ.'),
('grammar','A1-A2','A1-A2',46,120,'Y và en','Cách dùng thông dụng của y, en và đại từ nhấn mạnh.'),
('grammar','A1-A2','A1-A2',46,120,'Đại từ quan hệ cơ bản','Qui, que và où trong câu đơn giản.'),
('grammar','A1-A2','A1-A2',46,120,'Số lượng và đại từ bất định','Quelqu’un, quelque chose, tout, chaque, plusieurs, beaucoup de, peu de.'),
('grammar','A1-A2','A1-A2',46,120,'Phủ định mở rộng','Ne...plus, ne...rien, ne...personne và ne...aucun.'),
('grammar','A1-A2','A1-A2',46,120,'So sánh và siêu cấp','So sánh hơn, bằng, kém; le plus, le moins, meilleur và mieux.'),
('grammar','A1-A2','A1-A2',46,120,'Động từ khuyết thiếu','Vouloir, pouvoir, devoir, savoir và il faut + infinitif.'),
('grammar','A1-A2','A1-A2',46,120,'Liên từ và thời gian','Parce que, car, donc, mais, quand, si, puis, ensuite; depuis, pendant, il y a, dans, pour.'),
('grammar','A1-A2','A1-A2',46,120,'Chức năng giao tiếp','Sở thích, ý định, lời mời, yêu cầu lịch sự và venir de + infinitif.'),
('grammar','B1','B1',121,240,'Plus-que-parfait','Thứ tự thời gian trong câu chuyện và kể lại sự kiện.'),
('grammar','B1','B1',121,240,'Conditionnel présent','Giả định, mong muốn, đề nghị và si + imparfait.'),
('grammar','B1','B1',121,240,'Subjonctif présent','Il faut que, vouloir que, cảm xúc và sự cần thiết.'),
('grammar','B1','B1',121,240,'Đại từ quan hệ mở rộng','Dont, où, ce qui, ce que và ce dont.'),
('grammar','B1','B1',121,240,'Phối hợp đại từ','COD/COI, y, en với infinitif và impératif.'),
('grammar','B1','B1',121,240,'Câu bị động','Être + participe passé và tác nhân par/de.'),
('grammar','B1','B1',121,240,'Discours indirect','Tường thuật lời nói và câu hỏi gián tiếp cơ bản.'),
('grammar','B1','B1',121,240,'Gérondif','En + participe présent ở mức giới thiệu.'),
('grammar','B1','B1',121,240,'Liên kết ý','Nguyên nhân, hệ quả, mục đích, đối lập và nhượng bộ.'),
('grammar','B1','B1',121,240,'Từ nối đoạn văn','Kể chuyện, nêu ví dụ, giải thích và kết luận.'),
('grammar','B1','B1',121,240,'Diễn đạt ý kiến','Je pense que, je ne pense pas que, il me semble que.'),
('grammar','B2','B2',241,360,'Subjonctif nâng cao','Bien que, pour que, afin que, à condition que, avant que.'),
('grammar','B2','B2',241,360,'Conditionnel passé','Giả định, hối tiếc và thông tin chưa xác nhận.'),
('grammar','B2','B2',241,360,'Phối hợp thì','Concordance des temps trong tường thuật và lập luận.'),
('grammar','B2','B2',241,360,'Discours indirect nâng cao','Thay đổi đại từ, trạng từ thời gian và cấu trúc tường thuật.'),
('grammar','B2','B2',241,360,'Mệnh đề rút gọn','Participe présent, gérondif và adjectif verbal.'),
('grammar','B2','B2',241,360,'Danh hóa và bị động','Câu bị động nâng cao và nominalisation.'),
('grammar','B2','B2',241,360,'Đại từ quan hệ nâng cao','Lequel, laquelle, lesquels, auxquelles và duquel.'),
('grammar','B2','B2',241,360,'Liên từ nâng cao','Nguyên nhân, hệ quả, mục đích, điều kiện, đối lập và nhượng bộ.'),
('grammar','B2','B2',241,360,'Nhấn mạnh','C’est...qui/que và nhận diện đảo ngữ văn phong.'),
('grammar','B2','B2',241,360,'Liên kết logic và sắc thái','Pourtant, toutefois, néanmoins, en revanche, par conséquent.'),
('grammar','B2','B2',241,360,'Văn phong và lập luận','Mức độ chắc chắn, giả thuyết, văn phong trang trọng và phản biện.'),
('vocabulary','A0-A1','A0-A1',1,30,'Chào hỏi và tự giới thiệu','Chào hỏi, tạm biệt, phép lịch sự và giới thiệu bản thân.'),
('vocabulary','A0-A1','A0-A1',1,30,'Quốc gia và ngôn ngữ','Quốc tịch, ngôn ngữ, quốc gia và thành phố.'),
('vocabulary','A0-A1','A0-A1',1,30,'Số và lịch','Số đếm, tuổi, ngày tháng, thời gian và lịch.'),
('vocabulary','A0-A1','A0-A1',1,30,'Gia đình','Gia đình, họ hàng và tình trạng hôn nhân.'),
('vocabulary','A0-A1','A0-A1',1,30,'Nghề nghiệp và học tập','Nghề nghiệp, nơi làm việc, trường học và môn học.'),
('vocabulary','A0-A1','A0-A1',1,30,'Nhà cửa','Phòng, đồ nội thất và vật dụng trong nhà.'),
('vocabulary','A0-A1','A0-A1',1,30,'Thói quen hằng ngày','Hoạt động trong ngày và lịch trình cá nhân.'),
('vocabulary','A0-A1','A0-A1',1,30,'Thức ăn và nhà hàng','Thức ăn, đồ uống, gọi món và thanh toán.'),
('vocabulary','A0-A1','A0-A1',1,30,'Mua sắm','Quần áo, màu sắc, kích cỡ và giá cả.'),
('vocabulary','A0-A1','A0-A1',1,30,'Thành phố và phương hướng','Địa điểm, chỉ đường, phương hướng và giao thông.'),
('vocabulary','A0-A1','A0-A1',1,30,'Ngoại hình và cảm xúc','Ngoại hình, tính cách và cảm xúc cơ bản.'),
('vocabulary','A0-A1','A0-A1',1,30,'Thời tiết và thiên nhiên','Thời tiết, mùa và thiên nhiên thông dụng.'),
('vocabulary','A0-A1','A0-A1',1,30,'Sở thích và cuối tuần','Sở thích, thể thao, giải trí và hoạt động cuối tuần.'),
('vocabulary','A1-A2','A1-A2',46,120,'Du lịch và phương tiện','Phương tiện, sân bay, ga tàu, khách sạn và tham quan.'),
('vocabulary','A1-A2','A1-A2',46,120,'Đặt chỗ và hỏi thông tin','Đặt phòng, đặt bàn, hỏi giá và hỏi thông tin.'),
('vocabulary','A1-A2','A1-A2',46,120,'Sức khỏe','Cơ thể, triệu chứng, khám bệnh và mua thuốc.'),
('vocabulary','A1-A2','A1-A2',46,120,'Nhà ở và khu phố','Thuê nhà, tiện ích, khu phố và hàng xóm.'),
('vocabulary','A1-A2','A1-A2',46,120,'Lễ hội và lời mời','Sinh nhật, tiệc, lời mời và quà tặng.'),
('vocabulary','A1-A2','A1-A2',46,120,'Công việc và ứng tuyển','Nhiệm vụ, lịch làm việc và đơn xin việc.'),
('vocabulary','A1-A2','A1-A2',46,120,'Học tập và thi cử','Khóa học, thi cử và kế hoạch học.'),
('vocabulary','A1-A2','A1-A2',46,120,'Dịch vụ và khiếu nại','Đổi trả, bảo hành và khiếu nại cơ bản.'),
('vocabulary','A1-A2','A1-A2',46,120,'Trải nghiệm và kỷ niệm','Sự kiện quá khứ, trải nghiệm và kỷ niệm.'),
('vocabulary','A1-A2','A1-A2',46,120,'Kế hoạch tương lai','Mục tiêu, ước mơ và kế hoạch.'),
('vocabulary','A1-A2','A1-A2',46,120,'Tin nhắn và email','Email, tin nhắn, lời cảm ơn và xin lỗi.'),
('vocabulary','B1','B1',121,240,'Giáo dục và việc làm','Hệ thống trường học, học trực tuyến, tuyển dụng và phỏng vấn.'),
('vocabulary','B1','B1',121,240,'Quan hệ xã hội','Tình bạn, gia đình, xung đột và quan hệ xã hội.'),
('vocabulary','B1','B1',121,240,'Sức khỏe và lối sống','Sức khỏe thể chất, tinh thần, lối sống và thể thao.'),
('vocabulary','B1','B1',121,240,'Môi trường','Rác thải, tái chế, khí hậu và phát triển bền vững.'),
('vocabulary','B1','B1',121,240,'Công nghệ và truyền thông','Internet, điện thoại, mạng xã hội, tin tức và quảng cáo.'),
('vocabulary','B1','B1',121,240,'Văn hóa và nghệ thuật','Điện ảnh, sách, âm nhạc và trải nghiệm văn hóa.'),
('vocabulary','B1','B1',121,240,'Đời sống đô thị','Nhà ở, giao thông và đời sống đô thị/nông thôn.'),
('vocabulary','B1','B1',121,240,'Tiêu dùng và ngân sách','Mua sắm, tiền bạc và ngân sách cá nhân.'),
('vocabulary','B1','B1',121,240,'Ý kiến và cảm xúc','Ưu điểm, nhược điểm, đồng ý, phản đối, lý do và ví dụ.'),
('vocabulary','B2','B2',241,360,'Giáo dục đại học','Bình đẳng cơ hội, đào tạo nghề và chính sách giáo dục.'),
('vocabulary','B2','B2',241,360,'Thị trường lao động','Làm việc từ xa, tự động hóa và nghề nghiệp tương lai.'),
('vocabulary','B2','B2',241,360,'AI và đạo đức công nghệ','Quyền riêng tư, bảo mật dữ liệu và đạo đức công nghệ.'),
('vocabulary','B2','B2',241,360,'Kinh tế và bất bình đẳng','Lạm phát, chi phí sinh hoạt và bất bình đẳng.'),
('vocabulary','B2','B2',241,360,'Chính trị và công dân','Thể chế công, chính sách xã hội, quyền và trách nhiệm.'),
('vocabulary','B2','B2',241,360,'Y tế công cộng','Phòng bệnh và hệ thống chăm sóc sức khỏe.'),
('vocabulary','B2','B2',241,360,'Di cư và đa văn hóa','Hội nhập, bản sắc văn hóa và đa văn hóa.'),
('vocabulary','B2','B2',241,360,'Báo chí và kiểm chứng','Báo chí, truyền thông và kiểm chứng thông tin.'),
('vocabulary','B2','B2',241,360,'Khoa học và dữ liệu','Nghiên cứu, dữ liệu, bằng chứng và rủi ro.'),
('vocabulary','B2','B2',241,360,'Văn hóa và phê bình','Văn hóa, nghệ thuật, phê bình và sáng tạo.'),
('vocabulary','B2','B2',241,360,'Toàn cầu hóa','Quan hệ quốc tế, hợp tác và toàn cầu hóa.'),
('vocabulary','B2','B2',241,360,'Lập luận và tranh luận','Nguyên nhân, hệ quả, nhượng bộ, giả định và thuyết phục.'),
('vocabulary','B2','B2',241,360,'Văn bản trang trọng','Đơn kiến nghị, thư khiếu nại và bài luận.'),
('vocabulary','B2','B2',241,360,'Từ vựng sắc thái','Nuance, degré, probabilité và incertitude.')]

GRAMMAR_EXAMPLES={
 'Mạo từ':('Le/la/les désignent une chose connue; un/une/des introduisent une chose nouvelle.', ['J’ai un livre. Le livre est intéressant.','Je bois du café.']),
 'Đại từ chủ ngữ':('Le pronom indique qui fait l’action; le verbe s’accorde avec lui.', ['Je travaille à Toronto.','Nous étudions le français.']),
 'Câu hỏi':('Utilisez l’intonation, est-ce que ou l’inversion selon le registre.', ['Tu habites où ?','Est-ce que vous avez une réservation ?']),
 'Phủ định mở rộng':('Placez ne et le deuxième mot de négation autour du verbe.', ['Je ne travaille plus ici.','Elle ne connaît personne.']),
 'Passé composé':('Utilisez avoir ou être au présent avec un participe passé pour raconter une action terminée.', ['J’ai visité Montréal.','Elle est arrivée à huit heures.']),
 'Imparfait':('Utilisez l’imparfait pour le contexte, les habitudes et les descriptions dans le passé.', ['Quand j’étais petit, je lisais beaucoup.','Il faisait froid.']),
 'Tương lai đơn':('Le futur simple exprime un projet ou une prévision située dans l’avenir.', ['Je prendrai le train demain.','Nous visiterons Québec.']),
 'Conditionnel présent':('Le conditionnel rend une demande plus douce et exprime une hypothèse.', ['Je voudrais un café, s’il vous plaît.','On pourrait commencer à neuf heures.']),
 'Subjonctif présent':('Le subjonctif suit certaines expressions de nécessité, volonté, émotion ou doute.', ['Il faut que tu viennes.','Je veux qu’elle réussisse.']),
 'Câu bị động':('La voix passive met l’action ou le résultat au premier plan.', ['Le dossier est envoyé par courriel.','La décision a été annoncée hier.']),
 'Discours indirect':('Le discours indirect rapporte une parole sans répéter exactement la phrase originale.', ['Elle dit qu’elle est prête.','Il demande si nous avons compris.']),
 'Lập luận và tranh luận':('Organisez une opinion avec une idée, une raison, un exemple et une conclusion.', ['Je suis d’accord parce que…','Cependant, il faut aussi considérer…'])}
ROADMAP += [
('vocabulary','A0-A1','A0-A1',1,30,'Phương tiện giao thông và du lịch cơ bản','Phương tiện giao thông và các tình huống du lịch cơ bản cho A0–A1.'),
('vocabulary','A0-A1','A0-A1',1,30,'Từ hỏi, liên từ và cụm giao tiếp thiết yếu','Từ hỏi, liên từ và các cụm giao tiếp nền tảng cho A0–A1.'),
('vocabulary','A0-A1','A0-A1',1,30,'Tháng trong năm và tính từ sở hữu','Tên tháng và tính từ sở hữu thường dùng trong giao tiếp cơ bản.'),
('vocabulary','A0-A1','A0-A1',1,30,'Nhà ở, phòng và đồ nội thất','Phòng, đồ nội thất và vật dụng trong nhà ở.'),
]

ROADMAP = ROADMAP[:-4]
_a0_a1_additions = [
    ('vocabulary','A0-A1','A0-A1',1,30,'Nhà ở, phòng và đồ nội thất','Phòng, đồ nội thất và vật dụng trong nhà ở.'),
    ('vocabulary','A0-A1','A0-A1',1,30,'Từ hỏi, liên từ và cụm giao tiếp thiết yếu','Từ hỏi, liên từ và các cụm giao tiếp nền tảng cho A0–A1.'),
    ('vocabulary','A0-A1','A0-A1',1,30,'Tháng trong năm và tính từ sở hữu','Tên tháng và tính từ sở hữu thường dùng trong giao tiếp cơ bản.'),
]
_first_a1_vocab = next(i for i,item in enumerate(ROADMAP) if item[0]=='vocabulary' and item[1]=='A1-A2')
ROADMAP = ROADMAP[:_first_a1_vocab] + _a0_a1_additions + ROADMAP[_first_a1_vocab:]

_a1_a2_source_topics = [
    'Du lịch và phương tiện giao thông', 'Khách sạn và chỗ ở', 'Sân bay và hành trình',
    'Sức khỏe và cơ thể', 'Bác sĩ, thuốc và điều trị', 'Công việc và nghề nghiệp',
    'Tìm việc và học tập', 'Sự kiện và lời mời', 'Mua sắm và dịch vụ', 'Ăn uống và nhà hàng',
    'Thời tiết và môi trường', 'Thành phố và chỉ đường', 'Giao tiếp và cảm xúc',
    'Công nghệ và truyền thông', 'Nhà ở và sinh hoạt', 'Hoạt động, sở thích và thể thao',
    'Thời gian, kế hoạch và tương lai', 'Động từ quan trọng A1–A2', 'Tính từ và trạng từ A1–A2',
    'Cụm từ giao tiếp và email',
]
_first_b1_vocab = next(i for i,item in enumerate(ROADMAP) if item[0]=='vocabulary' and item[1]=='B1')
_a1_a2_insertions = [('vocabulary','A1-A2','A1-A2',46,120,title,f'Từ vựng A1–A2 theo chủ đề {title.lower()}.') for title in _a1_a2_source_topics]
ROADMAP = ROADMAP[:_first_a1_vocab] + _a1_a2_insertions + ROADMAP[_first_b1_vocab:]
_b1_source_topics = []
for source_topic, *_ in B1_VOCABULARY:
    if source_topic not in _b1_source_topics:
        _b1_source_topics.append(source_topic)
_b1_vocab_insertions = [('vocabulary','B1','B1',121,240,title,f'Từ vựng B1 theo chủ đề {title.lower()}.') for title in _b1_source_topics]
_first_b1_vocab = next(i for i,item in enumerate(ROADMAP) if item[0]=='vocabulary' and item[1]=='B1')
ROADMAP = ROADMAP[:_first_b1_vocab] + _b1_vocab_insertions + [item for item in ROADMAP[_first_b1_vocab:] if not (item[0]=='vocabulary' and item[1]=='B1')]
_b2_source_topics = []
for source_topic, *_ in B2_VOCABULARY:
    if source_topic not in _b2_source_topics:
        _b2_source_topics.append(source_topic)
_b2_vocab_insertions = [('vocabulary','B2','B2',241,360,title,f'Từ vựng B2 theo chủ đề {title.lower()}.') for title in _b2_source_topics]
_first_b2_vocab = next(i for i,item in enumerate(ROADMAP) if item[0]=='vocabulary' and item[1]=='B2')
ROADMAP = ROADMAP[:_first_b2_vocab] + _b2_vocab_insertions + [item for item in ROADMAP[_first_b2_vocab:] if not (item[0]=='vocabulary' and item[1]=='B2')]

# Keep the A0-A1 roadmap block in the exact order used by the A0-A1 source file.
# The first thirteen entries are the legacy lessons; the source file adds three
# lessons and places transport between city directions and food.
_a0_legacy = [item for item in ROADMAP if item[0]=='vocabulary' and item[1]=='A0-A1']
_a0_source_housing = _a0_a1_additions[0]
_a0_source_questions = _a0_a1_additions[1]
_a0_source_months = _a0_a1_additions[2]
_a0_source_transport = ('vocabulary','A0-A1','A0-A1',1,30,'Phương tiện giao thông và du lịch cơ bản','Phương tiện giao thông và các tình huống du lịch cơ bản cho A0–A1.')
_a0_ordered = [
    _a0_legacy[0], _a0_legacy[1], _a0_legacy[2], _a0_legacy[3], _a0_legacy[4],
    _a0_legacy[6], _a0_source_housing, _a0_legacy[9], _a0_source_transport,
    _a0_legacy[7], _a0_legacy[8], _a0_legacy[10], _a0_legacy[12], _a0_legacy[11],
    _a0_source_questions, _a0_source_months,
]
_first_a0_vocab = next(i for i,item in enumerate(ROADMAP) if item[0]=='vocabulary' and item[1]=='A0-A1')
ROADMAP = ROADMAP[:_first_a0_vocab] + _a0_ordered + [item for item in ROADMAP[_first_a0_vocab:] if not (item[0]=='vocabulary' and item[1]=='A0-A1')]

# The supplied grammar document covers exactly the first five A0-A1 chapters.
# Keep grammar scoped to the supplied source; generic roadmap placeholders are
# intentionally not seeded as grammar lessons.
_grammar_source_titles = [item[5] for item in ROADMAP if item[0]=='grammar'][:5]
ROADMAP = [item for item in ROADMAP if item[0] != 'grammar' or item[5] in _grammar_source_titles]

# Source-backed A0-A1 grammar chapters from French_Grammar_A1.docx.
# Keep the source material separate from the generic roadmap fallback so later
# roadmap additions continue to receive useful draft content.
GRAMMAR_BOOK_CHAPTERS = [
    {
        'overview': 'Nắm các quy tắc phát âm nền tảng: chữ cái, dấu phụ, nguyên âm mũi, âm câm, liaison, enchaînement và nhịp câu.',
        'objectives': ['Nhận biết chữ cái và dấu phụ trong tiếng Pháp.', 'Phân biệt âm mũi, âm câm, liaison và enchaînement.', 'Luyện nghe theo nhóm nhịp thay vì nhấn từng từ.'],
        'examples': ['Chữ cái: A, E, I, O, U là nguyên âm; Y cũng có thể mang giá trị nguyên âm. H là h muet hoặc h aspiré, đều không phát âm /h/.', 'Dấu phụ: école / père / fête / Noël / français / où — é thường /e/, è thường /ɛ/, ç giữ âm /s/ trước a, o, u.', 'Âm mũi: sans /sɑ̃/ · without · không có; bon /bɔ̃/ · good · tốt; pain /pɛ̃/ · bread · bánh mì; un /œ̃/ · one · một.', 'Âm câm: petit /pə.ti/, vous /vu/, grand /ɡʁɑ̃/; avec /a.vɛk/ là ngoại lệ có -c cuối được đọc; hôtel /o.tɛl/.', 'Liaison: les amis /le.z‿a.mi/, vous avez /vu.z‿a.ve/; enchaînement: avec elle /a.vɛ.k‿ɛl/, il arrive /i.la.ʁiv/.', 'Nhịp: Je travaille à Paris. (câu kể thường hạ giọng); Tu viens ? (có thể lên giọng); Je voudrais un café. (một nhóm nhịp).'],
        'practice': 'Đọc thành tiếng các cặp ou/u, é/è và các cụm les amis, vous avez; đánh dấu nhóm nhịp trong một câu ngắn.',
        'hint': 'Không tự suy đoán IPA từ tên chữ cái; học âm của từ và luyện liaison theo cụm thường gặp.',
        'detailed': 'Phát âm tiếng Pháp cần phân biệt chữ viết với âm thanh. Dấu phụ đi cùng chính tả của từ; nguyên âm mũi được đọc như một nguyên âm duy nhất khi n/m không đứng trước nguyên âm khác. Nhiều phụ âm cuối như -s, -t, -d, -x thường câm ở cuối từ đứng riêng, nhưng có thể xuất hiện lại trong liaison. Liaison và enchaînement đều làm lời nói liền mạch, nhưng liaison đưa một phụ âm vốn câm vào âm tiết sau còn enchaînement nối phụ âm vốn đã được phát âm.',
        'notes': 'Liaison không phải lúc nào cũng được phép; tránh tự nối mọi phụ âm cuối. Sau et thường không dùng liaison trong mẫu cơ bản: et elle. Nhịp tiếng Pháp thường tổ chức theo nhóm từ, không theo trọng âm cố định của từng từ như tiếng Anh.',
        'takeaway': 'Hãy học cách phát âm cùng từ và cụm từ cụ thể; đừng đọc tên từng chữ cái rồi suy ra âm của cả từ.',
        'exercises': [
            {'prompt': 'Âm nào cần luyện để phân biệt rouge và rue?', 'answer': 'Luyện /u/ trong ou với /y/ trong u; rouge có âm /u/, rue có âm /y/.'},
            {'prompt': 'Trong les amis, điều gì xảy ra?', 'answer': 'Liaison thường gặp nối s thành /z/: /le.za.mi/.'}
        ],
    },
    {
        'overview': 'Xây dựng câu khẳng định theo trật tự S–V–C và phân biệt c’est, ce sont, il/elle est và il y a.',
        'objectives': ['Tạo câu khẳng định theo chủ ngữ – động từ – bổ ngữ.', 'Dùng c’est và ce sont để giới thiệu hoặc nhận diện.', 'Dùng il y a để nói về sự tồn tại và phân biệt với c’est.'],
        'examples': ['S–V–C: Marie travaille à Paris. · Marie works in Paris. · Marie làm việc ở Paris.; Nous aimons le français.; Ils habitent à Montréal.', 'C’est un médecin. · This is a doctor. · Đây là một bác sĩ.; C’est Marie. · This is Marie. · Đây là Marie.; Ce sont mes amis. · These are my friends. · Đây là những người bạn của tôi.', 'C’est un professeur. / Il est professeur. · Giới thiệu bằng danh từ có mạo từ / nghề nghiệp không mạo từ.', 'Elle est gentille. · She is kind. · Cô ấy tốt bụng.; C’est intéressant. · That is interesting. · Điều đó thú vị.', 'Il y a un livre sur la table. · There is a book on the table. · Có một quyển sách trên bàn.; Il y a trois étudiants.; Il n’y a pas de café.', 'Trạng ngữ và phủ định: Je travaille aujourd’hui.; Elle habite à Lyon.; Je ne parle pas espagnol.; Il n’est pas ici.'],
        'practice': 'Viết bốn câu về nơi bạn sống: một câu S–V–C, một câu c’est, một câu ce sont và một câu il y a.',
        'hint': 'Động từ phải được chia theo chủ ngữ; il y a không đổi theo danh từ số ít hay số nhiều phía sau.',
        'detailed': 'Câu khẳng định cơ bản thường đi theo chủ ngữ – động từ đã chia – bổ ngữ. C’est thường dùng để giới thiệu hoặc nhận diện một người/vật; ce sont đi với danh từ số nhiều trong cách dùng chuẩn. Il/elle est thường mô tả một người đã xác định, đặc điểm hoặc nghề nghiệp trong nhiều ngữ cảnh. Il y a diễn tả sự hiện diện hoặc tồn tại, không phải hành động nhận diện.',
        'notes': 'Trong hội thoại thân mật đôi khi nghe c’est mes amis, nhưng khi học và viết chuẩn nên dùng ce sont mes amis. C’est un médecin và Il est médecin có cấu trúc, mục đích giao tiếp khác nhau. Sau phủ định, un/une/des hoặc mạo từ bộ phận thường chuyển thành de/d’ trong nhiều mẫu.',
        'takeaway': 'Hãy chọn cấu trúc theo mục đích: nhận diện bằng c’est/ce sont, mô tả người đã biết bằng il/elle est, và nói “có/tồn tại” bằng il y a.',
        'exercises': [
            {'prompt': 'Chọn cấu trúc: ___ trois livres sur la table.', 'answer': 'Il y a trois livres sur la table.'},
            {'prompt': 'Sửa câu: C’est mes amis.', 'answer': 'Trong văn viết chuẩn: Ce sont mes amis.'}
        ],
    },
    {
        'overview': 'Học chín đại từ chủ ngữ và cách chúng điều khiển việc chia động từ trong câu.',
        'objectives': ['Nhớ je, tu, il, elle, on, nous, vous, ils, elles.', 'Phân biệt tu/vous và on/nous theo ngữ cảnh.', 'Chọn ils/elles theo thành phần của nhóm và chia động từ đúng.'],
        'examples': ['Je / J’ · I · tôi; tu · you informal singular · bạn thân mật; il/elle · he/she/it · anh ấy/cô ấy/nó; on · one/we/people · người ta/chúng ta; nous · we · chúng tôi; vous · formal or plural you · lịch sự hoặc số nhiều; ils/elles · they · nhóm hỗn hợp/toàn nữ.', 'Tu es étudiant ? · Are you a student? · nói thân mật; Vous êtes professeur ? · lịch sự với một người; Vous êtes prêts ? · nói với một nhóm.', 'On va au cinéma. / Nous allons au cinéma. · We are going to the cinema. · On + va, nous + allons.', 'On est contents. · We are happy. · Động từ est; tính từ có thể hòa hợp theo nhóm.', 'Le livre → il; la voiture → elle; Paul et Marie → ils; Marie et Sophie → elles.', 'Être: je suis, tu es, il/elle/on est, nous sommes, vous êtes, ils/elles sont. Parler: je parle, tu parles, il/elle/on parle, nous parlons, vous parlez, ils/elles parlent.', 'Sai → đúng: Je aime → J’aime; Tu êtes → Tu es; Vous es → Vous êtes; On sommes → On est; Marie et Sophie → ils → elles.'],
        'practice': 'Thay tên trong ba câu bằng đại từ phù hợp, rồi đọc to các cặp tu/vous và on/nous.',
        'hint': 'Je rút thành j’ trước nguyên âm hoặc h muet; on luôn đi với dạng động từ ngôi ba số ít.',
        'detailed': 'Đại từ chủ ngữ thay thế tên người hoặc danh từ làm chủ ngữ và thường đứng trước động từ đã chia. Tu dùng với một người trong quan hệ thân mật; vous dùng cho số nhiều hoặc lịch sự. On có thể mang nghĩa người ta hoặc chúng ta nhưng luôn dùng dạng động từ ngôi ba số ít. Ils dùng cho nhóm nam hoặc nhóm hỗn hợp, còn elles dùng cho nhóm toàn nữ.',
        'notes': 'Không viết Je aime; phải viết J’aime. Không phải mọi h đều cho phép rút gọn: je hais giữ je. Với nhóm có cả giống đực và giống cái, quy tắc chuẩn dùng ils. Giống của đồ vật là giống ngữ pháp, không phải giới tính thực.',
        'takeaway': 'Nhìn chủ ngữ trước khi chia động từ; hình thức parle, parles và parlent có thể đồng âm nhưng khác chính tả.',
        'exercises': [
            {'prompt': 'Điền đại từ: ___ sommes étudiants. (chúng tôi)', 'answer': 'Nous sommes étudiants.'},
            {'prompt': 'Sửa câu: On sommes contents.', 'answer': 'On est contents. On luôn đi với dạng ngôi ba số ít.'}
        ],
    },
    {
        'overview': 'Học giống và số của danh từ, hòa hợp tính từ, vị trí tính từ và các dạng đặc biệt trước nguyên âm.',
        'objectives': ['Học danh từ cùng mạo từ để ghi nhớ giống.', 'Tạo số nhiều cơ bản và hòa hợp tính từ.', 'Nhận biết tính từ đứng trước, sau danh từ và các cặp đổi nghĩa.'],
        'examples': ['un livre · a book · giống đực; une table · a table · giống cái; un homme · a man · giống đực; une personne · a person · giống cái dù nói về người nam hay nữ.', 'un livre → des livres; un journal → des journaux; un animal → des animaux; un prix → des prix.', 'un petit livre / une petite maison / des petits livres / des petites maisons · hòa hợp giống và số.', 'un homme heureux / une femme heureuse · -eux → -euse.', 'une voiture rouge / un livre intéressant (tính từ thường đứng sau); une petite maison / un beau jardin (một số tính từ thường đứng trước).', 'un ancien professeur = một giáo viên cũ/trước đây; un bâtiment ancien = một tòa nhà cổ/cũ.', 'un grand homme = người đàn ông vĩ đại; un homme grand = người đàn ông cao; un pauvre homme = đáng thương; un homme pauvre = nghèo tiền bạc.', 'beau → bel trước nguyên âm: un bel homme; nouveau → nouvel: un nouvel appartement; vieux → vieil: un vieil ami.'],
        'practice': 'Viết cụm danh từ ở bốn dạng: giống đực số ít, giống cái số ít, số nhiều và trước một danh từ bắt đầu bằng nguyên âm.',
        'hint': 'Học danh từ cùng mạo từ; đừng áp dụng máy móc các quy tắc đuôi từ vì luôn có ngoại lệ.',
        'detailed': 'Danh từ tiếng Pháp thường thuộc giống đực hoặc giống cái và cần được học cùng mạo từ. Số nhiều thường thêm -s, dù -s cuối thường không phát âm. Tính từ thường hòa hợp theo giống và số: giống cái thường thêm -e, số nhiều thêm -s, nhưng có nhiều dạng bất quy tắc. Phần lớn tính từ đứng sau danh từ; một nhóm tính từ thông dụng về vẻ đẹp, tuổi, đánh giá và kích thước thường đứng trước. Một số tính từ đổi nghĩa tùy vị trí.',
        'notes': 'Đuôi -tion thường gợi ý giống cái nhưng không thay thế việc tra cứu. Các dạng cần nhớ gồm beau/belle, nouveau/nouvelle, vieux/vieille và bel/nouvel/vieil trước danh từ giống đực số ít bắt đầu bằng nguyên âm hoặc h muet.',
        'takeaway': 'Hãy học cụm danh từ hoàn chỉnh, rồi kiểm tra hòa hợp của cả mạo từ, danh từ và tính từ.',
        'exercises': [
            {'prompt': 'Đổi sang số nhiều: un livre intéressant.', 'answer': 'des livres intéressants.'},
            {'prompt': 'Chọn dạng đúng: ___ homme (beau/bel).', 'answer': 'un bel homme.'}
        ],
    },
    {
        'overview': 'Phân biệt mạo từ xác định, không xác định và bộ phận; học de/d’ trong phủ định, số lượng và các dạng co rút.',
        'objectives': ['Chọn le/la/l’/les hoặc un/une/des theo ngữ cảnh.', 'Dùng du/de la/de l’ cho lượng không xác định.', 'Nhận biết de/d’ sau phủ định, từ chỉ số lượng và trước tính từ số nhiều.'],
        'examples': ['Ba nhóm: le/la/l’/les = the, đối tượng đã biết hoặc nói chung; un/une/des = a/an/some, đối tượng chưa xác định; du/de la/de l’ = một lượng không xác định.', 'Mạo từ xác định: le livre, la table, l’ami/l’école, les livres.', 'Mạo từ không xác định: un chat, une voiture, des amis.', 'Mạo từ bộ phận: du pain, de la soupe, de l’eau.', 'J’aime le café. / Je voudrais un café. / Je bois du café. · Nói chung / một ly / một lượng không xác định.', 'Phủ định: J’ai un chien → Je n’ai pas de chien; Je mange du pain → Je ne mange pas de pain; J’ai des amis → Je n’ai pas d’amis.', 'Số lượng: beaucoup de livres, un peu d’eau, un kilo de pommes, trop de sucre.', 'Co rút: à + le → au (au marché), à + les → aux (aux étudiants), de + le → du (du Canada), de + les → des (des maisons).', 'Tính từ đứng trước danh từ số nhiều: des livres intéressants nhưng de beaux livres, de grandes maisons.', 'Phân biệt nhanh: c’est / il est; c’est / il y a; tu / vous; on / nous; ils / elles; le / un / du; du bộ phận / du = de + le.'],
        'practice': 'Viết sáu câu dùng đủ ba nhóm mạo từ, sau đó chuyển ba câu sang phủ định và kiểm tra de/d’.',
        'hint': 'Đừng đổi le/la/les chỉ vì phủ định; sau être, mạo từ có thể được giữ nguyên như trong Ce n’est pas un problème.',
        'detailed': 'Mạo từ xác định le, la, l’, les dùng khi đối tượng đã xác định hoặc khi nói chung về một loại. Mạo từ không xác định un, une, des dùng khi giới thiệu đối tượng chưa xác định. Mạo từ bộ phận du, de la, de l’ diễn tả một lượng không xác định của chất hoặc danh từ thường không đếm được. Trong nhiều cấu trúc phủ định với avoir, manger hoặc boire, các mạo từ không xác định và bộ phận chuyển thành de/d’.',
        'notes': 'L’ vẫn giữ giống của le hoặc la; đó không phải giống thứ ba. Du có thể là mạo từ bộ phận trong du pain hoặc de + le trong du Canada. Des có thể là số nhiều không xác định hoặc de + les. Với từ chỉ số lượng như beaucoup de và peu de, dùng de/d’ bất kể giống và số.',
        'takeaway': 'Chọn mạo từ theo mức độ xác định, loại danh từ và ý định nói; sau đó kiểm tra các quy tắc de/d’ đặc biệt.',
        'exercises': [
            {'prompt': 'Điền mạo từ: Je bois ___ eau.', 'answer': 'Je bois de l’eau.'},
            {'prompt': 'Chuyển sang phủ định: J’ai des livres.', 'answer': 'Je n’ai pas de livres.'}
        ],
    },
]

# Tables are kept as structured data so the web lesson preserves the source's
# scan-friendly comparison layout instead of converting everything to prose.
GRAMMAR_BOOK_TABLES = [
    [
        {'title':'Dấu phụ / Les accents','headers':['Dấu','Ví dụ','Vai trò'],'rows':[['é — accent aigu','école','Thường biểu thị /e/'],['è — accent grave','père','Thường biểu thị /ɛ/'],['ê — accent circonflexe','fête','Có thể liên quan lịch sử chính tả'],['ç — cédille','français','Giữ âm /s/ trước a, o, u'],['à / ù','à, où','Thường phân biệt từ đồng âm']]},
        {'title':'Liaison và enchaînement','headers':['Cụm từ','IPA gần với lời nói liên tục','Phân loại'],'rows':[['les amis','/le.z‿a.mi/','Liaison: -s thành /z/'],['vous avez','/vu.z‿a.ve/','Liaison: -s thành /z/'],['avec elle','/a.vɛ.k‿ɛl/','Enchaînement: /k/ vốn đã được phát âm'],['il arrive','/i.la.ʁiv/','Enchaînement: /l/ nối tự nhiên']]},
    ],
    [
        {'title':'Cấu trúc S–V–C','headers':['Sujet / Chủ ngữ','Verbe / Động từ','Complément / Bổ ngữ'],'rows':[['Marie','travaille','à Paris.'],['Nous','aimons','le français.'],['Ils','habitent','à Montréal.']]},
        {'title':'C’est / Ce sont','headers':['Français','English','Tiếng Việt'],'rows':[['C’est un médecin.','This is a doctor.','Đây là một bác sĩ.'],['C’est Marie.','This is Marie.','Đây là Marie.'],['Ce sont mes amis.','These are my friends.','Đây là những người bạn của tôi.']]},
        {'title':'Il y a','headers':['Français','English','Tiếng Việt'],'rows':[['Il y a un livre sur la table.','There is a book on the table.','Có một quyển sách trên bàn.'],['Il y a trois étudiants.','There are three students.','Có ba sinh viên.'],['Il n’y a pas de café.','There is no coffee.','Không có cà phê.']]},
    ],
    [
        {'title':'Đại từ chủ ngữ','headers':['Français','English','Ngữ cảnh'],'rows':[['Je / J’','I','Tôi'],['Tu','You informal singular','Bạn/cậu thân mật'],['Vous','You formal or plural','Lịch sự hoặc số nhiều'],['On','One / We / People','Người ta; chúng ta'],['Ils / Elles','They','Nhóm hỗn hợp / nhóm toàn nữ']]},
        {'title':'Être và parler','headers':['Đại từ','Être','Parler'],'rows':[['Je','suis','parle'],['Tu','es','parles'],['Il/Elle/On','est','parle'],['Nous','sommes','parlons'],['Vous','êtes','parlez'],['Ils/Elles','sont','parlent']]},
        {'title':'Lỗi thường gặp','headers':['Sai','Đúng','Vì sao'],'rows':[['Je aime','J’aime','Rút gọn je trước nguyên âm'],['Tu êtes','Tu es','Tu dùng es'],['Vous es','Vous êtes','Vous dùng êtes'],['On sommes','On est','On chia ngôi 3 số ít'],['Marie et Sophie → ils','Marie et Sophie → elles','Nhóm toàn nữ']]},
    ],
    [
        {'title':'Giống và số','headers':['Français','English','Quy tắc'],'rows':[['un livre → des livres','a book → books','Thêm -s'],['un journal → des journaux','a newspaper → newspapers','Nhiều danh từ -al → -aux'],['un prix → des prix','a price → prices','Kết thúc -x thường không đổi']]},
        {'title':'Vị trí tính từ','headers':['Français','English','Mẹo'],'rows':[['une voiture rouge','a red car','Màu sắc thường đứng sau'],['un livre intéressant','an interesting book','Nhận xét thường đứng sau'],['une petite maison','a small house','petit thường đứng trước'],['un beau jardin','a beautiful garden','beau thường đứng trước'],['un bâtiment ancien','an old building','ancien sau danh từ: cổ/cũ']]},
        {'title':'Tính từ đổi nghĩa','headers':['Sắc thái','English','Ý nghĩa'],'rows':[['un grand homme','a great man','grand trước: vĩ đại'],['un homme grand','a tall man','grand sau: cao'],['un pauvre homme','a poor/unfortunate man','pauvre trước: đáng thương'],['un homme pauvre','a poor man','pauvre sau: nghèo tiền bạc']]},
    ],
    [
        {'title':'Ba nhóm mạo từ','headers':['Mạo từ','English','Ý nghĩa tiếng Việt'],'rows':[['le / la / l’ / les','the','Xác định; đối tượng đã biết hoặc nói chung'],['un / une / des','a / an / some','Không xác định; một hoặc một số đối tượng'],['du / de la / de l’','some / unspecified amount','Bộ phận; lượng không xác định']]},
        {'title':'Mạo từ bộ phận','headers':['Giống / Điều kiện','Mạo từ','Ví dụ'],'rows':[['Đực ít','du','du pain'],['Cái ít','de la','de la soupe'],['Trước nguyên âm hoặc h muet','de l’','de l’eau']]},
        {'title':'Phủ định','headers':['Français','English','Biến đổi'],'rows':[['J’ai un chien → Je n’ai pas de chien.','I have a dog → I do not have a dog.','un → de'],['Je mange du pain → Je ne mange pas de pain.','I eat bread → I do not eat bread.','du → de'],['J’ai des amis → Je n’ai pas d’amis.','I have friends → I have no friends.','des → d’']]},
        {'title':'Co rút giới từ','headers':['Quy tắc','Français','English / Tiếng Việt'],'rows':[['à + le → au','Je vais au marché.','I go to the market. / Tôi đi chợ.'],['à + les → aux','Je parle aux étudiants.','I speak to the students. / Tôi nói với các sinh viên.'],['de + le → du','Je viens du Canada.','I come from Canada. / Tôi đến từ Canada.'],['de + les → des','La porte des maisons.','The door of the houses. / Cánh cửa của những ngôi nhà.']]},
        {'title':'Phân biệt nhanh','headers':['Cặp dễ nhầm','Câu mẫu','Quy tắc nhớ'],'rows':[['c’est / il est','C’est un médecin. / Il est médecin.','Giới thiệu bằng danh từ có mạo từ / nghề nghiệp không mạo từ'],['c’est / il y a','C’est une école. / Il y a une école ici.','Nhận diện / nói sự tồn tại'],['tu / vous','Tu es prêt ? / Vous êtes prêt ?','Thân mật / lịch sự hoặc số nhiều'],['on / nous','On va. / Nous allons.','On chia ngôi 3 số ít'],['le / un / du','le pain / un pain / du pain','Xác định / một đơn vị / lượng không xác định']]},
    ],
]

def lesson_for(kind,title,description,level):
    if kind=='grammar':
        grammar_titles=[item[5] for item in ROADMAP if item[0]=='grammar']
        chapter_index=grammar_titles.index(title) if title in grammar_titles else -1
        if 0 <= chapter_index < len(GRAMMAR_BOOK_CHAPTERS):
            chapter=GRAMMAR_BOOK_CHAPTERS[chapter_index]
            return (chapter['overview'], chapter['objectives'], chapter['examples'], GRAMMAR_BOOK_TABLES[chapter_index], chapter['practice'], chapter['hint'], 'French_Grammar_A1.docx · chương '+str(chapter_index+1))
    source='Tham chiếu theo lộ trình A0–B2; cách luyện dựa trên các dạng bài theo chủ đề của TV5MONDE, Fabulang và FrancoHub. Nội dung ví dụ được viết mới cho project.'
    if kind=='grammar':
        match=next((value for key,value in GRAMMAR_EXAMPLES.items() if key.lower() in title.lower()),None)
        overview,examples=match if match else (f'Bài học về {title.lower()}. {description}',[f'Je pratique {title.lower()} dans une phrase simple.','Pouvez-vous créer une phrase personnelle ?'])
        objectives=[f'Nhận biết và sử dụng {title.lower()} ở mức {level}.','Tạo ít nhất hai câu trong một tình huống đời sống.']
        practice=f'Viết hoặc nói 3 câu áp dụng chủ đề “{title}” trong một tình huống thực tế.'
        hint='Kiểm tra chủ ngữ, vị trí động từ và sự hòa hợp trước khi xem lại câu trả lời.'
    else:
        overview=f'Xây dựng vốn từ theo chủ đề {title.lower()} và học theo cụm từ, không chỉ học từng từ riêng lẻ. {description}'
        examples=[f'Je parle de {title.lower()} dans une situation quotidienne.','Donnez un exemple avec une expression complète, pas seulement un mot.']
        objectives=[f'Nhận diện từ và cụm từ chính về {title.lower()}.','Dùng từ vựng trong một câu nói hoặc tin nhắn ngắn.']
        practice=f'Viết 5 từ hoặc cụm từ về “{title}”, sau đó tạo 3 câu liên quan đến cuộc sống của bạn.'
        hint='Ưu tiên học giống danh từ, mạo từ, động từ đi kèm và một câu ví dụ.'
    return overview,objectives,examples,[],practice,hint,source
def detail_for(kind,title,description,level,examples,practice,hint):
    if kind=='grammar':
        grammar_titles=[item[5] for item in ROADMAP if item[0]=='grammar']
        chapter_index=grammar_titles.index(title) if title in grammar_titles else -1
        if 0 <= chapter_index < len(GRAMMAR_BOOK_CHAPTERS):
            chapter=GRAMMAR_BOOK_CHAPTERS[chapter_index]
            return chapter['detailed'],chapter['notes'],chapter['takeaway'],[]
        detailed=f'{title}: {description} Hãy bắt đầu bằng cách nhận diện cấu trúc trong câu mẫu, sau đó thay đổi một thành phần và kiểm tra xem ý nghĩa hoặc sắc thái có thay đổi không. Ở mức {level}, ưu tiên câu ngắn, đúng và gắn với tình huống giao tiếp thực tế trước khi viết câu dài.'
        notes=f'Chú ý lỗi thường gặp khi học {title.lower()}: đừng dịch từng từ từ tiếng Việt; hãy xác định chủ ngữ, động từ chính và vị trí của thành phần ngữ pháp.'
        takeaway=f'Có thể dùng {title.lower()} để tạo câu rõ nghĩa trong một tình huống quen thuộc.'
        exercises=[{'prompt':f'Tạo một câu tiếng Pháp áp dụng chủ đề “{title}”.','answer':'Câu trả lời mở. Kiểm tra cấu trúc, hòa hợp và vị trí thành phần theo ví dụ của bài.'},{'prompt':f'Giải thích vì sao chủ đề “{title}” phù hợp trong tình huống đời sống.','answer':'Câu trả lời mở. Nêu cấu trúc đã dùng và ý nghĩa của nó.'}]
    else:
        detailed=f'{title}: {description} Học theo nhóm từ và cụm từ thường đi cùng nhau. Với mỗi từ mới, hãy ghi mạo từ hoặc giống, cách phát âm, một động từ đi kèm và một câu liên quan đến cuộc sống của bạn. Ở mức {level}, mục tiêu là dùng từ để truyền đạt ý chứ không chỉ nhận ra nghĩa khi đọc.'
        notes=f'Ghi nhớ {title.lower()} theo cụm từ hoàn chỉnh; nếu là danh từ, luôn học cùng mạo từ; nếu là động từ, học thêm giới từ hoặc mẫu câu đi kèm.'
        takeaway=f'Có thể nói hoặc viết một thông điệp ngắn về {title.lower()} bằng vốn từ phù hợp với tình huống.'
        exercises=[{'prompt':f'Viết 5 từ hoặc cụm từ thuộc chủ đề “{title}”.','answer':'Câu trả lời mở. Mỗi mục nên có nghĩa, mạo từ hoặc từ loại và một ví dụ ngắn.'},{'prompt':f'Viết 3 câu tiếng Pháp về “{title}” bằng ít nhất 3 từ mới.','answer':'Câu trả lời mở. Kiểm tra mạo từ, giống/số, chia động từ và cách dùng trong ngữ cảnh.'}]
    return detailed,notes,takeaway,exercises

with app.app_context():
    init_db(); conn=db()
    for slug,name,level,desc in TOPICS: conn.execute('INSERT OR IGNORE INTO topics(slug,name,level,description) VALUES(?,?,?,?)',(slug,name,level,desc))
    for slug,fr,pos,gender,vi,en,ex,exvi in WORDS:
        tid=conn.execute('SELECT id FROM topics WHERE slug=?',(slug,)).fetchone()['id']; conn.execute('INSERT OR IGNORE INTO vocabulary(topic_id,french,part_of_speech,gender,vietnamese,english,example_fr,example_vi) SELECT ?,?,?,?,?,?,?,? WHERE NOT EXISTS (SELECT 1 FROM vocabulary WHERE french=?)',(tid,fr,pos,gender,vi,en,ex,exvi,fr))
    for slug,fr,pos,gender,vi,en,ex,exvi in EXTRA_WORDS:
        tid=conn.execute('SELECT id FROM topics WHERE slug=?',(slug,)).fetchone()['id']; conn.execute('INSERT OR IGNORE INTO vocabulary(topic_id,french,part_of_speech,gender,vietnamese,english,example_fr,example_vi) SELECT ?,?,?,?,?,?,?,? WHERE NOT EXISTS (SELECT 1 FROM vocabulary WHERE french=?)',(tid,fr,pos,gender,vi,en,ex,exvi,fr))
    for word_id,pronunciation in enumerate(PRONUNCIATIONS,1): conn.execute('INSERT INTO vocabulary_details(vocabulary_id,pronunciation) VALUES(?,?) ON CONFLICT(vocabulary_id) DO UPDATE SET pronunciation=excluded.pronunciation',(word_id,pronunciation))
    for slug,prompt,options,answer,explanation in QUIZZES:
        tid=conn.execute('SELECT id FROM topics WHERE slug=?',(slug,)).fetchone()['id']; conn.execute('INSERT OR IGNORE INTO quizzes(topic_id,prompt,options_json,answer_key,explanation) SELECT ?,?,?,?,? WHERE NOT EXISTS (SELECT 1 FROM quizzes WHERE prompt=?)',(tid,prompt,json.dumps(options,ensure_ascii=False),answer,explanation,prompt))
    for slug,title,level,instruction,prompt,options,answer,explanation in []:
        tid=conn.execute('SELECT id FROM topics WHERE slug=?',(slug,)).fetchone()['id']; conn.execute('INSERT OR IGNORE INTO grammar_activities(topic_id,title,level,instruction,prompt,options_json,answer_key,explanation) SELECT ?,?,?,?,?,?,?,? WHERE NOT EXISTS (SELECT 1 FROM grammar_activities WHERE prompt=?)',(tid,title,level,instruction,prompt,json.dumps(options,ensure_ascii=False),answer,explanation,prompt))
    for slug,title,level,instruction,prompt,options,answer,explanation in []:
        tid=conn.execute('SELECT id FROM topics WHERE slug=?',(slug,)).fetchone()['id']; conn.execute('INSERT OR IGNORE INTO grammar_activities(topic_id,title,level,instruction,prompt,options_json,answer_key,explanation) SELECT ?,?,?,?,?,?,?,? WHERE NOT EXISTS (SELECT 1 FROM grammar_activities WHERE prompt=?)',(tid,title,level,instruction,prompt,json.dumps(options,ensure_ascii=False),answer,explanation,prompt))
    conn.execute('UPDATE roadmap_topics SET sort_order=-1000000-id')
    legacy_b1_title_map={
        'Giáo dục và việc làm':'Công việc và sự nghiệp',
        'Quan hệ xã hội':'Quan hệ xã hội',
        'Sức khỏe và lối sống':'Sức khỏe và lối sống',
        'Môi trường':'Môi trường và khí hậu',
        'Công nghệ và truyền thông':'Công nghệ và Internet',
        'Văn hóa và nghệ thuật':'Văn hóa và giải trí',
        'Đời sống đô thị':'Thành phố và nhà ở',
        'Tiêu dùng và ngân sách':'Tiền bạc và tiêu dùng',
        'Ý kiến và cảm xúc':'Quan điểm và tranh luận',
    }
    for legacy_title, source_title in legacy_b1_title_map.items():
        legacy_row=conn.execute("SELECT id FROM roadmap_topics WHERE kind='vocabulary' AND level='B1' AND title=?",(legacy_title,)).fetchone()
        if legacy_row:
            conn.execute('UPDATE roadmap_topics SET title=?,description=? WHERE id=?',(source_title,f'Từ vựng B1 theo chủ đề {source_title.lower()}.',legacy_row['id']))
    legacy_b2_title_map={
        'Giáo dục đại học':'Giáo dục',
        'Thị trường lao động':'Công việc',
        'AI và đạo đức công nghệ':'Công nghệ',
        'Kinh tế và bất bình đẳng':'Kinh tế',
        'Chính trị và công dân':'Chính trị và công dân',
        'Y tế công cộng':'Sức khỏe',
        'Di cư và đa văn hóa':'Xã hội và bất bình đẳng',
        'Báo chí và kiểm chứng':'Truyền thông',
        'Khoa học và dữ liệu':'Khoa học',
        'Văn hóa và phê bình':'Văn hóa',
        'Toàn cầu hóa':'Toàn cầu hóa',
        'Lập luận và tranh luận':'Tranh luận',
        'Văn bản trang trọng':'Giao tiếp chuyên nghiệp',
        'Từ vựng sắc thái':'Cụm diễn đạt B2',
    }
    for legacy_title, source_title in legacy_b2_title_map.items():
        legacy_row=conn.execute("SELECT id FROM roadmap_topics WHERE kind='vocabulary' AND level='B2' AND title=?",(legacy_title,)).fetchone()
        if legacy_row:
            conn.execute('UPDATE roadmap_topics SET title=?,description=? WHERE id=?',(source_title,f'Từ vựng B2 theo chủ đề {source_title.lower()}.',legacy_row['id']))
    all_grammar_titles=[item[5] for item in ROADMAP if item[0]=='grammar']
    grammar_placeholders=','.join('?' for _ in all_grammar_titles)
    conn.execute(f"DELETE FROM roadmap_topics WHERE kind='grammar' AND title NOT IN ({grammar_placeholders})",all_grammar_titles)
    conn.execute('DELETE FROM grammar_activities')
    for order,(kind,level,stage,start_day,end_day,title,description) in enumerate(ROADMAP,1):
        existing=conn.execute('SELECT id FROM roadmap_topics WHERE kind=? AND level=? AND title=?',(kind,level,title)).fetchone()
        if not existing and title=='Nhà ở, phòng và đồ nội thất':
            existing=conn.execute('SELECT id FROM roadmap_topics WHERE kind=? AND title=?',(kind,'Nhà cửa')).fetchone()
        if existing:
            conn.execute('UPDATE roadmap_topics SET level=?,stage=?,day_start=?,day_end=?,title=?,description=?,sort_order=? WHERE id=?',(level,stage,start_day,end_day,title,description,order,existing['id']))
            topic_id=existing['id']
        else:
            topic_id=conn.execute('INSERT INTO roadmap_topics(kind,level,stage,day_start,day_end,title,description,sort_order) VALUES(?,?,?,?,?,?,?,?)',(kind,level,stage,start_day,end_day,title,description,order)).lastrowid
        overview,objectives,examples,tables,practice,hint,source=lesson_for(kind,title,description,level); detailed,notes,takeaway,exercises=detail_for(kind,title,description,level,examples,practice,hint)
        grammar_titles=[item[5] for item in ROADMAP if item[0]=='grammar']
        source_content=GRAMMAR_SOURCE_CONTENTS[grammar_titles.index(title)] if kind=='grammar' else ''
        conn.execute('INSERT INTO roadmap_lessons(topic_id,overview,objectives_json,examples_json,tables_json,practice_prompt,answer_hint,source_note,source_content) VALUES(?,?,?,?,?,?,?,?,?) ON CONFLICT(topic_id) DO UPDATE SET overview=excluded.overview,objectives_json=excluded.objectives_json,examples_json=excluded.examples_json,tables_json=excluded.tables_json,practice_prompt=excluded.practice_prompt,answer_hint=excluded.answer_hint,source_note=excluded.source_note,source_content=excluded.source_content',(topic_id,overview,json.dumps(objectives,ensure_ascii=False),json.dumps(examples,ensure_ascii=False),json.dumps(tables,ensure_ascii=False),practice,hint,source,json.dumps(source_content,ensure_ascii=False)))
        conn.execute('INSERT INTO roadmap_lesson_details(topic_id,detailed_explanation,notes,takeaway,exercises_json) VALUES(?,?,?,?,?) ON CONFLICT(topic_id) DO UPDATE SET detailed_explanation=excluded.detailed_explanation,notes=excluded.notes,takeaway=excluded.takeaway,exercises_json=excluded.exercises_json',(topic_id,detailed,notes,takeaway,json.dumps(exercises,ensure_ascii=False)))
    vocab_topic_orders=[order for order,(kind,*_) in enumerate(ROADMAP,1) if kind=='vocabulary']
    for (word, target_index) in zip(WORDS+EXTRA_WORDS, VOCABULARY_ROADMAP_INDEXES):
        roadmap_order=vocab_topic_orders[target_index-1]
        conn.execute('UPDATE vocabulary SET roadmap_topic_id=(SELECT id FROM roadmap_topics WHERE sort_order=?) WHERE french=?',(roadmap_order,word[1]))
    conn.execute("UPDATE vocabulary SET roadmap_topic_id=NULL WHERE roadmap_topic_id IN (SELECT id FROM roadmap_topics WHERE kind='vocabulary' AND level='A0-A1')")
    source_topic_titles=[item[5] for item in _a0_ordered]
    source_topic_title_by_source={}
    for source_topic, *_ in A0_A1_VOCABULARY:
        if source_topic not in source_topic_title_by_source:
            source_topic_title_by_source[source_topic]=source_topic_titles[len(source_topic_title_by_source)]
    for source_topic,fr,gender,pronunciation,en,vi,example_fr,example_vi,note in A0_A1_VOCABULARY:
        roadmap_title=source_topic_title_by_source[source_topic]
        pos='expression' if ' ' in fr else 'mot'
        existing=conn.execute('SELECT id FROM vocabulary WHERE french=? ORDER BY id LIMIT 1',(fr,)).fetchone()
        roadmap_row=conn.execute('SELECT id FROM roadmap_topics WHERE kind=? AND level=? AND title=?',('vocabulary','A0-A1',roadmap_title)).fetchone()
        if not roadmap_row:
            raise RuntimeError(f'Missing A0-A1 roadmap topic: {source_topic} -> {roadmap_title}')
        roadmap_topic_id=roadmap_row['id']
        values=(conn.execute("SELECT id FROM topics WHERE slug='premiers-pas'").fetchone()['id'],roadmap_topic_id,fr,pos,gender,vi,en,example_fr,example_vi)
        if existing:
            conn.execute('UPDATE vocabulary SET topic_id=?,roadmap_topic_id=?,french=?,part_of_speech=?,gender=?,vietnamese=?,english=?,example_fr=?,example_vi=? WHERE id=?',values+(existing['id'],))
            vocabulary_id=existing['id']
        else:
            cur=conn.execute('INSERT INTO vocabulary(topic_id,roadmap_topic_id,french,part_of_speech,gender,vietnamese,english,example_fr,example_vi) VALUES(?,?,?, ?,?,?,?,?,?)',values)
            vocabulary_id=cur.lastrowid
        conn.execute('INSERT INTO vocabulary_details(vocabulary_id,pronunciation) VALUES(?,?) ON CONFLICT(vocabulary_id) DO UPDATE SET pronunciation=excluded.pronunciation',(vocabulary_id,pronunciation))
    a1_placeholders=','.join('?' for _ in _a1_a2_source_topics)
    conn.execute(f"DELETE FROM roadmap_topics WHERE kind='vocabulary' AND level='A1-A2' AND title NOT IN ({a1_placeholders})",_a1_a2_source_topics)
    conn.execute("UPDATE vocabulary SET roadmap_topic_id=NULL WHERE roadmap_topic_id IN (SELECT id FROM roadmap_topics WHERE kind='vocabulary' AND level='A1-A2')")
    a1_topic_ids={}
    for topic_title, *_ in A1_A2_VOCABULARY:
        if topic_title not in a1_topic_ids:
            row=conn.execute('SELECT id FROM roadmap_topics WHERE kind=? AND level=? AND title=?',('vocabulary','A1-A2',topic_title)).fetchone()
            if not row:
                raise RuntimeError(f'Missing A1-A2 roadmap topic: {topic_title}')
            a1_topic_ids[topic_title]=row['id']
    broad_topic_id=conn.execute("SELECT id FROM topics WHERE slug='premiers-pas'").fetchone()['id']
    for source_topic,fr,gender,pronunciation,en,vi,example_fr,example_vi,note in A1_A2_VOCABULARY:
        roadmap_topic_id=a1_topic_ids[source_topic]
        pos='expression' if ' ' in fr else 'mot'
        existing=conn.execute('SELECT id FROM vocabulary WHERE french=? AND roadmap_topic_id=? ORDER BY id LIMIT 1',(fr,roadmap_topic_id)).fetchone()
        values=(broad_topic_id,roadmap_topic_id,fr,pos,gender,vi,en,example_fr,example_vi)
        if existing:
            conn.execute('UPDATE vocabulary SET topic_id=?,roadmap_topic_id=?,french=?,part_of_speech=?,gender=?,vietnamese=?,english=?,example_fr=?,example_vi=? WHERE id=?',values+(existing['id'],))
            vocabulary_id=existing['id']
        else:
            cur=conn.execute('INSERT INTO vocabulary(topic_id,roadmap_topic_id,french,part_of_speech,gender,vietnamese,english,example_fr,example_vi) VALUES(?,?,?, ?,?,?,?,?,?)',values)
            vocabulary_id=cur.lastrowid
        conn.execute('INSERT INTO vocabulary_details(vocabulary_id,pronunciation) VALUES(?,?) ON CONFLICT(vocabulary_id) DO UPDATE SET pronunciation=excluded.pronunciation',(vocabulary_id,pronunciation))
    b1_topic_ids={}
    for topic_title, *_ in B1_VOCABULARY:
        if topic_title not in b1_topic_ids:
            row=conn.execute('SELECT id FROM roadmap_topics WHERE kind=? AND level=? AND title=?',('vocabulary','B1',topic_title)).fetchone()
            if not row:
                raise RuntimeError(f'Missing B1 roadmap topic: {topic_title}')
            b1_topic_ids[topic_title]=row['id']
    for source_topic,fr,gender,pronunciation,en,vi,example_fr,example_vi,note in B1_VOCABULARY:
        roadmap_topic_id=b1_topic_ids[source_topic]
        pos='expression' if ' ' in fr else 'mot'
        existing=conn.execute('SELECT id FROM vocabulary WHERE french=? AND roadmap_topic_id=? ORDER BY id LIMIT 1',(fr,roadmap_topic_id)).fetchone()
        values=(broad_topic_id,roadmap_topic_id,fr,pos,gender,vi,en,example_fr,example_vi)
        if existing:
            conn.execute('UPDATE vocabulary SET topic_id=?,roadmap_topic_id=?,french=?,part_of_speech=?,gender=?,vietnamese=?,english=?,example_fr=?,example_vi=? WHERE id=?',values+(existing['id'],))
            vocabulary_id=existing['id']
        else:
            cur=conn.execute('INSERT INTO vocabulary(topic_id,roadmap_topic_id,french,part_of_speech,gender,vietnamese,english,example_fr,example_vi) VALUES(?,?,?, ?,?,?,?,?,?)',values)
            vocabulary_id=cur.lastrowid
        conn.execute('INSERT INTO vocabulary_details(vocabulary_id,pronunciation) VALUES(?,?) ON CONFLICT(vocabulary_id) DO UPDATE SET pronunciation=excluded.pronunciation',(vocabulary_id,pronunciation))
    b2_topic_ids={}
    for topic_title, *_ in B2_VOCABULARY:
        if topic_title not in b2_topic_ids:
            row=conn.execute('SELECT id FROM roadmap_topics WHERE kind=? AND level=? AND title=?',('vocabulary','B2',topic_title)).fetchone()
            if not row:
                raise RuntimeError(f'Missing B2 roadmap topic: {topic_title}')
            b2_topic_ids[topic_title]=row['id']
    for source_topic,fr,gender,en,vi,example_fr,example_vi,note in B2_VOCABULARY:
        roadmap_topic_id=b2_topic_ids[source_topic]
        pos='expression' if ' ' in fr else 'mot'
        existing=conn.execute('SELECT id FROM vocabulary WHERE french=? AND roadmap_topic_id=? ORDER BY id LIMIT 1',(fr,roadmap_topic_id)).fetchone()
        values=(broad_topic_id,roadmap_topic_id,fr,pos,gender,vi,en,example_fr,example_vi)
        if existing:
            conn.execute('UPDATE vocabulary SET topic_id=?,roadmap_topic_id=?,french=?,part_of_speech=?,gender=?,vietnamese=?,english=?,example_fr=?,example_vi=? WHERE id=?',values+(existing['id'],))
            vocabulary_id=existing['id']
        else:
            cur=conn.execute('INSERT INTO vocabulary(topic_id,roadmap_topic_id,french,part_of_speech,gender,vietnamese,english,example_fr,example_vi) VALUES(?,?,?, ?,?,?,?,?,?)',values)
            vocabulary_id=cur.lastrowid
        # The B2 source includes IPA for reference, but pronunciation is intentionally not stored or shown.
    conn.commit(); print('Seed completed.')


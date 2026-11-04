import json
from app import app,db,init_db
from vocabulary_sources.a0_a1_vocabulary import A0_A1_VOCABULARY
from vocabulary_sources.a1_a2_vocabulary import A1_A2_VOCABULARY
TOPICS=[('premiers-pas','Chào hỏi & giới thiệu','A1','Bắt đầu một cuộc trò chuyện tự nhiên.'),('vie-quotidienne','Đời sống hằng ngày','A1','Những từ dùng khi mua sắm và đi lại.'),('canada','Cuộc sống ở Canada','A2','Giao tiếp trong học tập và công việc.')]
WORDS=[('premiers-pas','bonjour','interjection','', 'xin chào','hello','Bonjour, comment allez-vous ?','Xin chào, bạn khỏe không?'),('premiers-pas','s’appeler','verbe','', 'tên là','to be called','Je m’appelle Linh.','Tôi tên là Linh.'),('premiers-pas','enchanté','adjectif','', 'rất vui được gặp','delighted','Enchanté de faire votre connaissance.','Rất vui được làm quen với bạn.'),('premiers-pas','la famille','nom','f', 'gia đình','family','Ma famille habite à Toronto.','Gia đình tôi sống ở Toronto.'),('premiers-pas','travailler','verbe','', 'làm việc','to work','Je travaille dans une école.','Tôi làm việc ở một trường học.'),('vie-quotidienne','le marché','nom','m', 'chợ','market','Je vais au marché samedi.','Tôi đi chợ vào thứ bảy.'),('vie-quotidienne','acheter','verbe','', 'mua','to buy','Je voudrais acheter du pain.','Tôi muốn mua bánh mì.'),('vie-quotidienne','combien','adverbe','', 'bao nhiêu','how much','Combien coûte ce livre ?','Cuốn sách này giá bao nhiêu?'),('vie-quotidienne','à gauche','locution','', 'bên trái','on the left','La banque est à gauche.','Ngân hàng ở bên trái.'),('vie-quotidienne','le billet','nom','m', 'vé','ticket','Un billet pour Montréal, s’il vous plaît.','Cho tôi một vé đi Montréal.'),('canada','le quartier','nom','m', 'khu phố','neighborhood','Mon quartier est calme.','Khu phố của tôi yên tĩnh.'),('canada','un rendez-vous','nom','m', 'cuộc hẹn','appointment','J’ai un rendez-vous demain.','Tôi có cuộc hẹn ngày mai.'),('canada','le travail','nom','m', 'công việc','work','Le travail commence à neuf heures.','Công việc bắt đầu lúc chín giờ.'),('canada','la neige','nom','f', 'tuyết','snow','La neige tombe en hiver.','Tuyết rơi vào mùa đông.'),('canada','bienvenue','nom','', 'chào mừng','welcome','Bienvenue au Canada !','Chào mừng đến Canada!')]
QUIZZES=[('premiers-pas','“Bonjour” có nghĩa là gì?',['Xin chào','Tạm biệt','Cảm ơn'],'Xin chào','Bonjour là lời chào.'),('vie-quotidienne','Chọn câu có nghĩa “Tôi muốn mua bánh mì”.',['Je vais au marché.','Je voudrais acheter du pain.','La banque est à gauche.'],'Je voudrais acheter du pain.','“Je voudrais acheter” nghĩa là “Tôi muốn mua”.'),('canada','“La neige” là gì?',['mưa','tuyết','gió'],'tuyết','Neige là tuyết.')]
GRAMMAR=[('premiers-pas','Articles: un, une, des','A1',"Choisissez l'article correct.",'___ famille habite a Toronto.',['Un','Une','Des'],'Une','Famille est un nom feminin.'),('vie-quotidienne','Le present des verbes en -er','A1','Choisissez la bonne forme du verbe.','Je ___ au marche le samedi.',['vais','va','allez'],'vais','Avec je, le verbe aller devient vais.'),('canada','La negation avec ne...pas','A2','Completez la phrase negative.','Je ___ travaille ___ dimanche.',['ne / pas','pas / ne','ne / jamais'],'ne / pas','La negation standard encadre le verbe: ne ... pas.')]
EXTRA_WORDS=[('premiers-pas','salut','interjection','', 'xin chào thân mật','hi','Salut, ça va ?','Chào, bạn khỏe không?'),('premiers-pas','au revoir','locution','', 'tạm biệt','goodbye','Au revoir et à demain.','Tạm biệt và hẹn gặp ngày mai.'),('premiers-pas','habiter','verbe','', 'sống ở','to live','J’habite à Toronto.','Tôi sống ở Toronto.'),('premiers-pas','aimer','verbe','', 'thích','to like','J’aime lire en français.','Tôi thích đọc bằng tiếng Pháp.'),('premiers-pas','aujourd’hui','adverbe','', 'hôm nay','today','Aujourd’hui, je travaille.','Hôm nay tôi làm việc.'),('vie-quotidienne','la boulangerie','nom','f', 'tiệm bánh','bakery','La boulangerie est près du marché.','Tiệm bánh gần khu chợ.'),('vie-quotidienne','le prix','nom','m', 'giá','price','Quel est le prix de ce livre ?','Giá của quyển sách này là bao nhiêu?'),('vie-quotidienne','prendre','verbe','', 'đi/bắt/dùng','to take','Je prends le métro.','Tôi đi tàu điện ngầm.'),('vie-quotidienne','tout droit','locution','', 'thẳng về phía trước','straight ahead','Allez tout droit, puis tournez à gauche.','Đi thẳng, sau đó rẽ trái.'),('vie-quotidienne','la réservation','nom','f', 'đặt chỗ','reservation','J’ai une réservation pour deux personnes.','Tôi có đặt chỗ cho hai người.'),('canada','le logement','nom','m', 'chỗ ở','housing','Je cherche un logement calme.','Tôi đang tìm chỗ ở yên tĩnh.'),('canada','le voisin','nom','m', 'hàng xóm nam','neighbour','Mon voisin parle français.','Hàng xóm của tôi nói tiếng Pháp.'),('canada','la réunion','nom','f', 'cuộc họp','meeting','La réunion commence à neuf heures.','Cuộc họp bắt đầu lúc chín giờ.'),('canada','postuler','verbe','', 'nộp đơn ứng tuyển','to apply','Je voudrais postuler à ce poste.','Tôi muốn ứng tuyển vị trí này.'),('canada','l’hiver','nom','m', 'mùa đông','winter','L’hiver est froid au Canada.','Mùa đông ở Canada lạnh.')]
PRONUNCIATIONS=['/bɔ̃.ʒuʁ/','/s‿a.pe.le/','/ɑ̃.ʃɑ̃.te/','/la fa.mij/','/tʁa.va.je/','/lə maʁ.ʃe/','/aʃ.te/','/kɔ̃.bjɛ̃/','/a ɡoʃ/','/lə bi.jɛ/','/lə kaʁ.tje/','/œ̃ ʁɑ̃.de.vu/','/lə tʁa.vaj/','/la nɛʒ/','/bjɛ̃.və.ny/','/sa.ly/','/o ʁə.vwaʁ/','/a.bi.te/','/e.me/','/o.ʒuʁ.dɥi/','/la bu.lɑ̃.ʒə.ʁi/','/lə pʁi/','/pʁɑ̃dʁ/','/tu dʁwa/','/la ʁe.zɛʁ.va.sjɔ̃/','/lə lɔʒ.mɑ̃/','/lə vwɛ.zɛ̃/','/la ʁe.y.njɔ̃/','/pɔʁ.ty.le/','/li.vɛʁ/']
EXTRA_GRAMMAR=[('premiers-pas','Les pronoms sujets','A1','Choisissez le pronom correct.','___ habite à Montréal.',['Je','Nous','Vous'],'Je','Le verbe habite correspond à je.'),('premiers-pas','La question avec est-ce que','A1','Choisissez la question correcte.','___ vous aimez le café ?',['Est-ce que','Pourquoi est-ce','Comment est-ce'],'Est-ce que','Est-ce que introduit une question oui/non.'),('vie-quotidienne','Les adjectifs possessifs','A1','Choisissez le possessif correct.','C’est ___ billet.',['mon','ma','mes'],'mon','Billet est masculin singulier: mon billet.'),('vie-quotidienne','Les prépositions de lieu','A1','Choisissez la préposition correcte.','La banque est ___ gauche.',['à','en','au'],'à','On dit à gauche et à droite.'),('canada','Le passé composé','A2','Choisissez la bonne forme.','Hier, j’___ travaillé.',['ai','as','suis'],'ai','Avec travailler, on utilise avoir: j’ai travaillé.'),('canada','Le futur proche','A2','Choisissez la bonne structure.','Nous ___ visiter Montréal demain.',['allons','avons','sommes'],'allons','Le futur proche se forme avec aller + infinitif.')]
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

def lesson_for(kind,title,description,level):
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
    return overview,objectives,examples,practice,hint,source
def detail_for(kind,title,description,level,examples,practice,hint):
    if kind=='grammar':
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
    for slug,title,level,instruction,prompt,options,answer,explanation in GRAMMAR:
        tid=conn.execute('SELECT id FROM topics WHERE slug=?',(slug,)).fetchone()['id']; conn.execute('INSERT OR IGNORE INTO grammar_activities(topic_id,title,level,instruction,prompt,options_json,answer_key,explanation) SELECT ?,?,?,?,?,?,?,? WHERE NOT EXISTS (SELECT 1 FROM grammar_activities WHERE prompt=?)',(tid,title,level,instruction,prompt,json.dumps(options,ensure_ascii=False),answer,explanation,prompt))
    for slug,title,level,instruction,prompt,options,answer,explanation in EXTRA_GRAMMAR:
        tid=conn.execute('SELECT id FROM topics WHERE slug=?',(slug,)).fetchone()['id']; conn.execute('INSERT OR IGNORE INTO grammar_activities(topic_id,title,level,instruction,prompt,options_json,answer_key,explanation) SELECT ?,?,?,?,?,?,?,? WHERE NOT EXISTS (SELECT 1 FROM grammar_activities WHERE prompt=?)',(tid,title,level,instruction,prompt,json.dumps(options,ensure_ascii=False),answer,explanation,prompt))
    conn.execute('UPDATE roadmap_topics SET sort_order=-1000000-id')
    for order,(kind,level,stage,start_day,end_day,title,description) in enumerate(ROADMAP,1):
        existing=conn.execute('SELECT id FROM roadmap_topics WHERE kind=? AND level=? AND title=?',(kind,level,title)).fetchone()
        if not existing and title=='Nhà ở, phòng và đồ nội thất':
            existing=conn.execute('SELECT id FROM roadmap_topics WHERE kind=? AND title=?',(kind,'Nhà cửa')).fetchone()
        if existing:
            conn.execute('UPDATE roadmap_topics SET level=?,stage=?,day_start=?,day_end=?,title=?,description=?,sort_order=? WHERE id=?',(level,stage,start_day,end_day,title,description,order,existing['id']))
            topic_id=existing['id']
        else:
            topic_id=conn.execute('INSERT INTO roadmap_topics(kind,level,stage,day_start,day_end,title,description,sort_order) VALUES(?,?,?,?,?,?,?,?)',(kind,level,stage,start_day,end_day,title,description,order)).lastrowid
        overview,objectives,examples,practice,hint,source=lesson_for(kind,title,description,level); detailed,notes,takeaway,exercises=detail_for(kind,title,description,level,examples,practice,hint)
        conn.execute('INSERT INTO roadmap_lessons(topic_id,overview,objectives_json,examples_json,practice_prompt,answer_hint,source_note) VALUES(?,?,?,?,?,?,?) ON CONFLICT(topic_id) DO UPDATE SET overview=excluded.overview,objectives_json=excluded.objectives_json,examples_json=excluded.examples_json,practice_prompt=excluded.practice_prompt,answer_hint=excluded.answer_hint,source_note=excluded.source_note',(topic_id,overview,json.dumps(objectives,ensure_ascii=False),json.dumps(examples,ensure_ascii=False),practice,hint,source))
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
    conn.commit(); print('Seed completed.')


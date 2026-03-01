-- Sample Data for Iran News Clustering Pipeline
-- This data is for testing purposes only

-- Insert source types
INSERT INTO source_type (name) VALUES 
('news_website'),
('tv_channel'),
('news_agency')
ON CONFLICT (name) DO NOTHING;

-- Insert sources
INSERT INTO sources (source_type_id, url, is_active) VALUES 
((SELECT id FROM source_type WHERE name = 'news_website'), 'https://www.channel12.co.il', true),
((SELECT id FROM source_type WHERE name = 'news_website'), 'https://www.ynet.co.il', true),
((SELECT id FROM source_type WHERE name = 'tv_channel'), 'https://www.aljazeera.net', true),
((SELECT id FROM source_type WHERE name = 'news_website'), 'https://www.alarabiya.net', true),
((SELECT id FROM source_type WHERE name = 'tv_channel'), 'https://www.almayadeen.net', true);

-- Insert Hebrew news articles about Iran sanctions (Topic 1)
INSERT INTO raw_data (source_id, source_type_id, url, content, published_at, is_processed) VALUES
((SELECT id FROM sources WHERE url = 'https://www.channel12.co.il'), (SELECT id FROM source_type WHERE name = 'news_website'), 'https://www.channel12.co.il/news/iran-sanctions-2024-001', 
'ארצות הברית הטילה סנקציות חדשות על איראן היום. הסנקציות מכוונות נגד תעשיית הנפט האיראנית ומטרתן להגביל את יכולתה של טהראן לממן את תוכנית הגרעין שלה. משרד האוצר האמריקאי הודיע כי הסנקציות כוללות הקפאת נכסים של חברות נפט איראניות וחברות שמסייעות להן לעקוף את הסנקציות הקיימות.', 
NOW() - INTERVAL '2 hours', false),

((SELECT id FROM sources WHERE url = 'https://www.ynet.co.il'), (SELECT id FROM source_type WHERE name = 'news_website'), 'https://www.ynet.co.il/articles/iran-oil-sanctions-2024', 
'הממשל האמריקאי מחמיר את הסנקציות על איראן. הסנקציות החדשות מתמקדות בתעשיית הנפט ומטרתן לחנוק את המשק האיראני. לפי הערכות, הסנקציות עשויות להפחית את יצוא הנפט האיראני ב-30 אחוזים. איראן הגיבה בחריפות וטענה כי הסנקציות הן פעולה עוינת.', 
NOW() - INTERVAL '3 hours', false),

((SELECT id FROM sources WHERE url = 'https://www.channel12.co.il'), (SELECT id FROM source_type WHERE name = 'news_website'), 'https://www.channel12.co.il/news/iran-economy-sanctions-impact', 
'הסנקציות האמריקאיות על איראן גורמות לנזק כלכלי משמעותי. המטבע האיראני ממשיך לרדת ומחירי המזון עולים. אזרחים איראניים מדווחים על קשיים כלכליים קשים. הממשלה האיראנית מנסה למצוא דרכים לעקוף את הסנקציות באמצעות סחר עם סין ורוסיה.', 
NOW() - INTERVAL '5 hours', false);

-- Insert Arabic news articles about Iran sanctions (Topic 1)
INSERT INTO raw_data (source_id, source_type_id, url, content, published_at, is_processed) VALUES
((SELECT id FROM sources WHERE url = 'https://www.aljazeera.net'), (SELECT id FROM source_type WHERE name = 'tv_channel'), 'https://www.aljazeera.net/news/iran-us-sanctions-2024', 
'فرضت الولايات المتحدة عقوبات جديدة على إيران تستهدف قطاع النفط. وتهدف العقوبات إلى الحد من قدرة طهران على تمويل برنامجها النووي. وأعلنت وزارة الخزانة الأمريكية أن العقوبات تشمل تجميد أصول شركات النفط الإيرانية والشركات التي تساعدها على التهرب من العقوبات القائمة.', 
NOW() - INTERVAL '1 hour', false),

((SELECT id FROM sources WHERE url = 'https://www.alarabiya.net'), (SELECT id FROM source_type WHERE name = 'news_website'), 'https://www.alarabiya.net/iran/sanctions-oil-sector-2024', 
'تشديد أمريكي جديد للعقوبات على إيران يستهدف صناعة النفط. العقوبات الجديدة تهدف إلى خنق الاقتصاد الإيراني. وفقا للتقديرات، قد تؤدي العقوبات إلى تقليل صادرات النفط الإيرانية بنسبة 30 بالمئة. ردت إيران بشدة واعتبرت العقوبات عملا عدائيا.', 
NOW() - INTERVAL '4 hours', false),

((SELECT id FROM sources WHERE url = 'https://www.almayadeen.net'), (SELECT id FROM source_type WHERE name = 'tv_channel'), 'https://www.almayadeen.net/news/iran-sanctions-economic-impact', 
'العقوبات الأمريكية على إيران تسبب أضرارا اقتصادية كبيرة. العملة الإيرانية تواصل الانخفاض وأسعار المواد الغذائية ترتفع. يبلغ المواطنون الإيرانيون عن صعوبات اقتصادية شديدة. تحاول الحكومة الإيرانية إيجاد طرق للتحايل على العقوبات من خلال التجارة مع الصين وروسيا.', 
NOW() - INTERVAL '6 hours', false);

-- Insert Hebrew news articles about Iran nuclear program (Topic 2)
INSERT INTO raw_data (source_id, source_type_id, url, content, published_at, is_processed) VALUES
((SELECT id FROM sources WHERE url = 'https://www.ynet.co.il'), (SELECT id FROM source_type WHERE name = 'news_website'), 'https://www.ynet.co.il/articles/iran-nuclear-enrichment-2024', 
'איראן מעשירה אורניום ברמות גבוהות יותר מאי פעם. לפי דיווחי הסוכנות הבינלאומית לאנרגיה אטומית, איראן הגיעה לרמת העשרה של 60 אחוזים. מומחים מזהירים כי איראן קרובה מאוד ליכולת לייצר נשק גרעיני. ישראל והמערב מביעים דאגה עמוקה מההתקדמות האיראנית.', 
NOW() - INTERVAL '8 hours', false),

((SELECT id FROM sources WHERE url = 'https://www.channel12.co.il'), (SELECT id FROM source_type WHERE name = 'news_website'), 'https://www.channel12.co.il/news/iaea-iran-nuclear-report', 
'הסוכנות הבינלאומית לאנרגיה אטומית פרסמה דוח חמור על תוכנית הגרעין האיראנית. הדוח מצביע על כך שאיראן מסרבת לשתף פעולה עם הפקחים. כמות האורניום המועשר באיראן גדלה באופן משמעותי. המדינות המערביות שוקלות צעדים נוספים נגד איראן.', 
NOW() - INTERVAL '10 hours', false),

((SELECT id FROM sources WHERE url = 'https://www.ynet.co.il'), (SELECT id FROM source_type WHERE name = 'news_website'), 'https://www.ynet.co.il/articles/iran-nuclear-facilities-expansion', 
'איראן מרחיבה את מתקני הגרעין שלה. תמונות לוויין מראות בנייה של מתקנים חדשים במספר אתרים. מומחים מעריכים שאיראן מתכוננת להגדיל את כמות האורניום המועשר. ישראל מתריעה מפני הסכנה הגרעינית האיראנית.', 
NOW() - INTERVAL '12 hours', false);

-- Insert Arabic news articles about Iran nuclear program (Topic 2)
INSERT INTO raw_data (source_id, source_type_id, url, content, published_at, is_processed) VALUES
((SELECT id FROM sources WHERE url = 'https://www.aljazeera.net'), (SELECT id FROM source_type WHERE name = 'tv_channel'), 'https://www.aljazeera.net/news/iran-uranium-enrichment-levels', 
'إيران تخصب اليورانيوم بمستويات أعلى من أي وقت مضى. وفقا لتقارير الوكالة الدولية للطاقة الذرية، وصلت إيران إلى مستوى تخصيب 60 بالمئة. يحذر الخبراء من أن إيران قريبة جدا من القدرة على إنتاج سلاح نووي. تعرب إسرائيل والغرب عن قلق عميق من التقدم الإيراني.', 
NOW() - INTERVAL '7 hours', false),

((SELECT id FROM sources WHERE url = 'https://www.alarabiya.net'), (SELECT id FROM source_type WHERE name = 'news_website'), 'https://www.alarabiya.net/iran/iaea-nuclear-program-report', 
'نشرت الوكالة الدولية للطاقة الذرية تقريرا خطيرا عن البرنامج النووي الإيراني. يشير التقرير إلى أن إيران ترفض التعاون مع المفتشين. كمية اليورانيوم المخصب في إيران زادت بشكل كبير. تدرس الدول الغربية اتخاذ إجراءات إضافية ضد إيران.', 
NOW() - INTERVAL '9 hours', false),

((SELECT id FROM sources WHERE url = 'https://www.almayadeen.net'), (SELECT id FROM source_type WHERE name = 'tv_channel'), 'https://www.almayadeen.net/news/iran-nuclear-facilities-development', 
'إيران توسع منشآتها النووية. تظهر صور الأقمار الصناعية بناء منشآت جديدة في عدة مواقع. يقدر الخبراء أن إيران تستعد لزيادة كمية اليورانيوم المخصب. تحذر إسرائيل من الخطر النووي الإيراني.', 
NOW() - INTERVAL '11 hours', false);

-- Insert Hebrew news articles about Iran-Russia relations (Topic 3)
INSERT INTO raw_data (source_id, source_type_id, url, content, published_at, is_processed) VALUES
((SELECT id FROM sources WHERE url = 'https://www.channel12.co.il'), (SELECT id FROM source_type WHERE name = 'news_website'), 'https://www.channel12.co.il/news/iran-russia-military-cooperation', 
'איראן ורוסיה מעמיקות את שיתוף הפעולה הצבאי ביניהן. איראן מספקת לרוסיה מל"טים לשימוש במלחמה באוקראינה. בתמורה, רוסיה מעבירה לאיראן טכנולוגיה צבאית מתקדמת. המערב מודאג מהשותפות ההולכת ומתהדקת בין שתי המדינות.', 
NOW() - INTERVAL '14 hours', false),

((SELECT id FROM sources WHERE url = 'https://www.ynet.co.il'), (SELECT id FROM source_type WHERE name = 'news_website'), 'https://www.ynet.co.il/articles/iran-russia-drones-deal', 
'רוסיה רוכשת מל"טים איראניים למלחמה באוקראינה. המל"טים האיראניים משמשים את רוסיה לתקיפות על תשתיות אוקראיניות. ארצות הברית מגנה את שיתוף הפעולה הצבאי בין איראן לרוסיה. ישראל עוקבת בדאגה אחר העמקת הקשרים בין המדינות.', 
NOW() - INTERVAL '16 hours', false);

-- Insert Arabic news articles about Iran-Russia relations (Topic 3)
INSERT INTO raw_data (source_id, source_type_id, url, content, published_at, is_processed) VALUES
((SELECT id FROM sources WHERE url = 'https://www.aljazeera.net'), (SELECT id FROM source_type WHERE name = 'tv_channel'), 'https://www.aljazeera.net/news/iran-russia-strategic-partnership', 
'إيران وروسيا تعمقان التعاون العسكري بينهما. تزود إيران روسيا بطائرات مسيرة للاستخدام في الحرب على أوكرانيا. في المقابل، تنقل روسيا لإيران تكنولوجيا عسكرية متقدمة. يشعر الغرب بالقلق من الشراكة المتنامية بين البلدين.', 
NOW() - INTERVAL '13 hours', false),

((SELECT id FROM sources WHERE url = 'https://www.alarabiya.net'), (SELECT id FROM source_type WHERE name = 'news_website'), 'https://www.alarabiya.net/iran/russia-drones-purchase-deal', 
'روسيا تشتري طائرات مسيرة إيرانية للحرب في أوكرانيا. تستخدم روسيا الطائرات المسيرة الإيرانية لشن هجمات على البنية التحتية الأوكرانية. تدين الولايات المتحدة التعاون العسكري بين إيران وروسيا. تراقب إسرائيل بقلق تعميق العلاقات بين البلدين.', 
NOW() - INTERVAL '15 hours', false);

-- Insert miscellaneous Hebrew news articles (Topic 4)
INSERT INTO raw_data (source_id, source_type_id, url, content, published_at, is_processed) VALUES
((SELECT id FROM sources WHERE url = 'https://www.ynet.co.il'), (SELECT id FROM source_type WHERE name = 'news_website'), 'https://www.ynet.co.il/articles/iran-protests-economy', 
'הפגנות פורצות באיראן בעקבות המצב הכלכלי הקשה. אזרחים איראניים יוצאים לרחובות במחאה על עליית המחירים והאבטלה. המשטר האיראני מגיב בכוח ועוצר מפגינים. ארגוני זכויות אדם מגנים את הדיכוי האיראני.', 
NOW() - INTERVAL '18 hours', false),

((SELECT id FROM sources WHERE url = 'https://www.channel12.co.il'), (SELECT id FROM source_type WHERE name = 'news_website'), 'https://www.channel12.co.il/news/iran-regional-influence', 
'איראן מנסה להרחיב את השפעתה האזורית. טהראן מחזקת את נוכחותה בסוריה, עיראק ולבנון. ישראל רואה באיראן איום אסטרטגי מרכזי. המערב מודאג מהשאיפות האיראניות להגמוניה אזורית.', 
NOW() - INTERVAL '20 hours', false);

-- Insert miscellaneous Arabic news articles (Topic 4)
INSERT INTO raw_data (source_id, source_type_id, url, content, published_at, is_processed) VALUES
((SELECT id FROM sources WHERE url = 'https://www.almayadeen.net'), (SELECT id FROM source_type WHERE name = 'tv_channel'), 'https://www.almayadeen.net/news/iran-economic-protests', 
'تندلع احتجاجات في إيران بسبب الوضع الاقتصادي الصعب. يخرج المواطنون الإيرانيون إلى الشوارع احتجاجا على ارتفاع الأسعار والبطالة. يرد النظام الإيراني بالقوة ويعتقل المتظاهرين. تدين منظمات حقوق الإنسان القمع الإيراني.', 
NOW() - INTERVAL '17 hours', false),

((SELECT id FROM sources WHERE url = 'https://www.aljazeera.net'), (SELECT id FROM source_type WHERE name = 'tv_channel'), 'https://www.aljazeera.net/news/iran-regional-expansion', 
'إيران تحاول توسيع نفوذها الإقليمي. تعزز طهران وجودها في سوريا والعراق ولبنان. تعتبر إسرائيل إيران تهديدا استراتيجيا رئيسيا. يشعر الغرب بالقلق من الطموحات الإيرانية للهيمنة الإقليمية.', 
NOW() - INTERVAL '19 hours', false);

-- Verify the inserted data
SELECT 'Sample data inserted successfully!' as status;
SELECT 'Total news articles:', COUNT(*) FROM raw_data;
SELECT 'Hebrew articles:', COUNT(*) FROM raw_data WHERE content LIKE '%א%' OR content LIKE '%ב%' OR content LIKE '%ג%';
SELECT 'Arabic articles:', COUNT(*) FROM raw_data WHERE content LIKE '%ا%' OR content LIKE '%ب%' OR content LIKE '%ت%';

# دليل التشغيل السريع - Iran News Pipeline Scheduler

## ✅ الإعداد الأولي (مرة واحدة فقط)

### 1. تثبيت المكتبات
```bash
pip install -r requirements.txt
```

### 2. التأكد من ملف `.env`
تأكد من وجود الملف وفيه:
```
DATABASE_HOST=...
DATABASE_PORT=5432
DATABASE_NAME=iran_news_db
DATABASE_USER=...
DATABASE_PASSWORD=...

OPENAI_API_KEY_IRAN_NEWS_TRANSLATION_HEBREW_ARABIC=sk-proj-...
OPENAI_API_KEY_IRAN_NEWS_CLUSTERING_ANALYSIS=sk-proj-...
OPENAI_API_KEY_IRAN_NEWS_REPORT_SUMMARIZATION=sk-proj-...
```

---

## 🚀 التشغيل

### طريقة 1: تشغيل الـ Scheduler (موصى به)
```bash
python run_scheduler.py
```

**ماذا يحدث؟**
- يشتغل تلقائياً كل 15 دقيقة
- يعالج آخر 10 أخبار غير معالجة
- يسجل كل العمليات في `pipeline_scheduler.log`
- اضغط `Ctrl+C` للإيقاف

### طريقة 2: تشغيل يدوي (مرة واحدة)
```bash
python test_scheduler.py
```

---

## 📊 ماذا يفعل البايبلاين؟

### المرحلة 1: الترجمة
- يجيب آخر 10 أخبار من `raw_data` حيث `translation_status = 'pending'`
- يكتشف اللغة (عبري/عربي)
- يترجم العبري للعربي
- يحفظ الترجمة في `arabic_content`

### المرحلة 2: الكلسترينج
- يجيب آخر 10 أخبار من `raw_data` حيث `is_processed = false`
- يستخرج النقاط الرئيسية من كل خبر
- يجمع الأخبار المتشابهة في كلسترات
- يعالج الأخبار الفريدة (كلسترات فردية)
- يحفظ الكلسترات في `clusters` و `cluster_members`

### المرحلة 3: توليد التقارير
- يجيب الكلسترات اللي ما عندها تقارير
- يولد تقرير احترافي لكل كلستر مع:
  * عنوان جذاب
  * محتوى احترافي
  * مصادر قابلة للنقر (Markdown hyperlinks)
  * تصنيف نوع المحتوى
- يحفظ التقارير في `output_content`
- يعلم الأخبار كـ `is_processed = true`

---

## ⚙️ التخصيص

### تغيير عدد الأخبار
افتح `pipeline_scheduler.py` وعدل:
```python
BATCH_SIZE = 10  # غير للرقم المطلوب
```

### تغيير الفترة الزمنية
افتح `pipeline_scheduler.py` وعدل:
```python
INTERVAL_MINUTES = 15  # غير للفترة المطلوبة (بالدقائق)
```

---

## 📝 Logs

### عرض Logs مباشر
```bash
tail -f pipeline_scheduler.log
```

### البحث في Logs
```bash
grep "ERROR" pipeline_scheduler.log
grep "completed successfully" pipeline_scheduler.log
```

---

## 🔍 استكشاف الأخطاء

### لا توجد أخبار للمعالجة
**السبب:** كل الأخبار معالجة أو لا توجد أخبار جديدة

**الحل:**
1. أضف أخبار جديدة لجدول `raw_data`
2. أو أعد تعيين الأخبار الموجودة:
```sql
UPDATE raw_data SET is_processed = false, translation_status = 'pending';
```

### أخطاء OpenAI API
**السبب:** مشكلة في API keys أو الرصيد

**الحل:**
1. تأكد من صحة API keys في `.env`
2. تأكد من وجود رصيد كافي
3. راجع `pipeline_scheduler.log` للتفاصيل

### أخطاء قاعدة البيانات
**السبب:** مشكلة في الاتصال

**الحل:**
1. تأكد من صحة بيانات الاتصال في `.env`
2. تأكد من أن قاعدة البيانات شغالة
3. اختبر الاتصال:
```bash
python tests/test_database_connection.py
```

---

## 📈 مراقبة الأداء

### الإحصائيات في كل تشغيل
```
Total execution time: X.XX seconds
News translated: X
Clusters created: X
Reports generated: X
News processed: X
```

### التكلفة التقريبية
- **ترجمة خبر واحد:** ~$0.001-0.002
- **كلسترينج 10 أخبار:** ~$0.01-0.02
- **توليد تقرير واحد:** ~$0.005-0.01
- **إجمالي 10 أخبار:** ~$0.05-0.10

---

## 🛑 الإيقاف

### إيقاف مؤقت
اضغط `Ctrl+C` في Terminal

### إيقاف نهائي (إذا كان يعمل كـ service)
```bash
sudo systemctl stop iran-news-pipeline
```

---

## 🔄 إعادة التشغيل

### بعد تعديل الكود
1. أوقف الـ Scheduler (`Ctrl+C`)
2. شغله مرة ثانية:
```bash
python run_scheduler.py
```

### بعد تعديل `.env`
نفس الخطوات أعلاه

---

## 💡 نصائح

1. **راقب Logs بانتظام** للتأكد من عدم وجود أخطاء
2. **راقب التكاليف** على OpenAI dashboard
3. **اختبر التعديلات** باستخدام `test_scheduler.py` قبل التشغيل التلقائي
4. **احتفظ بنسخة احتياطية** من قاعدة البيانات
5. **استخدم batch size صغير** (5-10) للبداية

---

## 📞 الدعم

إذا واجهت مشاكل:
1. راجع `pipeline_scheduler.log`
2. راجع `SCHEDULER_README.md` للتفاصيل
3. اختبر كل مرحلة على حدة:
   - `tests/test_translation_service.py`
   - `tests/test_clustering_pipeline.py`
   - `tests/test_report_generation_pipeline.py`

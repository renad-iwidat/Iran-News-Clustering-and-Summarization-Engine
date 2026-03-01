# Pipeline Scheduler - دليل الاستخدام

## نظرة عامة

الـ Scheduler يشغل البايبلاين تلقائياً كل 15 دقيقة لمعالجة آخر 10 أخبار غير معالجة.

---

## التشغيل السريع

### 1. تثبيت المكتبات
```bash
pip install -r requirements.txt
```

### 2. تشغيل الـ Scheduler
```bash
python run_scheduler.py
```

---

## الإعدادات

### تغيير عدد الأخبار المعالجة
افتح `pipeline_scheduler.py` وعدل:
```python
BATCH_SIZE = 10  # غير الرقم حسب حاجتك
```

### تغيير الفترة الزمنية
افتح `pipeline_scheduler.py` وعدل:
```python
INTERVAL_MINUTES = 15  # غير الرقم حسب حاجتك
```

---

## كيف يعمل؟

### المراحل
1. **Translation Pipeline**: يترجم الأخبار العبرية للعربية
2. **Clustering Pipeline**: يجمع الأخبار المتشابهة في كلسترات
3. **Report Generation Pipeline**: يولد تقارير احترافية مع عناوين ومصادر

### الجدولة
- يشتغل تلقائياً كل 15 دقيقة
- يعالج آخر 10 أخبار غير معالجة (`is_processed = false`)
- يسجل كل العمليات في `pipeline_scheduler.log`

---

## الإيقاف

اضغط `Ctrl+C` لإيقاف الـ Scheduler

---

## Logs

كل العمليات تتسجل في:
- **Console**: عرض مباشر
- **File**: `pipeline_scheduler.log`

---

## استكشاف الأخطاء

### المشكلة: الـ Scheduler ما يشتغل
**الحل:**
1. تأكد من تثبيت المكتبات: `pip install -r requirements.txt`
2. تأكد من ملف `.env` موجود وفيه المفاتيح الصحيحة
3. تأكد من الاتصال بقاعدة البيانات

### المشكلة: ما في أخبار للمعالجة
**الحل:**
- تأكد من وجود أخبار في جدول `raw_data` مع `is_processed = false`
- أضف أخبار جديدة للاختبار

### المشكلة: أخطاء OpenAI API
**الحل:**
- تأكد من صحة API keys في `.env`
- تأكد من وجود رصيد كافي في حساب OpenAI

---

## تشغيل يدوي (بدون جدولة)

إذا بدك تشغل البايبلاين مرة واحدة بدون جدولة:

```python
from main_pipeline_service import MainPipelineService

pipeline = MainPipelineService()
stats = pipeline.run_full_pipeline(batch_size=10)
print(stats)
```

---

## الإحصائيات

الـ Scheduler يعرض إحصائيات بعد كل تشغيل:
- عدد الأخبار المترجمة
- عدد الكلسترات المنشأة
- عدد التقارير المولدة
- عدد الأخبار المعالجة
- وقت التنفيذ الكلي

---

## Production Deployment

### استخدام systemd (Linux)
```bash
# إنشاء service file
sudo nano /etc/systemd/system/iran-news-pipeline.service
```

```ini
[Unit]
Description=Iran News Clustering Pipeline Scheduler
After=network.target

[Service]
Type=simple
User=your_user
WorkingDirectory=/path/to/iran_news_clustering_pipeline
ExecStart=/usr/bin/python3 run_scheduler.py
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# تفعيل وتشغيل
sudo systemctl enable iran-news-pipeline
sudo systemctl start iran-news-pipeline
sudo systemctl status iran-news-pipeline
```

### استخدام Docker
```dockerfile
FROM python:3.9

WORKDIR /app
COPY . /app

RUN pip install -r requirements.txt

CMD ["python", "run_scheduler.py"]
```

---

## ملاحظات مهمة

1. **التكلفة**: كل تشغيل يستخدم OpenAI API، راقب التكاليف
2. **الأداء**: معالجة 10 أخبار تاخذ تقريباً 2-5 دقائق
3. **الأخطاء**: الـ Scheduler يستمر بالعمل حتى لو فشل تشغيل واحد
4. **Logs**: راجع الـ logs بانتظام للتأكد من عدم وجود مشاكل

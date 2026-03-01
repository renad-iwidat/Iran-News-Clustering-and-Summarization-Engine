# Iran News Reports API - دليل الاستخدام

## 🚀 تشغيل الـ API

### 1. تثبيت المكتبات
```bash
pip install -r requirements.txt
```

### 2. تشغيل السيرفر
```bash
python run_api.py
```

السيرفر سيعمل على: `http://localhost:8000`

---

## 📚 التوثيق التفاعلي

بعد تشغيل السيرفر، يمكنك الوصول للتوثيق التفاعلي:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 🔌 Endpoints

### 1. GET `/api/reports` - جلب كل التقارير

**الوصف:** جلب كل التقارير مع pagination

**Parameters:**
- `page` (optional): رقم الصفحة (default: 1)
- `limit` (optional): عدد التقارير (default: 20, max: 100)

**مثال على الطلب:**
```
GET http://localhost:8000/api/reports?page=1&limit=20
```

**Response:**
```json
{
  "success": true,
  "total": 9,
  "page": 1,
  "limit": 20,
  "reports": [
    {
      "id": 1,
      "title": "واشنطن تفرض عقوبات جديدة على صناعة النفط الإيرانية",
      "content": "فرضت الإدارة الأمريكية عقوبات جديدة...",
      "content_type": "medium_news",
      "word_count": 250,
      "cluster_topic": "العقوبات الأمريكية على إيران",
      "sources": [
        {
          "name": "Channel12",
          "url": "https://www.channel12.co.il/news/..."
        },
        {
          "name": "Ynet",
          "url": "https://www.ynet.co.il/articles/..."
        }
      ],
      "created_at": "2026-03-01T01:30:06Z"
    }
  ]
}
```

---

### 2. GET `/api/reports/{id}` - جلب تقرير محدد

**الوصف:** جلب تقرير محدد بكل تفاصيله

**Parameters:**
- `id` (required): معرف التقرير

**مثال على الطلب:**
```
GET http://localhost:8000/api/reports/1
```

**Response:**
```json
{
  "success": true,
  "report": {
    "id": 1,
    "title": "واشنطن تفرض عقوبات جديدة على صناعة النفط الإيرانية",
    "content": "فرضت الإدارة الأمريكية عقوبات جديدة على إيران، تركز بشكل خاص على صناعة النفط... [المصدر: [Ynet](https://www.ynet.co.il)]",
    "content_type": "medium_news",
    "word_count": 250,
    "cluster_topic": "العقوبات الأمريكية على إيران",
    "sources": [
      {
        "name": "Channel12",
        "url": "https://www.channel12.co.il/news/..."
      },
      {
        "name": "Ynet",
        "url": "https://www.ynet.co.il/articles/..."
      },
      {
        "name": "Alarabiya",
        "url": "https://www.alarabiya.net/iran/..."
      },
      {
        "name": "Aljazeera",
        "url": "https://www.aljazeera.net/news/..."
      }
    ],
    "created_at": "2026-03-01T01:30:06Z"
  }
}
```

---

### 3. GET `/api/reports/latest` - آخر التقارير

**الوصف:** جلب آخر التقارير

**Parameters:**
- `limit` (optional): عدد التقارير (default: 10, max: 50)

**مثال على الطلب:**
```
GET http://localhost:8000/api/reports/latest?limit=10
```

**Response:**
```json
{
  "success": true,
  "count": 10,
  "reports": [
    {
      "id": 9,
      "title": "...",
      "content": "...",
      "content_type": "medium_news",
      "word_count": 200,
      "cluster_topic": "...",
      "sources": [...],
      "created_at": "2026-03-01T02:00:00Z"
    }
  ]
}
```

---

### 4. GET `/health` - فحص صحة الـ API

**الوصف:** التحقق من أن الـ API شغالة

**مثال على الطلب:**
```
GET http://localhost:8000/health
```

**Response:**
```json
{
  "status": "healthy",
  "database": "connected",
  "version": "1.0.0"
}
```

---

## 🎨 استخدام من الفرونت إند

### JavaScript / React Example

```javascript
// جلب كل التقارير
async function getAllReports(page = 1, limit = 20) {
  const response = await fetch(
    `http://localhost:8000/api/reports?page=${page}&limit=${limit}`
  );
  const data = await response.json();
  return data.reports;
}

// جلب تقرير محدد
async function getReportById(reportId) {
  const response = await fetch(
    `http://localhost:8000/api/reports/${reportId}`
  );
  const data = await response.json();
  return data.report;
}

// جلب آخر التقارير
async function getLatestReports(limit = 10) {
  const response = await fetch(
    `http://localhost:8000/api/reports/latest?limit=${limit}`
  );
  const data = await response.json();
  return data.reports;
}

// مثال على الاستخدام
getAllReports(1, 20).then(reports => {
  reports.forEach(report => {
    console.log(report.title);
    console.log(report.content_type);
    console.log(report.sources);
  });
});
```

### TypeScript Types

```typescript
interface NewsSource {
  name: string;
  url: string;
}

interface NewsReport {
  id: number;
  title: string;
  content: string;
  content_type: string;
  word_count: number;
  cluster_topic: string;
  sources: NewsSource[];
  created_at: string;
}

interface ReportsResponse {
  success: boolean;
  total: number;
  page: number;
  limit: number;
  reports: NewsReport[];
}

interface SingleReportResponse {
  success: boolean;
  report: NewsReport;
}
```

---

## 🔧 Error Handling

### Error Response Format

```json
{
  "detail": "Report not found"
}
```

### HTTP Status Codes

- `200 OK`: نجح الطلب
- `404 Not Found`: التقرير غير موجود
- `500 Internal Server Error`: خطأ في السيرفر

---

## 🌐 CORS

الـ API مفعل عليها CORS بشكل افتراضي، مما يسمح بالوصول من أي domain.

في الإنتاج، يُنصح بتحديد الـ domains المسموح بها:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-frontend-domain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 📊 Response Fields شرح

### Report Object

| Field | Type | Description |
|-------|------|-------------|
| `id` | integer | معرف التقرير |
| `title` | string | عنوان التقرير الجذاب |
| `content` | string | المحتوى الكامل مع المصادر (Markdown format) |
| `content_type` | string | نوع المحتوى (short_news, medium_news, long_news, explanation, analysis) |
| `word_count` | integer | عدد الكلمات في التقرير |
| `cluster_topic` | string | موضوع الكلستر الأصلي |
| `sources` | array | قائمة المصادر |
| `created_at` | string | وقت إنشاء التقرير (ISO 8601 format) |

### Source Object

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | اسم المصدر (مثل: Channel12, Ynet, الجزيرة) |
| `url` | string | رابط الخبر الأصلي |

---

## 🚀 Production Deployment

### استخدام Gunicorn (موصى به للإنتاج)

```bash
pip install gunicorn
gunicorn api.iran_news_reports_api:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### استخدام Docker

```dockerfile
FROM python:3.9

WORKDIR /app
COPY . /app

RUN pip install -r requirements.txt

CMD ["uvicorn", "api.iran_news_reports_api:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## 🔍 Testing

### استخدام curl

```bash
# جلب كل التقارير
curl http://localhost:8000/api/reports

# جلب تقرير محدد
curl http://localhost:8000/api/reports/1

# آخر التقارير
curl http://localhost:8000/api/reports/latest?limit=5

# Health check
curl http://localhost:8000/health
```

### استخدام Postman

1. افتح Postman
2. استورد الـ API من: http://localhost:8000/openapi.json
3. جرب الـ endpoints

---

## 💡 نصائح

1. **Pagination**: استخدم pagination للأداء الأفضل
2. **Caching**: فكر في استخدام caching للتقارير الشائعة
3. **Rate Limiting**: في الإنتاج، أضف rate limiting
4. **Monitoring**: راقب الأداء والأخطاء
5. **Security**: في الإنتاج، أضف authentication إذا لزم الأمر

---

## 📞 الدعم

إذا واجهت مشاكل:
1. تأكد من تشغيل السيرفر: `python run_api.py`
2. تأكد من الاتصال بقاعدة البيانات
3. راجع logs السيرفر
4. استخدم `/health` endpoint للتحقق من الحالة

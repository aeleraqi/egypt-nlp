# 🤝 المساهمة في Egypt NLP

شكراً لاهتمامك بالمساهمة في Egypt NLP! نرحب بجميع المساهمات. 🇪🇬

## 📋 طرق المساهمة

### 1️⃣ الإبلاغ عن الأخطاء (Bug Reports)

إذا وجدت خطأ:

1. تحقق من [Issues](https://github.com/USERNAME/egypt-nlp/issues) أنه لم يُبلّغ عنه
2. افتح Issue جديد واستخدم القالب
3. اشرح المشكلة بوضوح مع مثال

### 2️⃣ اقتراح ميزات جديدة

لديك فكرة؟

1. افتح Issue مع عنوان "Feature Request: ..."
2. اشرح الميزة المقترحة
3. اشرح حالة الاستخدام

### 3️⃣ إضافة بيانات جديدة

- مدن أو أحياء جديدة
- أخطاء إملائية شائعة
- تحسينات على قاموس التصحيح

### 4️⃣ تحسين الكود

## 🚀 كيفية المساهمة بالكود

### الخطوة 1: Fork المشروع

اضغط على زر "Fork" في أعلى الصفحة

### الخطوة 2: Clone المشروع

```bash
git clone https://github.com/YOUR-USERNAME/egypt-nlp.git
cd egypt-nlp
```

### الخطوة 3: إنشاء Branch جديد

```bash
git checkout -b feature/amazing-feature
```

أو

```bash
git checkout -b fix/bug-fix
```

### الخطوة 4: إعداد بيئة التطوير

```bash
# إنشاء virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# أو
venv\Scripts\activate  # Windows

# تثبيت المكتبة في وضع التطوير
pip install -e .

# تثبيت أدوات التطوير (اختياري)
pip install pytest black flake8
```

### الخطوة 5: إجراء التغييرات

1. عدّل الكود
2. اختبر التغييرات:

```bash
# اختبار يدوي
python demo.py
python egypt_nlp/examples.py

# اختبار تلقائي (إذا كنت تستخدم pytest)
pytest
```

### الخطوة 6: Commit التغييرات

```bash
git add .
git commit -m "وصف واضح للتغيير"
```

**أمثلة على رسائل Commit جيدة:**
```
✅ إضافة دعم لمحافظة الوادي الجديد
✅ إصلاح: خطأ في التعرف على "شرم الشيخ"
✅ تحسين: أداء fuzzy matching
✅ توثيق: إضافة أمثلة للمبتدئين
```

### الخطوة 7: Push للـ Branch

```bash
git push origin feature/amazing-feature
```

### الخطوة 8: فتح Pull Request

1. اذهب إلى repository الخاص بك على GitHub
2. اضغط "Compare & pull request"
3. اكتب وصف واضح للتغييرات
4. اضغط "Create pull request"

## 📝 معايير الكود

### 1. الأسلوب

- اتبع [PEP 8](https://pep8.org/)
- استخدم أسماء متغيرات واضحة
- أضف docstrings للوظائف

```python
def extract_locations(text: str) -> List[Dict]:
    """
    استخراج المواقع الجغرافية من النص
    
    Args:
        text: النص المراد البحث فيه
    
    Returns:
        قائمة بالمواقع المستخرجة
    """
    pass
```

### 2. التنسيق

```bash
# استخدم Black للتنسيق التلقائي
black egypt_nlp/

# فحص بـ flake8
flake8 egypt_nlp/
```

### 3. الاختبارات

- أضف tests للميزات الجديدة
- تأكد أن الـ tests القديمة تعمل

### 4. التوثيق

- حدّث README.md إذا لزم الأمر
- أضف أمثلة للميزات الجديدة
- حدّث CHANGELOG.md

## 🎯 أنواع المساهمات المطلوبة

### عالية الأولوية 🔥

- [ ] إضافة tests شاملة
- [ ] دعم اللغة الإنجليزية
- [ ] تحسين Fuzzy Matching
- [ ] إضافة أخطاء إملائية شائعة جديدة

### متوسطة الأولوية ⭐

- [ ] تحسين الأداء
- [ ] إضافة أمثلة جديدة
- [ ] تحسين التوثيق
- [ ] إضافة الإحداثيات الجغرافية

### منخفضة الأولوية 💡

- [ ] دعم اللهجات المحلية
- [ ] واجهة ويب
- [ ] API

## ❓ أسئلة شائعة

### كيف أضيف مدينة جديدة؟

1. عدّل `egypt_nlp/data.py`
2. أضف المدينة في `ADMINISTRATIVE_DATA`
3. اختبر التغيير

### كيف أضيف خطأ إملائي شائع؟

1. عدّل `egypt_nlp/extractor_enhanced.py`
2. أضف في `self.common_errors`
3. اختبر التصحيح

### كيف أبلّغ عن مشكلة أمنية؟

أرسل email خاص إلى: security@egypt-nlp.com
(لا تفتح Issue عام)

## 🙏 شكر وتقدير

كل المساهمين سيُذكرون في:
- README.md
- Release notes
- الموقع الإلكتروني (قريباً)

## 📜 اتفاقية السلوك

### القواعد الأساسية

- 🤝 احترم الجميع
- 💬 كن بناءً في النقد
- 🎯 ركز على المشكلة، ليس الشخص
- 🌍 رحّب بالجميع

### غير مقبول

- ❌ اللغة المسيئة
- ❌ التحرش
- ❌ السلوك غير المهني

## 📞 تواصل معنا

- **GitHub Issues**: للأخطاء والاقتراحات
- **Discussions**: للأسئلة العامة
- **Email**: contact@egypt-nlp.com

---

شكراً لمساهمتك في جعل Egypt NLP أفضل! 🇪🇬❤️

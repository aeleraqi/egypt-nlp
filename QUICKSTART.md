# 🚀 دليل البداية السريعة - Egypt NLP

## التثبيت

```bash
# من المجلد الحالي
cd /path/to/egypt-nlp
pip install -e .

# أو نسخ المجلد egypt_nlp إلى مشروعك
```

## الاستخدام البسيط

### 1. استيراد المكتبة

```python
from egypt_nlp import extract, find_governorate, EgyptGeoExtractor
```

### 2. استخراج المواقع

```python
text = "أنا من القاهرة، أعيش في مدينة نصر"
locations = extract(text)

for loc in locations:
    print(loc['name'], '-', loc['type'])
```

### 3. العثور على المحافظة

```python
text = "سافرت إلى شرم الشيخ"
governorate = find_governorate(text)
print(governorate)  # جنوب سيناء
```

### 4. استخدام متقدم

```python
extractor = EgyptGeoExtractor()

# معلومات تفصيلية
info = extractor.get_location_info("الزمالك")
print(info)

# التسلسل الهرمي
hierarchy = extractor.get_hierarchy("الزمالك")
print(hierarchy)

# إحصائيات
stats = extractor.get_statistics("نص طويل هنا...")
print(stats['governorates'])
```

## أمثلة جاهزة

```bash
# تشغيل العرض التجريبي
python demo.py

# تشغيل كل الأمثلة
python egypt_nlp/examples.py
```

## الوظائف الرئيسية

| الوظيفة | الوصف |
|---------|--------|
| `extract(text)` | استخراج كل المواقع من النص |
| `find_governorate(text)` | العثور على المحافظة |
| `extractor.extract_locations(text)` | استخراج مع معلومات تفصيلية |
| `extractor.get_location_info(name)` | معلومات عن موقع محدد |
| `extractor.get_hierarchy(name)` | التسلسل الهرمي |
| `extractor.get_statistics(text)` | إحصائيات النص |
| `extractor.search_by_governorate(gov)` | بحث بالمحافظة |
| `extractor.search_by_region(region)` | بحث بالإقليم |

## المستويات الإدارية

```
الإقليم الاقتصادي (7 أقاليم)
    ↓
المحافظة (27 محافظة)
    ↓
المركز/الحي (283 مركز)
    ↓
الوحدة المحلية (762 وحدة)
```

## المساعدة

للمزيد من المعلومات، اقرأ:
- `README.md` - الوثائق الكاملة
- `examples.py` - أمثلة شاملة
- `demo.py` - عرض تجريبي سريع

---
Made with ❤️ in Egypt 🇪🇬

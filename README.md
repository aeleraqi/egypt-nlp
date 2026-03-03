# 🇪🇬 Egypt NLP - مكتبة استخراج الكيانات الجغرافية المصرية

مكتبة Python متخصصة في التعرف على واستخراج الأسماء الجغرافية المصرية من النصوص العربية.

A specialized Python library for extracting and recognizing Egyptian geographic entities from Arabic text.

## ✨ المميزات / Features

- 🏛️ **قاعدة بيانات شاملة**: جميع محافظات مصر الـ 27 مع المراكز والوحدات المحلية
- 🔍 **استخراج ذكي**: التعرف التلقائي على المواقع في النصوص العربية
- 🗺️ **التسلسل الهرمي**: الحصول على التقسيم الإداري الكامل لأي موقع
- 📊 **تحليل إحصائي**: احصاءات شاملة عن المواقع المذكورة في النصوص
- 🌍 **الأقاليم الاقتصادية**: تصنيف حسب الأقاليم السبعة
- 🔤 **تطبيع النصوص**: معالجة الاختلافات في الكتابة والتشكيل
- 🚀 **سريع وفعال**: بحث محسّن باستخدام فهارس متقدمة

## 📦 التثبيت / Installation

```bash
# من المصدر
git clone https://github.com/yourusername/egypt-nlp.git
cd egypt-nlp
pip install -e .

# أو باستخدام pip (قريباً)
pip install egypt-nlp
```

## 🚀 بداية سريعة / Quick Start

### استخراج بسيط

```python
from egypt_nlp import extract

text = "أنا من القاهرة، أعيش في مدينة نصر"
locations = extract(text)

for loc in locations:
    print(f"{loc['name']} - {loc['type']}")
```

**النتيجة:**
```
القاهرة - governorate
مدينة نصر - district
```

### العثور على المحافظة

```python
from egypt_nlp import find_governorate

text = "سافرت إلى شرم الشيخ"
governorate = find_governorate(text)
print(governorate)  # جنوب سيناء
```

## 📚 أمثلة متقدمة / Advanced Examples

### 1. استخدام الكلاس الرئيسي

```python
from egypt_nlp import EgyptGeoExtractor

extractor = EgyptGeoExtractor()

# استخراج المواقع
text = "ولدت في الإسكندرية ودرست في القاهرة"
locations = extractor.extract_locations(text)

for loc in locations:
    print(f"📍 {loc['name']}")
    print(f"   النوع: {loc['type']}")
    print(f"   المحافظة: {loc['info']['governorate']}")
    print(f"   الإقليم: {loc['info']['region']}")
```

### 2. الحصول على معلومات تفصيلية

```python
extractor = EgyptGeoExtractor()

# معلومات عن موقع محدد
info = extractor.get_location_info("مدينة نصر")

print(info)
# {
#     'level': 'district',
#     'district': 'مدينة نصر',
#     'governorate': 'القاهرة',
#     'region': 'القاهرة الكبرى',
#     'type': 'حضري',
#     'units': ['الحي الأول', 'الحي الثامن', ...]
# }
```

### 3. التسلسل الهرمي

```python
hierarchy = extractor.get_hierarchy("الزمالك")

print(hierarchy)
# {
#     'region': 'القاهرة الكبرى',
#     'governorate': 'القاهرة',
#     'district': 'القاهرة',
#     'unit': 'الزمالك'
# }
```

### 4. إحصائيات النص

```python
text = """
بدأت رحلتي من القاهرة، مررت بالجيزة والإسكندرية.
زرت مرسى مطروح والعلمين قبل العودة.
"""

stats = extractor.get_statistics(text)

print(f"المحافظات: {stats['governorates']}")
print(f"الأقاليم: {stats['regions']}")
print(f"إجمالي المواقع: {stats['total_locations']}")
```

### 5. البحث عن محافظة

```python
result = extractor.search_by_governorate("القاهرة")

print(f"الإقليم: {result['region']}")
print(f"عدد المراكز: {result['total_districts']}")
print(f"عدد الوحدات: {result['total_units']}")
```

### 6. البحث عن إقليم

```python
result = extractor.search_by_region("القاهرة الكبرى")

print(f"المحافظات: {result['governorates']}")
print(f"عدد المحافظات: {result['total_governorates']}")
```

### 7. استخراج مع السياق

```python
locations = extractor.extract_with_context(
    text="ولدت في القاهرة ودرست في الإسكندرية",
    context_chars=20
)

for loc in locations:
    print(f"{loc['name']}: {loc['full_context']}")
```

## 🗂️ هيكل البيانات / Data Structure

### المستويات الإدارية

```
الإقليم الاقتصادي (Region)
    ↓
المحافظة (Governorate)
    ↓
المركز/الحي (District)
    ↓
الوحدة المحلية/الحي الفرعي (Unit)
```

### الأقاليم السبعة

1. **القاهرة الكبرى**: القاهرة، الجيزة، القليوبية
2. **الإسكندرية**: الإسكندرية، البحيرة، مطروح
3. **قناة السويس**: بورسعيد، الإسماعيلية، السويس، شمال سيناء، جنوب سيناء
4. **الدلتا**: الدقهلية، الشرقية، الغربية، كفر الشيخ، المنوفية، دمياط
5. **شمال الصعيد**: الفيوم، بني سويف، المنيا
6. **وسط الصعيد**: أسيوط، سوهاج
7. **جنوب الصعيد**: قنا، الأقصر، أسوان، البحر الأحمر، الوادي الجديد

## 🔧 الوظائف المتاحة / Available Functions

### الوظائف السريعة

- `extract(text)` - استخراج سريع للمواقع
- `find_governorate(text)` - العثور على أول محافظة

### كلاس EgyptGeoExtractor

#### وظائف الاستخراج
- `extract_locations(text)` - استخراج كل المواقع
- `extract_with_context(text, context_chars)` - استخراج مع السياق
- `find_governorate(text)` - العثور على محافظة
- `find_all_governorates(text)` - كل المحافظات
- `find_region(text)` - تحديد الإقليم

#### وظائف المعلومات
- `get_location_info(location_name)` - معلومات تفصيلية
- `get_hierarchy(location_name)` - التسلسل الهرمي
- `get_statistics(text)` - إحصائيات النص

#### وظائف البحث
- `search_by_governorate(governorate)` - بحث بالمحافظة
- `search_by_region(region)` - بحث بالإقليم
- `is_location_in_text(text, location)` - التحقق من وجود موقع

## 📊 حالات الاستخدام / Use Cases

### 1. تحليل النصوص الإخبارية

```python
news = """
افتتح الرئيس مشروع جديد في الإسكندرية يربط العجمي بالعامرية.
المشروع سيخدم محافظات الإسكندرية والبحيرة ومطروح.
"""

locations = extract(news)
stats = extractor.get_statistics(news)

print(f"المناطق المتأثرة: {stats['governorates']}")
```

### 2. تصنيف المحتوى الجغرافي

```python
def classify_by_region(text):
    extractor = EgyptGeoExtractor()
    region = extractor.find_region(text)
    return region

# استخدام
article_region = classify_by_region("حادث في طريق القاهرة الإسكندرية")
```

### 3. استخراج بيانات من النماذج

```python
form_data = "العنوان: شارع النيل، الزمالك، القاهرة"
extractor = EgyptGeoExtractor()

governorate = extractor.find_governorate(form_data)
hierarchy = extractor.get_hierarchy("الزمالك")

print(f"المحافظة: {governorate}")
print(f"الحي: {hierarchy['unit']}")
```

### 4. تحليل وسائل التواصل الاجتماعي

```python
tweet = "الجو جميل اليوم في شرم الشيخ #مصر #السياحة"
locations = extract(tweet)

for loc in locations:
    print(f"موقع مذكور: {loc['name']}")
```

## 🧪 تشغيل الأمثلة / Running Examples

```bash
cd egypt_nlp
python examples.py
```

## 📈 الإحصائيات / Statistics

- **27 محافظة**
- **283 مركز وحي**
- **762 وحدة محلية وحي فرعي**
- **7 أقاليم اقتصادية**

## 🤝 المساهمة / Contributing

نرحب بالمساهمات! يرجى:

1. Fork المشروع
2. إنشاء فرع للميزة الجديدة (`git checkout -b feature/AmazingFeature`)
3. Commit التغييرات (`git commit -m 'Add some AmazingFeature'`)
4. Push للفرع (`git push origin feature/AmazingFeature`)
5. فتح Pull Request

## 📝 الترخيص / License

هذا المشروع مرخص تحت رخصة MIT - انظر ملف [LICENSE](LICENSE) للتفاصيل.

## 🙏 شكر وتقدير / Acknowledgments

- بيانات التقسيم الإداري من الجهاز المركزي للتعبئة العامة والإحصاء
- مساهمات المجتمع المفتوح

## 📧 التواصل / Contact

- GitHub Issues: [Report Bug](https://github.com/yourusername/egypt-nlp/issues)
- Email: your.email@example.com

## 🗺️ خارطة الطريق / Roadmap

- [ ] إضافة fuzzy matching للأسماء المشابهة
- [ ] دعم اللغة الإنجليزية
- [ ] إضافة الأحداثيات الجغرافية (GPS)
- [ ] دمج مع خرائط جوجل
- [ ] API للاستخدام عبر الويب
- [ ] تطبيق ويب تفاعلي

---

Made with ❤️ in Egypt 🇪🇬

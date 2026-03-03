# 📝 Changelog - سجل التغييرات

## [2.0.0] - 2024-03-03

### ✨ ميزات جديدة (New Features)

#### 🔧 معالجة الأخطاء الكتابية
- **Fuzzy Matching**: التطابق التقريبي باستخدام Levenshtein Distance
- **EnhancedEgyptGeoExtractor**: كلاس جديد محسّن
- **قاموس الأخطاء الشائعة**: أكثر من 50 خطأ إملائي شائع
- **اقتراح التصحيحات**: وظيفة `suggest_corrections()`
- **مستويات الثقة**: Confidence scores لكل تطابق

#### 📊 الأخطاء المعالجة
- الأخطاء الإملائية في أسماء المحافظات
- الأخطاء في المدن الجديدة (6 أكتوبر، 10 رمضان)
- الأخطاء في الأحياء الشائعة
- اختلافات الكتابة (الهمزات، التاء المربوطة)

### 🔄 تحسينات (Improvements)

- **تطبيع محسّن**: معالجة أفضل للنصوص العربية
- **أداء أفضل**: فهارس محسّنة للبحث
- **دقة أعلى**: تقليل False Positives

### 📚 توثيق جديد

- `SPELLING_ERRORS.md`: دليل شامل لمعالجة الأخطاء
- `examples_enhanced.py`: 7 أمثلة جديدة
- تحديث `README.md` بالميزات الجديدة

### 🆕 وظائف جديدة

```python
# EnhancedEgyptGeoExtractor
extractor = EnhancedEgyptGeoExtractor(fuzzy_threshold=0.85)

# extract_enhanced
locations = extract_enhanced(text)

# suggest_corrections
suggestions = suggest_corrections(text)

# find_closest_match
match = extractor.find_closest_match("الاسكندريه")
```

### 📦 الملفات الجديدة

- `extractor_enhanced.py`: المستخرج المحسّن
- `examples_enhanced.py`: أمثلة معالجة الأخطاء
- `SPELLING_ERRORS.md`: توثيق شامل

---

## [1.0.0] - 2024-03-02

### 🎉 الإصدار الأولي (Initial Release)

#### ✨ الميزات الأساسية

- **قاعدة بيانات شاملة**: 27 محافظة، 283 مركز، 762 وحدة
- **استخراج ذكي**: التعرف على المواقع في النصوص
- **التسلسل الهرمي**: معلومات تفصيلية لكل موقع
- **الأقاليم الاقتصادية**: 7 أقاليم
- **تطبيع أساسي**: إزالة التشكيل وتوحيد الأحرف

#### 📚 المكونات

```python
# EgyptGeoExtractor
extractor = EgyptGeoExtractor()

# extract
locations = extract(text)

# find_governorate
gov = find_governorate(text)
```

#### 🔧 الوظائف الأساسية

- `extract_locations()`: استخراج المواقع
- `get_location_info()`: معلومات تفصيلية
- `get_hierarchy()`: التسلسل الهرمي
- `get_statistics()`: إحصائيات النص
- `search_by_governorate()`: البحث بالمحافظة
- `search_by_region()`: البحث بالإقليم

#### 📦 الملفات

- `data.py`: قاعدة البيانات
- `extractor.py`: المستخرج الأساسي
- `examples.py`: 10 أمثلة شاملة
- `README.md`: توثيق كامل
- `setup.py`: التثبيت

---

## 🔮 خطط مستقبلية (Roadmap)

### النسخة 2.1.0 (قريباً)
- [ ] دعم اللغة الإنجليزية
- [ ] تحسين Fuzzy Matching
- [ ] إضافة الإحداثيات الجغرافية (GPS)
- [ ] API للاستخدام عبر الويب

### النسخة 3.0.0 (مستقبلاً)
- [ ] تكامل مع خرائط جوجل
- [ ] Machine Learning للتعرف السياقي
- [ ] دعم اللهجات المحلية
- [ ] تطبيق ويب تفاعلي

---

## 📊 إحصائيات الإصدارات

| الإصدار | التاريخ | المحافظات | الوحدات | الميزات الجديدة |
|---------|---------|-----------|---------|-----------------|
| 2.0.0 | 2024-03-03 | 27 | 762 | معالجة الأخطاء |
| 1.0.0 | 2024-03-02 | 27 | 762 | الإصدار الأولي |

---

## 🙏 شكر وتقدير

شكراً لكل من ساهم في تطوير المكتبة!

---

Made with ❤️ in Egypt 🇪🇬

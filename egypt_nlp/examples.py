# -*- coding: utf-8 -*-
"""
أمثلة على استخدام مكتبة Egypt NLP
Examples of using Egypt NLP library
"""

from egypt_nlp import EgyptGeoExtractor, extract, find_governorate


def example_1_basic_extraction():
    """مثال 1: استخراج بسيط للمواقع"""
    print("=" * 60)
    print("مثال 1: استخراج المواقع الجغرافية من النص")
    print("=" * 60)
    
    text = """
    أنا من القاهرة، ولدت في مدينة نصر وأعيش الآن في المعادي.
    درست في جامعة الإسكندرية وعملت في الغردقة لمدة سنتين.
    """
    
    locations = extract(text)
    
    print(f"النص: {text}")
    print(f"\nعدد المواقع المستخرجة: {len(locations)}\n")
    
    for loc in locations:
        print(f"- {loc['name']} ({loc['type']})")
        print(f"  الموقع في النص: من {loc['start']} إلى {loc['end']}")
        print(f"  المستوى: {loc['info']['level']}")
        if 'governorate' in loc['info']:
            print(f"  المحافظة: {loc['info']['governorate']}")
        if 'region' in loc['info']:
            print(f"  الإقليم: {loc['info']['region']}")
        print()


def example_2_find_governorate():
    """مثال 2: العثور على المحافظة"""
    print("=" * 60)
    print("مثال 2: تحديد المحافظة من النص")
    print("=" * 60)
    
    texts = [
        "أعيش في مدينة نصر",
        "سافرت إلى شرم الشيخ",
        "أنا من الإسكندرية",
        "درست في جامعة طنطا"
    ]
    
    for text in texts:
        gov = find_governorate(text)
        print(f"النص: {text}")
        print(f"المحافظة: {gov}\n")


def example_3_detailed_info():
    """مثال 3: الحصول على معلومات تفصيلية"""
    print("=" * 60)
    print("مثال 3: معلومات تفصيلية عن المواقع")
    print("=" * 60)
    
    extractor = EgyptGeoExtractor()
    
    locations = ["القاهرة", "مدينة نصر", "الزمالك", "السادس من أكتوبر"]
    
    for location in locations:
        print(f"\n📍 {location}")
        print("-" * 40)
        
        info = extractor.get_location_info(location)
        if info:
            print(f"المستوى الإداري: {info['level']}")
            print(f"المحافظة: {info.get('governorate', location)}")
            print(f"الإقليم الاقتصادي: {info['region']}")
            print(f"النوع: {info['type']}")
            
            if info['level'] == 'governorate':
                print(f"عدد المراكز: {len(info['districts'])}")
            elif info['level'] == 'district':
                print(f"عدد الوحدات: {len(info['units'])}")


def example_4_hierarchy():
    """مثال 4: التسلسل الهرمي"""
    print("=" * 60)
    print("مثال 4: التسلسل الهرمي الكامل")
    print("=" * 60)
    
    extractor = EgyptGeoExtractor()
    
    locations = ["الزمالك", "مدينة نصر", "القاهرة", "شرم الشيخ"]
    
    for location in locations:
        hierarchy = extractor.get_hierarchy(location)
        if hierarchy:
            print(f"\n🏛️ {location}")
            print(f"   الإقليم: {hierarchy.get('region', 'غير محدد')}")
            print(f"   المحافظة: {hierarchy.get('governorate', 'غير محدد')}")
            if 'district' in hierarchy:
                print(f"   المركز/الحي: {hierarchy['district']}")
            if 'unit' in hierarchy:
                print(f"   الوحدة المحلية: {hierarchy['unit']}")


def example_5_search_by_governorate():
    """مثال 5: البحث بالمحافظة"""
    print("=" * 60)
    print("مثال 5: البحث عن معلومات محافظة")
    print("=" * 60)
    
    extractor = EgyptGeoExtractor()
    
    governorate = "القاهرة"
    result = extractor.search_by_governorate(governorate)
    
    if result:
        print(f"\n📊 محافظة {governorate}")
        print(f"الإقليم: {result['region']}")
        print(f"النوع: {result['type']}")
        print(f"عدد المراكز/الأحياء: {result['total_districts']}")
        print(f"عدد الوحدات المحلية: {result['total_units']}")
        print(f"\nالمراكز والأحياء:")
        for district in result['districts'][:5]:  # أول 5 فقط
            print(f"  - {district['name']} ({district['type']}) - {len(district['units'])} وحدة")


def example_6_statistics():
    """مثال 6: إحصائيات النص"""
    print("=" * 60)
    print("مثال 6: إحصائيات المواقع في النص")
    print("=" * 60)
    
    text = """
    بدأت رحلتي من القاهرة، مررت بالجيزة والسادس من أكتوبر.
    ثم توجهت إلى الإسكندرية عبر الصحراوي.
    زرت مرسى مطروح والعلمين قبل العودة إلى مدينة نصر.
    """
    
    extractor = EgyptGeoExtractor()
    stats = extractor.get_statistics(text)
    
    print(f"النص:\n{text}\n")
    print(f"📈 الإحصائيات:")
    print(f"   إجمالي المواقع: {stats['total_locations']}")
    print(f"   عدد المحافظات: {len(stats['governorates'])}")
    print(f"   عدد المراكز: {len(stats['districts'])}")
    print(f"   عدد الوحدات: {len(stats['units'])}")
    print(f"\n   المحافظات المذكورة: {', '.join(stats['governorates'])}")
    print(f"   الأقاليم المذكورة: {', '.join(stats['regions'])}")


def example_7_context_extraction():
    """مثال 7: استخراج مع السياق"""
    print("=" * 60)
    print("مثال 7: استخراج المواقع مع السياق المحيط")
    print("=" * 60)
    
    text = "ولدت في القاهرة ودرست في الإسكندرية وأعمل حالياً في شرم الشيخ"
    
    extractor = EgyptGeoExtractor()
    locations = extractor.extract_with_context(text, context_chars=15)
    
    print(f"النص: {text}\n")
    
    for loc in locations:
        print(f"📍 {loc['name']}")
        print(f"   السياق الكامل: ...{loc['full_context']}...")
        print()


def example_8_check_location():
    """مثال 8: التحقق من وجود موقع"""
    print("=" * 60)
    print("مثال 8: التحقق من وجود موقع في النص")
    print("=" * 60)
    
    text = "أنا من القاهرة وأعيش في مدينة نصر"
    
    extractor = EgyptGeoExtractor()
    
    locations_to_check = ["القاهرة", "الإسكندرية", "مدينة نصر", "الزمالك"]
    
    print(f"النص: {text}\n")
    
    for location in locations_to_check:
        exists = extractor.is_location_in_text(text, location)
        status = "✅ موجود" if exists else "❌ غير موجود"
        print(f"{location}: {status}")


def example_9_search_by_region():
    """مثال 9: البحث بالإقليم"""
    print("=" * 60)
    print("مثال 9: البحث عن معلومات إقليم")
    print("=" * 60)
    
    extractor = EgyptGeoExtractor()
    
    region = "القاهرة الكبرى"
    result = extractor.search_by_region(region)
    
    if result:
        print(f"\n🗺️ إقليم {region}")
        print(f"عدد المحافظات: {result['total_governorates']}")
        print(f"المحافظات: {', '.join(result['governorates'])}")


def example_10_real_world():
    """مثال 10: حالة استخدام واقعية"""
    print("=" * 60)
    print("مثال 10: تحليل نص إخباري")
    print("=" * 60)
    
    news_text = """
    أعلنت وزارة النقل عن افتتاح طريق جديد يربط القاهرة بالإسكندرية
    مروراً بمدينة السادات ووادي النطرون. سيسهل الطريق الجديد الوصول
    إلى مدينة العلمين الجديدة ومرسى مطروح. كما سيخدم الطريق سكان
    محافظات الجيزة والمنوفية والبحيرة.
    """
    
    extractor = EgyptGeoExtractor()
    
    print(f"النص:\n{news_text}\n")
    
    # استخراج المواقع
    locations = extractor.extract_locations(news_text)
    print(f"📍 المواقع المستخرجة ({len(locations)}):")
    for loc in locations:
        print(f"   - {loc['name']} ({loc['info']['level']})")
    
    # الإحصائيات
    stats = extractor.get_statistics(news_text)
    print(f"\n📊 التحليل:")
    print(f"   المحافظات المتأثرة: {', '.join(stats['governorates'])}")
    print(f"   الأقاليم المشمولة: {', '.join(stats['regions'])}")


def run_all_examples():
    """تشغيل كل الأمثلة"""
    examples = [
        example_1_basic_extraction,
        example_2_find_governorate,
        example_3_detailed_info,
        example_4_hierarchy,
        example_5_search_by_governorate,
        example_6_statistics,
        example_7_context_extraction,
        example_8_check_location,
        example_9_search_by_region,
        example_10_real_world,
    ]
    
    for i, example in enumerate(examples, 1):
        try:
            example()
            print("\n" + "=" * 60 + "\n")
        except Exception as e:
            print(f"خطأ في المثال {i}: {e}\n")


if __name__ == "__main__":
    print("\n" + "🇪🇬" * 20)
    print("Egypt NLP - أمثلة استخدام المكتبة")
    print("🇪🇬" * 20 + "\n")
    
    run_all_examples()
    
    print("\n✅ انتهت الأمثلة!")

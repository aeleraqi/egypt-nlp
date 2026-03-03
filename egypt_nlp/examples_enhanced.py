# -*- coding: utf-8 -*-
"""
أمثلة على معالجة الأخطاء الكتابية
Examples of Spelling Error Handling
"""

import sys
sys.path.insert(0, '/home/claude')

from egypt_nlp import EnhancedEgyptGeoExtractor, extract_enhanced, suggest_corrections


def example_1_spelling_errors():
    """مثال 1: معالجة الأخطاء الإملائية الشائعة"""
    print("=" * 70)
    print("📝 مثال 1: معالجة الأخطاء الإملائية")
    print("=" * 70)
    
    texts_with_errors = [
        "أنا من الاسكندريه",  # خطأ: الاسكندريه → الإسكندرية
        "سافرت إلى الغرقه",  # خطأ: الغرقه → الغردقة
        "أعيش في 6 اكتوبر",  # خطأ: 6 اكتوبر → السادس من أكتوبر
        "درست في اسيوط",     # خطأ: اسيوط → أسيوط
        "زرت شرم الاسبوع الماضي",  # شرم → شرم الشيخ
    ]
    
    extractor = EnhancedEgyptGeoExtractor(fuzzy_threshold=0.80)
    
    for text in texts_with_errors:
        print(f"\n📄 النص: {text}")
        locations = extractor.extract_locations(text, use_fuzzy=True)
        
        for loc in locations:
            if loc['match_type'] == 'fuzzy':
                print(f"   ✅ تصحيح: '{loc.get('original_text', '')}' → '{loc['name']}'")
                print(f"   📍 المحافظة: {loc['info']['governorate']}")
                print(f"   🎯 الثقة: {loc['confidence']:.2%}")
            else:
                print(f"   ✅ تطابق دقيق: {loc['name']}")


def example_2_suggest_corrections():
    """مثال 2: اقتراح التصحيحات"""
    print("\n" + "=" * 70)
    print("💡 مثال 2: اقتراح التصحيحات للنص")
    print("=" * 70)
    
    text = """
    رحلتي كانت رائعة! زرت الاسكندريه والغرقه وشرم.
    كما زرت اسيوط والاقصر واسوان.
    """
    
    print(f"\n📄 النص الأصلي:\n{text}")
    
    extractor = EnhancedEgyptGeoExtractor()
    suggestions = extractor.suggest_corrections(text, threshold=0.70)
    
    print(f"\n💡 التصحيحات المقترحة ({len(suggestions)}):\n")
    
    for i, sugg in enumerate(suggestions, 1):
        print(f"{i}. '{sugg['original']}' → '{sugg['suggestion']}'")
        print(f"   التشابه: {sugg['similarity']:.2%}")
        print(f"   النوع: {sugg['type']}")
        print()


def example_3_fuzzy_threshold():
    """مثال 3: التحكم في حد التشابه"""
    print("=" * 70)
    print("🎚️ مثال 3: التحكم في حساسية التطابق")
    print("=" * 70)
    
    text = "أنا من الأسكندرية"  # خطأ بسيط
    
    print(f"\n📄 النص: {text}\n")
    
    thresholds = [0.95, 0.85, 0.75]
    
    for threshold in thresholds:
        extractor = EnhancedEgyptGeoExtractor(fuzzy_threshold=threshold)
        locations = extractor.extract_locations(text, use_fuzzy=True)
        
        print(f"حد التشابه: {threshold:.0%}")
        if locations:
            for loc in locations:
                print(f"   ✅ وجد: {loc['name']} (ثقة: {loc['confidence']:.2%})")
        else:
            print(f"   ❌ لم يتم العثور على تطابق")
        print()


def example_4_mixed_text():
    """مثال 4: نص مختلط بأخطاء وبدونها"""
    print("=" * 70)
    print("🔀 مثال 4: نص مختلط (أخطاء + صحيح)")
    print("=" * 70)
    
    text = """
    رحلة عمل من القاهرة إلى الاسكندريه مروراً بالبحيره.
    ثم سافرت إلى الغرقه ومرسى مطروح.
    """
    
    print(f"\n📄 النص:\n{text}\n")
    
    extractor = EnhancedEgyptGeoExtractor(fuzzy_threshold=0.85)
    locations = extractor.extract_locations(text, use_fuzzy=True)
    
    print("📍 المواقع المستخرجة:\n")
    
    for i, loc in enumerate(locations, 1):
        print(f"{i}. {loc['name']}")
        if loc['match_type'] == 'fuzzy':
            print(f"   🔧 تم التصحيح من: {loc.get('original_text', 'N/A')}")
            print(f"   🎯 الثقة: {loc['confidence']:.2%}")
        else:
            print(f"   ✓ تطابق دقيق")
        print(f"   📌 المحافظة: {loc['info']['governorate']}")
        print(f"   🗺️ الإقليم: {loc['info']['region']}")
        print()


def example_5_common_mistakes():
    """مثال 5: الأخطاء الشائعة المعالجة"""
    print("=" * 70)
    print("📋 مثال 5: قائمة الأخطاء الشائعة المدعومة")
    print("=" * 70)
    
    common_mistakes = [
        ("الاسكندريه", "الإسكندرية"),
        ("الغرقه", "الغردقة"),
        ("6 اكتوبر", "السادس من أكتوبر"),
        ("10 رمضان", "العاشر من رمضان"),
        ("اسيوط", "أسيوط"),
        ("سوهاج", "سوهاج"),
        ("الاقصر", "الأقصر"),
        ("اسوان", "أسوان"),
        ("مدينه نصر", "مدينة نصر"),
        ("المعادى", "المعادي"),
    ]
    
    extractor = EnhancedEgyptGeoExtractor()
    
    print("\n✅ الأخطاء الشائعة المعالجة تلقائياً:\n")
    
    for i, (error, correct) in enumerate(common_mistakes, 1):
        text = f"أنا من {error}"
        locations = extractor.extract_locations(text, use_fuzzy=True)
        
        if locations:
            found = locations[0]['name']
            status = "✅" if found == correct else "⚠️"
            print(f"{i}. '{error}' → '{found}' {status}")
        else:
            print(f"{i}. '{error}' → ❌ لم يتم التعرف")


def example_6_confidence_levels():
    """مثال 6: مستويات الثقة"""
    print("\n" + "=" * 70)
    print("📊 مثال 6: مستويات الثقة في التطابق")
    print("=" * 70)
    
    test_words = [
        "الإسكندرية",      # تطابق دقيق - ثقة 100%
        "الاسكندرية",      # خطأ شائع - ثقة عالية
        "اسكندريه",        # خطأ شائع آخر - ثقة عالية
        "الأسكندرية",      # خطأ في الهمزة - ثقة متوسطة
        "سكندرية",         # ناقص "ال" - ثقة متوسطة
    ]
    
    extractor = EnhancedEgyptGeoExtractor(fuzzy_threshold=0.70)
    
    print("\n📈 مستويات الثقة للكلمات المختلفة:\n")
    
    for word in test_words:
        match_result = extractor.find_closest_match(word, threshold=0.70)
        
        if match_result:
            location, confidence = match_result
            confidence_level = "🟢 عالية" if confidence >= 0.90 else "🟡 متوسطة" if confidence >= 0.75 else "🔴 منخفضة"
            print(f"'{word}'")
            print(f"   → {location}")
            print(f"   الثقة: {confidence:.2%} {confidence_level}")
        else:
            print(f"'{word}' → ❌ لم يتم العثور على تطابق")
        print()


def example_7_real_world_news():
    """مثال 7: تحليل نص إخباري بأخطاء إملائية"""
    print("=" * 70)
    print("📰 مثال 7: تحليل نص إخباري واقعي")
    print("=" * 70)
    
    news_with_errors = """
    افتتح الرئيس اليوم مشروعا جديدا يربط القاهره بالاسكندريه
    عبر الطريق الصحراوى. المشروع سيخدم محافظات الجيزه والبحيره
    ويسهل الوصول الى مدينة العلمين الجديده والغرقه ومرسى مطروح.
    """
    
    print(f"\n📄 النص الإخباري (يحتوي على أخطاء):\n{news_with_errors}\n")
    
    extractor = EnhancedEgyptGeoExtractor(fuzzy_threshold=0.85)
    
    # استخراج المواقع
    locations = extractor.extract_locations(news_with_errors, use_fuzzy=True)
    
    print(f"📍 المواقع المستخرجة ({len(locations)}):\n")
    
    exact_matches = [loc for loc in locations if loc['match_type'] == 'exact']
    fuzzy_matches = [loc for loc in locations if loc['match_type'] == 'fuzzy']
    
    print(f"✅ تطابقات دقيقة ({len(exact_matches)}):")
    for loc in exact_matches:
        print(f"   - {loc['name']}")
    
    print(f"\n🔧 تطابقات تم تصحيحها ({len(fuzzy_matches)}):")
    for loc in fuzzy_matches:
        print(f"   - {loc['name']} (كانت: {loc.get('original_text', 'N/A')})")
    
    # الإحصائيات
    governorates = set()
    for loc in locations:
        if 'governorate' in loc['info']:
            governorates.add(loc['info']['governorate'])
    
    print(f"\n📊 الإحصائيات:")
    print(f"   المحافظات المذكورة: {', '.join(governorates)}")
    print(f"   إجمالي المواقع: {len(locations)}")
    print(f"   دقة التطابق: {len(exact_matches)}/{len(locations)}")


def run_all_examples():
    """تشغيل كل الأمثلة"""
    examples = [
        example_1_spelling_errors,
        example_2_suggest_corrections,
        example_3_fuzzy_threshold,
        example_4_mixed_text,
        example_5_common_mistakes,
        example_6_confidence_levels,
        example_7_real_world_news,
    ]
    
    for example in examples:
        try:
            example()
            print("\n" + "=" * 70 + "\n")
        except Exception as e:
            print(f"خطأ: {e}\n")


if __name__ == "__main__":
    print("\n" + "🇪🇬" * 30)
    print("Egypt NLP Enhanced - معالجة الأخطاء الكتابية")
    print("🇪🇬" * 30 + "\n")
    
    run_all_examples()
    
    print("\n✅ انتهت الأمثلة!")
    print("\n💡 نصيحة: يمكنك ضبط fuzzy_threshold للتحكم في حساسية التطابق")
    print("   - 0.95-1.0: صارم جداً (أخطاء بسيطة فقط)")
    print("   - 0.85-0.94: متوازن (الأفضل للاستخدام العام)")
    print("   - 0.70-0.84: متساهل (يقبل اختلافات أكبر)")

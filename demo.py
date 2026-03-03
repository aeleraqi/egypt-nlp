#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Egypt NLP - Demo Script
سكريبت تجريبي لاختبار المكتبة
"""

import sys
sys.path.insert(0, '/home/claude')

from egypt_nlp import EgyptGeoExtractor, extract, find_governorate


def demo():
    """تشغيل عرض تجريبي للمكتبة"""
    
    print("\n" + "🇪🇬" * 30)
    print("Egypt NLP - مكتبة استخراج الكيانات الجغرافية المصرية")
    print("🇪🇬" * 30 + "\n")
    
    # ==================== مثال 1 ====================
    print("=" * 70)
    print("📍 مثال 1: استخراج بسيط للمواقع")
    print("=" * 70)
    
    text1 = "أنا من القاهرة، ولدت في مدينة نصر وأعيش الآن في المعادي"
    print(f"\n النص: {text1}\n")
    
    locations = extract(text1)
    print(f"✅ تم العثور على {len(locations)} موقع:\n")
    
    for i, loc in enumerate(locations, 1):
        print(f"{i}. {loc['name']}")
        print(f"   النوع: {loc['type']}")
        print(f"   المحافظة: {loc['info'].get('governorate', 'N/A')}")
        print(f"   الإقليم: {loc['info']['region']}")
        print()
    
    # ==================== مثال 2 ====================
    print("=" * 70)
    print("🔍 مثال 2: العثور على المحافظة من النص")
    print("=" * 70)
    
    texts = [
        "سافرت إلى شرم الشيخ الأسبوع الماضي",
        "أعيش في حي المهندسين",
        "درست في جامعة الإسكندرية",
    ]
    
    for text in texts:
        gov = find_governorate(text)
        print(f"\n📝 النص: {text}")
        print(f"🏛️ المحافظة: {gov}")
    
    # ==================== مثال 3 ====================
    print("\n" + "=" * 70)
    print("📊 مثال 3: تحليل نص إخباري")
    print("=" * 70)
    
    news = """
    افتتح الرئيس اليوم مشروع تطوير طريق القاهرة الإسكندرية الصحراوي
    الذي يمر بمدينة السادات ووادي النطرون. المشروع سيخدم محافظات الجيزة
    والمنوفية والبحيرة، ويسهل الوصول إلى مدينة العلمين الجديدة ومرسى مطروح.
    """
    
    print(f"\n📰 النص الإخباري:\n{news}")
    
    extractor = EgyptGeoExtractor()
    stats = extractor.get_statistics(news)
    
    print(f"\n📈 التحليل الإحصائي:")
    print(f"   إجمالي المواقع المذكورة: {stats['total_locations']}")
    print(f"   المحافظات ({len(stats['governorates'])}): {', '.join(stats['governorates'])}")
    print(f"   المراكز ({len(stats['districts'])}): {', '.join(stats['districts'])}")
    print(f"   الأقاليم المشمولة: {', '.join(stats['regions'])}")
    
    # ==================== مثال 4 ====================
    print("\n" + "=" * 70)
    print("🏛️ مثال 4: التسلسل الهرمي للمواقع")
    print("=" * 70)
    
    locations_to_check = ["الزمالك", "السادس من أكتوبر", "شرم الشيخ"]
    
    for location in locations_to_check:
        hierarchy = extractor.get_hierarchy(location)
        if hierarchy:
            print(f"\n📍 {location}")
            print(f"   ├─ الإقليم: {hierarchy.get('region')}")
            print(f"   ├─ المحافظة: {hierarchy.get('governorate')}")
            if 'district' in hierarchy:
                print(f"   ├─ المركز/الحي: {hierarchy['district']}")
            if 'unit' in hierarchy:
                print(f"   └─ الوحدة المحلية: {hierarchy['unit']}")
    
    # ==================== مثال 5 ====================
    print("\n" + "=" * 70)
    print("🔎 مثال 5: معلومات تفصيلية عن محافظة")
    print("=" * 70)
    
    governorate = "القاهرة"
    result = extractor.search_by_governorate(governorate)
    
    if result:
        print(f"\n🏛️ محافظة {governorate}")
        print(f"   الإقليم الاقتصادي: {result['region']}")
        print(f"   نوع المحافظة: {result['type']}")
        print(f"   عدد المراكز/الأحياء: {result['total_districts']}")
        print(f"   عدد الوحدات المحلية: {result['total_units']}")
        print(f"\n   أمثلة على الأحياء:")
        for district in result['districts'][:5]:
            print(f"      • {district['name']} ({district['type']}) - {len(district['units'])} وحدة")
    
    # ==================== النهاية ====================
    print("\n" + "=" * 70)
    print("✅ انتهى العرض التجريبي!")
    print("=" * 70)
    
    print("\n📚 للمزيد من الأمثلة، شغّل:")
    print("   python egypt_nlp/examples.py")
    print("\n📖 للوثائق الكاملة، اقرأ:")
    print("   egypt_nlp/README.md")
    print("\n" + "🇪🇬" * 30 + "\n")


if __name__ == "__main__":
    try:
        demo()
    except Exception as e:
        print(f"\n❌ خطأ: {e}")
        import traceback
        traceback.print_exc()

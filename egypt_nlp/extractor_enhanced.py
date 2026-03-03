# -*- coding: utf-8 -*-
"""
Enhanced Egyptian Geographic Named Entity Extractor with Fuzzy Matching
مستخرج محسّن مع معالجة الأخطاء الكتابية
"""

import re
from typing import List, Dict, Tuple, Optional, Set
from .data import ADMINISTRATIVE_DATA, REGIONS, ALIASES


def levenshtein_distance(s1: str, s2: str) -> int:
    """
    حساب مسافة التحرير (Levenshtein Distance) بين نصين
    Calculate edit distance between two strings
    """
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)
    
    if len(s2) == 0:
        return len(s1)
    
    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    
    return previous_row[-1]


def similarity_ratio(s1: str, s2: str) -> float:
    """
    حساب نسبة التشابه بين نصين (0-1)
    Calculate similarity ratio between two strings
    """
    distance = levenshtein_distance(s1, s2)
    max_len = max(len(s1), len(s2))
    if max_len == 0:
        return 1.0
    return 1 - (distance / max_len)


class EnhancedEgyptGeoExtractor:
    """
    مستخرج محسّن للكيانات الجغرافية المصرية مع معالجة الأخطاء الكتابية
    Enhanced Egyptian Geographic Entity Extractor with spelling error handling
    """
    
    def __init__(self, fuzzy_threshold: float = 0.85):
        """
        تهيئة المستخرج
        
        Args:
            fuzzy_threshold: حد التشابه المطلوب (0-1). القيمة الافتراضية 0.85
                            كلما زادت القيمة، كلما كان التطابق أكثر صرامة
        """
        self.data = ADMINISTRATIVE_DATA
        self.regions = REGIONS
        self.aliases = ALIASES
        self.fuzzy_threshold = fuzzy_threshold
        
        # بناء قوائم البحث
        self._build_search_indices()
        self._build_common_errors()
    
    def _build_search_indices(self):
        """بناء فهارس البحث السريع"""
        # قائمة كل المحافظات
        self.governorates = set(self.data.keys())
        
        # قائمة كل المراكز والأحياء
        self.districts = set()
        for gov_data in self.data.values():
            self.districts.update(gov_data['districts'].keys())
        
        # قائمة كل الوحدات المحلية والأحياء الفرعية
        self.units = set()
        for gov_data in self.data.values():
            for district_data in gov_data['districts'].values():
                self.units.update(district_data['units'])
        
        # قائمة كل الأسماء
        self.all_locations = self.governorates | self.districts | self.units
        
        # خريطة من الاسم إلى النوع
        self.location_types = {}
        for gov in self.governorates:
            self.location_types[gov] = 'governorate'
        for district in self.districts:
            self.location_types[district] = 'district'
        for unit in self.units:
            self.location_types[unit] = 'unit'
    
    def _build_common_errors(self):
        """بناء قاموس الأخطاء الشائعة"""
        self.common_errors = {
            # أخطاء شائعة في أسماء المحافظات
            'الاسكندرية': 'الإسكندرية',
            'الاسكندريه': 'الإسكندرية',
            'اسكندرية': 'الإسكندرية',
            'اسكندريه': 'الإسكندرية',
            'الأسكندرية': 'الإسكندرية',
            'الأسكندريه': 'الإسكندرية',
            
            'الاسماعيلية': 'الإسماعيلية',
            'الاسماعيليه': 'الإسماعيلية',
            'اسماعيلية': 'الإسماعيلية',
            'الأسماعيلية': 'الإسماعيلية',
            
            'القاهره': 'القاهرة',
            'قاهرة': 'القاهرة',
            
            'الجيزه': 'الجيزة',
            'جيزة': 'الجيزة',
            'الجيزة': 'الجيزة',
            
            'بورسعيد': 'بورسعيد',
            'بور سعيد': 'بورسعيد',
            'بورسعد': 'بورسعيد',
            
            'اسيوط': 'أسيوط',
            'اسيوط': 'أسيوط',
            'أسيوط': 'أسيوط',
            
            'سوهاج': 'سوهاج',
            'سوهاج': 'سوهاج',
            
            'الاقصر': 'الأقصر',
            'اقصر': 'الأقصر',
            'لاقصر': 'الأقصر',
            
            'اسوان': 'أسوان',
            'أسوان': 'أسوان',
            
            'الغرقه': 'الغردقة',
            'الغردقه': 'الغردقة',
            'غردقة': 'الغردقة',
            'الغرقة': 'الغردقة',
            'هرجادة': 'الغردقة',
            
            'شرم': 'شرم الشيخ',
            'شرم الشيخ': 'شرم الشيخ',
            
            # أخطاء في المدن الجديدة
            '6 اكتوبر': 'السادس من أكتوبر',
            '6 أكتوبر': 'السادس من أكتوبر',
            'ستة اكتوبر': 'السادس من أكتوبر',
            '6اكتوبر': 'السادس من أكتوبر',
            
            '10 رمضان': 'العاشر من رمضان',
            'عاشر رمضان': 'العاشر من رمضان',
            '10رمضان': 'العاشر من رمضان',
            
            '15 مايو': '15 مايو',
            'خمستاشر مايو': '15 مايو',
            
            # أحياء شائعة
            'مدينه نصر': 'مدينة نصر',
            'مدينة نصر': 'مدينة نصر',
            'مدينه نصر': 'مدينة نصر',
            
            'مصر الجديده': 'مصر الجديدة',
            'مصر الجديدة': 'مصر الجديدة',
            
            'المعادى': 'المعادي',
            'المعادي': 'المعادي',
            
            'الزمالك': 'الزمالك',
            'زمالك': 'الزمالك',
            
            'المهندسين': 'المهندسين',
            'مهندسين': 'المهندسين',
            
            'الدقى': 'الدقي',
            'دقي': 'الدقي',
        }
    
    def normalize_text(self, text: str) -> str:
        """
        تطبيع النص العربي مع معالجة الأخطاء الشائعة
        Normalize Arabic text with common error handling
        """
        # إزالة التشكيل
        text = re.sub(r'[\u064B-\u065F\u0670]', '', text)
        
        # توحيد الهمزات
        text = re.sub(r'[إأآا]', 'ا', text)
        text = re.sub(r'[ىي]', 'ي', text)
        text = re.sub(r'ة', 'ه', text)
        
        # استبدال الأخطاء الشائعة
        for error, correct in self.common_errors.items():
            text = text.replace(error, correct)
        
        # استبدال الأسماء البديلة
        for alias, canonical in self.aliases.items():
            text = text.replace(alias, canonical)
        
        return text
    
    def find_closest_match(self, word: str, threshold: Optional[float] = None) -> Optional[Tuple[str, float]]:
        """
        إيجاد أقرب تطابق لكلمة باستخدام Fuzzy Matching
        Find closest match for a word using fuzzy matching
        
        Args:
            word: الكلمة المراد البحث عنها
            threshold: حد التشابه المطلوب (يستخدم القيمة الافتراضية إذا لم يتم تحديده)
        
        Returns:
            (اسم الموقع الأقرب, نسبة التشابه) أو None
        """
        if threshold is None:
            threshold = self.fuzzy_threshold
        
        best_match = None
        best_similarity = 0.0
        
        # تطبيع الكلمة
        normalized_word = self.normalize_text(word)
        
        # البحث في كل المواقع
        for location in self.all_locations:
            normalized_location = self.normalize_text(location)
            similarity = similarity_ratio(normalized_word, normalized_location)
            
            if similarity > best_similarity and similarity >= threshold:
                best_similarity = similarity
                best_match = location
        
        if best_match:
            return (best_match, best_similarity)
        
        return None
    
    def extract_locations(self, text: str, normalize: bool = True, use_fuzzy: bool = True) -> List[Dict]:
        """
        استخراج المواقع الجغرافية مع معالجة الأخطاء
        Extract geographic locations with error handling
        
        Args:
            text: النص المراد البحث فيه
            normalize: تطبيع النص قبل البحث
            use_fuzzy: استخدام fuzzy matching للكلمات غير المطابقة تماماً
        
        Returns:
            قائمة بالمواقع المستخرجة
        """
        original_text = text
        if normalize:
            text = self.normalize_text(text)
        
        found_locations = []
        
        # 1. البحث الدقيق أولاً
        for location in self.all_locations:
            pattern = r'\b' + re.escape(location) + r'\b'
            matches = re.finditer(pattern, text)
            
            for match in matches:
                location_info = self.get_location_info(location)
                if location_info:
                    found_locations.append({
                        'name': location,
                        'type': self.location_types.get(location, 'unknown'),
                        'start': match.start(),
                        'end': match.end(),
                        'info': location_info,
                        'match_type': 'exact',
                        'confidence': 1.0
                    })
        
        # 2. Fuzzy matching للكلمات المتبقية
        if use_fuzzy:
            # استخراج الكلمات من النص
            words = re.findall(r'\b[\u0600-\u06FF\s]+\b', text)
            
            for word in words:
                word = word.strip()
                if len(word) < 3:  # تجاهل الكلمات القصيرة جداً
                    continue
                
                # تحقق إذا كانت الكلمة موجودة بالفعل في النتائج
                already_found = any(loc['name'] == word for loc in found_locations)
                if already_found:
                    continue
                
                # البحث عن تطابق قريب
                match_result = self.find_closest_match(word)
                if match_result:
                    location, similarity = match_result
                    
                    # تحقق أن هذا الموقع لم يتم إضافته مسبقاً
                    if not any(loc['name'] == location for loc in found_locations):
                        location_info = self.get_location_info(location)
                        if location_info:
                            # البحث عن موقع الكلمة في النص الأصلي
                            pattern = r'\b' + re.escape(word) + r'\b'
                            matches = re.finditer(pattern, original_text, re.IGNORECASE)
                            
                            for match in matches:
                                found_locations.append({
                                    'name': location,
                                    'original_text': word,
                                    'type': self.location_types.get(location, 'unknown'),
                                    'start': match.start(),
                                    'end': match.end(),
                                    'info': location_info,
                                    'match_type': 'fuzzy',
                                    'confidence': similarity
                                })
        
        # ترتيب حسب الموقع في النص
        found_locations.sort(key=lambda x: x['start'])
        
        # إزالة التكرارات (نفس الموقع في نفس المكان)
        unique_locations = []
        seen = set()
        for loc in found_locations:
            key = (loc['name'], loc['start'], loc['end'])
            if key not in seen:
                seen.add(key)
                unique_locations.append(loc)
        
        return unique_locations
    
    def get_location_info(self, location_name: str) -> Optional[Dict]:
        """الحصول على معلومات تفصيلية عن موقع"""
        # البحث كمحافظة
        if location_name in self.data:
            return {
                'level': 'governorate',
                'governorate': location_name,
                'region': self.data[location_name]['region'],
                'type': self.data[location_name]['type'],
                'districts': list(self.data[location_name]['districts'].keys())
            }
        
        # البحث كمركز/حي
        for gov_name, gov_data in self.data.items():
            if location_name in gov_data['districts']:
                district_data = gov_data['districts'][location_name]
                return {
                    'level': 'district',
                    'district': location_name,
                    'governorate': gov_name,
                    'region': gov_data['region'],
                    'type': district_data['type'],
                    'units': district_data['units']
                }
        
        # البحث كوحدة محلية
        for gov_name, gov_data in self.data.items():
            for district_name, district_data in gov_data['districts'].items():
                if location_name in district_data['units']:
                    return {
                        'level': 'unit',
                        'unit': location_name,
                        'district': district_name,
                        'governorate': gov_name,
                        'region': gov_data['region'],
                        'type': district_data['type']
                    }
        
        return None
    
    def suggest_corrections(self, text: str, threshold: float = 0.7) -> List[Dict]:
        """
        اقتراح التصحيحات للأخطاء المحتملة في النص
        Suggest corrections for potential errors
        
        Args:
            text: النص المراد فحصه
            threshold: الحد الأدنى للتشابه لاقتراح التصحيح
        
        Returns:
            قائمة بالتصحيحات المقترحة
        """
        suggestions = []
        words = re.findall(r'\b[\u0600-\u06FF\s]+\b', text)
        
        for word in words:
            word = word.strip()
            if len(word) < 3:
                continue
            
            # تحقق إذا كانت الكلمة موجودة بالفعل
            if word in self.all_locations:
                continue
            
            # البحث عن تطابق قريب
            match_result = self.find_closest_match(word, threshold=threshold)
            if match_result:
                location, similarity = match_result
                suggestions.append({
                    'original': word,
                    'suggestion': location,
                    'similarity': similarity,
                    'type': self.location_types.get(location, 'unknown')
                })
        
        return suggestions


# دوال مساعدة محسّنة
def extract_enhanced(text: str, fuzzy_threshold: float = 0.85) -> List[Dict]:
    """
    دالة سريعة لاستخراج المواقع مع معالجة الأخطاء
    Quick function with error handling
    """
    extractor = EnhancedEgyptGeoExtractor(fuzzy_threshold=fuzzy_threshold)
    return extractor.extract_locations(text)


def suggest_corrections(text: str) -> List[Dict]:
    """
    دالة سريعة لاقتراح التصحيحات
    Quick function to suggest corrections
    """
    extractor = EnhancedEgyptGeoExtractor()
    return extractor.suggest_corrections(text)

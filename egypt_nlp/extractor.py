# -*- coding: utf-8 -*-
"""
Egyptian Geographic Named Entity Extractor
مستخرج الكيانات الجغرافية المصرية
"""

import re
from typing import List, Dict, Tuple, Optional, Set
from .data import ADMINISTRATIVE_DATA, REGIONS, ALIASES


class EgyptGeoExtractor:
    """
    مستخرج الكيانات الجغرافية المصرية من النصوص العربية
    Egyptian Geographic Entity Extractor for Arabic text
    """
    
    def __init__(self):
        """تهيئة المستخرج وبناء قواعد البيانات"""
        self.data = ADMINISTRATIVE_DATA
        self.regions = REGIONS
        self.aliases = ALIASES
        
        # بناء قوائم البحث
        self._build_search_indices()
    
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
        
        # قائمة كل الأسماء (للبحث السريع)
        self.all_locations = self.governorates | self.districts | self.units
        
        # خريطة من الاسم إلى النوع
        self.location_types = {}
        for gov in self.governorates:
            self.location_types[gov] = 'governorate'
        for district in self.districts:
            self.location_types[district] = 'district'
        for unit in self.units:
            self.location_types[unit] = 'unit'
    
    def normalize_text(self, text: str) -> str:
        """
        تطبيع النص العربي
        Normalize Arabic text
        """
        # إزالة التشكيل
        text = re.sub(r'[\u064B-\u065F\u0670]', '', text)
        
        # توحيد الهمزات
        text = re.sub(r'[إأآا]', 'ا', text)
        text = re.sub(r'[ىي]', 'ي', text)
        text = re.sub(r'ة', 'ه', text)
        
        # استبدال الأسماء البديلة
        for alias, canonical in self.aliases.items():
            text = text.replace(alias, canonical)
        
        return text
    
    def extract_locations(self, text: str, normalize: bool = True) -> List[Dict]:
        """
        استخراج كل المواقع الجغرافية من النص
        Extract all geographic locations from text
        
        Args:
            text: النص المراد البحث فيه
            normalize: تطبيع النص قبل البحث
        
        Returns:
            قائمة بالمواقع المستخرجة مع معلوماتها
        """
        if normalize:
            text = self.normalize_text(text)
        
        found_locations = []
        
        # البحث عن كل موقع في النص
        for location in self.all_locations:
            # البحث باستخدام regex للكلمة الكاملة
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
                        'info': location_info
                    })
        
        # ترتيب حسب الموقع في النص
        found_locations.sort(key=lambda x: x['start'])
        
        return found_locations
    
    def get_location_info(self, location_name: str) -> Optional[Dict]:
        """
        الحصول على معلومات تفصيلية عن موقع جغرافي
        Get detailed information about a geographic location
        
        Args:
            location_name: اسم الموقع
        
        Returns:
            معلومات الموقع أو None إذا لم يتم العثور عليه
        """
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
        
        # البحث كوحدة محلية/حي فرعي
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
    
    def find_governorate(self, text: str) -> Optional[str]:
        """
        العثور على أول محافظة مذكورة في النص
        Find the first governorate mentioned in text
        """
        locations = self.extract_locations(text)
        for loc in locations:
            if loc['type'] == 'governorate':
                return loc['name']
            elif loc['info']['level'] in ['district', 'unit']:
                return loc['info']['governorate']
        return None
    
    def find_all_governorates(self, text: str) -> List[str]:
        """
        العثور على كل المحافظات المذكورة في النص
        Find all governorates mentioned in text
        """
        locations = self.extract_locations(text)
        governorates = set()
        
        for loc in locations:
            if loc['type'] == 'governorate':
                governorates.add(loc['name'])
            elif loc['info']['level'] in ['district', 'unit']:
                governorates.add(loc['info']['governorate'])
        
        return list(governorates)
    
    def find_region(self, text: str) -> Optional[str]:
        """
        تحديد الإقليم الاقتصادي من النص
        Identify economic region from text
        """
        governorate = self.find_governorate(text)
        if governorate:
            for region, govs in self.regions.items():
                if governorate in govs:
                    return region
        return None
    
    def is_location_in_text(self, text: str, location_name: str) -> bool:
        """
        التحقق من وجود موقع معين في النص
        Check if a specific location exists in text
        """
        locations = self.extract_locations(text)
        for loc in locations:
            if loc['name'] == location_name:
                return True
            # التحقق من المحافظة أو المركز للوحدات المحلية
            if loc['info']['level'] == 'unit' and loc['info'].get('district') == location_name:
                return True
            if loc['info'].get('governorate') == location_name:
                return True
        return False
    
    def get_hierarchy(self, location_name: str) -> Optional[Dict]:
        """
        الحصول على التسلسل الهرمي الكامل لموقع
        Get complete hierarchy for a location
        
        Returns:
            {
                'region': الإقليم,
                'governorate': المحافظة,
                'district': المركز (إن وجد),
                'unit': الوحدة المحلية (إن وجدت)
            }
        """
        info = self.get_location_info(location_name)
        if not info:
            return None
        
        hierarchy = {}
        
        if info['level'] == 'governorate':
            hierarchy['region'] = info['region']
            hierarchy['governorate'] = location_name
        
        elif info['level'] == 'district':
            hierarchy['region'] = info['region']
            hierarchy['governorate'] = info['governorate']
            hierarchy['district'] = location_name
        
        elif info['level'] == 'unit':
            hierarchy['region'] = info['region']
            hierarchy['governorate'] = info['governorate']
            hierarchy['district'] = info['district']
            hierarchy['unit'] = location_name
        
        return hierarchy
    
    def extract_with_context(self, text: str, context_chars: int = 50) -> List[Dict]:
        """
        استخراج المواقع مع السياق المحيط
        Extract locations with surrounding context
        
        Args:
            text: النص المراد البحث فيه
            context_chars: عدد الحروف قبل وبعد الموقع
        
        Returns:
            قائمة بالمواقع مع السياق
        """
        locations = self.extract_locations(text)
        
        for loc in locations:
            start_ctx = max(0, loc['start'] - context_chars)
            end_ctx = min(len(text), loc['end'] + context_chars)
            
            loc['context_before'] = text[start_ctx:loc['start']]
            loc['context_after'] = text[loc['end']:end_ctx]
            loc['full_context'] = text[start_ctx:end_ctx]
        
        return locations
    
    def get_statistics(self, text: str) -> Dict:
        """
        الحصول على إحصائيات المواقع في النص
        Get statistics of locations in text
        """
        locations = self.extract_locations(text)
        
        stats = {
            'total_locations': len(locations),
            'governorates': set(),
            'districts': set(),
            'units': set(),
            'regions': set(),
            'by_type': {
                'governorate': 0,
                'district': 0,
                'unit': 0
            }
        }
        
        for loc in locations:
            stats['by_type'][loc['type']] += 1
            
            if loc['type'] == 'governorate':
                stats['governorates'].add(loc['name'])
            elif loc['type'] == 'district':
                stats['districts'].add(loc['name'])
            elif loc['type'] == 'unit':
                stats['units'].add(loc['name'])
            
            if 'region' in loc['info']:
                stats['regions'].add(loc['info']['region'])
        
        # تحويل المجموعات إلى قوائم
        stats['governorates'] = list(stats['governorates'])
        stats['districts'] = list(stats['districts'])
        stats['units'] = list(stats['units'])
        stats['regions'] = list(stats['regions'])
        
        return stats
    
    def search_by_governorate(self, governorate: str) -> Optional[Dict]:
        """
        البحث عن كل المعلومات المتعلقة بمحافظة
        Search for all information about a governorate
        """
        if governorate not in self.data:
            return None
        
        gov_data = self.data[governorate]
        
        return {
            'governorate': governorate,
            'region': gov_data['region'],
            'type': gov_data['type'],
            'districts': [
                {
                    'name': district,
                    'type': district_data['type'],
                    'units': district_data['units']
                }
                for district, district_data in gov_data['districts'].items()
            ],
            'total_districts': len(gov_data['districts']),
            'total_units': sum(len(d['units']) for d in gov_data['districts'].values())
        }
    
    def search_by_region(self, region: str) -> Optional[Dict]:
        """
        البحث عن كل المعلومات المتعلقة بإقليم
        Search for all information about a region
        """
        if region not in self.regions:
            return None
        
        governorates = self.regions[region]
        
        return {
            'region': region,
            'governorates': governorates,
            'total_governorates': len(governorates),
            'details': {
                gov: self.data[gov] 
                for gov in governorates
            }
        }


# دالة مساعدة للاستخدام السريع
def extract(text: str) -> List[Dict]:
    """
    دالة سريعة لاستخراج المواقع من النص
    Quick function to extract locations from text
    
    Usage:
        from egypt_nlp import extract
        locations = extract("أنا من القاهرة، أعيش في مدينة نصر")
    """
    extractor = EgyptGeoExtractor()
    return extractor.extract_locations(text)


def find_governorate(text: str) -> Optional[str]:
    """
    دالة سريعة للعثور على المحافظة
    Quick function to find governorate
    """
    extractor = EgyptGeoExtractor()
    return extractor.find_governorate(text)

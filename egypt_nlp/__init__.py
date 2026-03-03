# -*- coding: utf-8 -*-
"""
Egypt NLP - Egyptian Geographic Named Entity Extraction
مكتبة استخراج الكيانات الجغرافية المصرية

A Python library for extracting and recognizing Egyptian geographic entities
from Arabic text with spelling error handling.

Usage:
    from egypt_nlp import EgyptGeoExtractor, extract, find_governorate
    
    # Quick extraction
    locations = extract("أنا من القاهرة، أعيش في مدينة نصر")
    
    # Enhanced extraction with fuzzy matching
    from egypt_nlp import EnhancedEgyptGeoExtractor, extract_enhanced
    
    extractor = EnhancedEgyptGeoExtractor(fuzzy_threshold=0.85)
    locations = extractor.extract_locations("أنا من الاسكندريه")  # يصحح "الإسكندرية"
    
    # Suggest corrections
    suggestions = extractor.suggest_corrections("نص به أخطاء")
"""

__version__ = '2.0.0'
__author__ = 'Egypt NLP Team'
__license__ = 'MIT'

from .extractor import (
    EgyptGeoExtractor,
    extract,
    find_governorate
)

from .extractor_enhanced import (
    EnhancedEgyptGeoExtractor,
    extract_enhanced,
    suggest_corrections
)

from .data import (
    ADMINISTRATIVE_DATA,
    REGIONS,
    ALIASES
)

__all__ = [
    'EgyptGeoExtractor',
    'extract',
    'find_governorate',
    'EnhancedEgyptGeoExtractor',
    'extract_enhanced',
    'suggest_corrections',
    'ADMINISTRATIVE_DATA',
    'REGIONS',
    'ALIASES',
]

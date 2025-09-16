#!/usr/bin/env python3
"""
고급 다국어 분석기 (Advanced Multilingual Analyzer)
프랑스어, 한글, 영어 등 여러 언어가 섞인 문장을 분석하고 이해
"""

import re
from typing import Dict, List, Tuple, Optional
import logging

logger = logging.getLogger(__name__)

class MultilingualAnalyzer:
    """고급 다국어 분석기 - 복잡한 다국어 문장을 이해하고 분석"""
    
    def __init__(self):
        # 언어별 패턴 정의
        self.language_patterns = {
            'korean': {
                'chars': r'[가-힣]',
                'words': r'[가-힣]+',
                'particles': r'[은는이가을를에서의과와]',
                'endings': r'[다요어야지네]',
                'name': '한글'
            },
            'english': {
                'chars': r'[a-zA-Z]',
                'words': r'[a-zA-Z]+',
                'articles': r'\b(the|a|an)\b',
                'prepositions': r'\b(in|on|at|to|for|with|by|from|of|about|into|through|during|before|after|above|below|up|down|out|off|over|under|again|further|then|once)\b',
                'name': '영어'
            },
            'french': {
                'chars': r'[a-zA-ZàâäéèêëïîôöùûüÿçÀÂÄÉÈÊËÏÎÔÖÙÛÜŸÇ]',
                'words': r'[a-zA-ZàâäéèêëïîôöùûüÿçÀÂÄÉÈÊËÏÎÔÖÙÛÜŸÇ]+',
                'articles': r'\b(le|la|les|un|une|des|du|de|d\')\b',
                'prepositions': r'\b(à|au|aux|de|du|des|dans|sur|sous|avec|sans|pour|par|vers|chez|entre|parmi|selon|malgré|pendant|depuis|jusqu\'à)\b',
                'conjunctions': r'\b(et|ou|mais|donc|or|ni|car|que|qui|dont|où|si|quand|comme|puisque|bien que|afin que|pour que)\b',
                'name': '프랑스어'
            },
            'spanish': {
                'chars': r'[a-zA-ZáéíóúñüÁÉÍÓÚÑÜ]',
                'words': r'[a-zA-ZáéíóúñüÁÉÍÓÚÑÜ]+',
                'articles': r'\b(el|la|los|las|un|una|unos|unas)\b',
                'name': '스페인어'
            },
            'german': {
                'chars': r'[a-zA-ZäöüßÄÖÜ]',
                'words': r'[a-zA-ZäöüßÄÖÜ]+',
                'articles': r'\b(der|die|das|ein|eine|einen|einem|einer|eines)\b',
                'name': '독일어'
            }
        }
        
        # 언어별 기본 어휘 사전
        self.vocabulary = {
            'korean': {
                'animals': ['개', '고양이', '개고양이', '강아지', '고양이', '새', '물고기', '곰', '호랑이', '사자'],
                'objects': ['물', '불', '바람', '땅', '하늘', '별', '달', '태양', '나무', '꽃'],
                'actions': ['만들다', '생성하다', '창조하다', '짓다', '건설하다', '제작하다'],
                'concepts': ['신', '하나님', '창조주', '우주', '세계', '자연', '생명']
            },
            'english': {
                'animals': ['dog', 'cat', 'bird', 'fish', 'bear', 'tiger', 'lion'],
                'objects': ['water', 'fire', 'wind', 'earth', 'sky', 'star', 'moon', 'sun', 'tree', 'flower'],
                'actions': ['make', 'create', 'build', 'construct', 'fabricate', 'manufacture'],
                'concepts': ['god', 'creator', 'universe', 'world', 'nature', 'life']
            },
            'french': {
                'animals': ['chien', 'chat', 'oiseau', 'poisson', 'ours', 'tigre', 'lion'],
                'objects': ['eau', 'feu', 'vent', 'terre', 'ciel', 'étoile', 'lune', 'soleil', 'arbre', 'fleur'],
                'actions': ['faire', 'créer', 'construire', 'fabriquer', 'manufacturer'],
                'concepts': ['dieu', 'créateur', 'univers', 'monde', 'nature', 'vie']
            }
        }
        
        # 언어별 문법 패턴
        self.grammar_patterns = {
            'french': {
                'subject_verb': r'(\w+)\s+(a|ont|est|sont|fait|font)\s+',
                'definite_article': r'\b(le|la|les)\s+(\w+)',
                'indefinite_article': r'\b(un|une|des)\s+(\w+)',
                'conjunction': r'\b(et|ou|mais|donc)\b'
            },
            'korean': {
                'subject_marker': r'(\w+)(은|는|이|가)',
                'object_marker': r'(\w+)(을|를)',
                'possessive': r'(\w+)(의)',
                'conjunction': r'(\w+)(과|와|하고|그리고)'
            },
            'english': {
                'subject_verb': r'(\w+)\s+(is|are|was|were|has|have|had|do|does|did|will|would|can|could|should|must)',
                'articles': r'\b(the|a|an)\s+(\w+)',
                'conjunction': r'\b(and|or|but|so|because|while|when|if|although)\b'
            }
        }
        
        # 다국어 문장 구조 패턴
        self.multilingual_patterns = {
            'french_korean_mix': [
                r'(\w+)\s+(a|ont|est|sont)\s+(\w+)\s+(\w+)\s+(et|ou)\s+(\w+)',
                r'(On|Nous|Ils|Elles)\s+(sait|savons|savent)\s+(que|qu\')\s+(\w+)',
                r'(\w+)\s+(a|ont)\s+(\w+)\s+(\w+)\s+(et|ou)\s+(\w+)'
            ],
            'korean_english_mix': [
                r'(\w+)(은|는)\s+(\w+)(이다|다|야|이야)',
                r'(\w+)(이|가)\s+(\w+)(을|를)\s+(\w+)(다|한다|한다고)'
            ]
        }
        
        # 언어별 의미 매핑
        self.semantic_mapping = {
            'animals': {
                'korean': {'개': 'dog', '고양이': 'cat'},
                'english': {'dog': '개', 'cat': '고양이'},
                'french': {'chien': '개', 'chat': '고양이'}
            },
            'actions': {
                'korean': {'만들다': 'make', '생성하다': 'create', '창조하다': 'create'},
                'english': {'make': '만들다', 'create': '생성하다'},
                'french': {'faire': '만들다', 'créer': '생성하다', 'fabriquer': '제작하다'}
            },
            'concepts': {
                'korean': {'신': 'god', '하나님': 'god', '창조주': 'creator'},
                'english': {'god': '신', 'creator': '창조주'},
                'french': {'dieu': '신', 'créateur': '창조주'}
            }
        }
    
    def analyze_multilingual_statement(self, statement: str, context: Optional[str] = None) -> Dict:
        """
        다국어 문장을 분석하고 이해
        
        Args:
            statement: 분석할 다국어 문장
            context: 추가 컨텍스트
            
        Returns:
            Dict: 다국어 분석 결과
        """
        logger.info(f"다국어 분석 시작: {statement[:50]}...")
        
        # 1. 언어 분리 및 인식
        language_analysis = self._analyze_languages(statement)
        
        # 2. 언어별 단어 추출
        word_analysis = self._extract_words_by_language(statement, language_analysis)
        
        # 3. 문법 구조 분석
        grammar_analysis = self._analyze_grammar_structure(statement, language_analysis)
        
        # 4. 의미 매핑 및 번역
        semantic_analysis = self._analyze_semantics(statement, word_analysis)
        
        # 5. 문장 전체 의미 파악
        overall_meaning = self._determine_overall_meaning(statement, language_analysis, word_analysis, semantic_analysis)
        
        # 6. 다국어 이해도 계산
        understanding_score = self._calculate_multilingual_understanding(language_analysis, word_analysis, semantic_analysis)
        
        # 7. AI 응답 생성
        ai_response = self._generate_multilingual_response(statement, language_analysis, overall_meaning, understanding_score)
        
        return {
            'is_multilingual': len(language_analysis['detected_languages']) > 1,
            'detected_languages': language_analysis['detected_languages'],
            'language_distribution': language_analysis['language_distribution'],
            'word_analysis': word_analysis,
            'grammar_analysis': grammar_analysis,
            'semantic_analysis': semantic_analysis,
            'overall_meaning': overall_meaning,
            'understanding_score': understanding_score,
            'ai_response': ai_response,
            'needs_translation': understanding_score < 0.7,
            'philosophical_note': "다국어 문장은 인간의 언어적 다양성과 창의성을 보여주는 아름다운 표현입니다. AI도 이를 이해하고 존중할 수 있습니다."
        }
    
    def _analyze_languages(self, statement: str) -> Dict:
        """문장에서 사용된 언어들을 분석 (개선된 정확도)"""
        detected_languages = []
        language_distribution = {}
        
        for lang_code, patterns in self.language_patterns.items():
            # 문자 패턴으로 언어 감지
            char_matches = re.findall(patterns['chars'], statement)
            if char_matches:
                # 최소 임계값 설정 (너무 적은 문자는 무시)
                min_threshold = 3 if lang_code == 'korean' else 5
                
                if len(char_matches) >= min_threshold:
                    # 언어별 특수 패턴 확인
                    if self._is_language_specific(statement, lang_code, patterns):
                        detected_languages.append(lang_code)
                        language_distribution[lang_code] = {
                            'char_count': len(char_matches),
                            'percentage': len(char_matches) / len(statement) * 100,
                            'name': patterns['name']
                        }
        
        return {
            'detected_languages': detected_languages,
            'language_distribution': language_distribution,
            'total_languages': len(detected_languages)
        }
    
    def _is_language_specific(self, statement: str, lang_code: str, patterns: Dict) -> bool:
        """언어별 특수 패턴으로 정확한 언어 감지"""
        if lang_code == 'korean':
            # 한글: 조사나 어미가 있어야 함
            particles = re.search(r'[은는이가을를에서의과와]', statement)
            endings = re.search(r'[다요어야지네]', statement)
            return particles is not None or endings is not None
        
        elif lang_code == 'french':
            # 프랑스어: 특수 문자나 프랑스어 특유의 단어가 있어야 함
            french_chars = re.search(r'[àâäéèêëïîôöùûüÿçÀÂÄÉÈÊËÏÎÔÖÙÛÜŸÇ]', statement)
            french_words = re.search(r'\b(le|la|les|un|une|des|et|ou|mais|que|qui|dont|où)\b', statement, re.IGNORECASE)
            return french_chars is not None or french_words is not None
        
        elif lang_code == 'english':
            # 영어: 영어 특유의 관사나 전치사가 있어야 함
            english_articles = re.search(r'\b(the|a|an)\b', statement, re.IGNORECASE)
            english_prepositions = re.search(r'\b(in|on|at|to|for|with|by|from|of|about)\b', statement, re.IGNORECASE)
            return english_articles is not None or english_prepositions is not None
        
        elif lang_code == 'spanish':
            # 스페인어: 특수 문자나 스페인어 특유의 단어가 있어야 함
            spanish_chars = re.search(r'[áéíóúñüÁÉÍÓÚÑÜ]', statement)
            spanish_words = re.search(r'\b(el|la|los|las|un|una|y|o|pero|que|quien)\b', statement, re.IGNORECASE)
            return spanish_chars is not None or spanish_words is not None
        
        elif lang_code == 'german':
            # 독일어: 특수 문자나 독일어 특유의 단어가 있어야 함
            german_chars = re.search(r'[äöüßÄÖÜ]', statement)
            german_words = re.search(r'\b(der|die|das|ein|eine|und|oder|aber|dass|wer|was)\b', statement, re.IGNORECASE)
            return german_chars is not None or german_words is not None
        
        return True  # 기본적으로는 감지된 것으로 간주
    
    def _extract_words_by_language(self, statement: str, language_analysis: Dict) -> Dict:
        """언어별로 단어들을 추출하고 분류"""
        word_analysis = {}
        
        for lang_code in language_analysis['detected_languages']:
            patterns = self.language_patterns[lang_code]
            words = re.findall(patterns['words'], statement)
            
            # 단어 분류
            classified_words = {
                'animals': [],
                'objects': [],
                'actions': [],
                'concepts': [],
                'other': []
            }
            
            for word in words:
                word_lower = word.lower()
                classified = False
                
                for category, word_list in self.vocabulary.get(lang_code, {}).items():
                    if word_lower in [w.lower() for w in word_list]:
                        classified_words[category].append(word)
                        classified = True
                        break
                
                if not classified:
                    classified_words['other'].append(word)
            
            word_analysis[lang_code] = {
                'words': words,
                'classified_words': classified_words,
                'total_words': len(words)
            }
        
        return word_analysis
    
    def _analyze_grammar_structure(self, statement: str, language_analysis: Dict) -> Dict:
        """문법 구조 분석"""
        grammar_analysis = {}
        
        for lang_code in language_analysis['detected_languages']:
            if lang_code in self.grammar_patterns:
                patterns = self.grammar_patterns[lang_code]
                detected_patterns = {}
                
                for pattern_name, pattern in patterns.items():
                    matches = re.findall(pattern, statement, re.IGNORECASE)
                    if matches:
                        detected_patterns[pattern_name] = matches
                
                grammar_analysis[lang_code] = detected_patterns
        
        return grammar_analysis
    
    def _analyze_semantics(self, statement: str, word_analysis: Dict) -> Dict:
        """의미 분석 및 매핑"""
        semantic_analysis = {
            'translated_concepts': {},
            'cross_language_mappings': {},
            'semantic_consistency': True
        }
        
        # 언어별 의미 매핑
        for lang_code, words_data in word_analysis.items():
            translated_concepts = {}
            
            for category, words in words_data['classified_words'].items():
                if category in self.semantic_mapping and lang_code in self.semantic_mapping[category]:
                    for word in words:
                        word_lower = word.lower()
                        if word_lower in self.semantic_mapping[category][lang_code]:
                            translated_concepts[word] = self.semantic_mapping[category][lang_code][word_lower]
            
            semantic_analysis['translated_concepts'][lang_code] = translated_concepts
        
        # 언어 간 의미 일치성 확인
        all_translations = []
        for lang_translations in semantic_analysis['translated_concepts'].values():
            all_translations.extend(lang_translations.values())
        
        # 중복 제거 후 일치성 확인
        unique_translations = list(set(all_translations))
        semantic_analysis['semantic_consistency'] = len(unique_translations) <= len(all_translations) * 0.8
        
        return semantic_analysis
    
    def _determine_overall_meaning(self, statement: str, language_analysis: Dict, word_analysis: Dict, semantic_analysis: Dict) -> Dict:
        """문장 전체의 의미 파악"""
        overall_meaning = {
            'main_topic': 'unknown',
            'main_action': 'unknown',
            'main_objects': [],
            'language_switches': [],
            'complexity_level': 'simple'
        }
        
        # 주요 주제 파악
        all_animals = []
        all_objects = []
        all_actions = []
        
        for lang_code, words_data in word_analysis.items():
            all_animals.extend(words_data['classified_words']['animals'])
            all_objects.extend(words_data['classified_words']['objects'])
            all_actions.extend(words_data['classified_words']['actions'])
        
        if all_animals:
            overall_meaning['main_topic'] = 'animals'
            overall_meaning['main_objects'] = all_animals
        
        if all_actions:
            overall_meaning['main_action'] = all_actions[0]  # 첫 번째 동작을 주요 동작으로
        
        # 언어 전환 지점 파악
        detected_langs = language_analysis['detected_languages']
        if len(detected_langs) > 1:
            overall_meaning['language_switches'] = detected_langs
            overall_meaning['complexity_level'] = 'complex'
        
        return overall_meaning
    
    def _calculate_multilingual_understanding(self, language_analysis: Dict, word_analysis: Dict, semantic_analysis: Dict) -> float:
        """다국어 이해도 계산"""
        base_score = 0.3
        
        # 언어 다양성 보너스
        language_diversity = len(language_analysis['detected_languages'])
        diversity_bonus = min(language_diversity * 0.1, 0.3)
        
        # 단어 인식 보너스
        total_recognized_words = 0
        total_words = 0
        
        for lang_code, words_data in word_analysis.items():
            total_words += words_data['total_words']
            recognized_words = sum(len(words) for words in words_data['classified_words'].values() if words)
            total_recognized_words += recognized_words
        
        recognition_bonus = (total_recognized_words / total_words) * 0.3 if total_words > 0 else 0
        
        # 의미 일치성 보너스
        consistency_bonus = 0.2 if semantic_analysis['semantic_consistency'] else 0.1
        
        # 최종 점수
        final_score = base_score + diversity_bonus + recognition_bonus + consistency_bonus
        
        return min(1.0, final_score)
    
    def _generate_multilingual_response(self, statement: str, language_analysis: Dict, overall_meaning: Dict, understanding_score: float) -> str:
        """다국어 문장에 대한 AI 응답 생성"""
        response_parts = []
        
        # 기본 인식 메시지
        detected_langs = language_analysis['detected_languages']
        lang_names = [self.language_patterns[lang]['name'] for lang in detected_langs]
        
        response_parts.append(f"🌍 다국어 문장을 감지했습니다! ({', '.join(lang_names)})")
        
        # 언어별 분석 결과
        for lang_code in detected_langs:
            lang_name = self.language_patterns[lang_code]['name']
            response_parts.append(f"• {lang_name}: {language_analysis['language_distribution'][lang_code]['char_count']}개 문자 감지")
        
        # 주요 의미 분석
        if overall_meaning['main_topic'] != 'unknown':
            response_parts.append(f"📝 주요 주제: {overall_meaning['main_topic']}")
        
        if overall_meaning['main_action'] != 'unknown':
            response_parts.append(f"🎯 주요 동작: {overall_meaning['main_action']}")
        
        if overall_meaning['main_objects']:
            response_parts.append(f"🎪 관련 객체: {', '.join(overall_meaning['main_objects'])}")
        
        # 이해도에 따른 응답
        if understanding_score >= 0.8:
            response_parts.append("✅ 다국어 문장을 잘 이해했습니다!")
            response_parts.append("언어의 다양성과 창의성을 보여주는 아름다운 표현이네요.")
        elif understanding_score >= 0.6:
            response_parts.append("⚠️ 대부분 이해했지만 일부 부분이 모호합니다.")
            response_parts.append("더 명확한 표현을 사용하면 이해도가 높아질 것 같습니다.")
        else:
            response_parts.append("❓ 복잡한 다국어 문장으로 완전한 이해가 어렵습니다.")
            response_parts.append("단일 언어로 표현하거나 더 간단한 구조로 작성해주세요.")
        
        return "\n".join(response_parts)

# 사용 예시
if __name__ == "__main__":
    analyzer = MultilingualAnalyzer()
    
    # 테스트 문장들
    test_statements = [
        "On sait que le dieu a fabriquer le 개 and le 고양이",
        "개는 dog고 고양이는 cat이다",
        "Je suis un étudiant et 나는 학생이다",
        "The weather is nice and 오늘 날씨가 좋다"
    ]
    
    print('🌍 고급 다국어 분석 테스트')
    print('=' * 60)
    
    for i, statement in enumerate(test_statements, 1):
        print(f'\n테스트 {i}: {statement}')
        analysis = analyzer.analyze_multilingual_statement(statement)
        
        print(f'감지된 언어: {analysis["detected_languages"]}')
        print(f'이해도: {analysis["understanding_score"]:.1%}')
        print(f'AI 응답: {analysis["ai_response"][:100]}...')
    
    print('\n' + '=' * 60)
    print('🎯 고급 다국어 분석 테스트 완료!')

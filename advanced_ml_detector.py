#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
고급 머신러닝 기반 거짓말 탐지기
우선순위 3-1: 머신러닝 모델 통합

작성일: 2025-09-19
버전: 2.0.0-enterprise
"""

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.preprocessing import StandardScaler
import torch
from transformers import AutoTokenizer, AutoModel, pipeline
import logging
from datetime import datetime
from typing import List, Dict, Tuple, Optional
import joblib
import os
import json

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AdvancedMLDetector:
    """고급 머신러닝 기반 거짓말 탐지기"""
    
    def __init__(self):
        self.models = {}
        self.vectorizer = None
        self.scaler = StandardScaler()
        self.tokenizer = None
        self.bert_model = None
        self.bert_pipeline = None
        self.model_weights = {
            'random_forest': 0.25,
            'gradient_boosting': 0.25,
            'logistic_regression': 0.25,
            'bert_classifier': 0.25
        }
        self.is_trained = False
        self.model_path = 'models/'
        self.ensure_model_directory()
        
        # 모델 초기화
        self.initialize_models()
        
        logger.info("고급 머신러닝 탐지기가 초기화되었습니다.")
    
    def ensure_model_directory(self):
        """모델 저장 디렉토리 생성"""
        if not os.path.exists(self.model_path):
            os.makedirs(self.model_path)
            logger.info(f"모델 디렉토리 생성: {self.model_path}")
    
    def initialize_models(self):
        """모델 초기화"""
        try:
            # 전통적인 ML 모델들
            self.models['random_forest'] = RandomForestClassifier(
                n_estimators=100,
                max_depth=10,
                random_state=42,
                n_jobs=-1
            )
            
            self.models['gradient_boosting'] = GradientBoostingClassifier(
                n_estimators=100,
                learning_rate=0.1,
                max_depth=6,
                random_state=42
            )
            
            self.models['logistic_regression'] = LogisticRegression(
                random_state=42,
                max_iter=1000
            )
            
            self.models['svm'] = SVC(
                kernel='rbf',
                probability=True,
                random_state=42
            )
            
            # BERT 모델 초기화
            self.initialize_bert_model()
            
            logger.info("모든 모델이 성공적으로 초기화되었습니다.")
            
        except Exception as e:
            logger.error(f"모델 초기화 중 오류: {str(e)}")
            # BERT 없이도 작동하도록 설정
            self.model_weights['bert_classifier'] = 0.0
            self.model_weights['random_forest'] = 0.33
            self.model_weights['gradient_boosting'] = 0.33
            self.model_weights['logistic_regression'] = 0.34
    
    def initialize_bert_model(self):
        """BERT 모델 초기화"""
        try:
            # 한국어 BERT 모델 사용
            model_name = "klue/bert-base"
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.bert_model = AutoModel.from_pretrained(model_name)
            
            # 텍스트 분류 파이프라인 생성
            self.bert_pipeline = pipeline(
                "text-classification",
                model=model_name,
                tokenizer=self.tokenizer,
                device=0 if torch.cuda.is_available() else -1
            )
            
            logger.info("BERT 모델이 성공적으로 초기화되었습니다.")
            
        except Exception as e:
            logger.warning(f"BERT 모델 초기화 실패: {str(e)}")
            logger.warning("BERT 없이 전통적인 ML 모델만 사용합니다.")
            self.bert_pipeline = None
    
    def generate_synthetic_data(self, num_samples=1000):
        """합성 학습 데이터 생성"""
        logger.info("합성 학습 데이터를 생성하고 있습니다...")
        
        # 진실한 문장들
        true_statements = [
            "지구는 둥글다.",
            "물은 100도에서 끓는다.",
            "1 + 1 = 2이다.",
            "태양은 별이다.",
            "인간은 포유동물이다.",
            "한국은 아시아에 있다.",
            "파리는 프랑스의 수도이다.",
            "물은 H2O로 구성된다.",
            "지구는 태양계에 있다.",
            "인간은 두 개의 눈을 가진다.",
            "고양이는 동물이다.",
            "책은 읽을 수 있다.",
            "컴퓨터는 전자기기이다.",
            "학교는 교육 기관이다.",
            "병원은 치료하는 곳이다.",
            "음식은 영양을 제공한다.",
            "운동은 건강에 좋다.",
            "독서는 지식을 늘린다.",
            "친구는 소중하다.",
            "가족은 사랑한다."
        ]
        
        # 거짓 문장들
        false_statements = [
            "지구는 평평하다.",
            "물은 200도에서 끓는다.",
            "1 + 1 = 3이다.",
            "태양은 행성이다.",
            "인간은 파충류이다.",
            "한국은 유럽에 있다.",
            "파리는 독일의 수도이다.",
            "물은 H3O로 구성된다.",
            "지구는 화성계에 있다.",
            "인간은 세 개의 눈을 가진다.",
            "고양이는 식물이다.",
            "책은 먹을 수 있다.",
            "컴퓨터는 생물이다.",
            "학교는 요리하는 곳이다.",
            "병원은 놀이터이다.",
            "음식은 독을 제공한다.",
            "운동은 건강에 나쁘다.",
            "독서는 지식을 줄인다.",
            "친구는 무가치하다.",
            "가족은 미워한다."
        ]
        
        # 데이터 확장
        true_data = []
        false_data = []
        
        for _ in range(num_samples // 2):
            # 진실한 문장 선택 및 변형
            base_statement = np.random.choice(true_statements)
            true_data.append({
                'text': base_statement,
                'label': 1,  # 진실
                'confidence': np.random.uniform(0.7, 1.0)
            })
            
            # 거짓 문장 선택 및 변형
            base_statement = np.random.choice(false_statements)
            false_data.append({
                'text': base_statement,
                'label': 0,  # 거짓
                'confidence': np.random.uniform(0.7, 1.0)
            })
        
        # 데이터 결합
        all_data = true_data + false_data
        np.random.shuffle(all_data)
        
        # DataFrame으로 변환
        df = pd.DataFrame(all_data)
        
        logger.info(f"합성 데이터 생성 완료: {len(df)}개 샘플")
        return df
    
    def extract_features(self, texts):
        """텍스트에서 특징 추출"""
        features = []
        
        for text in texts:
            feature_dict = {}
            
            # 기본 텍스트 특징
            feature_dict['length'] = len(text)
            feature_dict['word_count'] = len(text.split())
            feature_dict['char_count'] = len(text.replace(' ', ''))
            feature_dict['avg_word_length'] = feature_dict['char_count'] / max(feature_dict['word_count'], 1)
            
            # 구두점 특징
            feature_dict['exclamation_count'] = text.count('!')
            feature_dict['question_count'] = text.count('?')
            feature_dict['period_count'] = text.count('.')
            feature_dict['comma_count'] = text.count(',')
            
            # 대소문자 특징
            feature_dict['upper_ratio'] = sum(1 for c in text if c.isupper()) / max(len(text), 1)
            feature_dict['lower_ratio'] = sum(1 for c in text if c.islower()) / max(len(text), 1)
            
            # 숫자 특징
            feature_dict['digit_count'] = sum(1 for c in text if c.isdigit())
            feature_dict['digit_ratio'] = feature_dict['digit_count'] / max(len(text), 1)
            
            # 특수 문자 특징
            feature_dict['special_char_count'] = sum(1 for c in text if not c.isalnum() and not c.isspace())
            feature_dict['special_char_ratio'] = feature_dict['special_char_count'] / max(len(text), 1)
            
            # 반복 문자 특징
            feature_dict['repeated_chars'] = sum(1 for i in range(len(text)-1) if text[i] == text[i+1])
            
            # 감정적 표현 특징
            emotional_words = ['정말', '완전', '절대', '매우', '너무', '진짜', '정말로', '완전히', '절대적으로']
            feature_dict['emotional_word_count'] = sum(1 for word in emotional_words if word in text)
            
            # 확신 표현 특징
            certainty_words = ['확실', '분명', '틀림없', '당연', '물론', '확실히', '분명히']
            feature_dict['certainty_word_count'] = sum(1 for word in certainty_words if word in text)
            
            # 부정 표현 특징
            negative_words = ['아니', '안', '못', '없', '모르', '틀렸', '잘못']
            feature_dict['negative_word_count'] = sum(1 for word in negative_words if word in text)
            
            features.append(feature_dict)
        
        return pd.DataFrame(features)
    
    def get_bert_embeddings(self, texts):
        """BERT 임베딩 추출"""
        if self.bert_pipeline is None:
            return np.zeros((len(texts), 768))  # BERT 기본 차원
        
        try:
            embeddings = []
            for text in texts:
                # BERT 토크나이저로 토큰화
                inputs = self.tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
                
                # BERT 모델로 임베딩 추출
                with torch.no_grad():
                    outputs = self.bert_model(**inputs)
                    # [CLS] 토큰의 임베딩 사용
                    embedding = outputs.last_hidden_state[:, 0, :].numpy()
                    embeddings.append(embedding[0])
            
            return np.array(embeddings)
            
        except Exception as e:
            logger.warning(f"BERT 임베딩 추출 실패: {str(e)}")
            return np.zeros((len(texts), 768))
    
    def train_models(self, X_text, y, X_features=None):
        """모델 훈련"""
        logger.info("모델 훈련을 시작합니다...")
        
        try:
            # TF-IDF 벡터화
            self.vectorizer = TfidfVectorizer(
                max_features=1000,
                ngram_range=(1, 2),
                stop_words=None
            )
            X_tfidf = self.vectorizer.fit_transform(X_text)
            
            # 특징 추출
            if X_features is None:
                X_features = self.extract_features(X_text)
            
            # BERT 임베딩
            X_bert = self.get_bert_embeddings(X_text)
            
            # 특징 결합
            X_combined = np.hstack([
                X_tfidf.toarray(),
                X_features.values,
                X_bert
            ])
            
            # 데이터 분할
            X_train, X_test, y_train, y_test = train_test_split(
                X_combined, y, test_size=0.2, random_state=42, stratify=y
            )
            
            # 특징 정규화
            X_train_scaled = self.scaler.fit_transform(X_train)
            X_test_scaled = self.scaler.transform(X_test)
            
            # 각 모델 훈련
            model_scores = {}
            
            for name, model in self.models.items():
                if name == 'svm':
                    # SVM은 정규화된 데이터 사용
                    model.fit(X_train_scaled, y_train)
                    y_pred = model.predict(X_test_scaled)
                else:
                    # 다른 모델들은 원본 데이터 사용
                    model.fit(X_train, y_train)
                    y_pred = model.predict(X_test)
                
                # 성능 평가
                accuracy = accuracy_score(y_test, y_pred)
                precision = precision_score(y_test, y_pred, average='weighted')
                recall = recall_score(y_test, y_pred, average='weighted')
                f1 = f1_score(y_test, y_pred, average='weighted')
                
                model_scores[name] = {
                    'accuracy': accuracy,
                    'precision': precision,
                    'recall': recall,
                    'f1': f1
                }
                
                logger.info(f"{name} 모델 훈련 완료 - 정확도: {accuracy:.3f}, F1: {f1:.3f}")
            
            # BERT 분류기 훈련 (간단한 로지스틱 회귀)
            if self.bert_pipeline is not None:
                bert_classifier = LogisticRegression(random_state=42, max_iter=1000)
                bert_classifier.fit(X_bert, y)
                self.models['bert_classifier'] = bert_classifier
                
                # BERT 성능 평가
                y_pred_bert = bert_classifier.predict(X_bert)
                bert_accuracy = accuracy_score(y, y_pred_bert)
                model_scores['bert_classifier'] = {'accuracy': bert_accuracy}
                logger.info(f"BERT 분류기 훈련 완료 - 정확도: {bert_accuracy:.3f}")
            
            self.is_trained = True
            
            # 모델 저장
            self.save_models()
            
            logger.info("모든 모델 훈련이 완료되었습니다.")
            return model_scores
            
        except Exception as e:
            logger.error(f"모델 훈련 중 오류: {str(e)}")
            return None
    
    def predict(self, text):
        """텍스트 진실성 예측"""
        if not self.is_trained:
            logger.warning("모델이 훈련되지 않았습니다. 기본 휴리스틱을 사용합니다.")
            return self.heuristic_prediction(text)
        
        try:
            # 특징 추출
            X_tfidf = self.vectorizer.transform([text])
            X_features = self.extract_features([text])
            X_bert = self.get_bert_embeddings([text])
            
            # 특징 결합
            X_combined = np.hstack([
                X_tfidf.toarray(),
                X_features.values,
                X_bert
            ])
            
            # 각 모델 예측
            predictions = {}
            probabilities = {}
            
            for name, model in self.models.items():
                if name == 'svm':
                    X_scaled = self.scaler.transform(X_combined)
                    pred = model.predict(X_scaled)[0]
                    prob = model.predict_proba(X_scaled)[0]
                else:
                    pred = model.predict(X_combined)[0]
                    if hasattr(model, 'predict_proba'):
                        prob = model.predict_proba(X_combined)[0]
                    else:
                        prob = [0.5, 0.5]  # 기본 확률
                
                predictions[name] = pred
                probabilities[name] = prob[1] if len(prob) > 1 else prob[0]
            
            # 가중 평균 예측
            weighted_prediction = 0
            total_weight = 0
            
            for name, weight in self.model_weights.items():
                if name in predictions:
                    weighted_prediction += predictions[name] * weight
                    total_weight += weight
            
            if total_weight > 0:
                final_prediction = weighted_prediction / total_weight
            else:
                final_prediction = 0.5
            
            # 가중 평균 확률
            weighted_probability = 0
            for name, weight in self.model_weights.items():
                if name in probabilities:
                    weighted_probability += probabilities[name] * weight
            
            if total_weight > 0:
                final_probability = weighted_probability / total_weight
            else:
                final_probability = 0.5
            
            return {
                'prediction': int(final_prediction > 0.5),
                'probability': float(final_probability),
                'confidence': abs(final_probability - 0.5) * 2,
                'individual_predictions': predictions,
                'individual_probabilities': probabilities
            }
            
        except Exception as e:
            logger.error(f"예측 중 오류: {str(e)}")
            return self.heuristic_prediction(text)
    
    def heuristic_prediction(self, text):
        """휴리스틱 기반 예측 (백업)"""
        # 간단한 휴리스틱 규칙
        truth_indicators = ['확실', '분명', '틀림없', '사실', '진실']
        lie_indicators = ['아니', '틀렸', '잘못', '거짓', '가짜']
        
        truth_score = sum(1 for word in truth_indicators if word in text)
        lie_score = sum(1 for word in lie_indicators if word in text)
        
        if truth_score > lie_score:
            return {'prediction': 1, 'probability': 0.7, 'confidence': 0.4}
        elif lie_score > truth_score:
            return {'prediction': 0, 'probability': 0.3, 'confidence': 0.4}
        else:
            return {'prediction': 1, 'probability': 0.5, 'confidence': 0.1}
    
    def save_models(self):
        """모델 저장"""
        try:
            for name, model in self.models.items():
                if model is not None:
                    model_path = os.path.join(self.model_path, f"{name}_model.pkl")
                    joblib.dump(model, model_path)
            
            # 벡터라이저와 스케일러 저장
            if self.vectorizer is not None:
                joblib.dump(self.vectorizer, os.path.join(self.model_path, "vectorizer.pkl"))
            joblib.dump(self.scaler, os.path.join(self.model_path, "scaler.pkl"))
            
            # 모델 가중치 저장
            with open(os.path.join(self.model_path, "model_weights.json"), 'w') as f:
                json.dump(self.model_weights, f)
            
            logger.info("모델이 성공적으로 저장되었습니다.")
            
        except Exception as e:
            logger.error(f"모델 저장 중 오류: {str(e)}")
    
    def load_models(self):
        """모델 로드"""
        try:
            # 모델 로드
            for name in self.models.keys():
                model_path = os.path.join(self.model_path, f"{name}_model.pkl")
                if os.path.exists(model_path):
                    self.models[name] = joblib.load(model_path)
            
            # 벡터라이저와 스케일러 로드
            vectorizer_path = os.path.join(self.model_path, "vectorizer.pkl")
            if os.path.exists(vectorizer_path):
                self.vectorizer = joblib.load(vectorizer_path)
            
            scaler_path = os.path.join(self.model_path, "scaler.pkl")
            if os.path.exists(scaler_path):
                self.scaler = joblib.load(scaler_path)
            
            # 모델 가중치 로드
            weights_path = os.path.join(self.model_path, "model_weights.json")
            if os.path.exists(weights_path):
                with open(weights_path, 'r') as f:
                    self.model_weights = json.load(f)
            
            self.is_trained = True
            logger.info("모델이 성공적으로 로드되었습니다.")
            
        except Exception as e:
            logger.error(f"모델 로드 중 오류: {str(e)}")
    
    def evaluate_model_performance(self, X_text, y):
        """모델 성능 평가"""
        if not self.is_trained:
            logger.warning("모델이 훈련되지 않았습니다.")
            return None
        
        try:
            predictions = []
            probabilities = []
            
            for text in X_text:
                result = self.predict(text)
                predictions.append(result['prediction'])
                probabilities.append(result['probability'])
            
            # 성능 메트릭 계산
            accuracy = accuracy_score(y, predictions)
            precision = precision_score(y, predictions, average='weighted')
            recall = recall_score(y, predictions, average='weighted')
            f1 = f1_score(y, predictions, average='weighted')
            
            return {
                'accuracy': accuracy,
                'precision': precision,
                'recall': recall,
                'f1_score': f1,
                'predictions': predictions,
                'probabilities': probabilities
            }
            
        except Exception as e:
            logger.error(f"성능 평가 중 오류: {str(e)}")
            return None

def main():
    """메인 함수 - 모델 훈련 및 테스트"""
    detector = AdvancedMLDetector()
    
    # 합성 데이터 생성
    logger.info("합성 데이터를 생성하고 있습니다...")
    data = detector.generate_synthetic_data(1000)
    
    # 데이터 분할
    X_text = data['text'].tolist()
    y = data['label'].tolist()
    
    # 모델 훈련
    logger.info("모델 훈련을 시작합니다...")
    scores = detector.train_models(X_text, y)
    
    if scores:
        logger.info("모델 훈련 완료!")
        for name, score in scores.items():
            logger.info(f"{name}: {score}")
    
    # 테스트 예측
    test_texts = [
        "지구는 둥글다.",
        "지구는 평평하다.",
        "물은 100도에서 끓는다.",
        "물은 200도에서 끓는다."
    ]
    
    logger.info("테스트 예측을 수행합니다...")
    for text in test_texts:
        result = detector.predict(text)
        logger.info(f"문장: {text}")
        logger.info(f"예측: {'진실' if result['prediction'] else '거짓'}")
        logger.info(f"확률: {result['probability']:.3f}")
        logger.info(f"신뢰도: {result['confidence']:.3f}")
        logger.info("-" * 50)

if __name__ == '__main__':
    main()

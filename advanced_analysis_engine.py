"""
고급 분석 엔진
패턴 분석, 예측, 사용자 행동 분석, 실시간 대시보드 기능을 제공합니다.
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest
from sklearn.linear_model import LinearRegression
from sklearn.metrics import silhouette_score
import plotly.graph_objs as go
import plotly.express as px
from plotly.subplots import make_subplots
import logging
from collections import defaultdict, Counter
import json

logger = logging.getLogger(__name__)

class PatternAnalyzer:
    """패턴 분석 클래스"""
    
    def __init__(self):
        self.scaler = StandardScaler()
        self.cluster_models = {}
        self.anomaly_detector = IsolationForest(contamination=0.1, random_state=42)
        
    def analyze_truth_patterns(self, analysis_data: List[Dict]) -> Dict[str, Any]:
        """진실성 패턴 분석"""
        try:
            if not analysis_data:
                return {"error": "분석할 데이터가 없습니다."}
            
            df = pd.DataFrame(analysis_data)
            
            # 기본 통계
            patterns = {
                "total_analyses": len(df),
                "average_truth_score": df['truth_score'].mean() if 'truth_score' in df.columns else 0,
                "average_confidence": df['confidence_score'].mean() if 'confidence_score' in df.columns else 0,
                "processing_time_stats": {
                    "mean": df['processing_time'].mean() if 'processing_time' in df.columns else 0,
                    "std": df['processing_time'].std() if 'processing_time' in df.columns else 0,
                    "min": df['processing_time'].min() if 'processing_time' in df.columns else 0,
                    "max": df['processing_time'].max() if 'processing_time' in df.columns else 0
                }
            }
            
            # 시간대별 패턴 분석
            if 'created_at' in df.columns:
                df['created_at'] = pd.to_datetime(df['created_at'])
                df['hour'] = df['created_at'].dt.hour
                df['day_of_week'] = df['created_at'].dt.dayofweek
                
                patterns['hourly_distribution'] = df['hour'].value_counts().to_dict()
                patterns['daily_distribution'] = df['day_of_week'].value_counts().to_dict()
            
            # 진실성 점수 분포 분석
            if 'truth_score' in df.columns:
                truth_scores = df['truth_score'].dropna()
                patterns['truth_score_distribution'] = {
                    "histogram": np.histogram(truth_scores, bins=10)[0].tolist(),
                    "percentiles": {
                        "25th": np.percentile(truth_scores, 25),
                        "50th": np.percentile(truth_scores, 50),
                        "75th": np.percentile(truth_scores, 75),
                        "90th": np.percentile(truth_scores, 90)
                    }
                }
            
            # 클러스터링 분석
            if len(df) >= 3:
                features = ['truth_score', 'confidence_score', 'processing_time']
                available_features = [f for f in features if f in df.columns]
                
                if available_features:
                    X = df[available_features].fillna(0)
                    X_scaled = self.scaler.fit_transform(X)
                    
                    # 최적 클러스터 수 찾기
                    best_k = 2
                    best_score = -1
                    for k in range(2, min(6, len(df))):
                        kmeans = KMeans(n_clusters=k, random_state=42)
                        labels = kmeans.fit_predict(X_scaled)
                        score = silhouette_score(X_scaled, labels)
                        if score > best_score:
                            best_score = score
                            best_k = k
                    
                    # 최적 클러스터로 분석
                    kmeans = KMeans(n_clusters=best_k, random_state=42)
                    cluster_labels = kmeans.fit_predict(X_scaled)
                    
                    patterns['clustering'] = {
                        "optimal_clusters": best_k,
                        "silhouette_score": best_score,
                        "cluster_distribution": Counter(cluster_labels).to_dict(),
                        "cluster_centers": kmeans.cluster_centers_.tolist()
                    }
            
            # 이상치 탐지
            if len(df) >= 10:
                numeric_cols = df.select_dtypes(include=[np.number]).columns
                if len(numeric_cols) > 0:
                    X_numeric = df[numeric_cols].fillna(0)
                    anomaly_labels = self.anomaly_detector.fit_predict(X_numeric)
                    patterns['anomalies'] = {
                        "total_anomalies": sum(anomaly_labels == -1),
                        "anomaly_rate": sum(anomaly_labels == -1) / len(anomaly_labels),
                        "anomaly_indices": [i for i, label in enumerate(anomaly_labels) if label == -1]
                    }
            
            return patterns
            
        except Exception as e:
            logger.error(f"패턴 분석 실패: {e}")
            return {"error": f"패턴 분석 중 오류가 발생했습니다: {str(e)}"}
    
    def analyze_user_behavior(self, user_data: List[Dict]) -> Dict[str, Any]:
        """사용자 행동 분석"""
        try:
            if not user_data:
                return {"error": "사용자 데이터가 없습니다."}
            
            df = pd.DataFrame(user_data)
            
            behavior_analysis = {
                "total_users": df['user_id'].nunique() if 'user_id' in df.columns else 0,
                "total_sessions": df['session_id'].nunique() if 'session_id' in df.columns else 0,
                "average_analyses_per_user": len(df) / df['user_id'].nunique() if 'user_id' in df.columns else 0
            }
            
            # 사용자별 분석 패턴
            if 'user_id' in df.columns and 'created_at' in df.columns:
                df['created_at'] = pd.to_datetime(df['created_at'])
                user_activity = df.groupby('user_id').agg({
                    'created_at': ['count', 'min', 'max'],
                    'truth_score': 'mean',
                    'confidence_score': 'mean',
                    'processing_time': 'mean'
                }).round(3)
                
                behavior_analysis['user_activity'] = user_activity.to_dict()
            
            # 세션 분석
            if 'session_id' in df.columns and 'created_at' in df.columns:
                session_analysis = df.groupby('session_id').agg({
                    'created_at': ['count', 'min', 'max'],
                    'truth_score': 'mean',
                    'confidence_score': 'mean'
                }).round(3)
                
                behavior_analysis['session_analysis'] = session_analysis.to_dict()
            
            return behavior_analysis
            
        except Exception as e:
            logger.error(f"사용자 행동 분석 실패: {e}")
            return {"error": f"사용자 행동 분석 중 오류가 발생했습니다: {str(e)}"}

class PredictiveAnalyzer:
    """예측 분석 클래스"""
    
    def __init__(self):
        self.models = {}
        self.scaler = StandardScaler()
    
    def predict_truth_score(self, features: Dict[str, Any]) -> Dict[str, Any]:
        """진실성 점수 예측"""
        try:
            # 간단한 선형 회귀 모델 사용
            # 실제로는 더 복잡한 모델을 사용할 수 있습니다
            model = LinearRegression()
            
            # 예측을 위한 기본 특성들
            feature_vector = np.array([
                features.get('text_length', 0),
                features.get('word_count', 0),
                features.get('sentence_count', 0),
                features.get('has_numbers', 0),
                features.get('has_quotes', 0),
                features.get('has_question_marks', 0),
                features.get('has_exclamation_marks', 0)
            ]).reshape(1, -1)
            
            # 간단한 휴리스틱 기반 예측
            predicted_score = 0.5  # 기본값
            
            # 텍스트 길이 기반 조정
            if features.get('text_length', 0) > 100:
                predicted_score += 0.1
            elif features.get('text_length', 0) < 20:
                predicted_score -= 0.1
            
            # 숫자 포함 여부
            if features.get('has_numbers', 0):
                predicted_score += 0.05
            
            # 질문이나 감탄사 포함 여부
            if features.get('has_question_marks', 0) or features.get('has_exclamation_marks', 0):
                predicted_score -= 0.05
            
            # 점수 범위 제한
            predicted_score = max(0.0, min(1.0, predicted_score))
            
            return {
                "predicted_truth_score": predicted_score,
                "confidence": 0.7,  # 예측 신뢰도
                "features_used": list(features.keys()),
                "model_type": "heuristic"
            }
            
        except Exception as e:
            logger.error(f"진실성 점수 예측 실패: {e}")
            return {"error": f"예측 중 오류가 발생했습니다: {str(e)}"}
    
    def predict_system_load(self, historical_data: List[Dict]) -> Dict[str, Any]:
        """시스템 부하 예측"""
        try:
            if len(historical_data) < 10:
                return {"error": "예측을 위한 충분한 데이터가 없습니다."}
            
            df = pd.DataFrame(historical_data)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df = df.sort_values('timestamp')
            
            # 시간별 요청 수 계산
            df['hour'] = df['timestamp'].dt.hour
            hourly_requests = df.groupby('hour').size()
            
            # 다음 시간대 예측 (간단한 평균 기반)
            current_hour = datetime.now().hour
            next_hour = (current_hour + 1) % 24
            
            # 과거 같은 시간대의 평균 요청 수
            historical_same_hour = hourly_requests.get(next_hour, 0)
            average_requests = hourly_requests.mean()
            
            predicted_requests = max(historical_same_hour, average_requests)
            
            return {
                "predicted_requests_next_hour": int(predicted_requests),
                "current_hour_requests": int(hourly_requests.get(current_hour, 0)),
                "average_requests": float(average_requests),
                "prediction_confidence": 0.6
            }
            
        except Exception as e:
            logger.error(f"시스템 부하 예측 실패: {e}")
            return {"error": f"시스템 부하 예측 중 오류가 발생했습니다: {str(e)}"}

class RealTimeDashboard:
    """실시간 대시보드 클래스"""
    
    def __init__(self):
        self.metrics_cache = {}
        self.update_interval = 30  # 30초마다 업데이트
    
    def generate_dashboard_data(self, analysis_data: List[Dict]) -> Dict[str, Any]:
        """대시보드 데이터 생성"""
        try:
            if not analysis_data:
                return {"error": "대시보드 데이터가 없습니다."}
            
            df = pd.DataFrame(analysis_data)
            
            # 기본 메트릭
            dashboard_data = {
                "timestamp": datetime.now().isoformat(),
                "total_analyses": len(df),
                "real_time_metrics": self._calculate_real_time_metrics(df),
                "charts": self._generate_charts(df),
                "alerts": self._generate_alerts(df)
            }
            
            return dashboard_data
            
        except Exception as e:
            logger.error(f"대시보드 데이터 생성 실패: {e}")
            return {"error": f"대시보드 데이터 생성 중 오류가 발생했습니다: {str(e)}"}
    
    def _calculate_real_time_metrics(self, df: pd.DataFrame) -> Dict[str, Any]:
        """실시간 메트릭 계산"""
        metrics = {}
        
        # 최근 1시간 분석 수
        if 'created_at' in df.columns:
            df['created_at'] = pd.to_datetime(df['created_at'])
            one_hour_ago = datetime.now() - timedelta(hours=1)
            recent_analyses = df[df['created_at'] >= one_hour_ago]
            metrics['analyses_last_hour'] = len(recent_analyses)
        
        # 평균 처리 시간
        if 'processing_time' in df.columns:
            metrics['average_processing_time'] = float(df['processing_time'].mean())
        
        # 평균 진실성 점수
        if 'truth_score' in df.columns:
            metrics['average_truth_score'] = float(df['truth_score'].mean())
        
        # 평균 신뢰도
        if 'confidence_score' in df.columns:
            metrics['average_confidence'] = float(df['confidence_score'].mean())
        
        return metrics
    
    def _generate_charts(self, df: pd.DataFrame) -> Dict[str, Any]:
        """차트 데이터 생성"""
        charts = {}
        
        # 진실성 점수 분포 히스토그램
        if 'truth_score' in df.columns:
            truth_scores = df['truth_score'].dropna()
            hist, bins = np.histogram(truth_scores, bins=20)
            
            charts['truth_score_distribution'] = {
                "type": "histogram",
                "data": {
                    "x": bins[:-1].tolist(),
                    "y": hist.tolist()
                },
                "title": "진실성 점수 분포"
            }
        
        # 시간별 분석 수
        if 'created_at' in df.columns:
            df['created_at'] = pd.to_datetime(df['created_at'])
            df['hour'] = df['created_at'].dt.hour
            hourly_counts = df['hour'].value_counts().sort_index()
            
            charts['hourly_analyses'] = {
                "type": "bar",
                "data": {
                    "x": hourly_counts.index.tolist(),
                    "y": hourly_counts.values.tolist()
                },
                "title": "시간별 분석 수"
            }
        
        # 처리 시간 vs 진실성 점수 산점도
        if 'processing_time' in df.columns and 'truth_score' in df.columns:
            charts['processing_vs_truth'] = {
                "type": "scatter",
                "data": {
                    "x": df['processing_time'].tolist(),
                    "y": df['truth_score'].tolist()
                },
                "title": "처리 시간 vs 진실성 점수"
            }
        
        return charts
    
    def _generate_alerts(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """알림 생성"""
        alerts = []
        
        # 처리 시간이 너무 긴 경우
        if 'processing_time' in df.columns:
            avg_processing_time = df['processing_time'].mean()
            if avg_processing_time > 10:  # 10초 이상
                alerts.append({
                    "type": "warning",
                    "message": f"평균 처리 시간이 {avg_processing_time:.2f}초로 높습니다.",
                    "timestamp": datetime.now().isoformat()
                })
        
        # 진실성 점수가 낮은 경우
        if 'truth_score' in df.columns:
            avg_truth_score = df['truth_score'].mean()
            if avg_truth_score < 0.3:
                alerts.append({
                    "type": "warning",
                    "message": f"평균 진실성 점수가 {avg_truth_score:.2f}로 낮습니다.",
                    "timestamp": datetime.now().isoformat()
                })
        
        # 신뢰도가 낮은 경우
        if 'confidence_score' in df.columns:
            avg_confidence = df['confidence_score'].mean()
            if avg_confidence < 0.5:
                alerts.append({
                    "type": "warning",
                    "message": f"평균 신뢰도가 {avg_confidence:.2f}로 낮습니다.",
                    "timestamp": datetime.now().isoformat()
                })
        
        return alerts

class AdvancedAnalysisEngine:
    """고급 분석 엔진 메인 클래스"""
    
    def __init__(self):
        self.pattern_analyzer = PatternAnalyzer()
        self.predictive_analyzer = PredictiveAnalyzer()
        self.dashboard = RealTimeDashboard()
    
    def analyze_patterns(self, analysis_data: List[Dict]) -> Dict[str, Any]:
        """패턴 분석 실행"""
        return self.pattern_analyzer.analyze_truth_patterns(analysis_data)
    
    def analyze_user_behavior(self, user_data: List[Dict]) -> Dict[str, Any]:
        """사용자 행동 분석 실행"""
        return self.pattern_analyzer.analyze_user_behavior(user_data)
    
    def predict_truth_score(self, features: Dict[str, Any]) -> Dict[str, Any]:
        """진실성 점수 예측 실행"""
        return self.predictive_analyzer.predict_truth_score(features)
    
    def predict_system_load(self, historical_data: List[Dict]) -> Dict[str, Any]:
        """시스템 부하 예측 실행"""
        return self.predictive_analyzer.predict_system_load(historical_data)
    
    def generate_dashboard_data(self, analysis_data: List[Dict]) -> Dict[str, Any]:
        """대시보드 데이터 생성 실행"""
        return self.dashboard.generate_dashboard_data(analysis_data)
    
    def generate_comprehensive_report(self, analysis_data: List[Dict], user_data: List[Dict]) -> Dict[str, Any]:
        """종합 분석 보고서 생성"""
        try:
            report = {
                "timestamp": datetime.now().isoformat(),
                "pattern_analysis": self.analyze_patterns(analysis_data),
                "user_behavior_analysis": self.analyze_user_behavior(user_data),
                "dashboard_data": self.generate_dashboard_data(analysis_data),
                "recommendations": self._generate_recommendations(analysis_data, user_data)
            }
            
            return report
            
        except Exception as e:
            logger.error(f"종합 보고서 생성 실패: {e}")
            return {"error": f"종합 보고서 생성 중 오류가 발생했습니다: {str(e)}"}
    
    def _generate_recommendations(self, analysis_data: List[Dict], user_data: List[Dict]) -> List[str]:
        """추천사항 생성"""
        recommendations = []
        
        if not analysis_data:
            return ["분석 데이터가 부족합니다. 더 많은 데이터를 수집해주세요."]
        
        df = pd.DataFrame(analysis_data)
        
        # 처리 시간 최적화 추천
        if 'processing_time' in df.columns:
            avg_processing_time = df['processing_time'].mean()
            if avg_processing_time > 5:
                recommendations.append("처리 시간이 평균 5초를 초과합니다. 시스템 성능 최적화를 고려해주세요.")
        
        # 진실성 점수 개선 추천
        if 'truth_score' in df.columns:
            avg_truth_score = df['truth_score'].mean()
            if avg_truth_score < 0.5:
                recommendations.append("평균 진실성 점수가 낮습니다. 분석 알고리즘 개선을 고려해주세요.")
        
        # 신뢰도 개선 추천
        if 'confidence_score' in df.columns:
            avg_confidence = df['confidence_score'].mean()
            if avg_confidence < 0.6:
                recommendations.append("평균 신뢰도가 낮습니다. 모델 정확도 개선을 고려해주세요.")
        
        # 사용자 경험 개선 추천
        if user_data:
            user_df = pd.DataFrame(user_data)
            if 'user_id' in user_df.columns:
                unique_users = user_df['user_id'].nunique()
                total_analyses = len(user_df)
                if unique_users > 0 and total_analyses / unique_users < 2:
                    recommendations.append("사용자당 평균 분석 수가 낮습니다. 사용자 참여도 향상 방안을 고려해주세요.")
        
        if not recommendations:
            recommendations.append("시스템이 정상적으로 작동하고 있습니다.")
        
        return recommendations

# 전역 고급 분석 엔진 인스턴스
advanced_analysis_engine = AdvancedAnalysisEngine()

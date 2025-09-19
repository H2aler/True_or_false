"""
데이터베이스 설정 및 연결 관리
PostgreSQL과 Redis를 사용한 데이터 저장 및 캐싱
"""

import os
import psycopg2
import redis
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Float, Boolean, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from typing import Optional, Dict, Any, List
import logging

# 로깅 설정
logger = logging.getLogger(__name__)

# 데이터베이스 설정
DATABASE_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': os.getenv('DB_PORT', '5432'),
    'database': os.getenv('DB_NAME', 'ai_truth_db'),
    'user': os.getenv('DB_USER', 'ai_truth_user'),
    'password': os.getenv('DB_PASSWORD', 'ai_truth_password')
}

# Redis 설정
REDIS_CONFIG = {
    'host': os.getenv('REDIS_HOST', 'localhost'),
    'port': int(os.getenv('REDIS_PORT', '6379')),
    'db': int(os.getenv('REDIS_DB', '0')),
    'decode_responses': True
}

# SQLAlchemy 설정
Base = declarative_base()

class AnalysisRecord(Base):
    """분석 기록 테이블"""
    __tablename__ = 'analysis_records'
    
    id = Column(Integer, primary_key=True)
    statement = Column(Text, nullable=False)
    context = Column(Text)
    analysis_mode = Column(String(50), default='all')
    user_id = Column(String(100))
    session_id = Column(String(100))
    
    # 분석 결과
    truth_score = Column(Float)
    confidence_score = Column(Float)
    analysis_result = Column(JSON)
    
    # 메타데이터
    created_at = Column(DateTime, default=datetime.utcnow)
    processing_time = Column(Float)
    ip_address = Column(String(45))
    user_agent = Column(Text)
    
    # AI 자체 분석 결과
    ai_self_analysis = Column(JSON)
    ai_confidence = Column(Float)
    
    # 웹 연구 결과
    web_research_result = Column(JSON)
    fact_verification = Column(JSON)
    
    # 일관성 분석 결과
    consistency_score = Column(Float)
    consistency_analysis = Column(JSON)

class UserSession(Base):
    """사용자 세션 테이블"""
    __tablename__ = 'user_sessions'
    
    id = Column(Integer, primary_key=True)
    session_id = Column(String(100), unique=True, nullable=False)
    user_id = Column(String(100))
    ip_address = Column(String(45))
    user_agent = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_activity = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    # 세션 메타데이터
    total_analyses = Column(Integer, default=0)
    total_processing_time = Column(Float, default=0.0)
    preferred_analysis_mode = Column(String(50), default='all')

class SystemMetrics(Base):
    """시스템 메트릭 테이블"""
    __tablename__ = 'system_metrics'
    
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    metric_name = Column(String(100), nullable=False)
    metric_value = Column(Float, nullable=False)
    metric_type = Column(String(50))  # counter, gauge, histogram
    tags = Column(JSON)

class DatabaseManager:
    """데이터베이스 관리 클래스"""
    
    def __init__(self):
        self.engine = None
        self.Session = None
        self.redis_client = None
        self._connect()
    
    def _connect(self):
        """데이터베이스 연결 설정"""
        try:
            # PostgreSQL 연결
            connection_string = f"postgresql://{DATABASE_CONFIG['user']}:{DATABASE_CONFIG['password']}@{DATABASE_CONFIG['host']}:{DATABASE_CONFIG['port']}/{DATABASE_CONFIG['database']}"
            self.engine = create_engine(connection_string, pool_pre_ping=True, pool_recycle=300)
            self.Session = sessionmaker(bind=self.engine)
            
            # 테이블 생성
            Base.metadata.create_all(self.engine)
            
            # Redis 연결
            self.redis_client = redis.Redis(**REDIS_CONFIG)
            self.redis_client.ping()  # 연결 테스트
            
            logger.info("데이터베이스 연결 성공")
            
        except Exception as e:
            logger.error(f"데이터베이스 연결 실패: {e}")
            raise
    
    def get_session(self):
        """데이터베이스 세션 반환"""
        return self.Session()
    
    def get_redis(self):
        """Redis 클라이언트 반환"""
        return self.redis_client
    
    def save_analysis_record(self, analysis_data: Dict[str, Any]) -> int:
        """분석 기록 저장"""
        try:
            session = self.get_session()
            record = AnalysisRecord(**analysis_data)
            session.add(record)
            session.commit()
            record_id = record.id
            session.close()
            
            # Redis에 캐시 저장
            self.redis_client.setex(
                f"analysis:{record_id}", 
                3600,  # 1시간 TTL
                str(record_id)
            )
            
            return record_id
            
        except Exception as e:
            logger.error(f"분석 기록 저장 실패: {e}")
            raise
    
    def get_analysis_record(self, record_id: int) -> Optional[AnalysisRecord]:
        """분석 기록 조회"""
        try:
            session = self.get_session()
            record = session.query(AnalysisRecord).filter_by(id=record_id).first()
            session.close()
            return record
            
        except Exception as e:
            logger.error(f"분석 기록 조회 실패: {e}")
            return None
    
    def get_recent_analyses(self, limit: int = 10) -> List[AnalysisRecord]:
        """최근 분석 기록 조회"""
        try:
            session = self.get_session()
            records = session.query(AnalysisRecord).order_by(AnalysisRecord.created_at.desc()).limit(limit).all()
            session.close()
            return records
            
        except Exception as e:
            logger.error(f"최근 분석 기록 조회 실패: {e}")
            return []
    
    def save_user_session(self, session_data: Dict[str, Any]) -> int:
        """사용자 세션 저장"""
        try:
            session = self.get_session()
            user_session = UserSession(**session_data)
            session.add(user_session)
            session.commit()
            session_id = user_session.id
            session.close()
            return session_id
            
        except Exception as e:
            logger.error(f"사용자 세션 저장 실패: {e}")
            raise
    
    def update_user_session(self, session_id: str, update_data: Dict[str, Any]):
        """사용자 세션 업데이트"""
        try:
            session = self.get_session()
            user_session = session.query(UserSession).filter_by(session_id=session_id).first()
            if user_session:
                for key, value in update_data.items():
                    setattr(user_session, key, value)
                user_session.last_activity = datetime.utcnow()
                session.commit()
            session.close()
            
        except Exception as e:
            logger.error(f"사용자 세션 업데이트 실패: {e}")
    
    def save_system_metric(self, metric_name: str, metric_value: float, metric_type: str = "gauge", tags: Dict = None):
        """시스템 메트릭 저장"""
        try:
            session = self.get_session()
            metric = SystemMetrics(
                metric_name=metric_name,
                metric_value=metric_value,
                metric_type=metric_type,
                tags=tags or {}
            )
            session.add(metric)
            session.commit()
            session.close()
            
        except Exception as e:
            logger.error(f"시스템 메트릭 저장 실패: {e}")
    
    def get_system_metrics(self, metric_name: str, hours: int = 24) -> List[SystemMetrics]:
        """시스템 메트릭 조회"""
        try:
            session = self.get_session()
            from datetime import timedelta
            since = datetime.utcnow() - timedelta(hours=hours)
            metrics = session.query(SystemMetrics).filter(
                SystemMetrics.metric_name == metric_name,
                SystemMetrics.timestamp >= since
            ).order_by(SystemMetrics.timestamp.desc()).all()
            session.close()
            return metrics
            
        except Exception as e:
            logger.error(f"시스템 메트릭 조회 실패: {e}")
            return []
    
    def cache_set(self, key: str, value: Any, ttl: int = 3600):
        """Redis 캐시 저장"""
        try:
            if isinstance(value, (dict, list)):
                value = str(value)
            self.redis_client.setex(key, ttl, value)
        except Exception as e:
            logger.error(f"캐시 저장 실패: {e}")
    
    def cache_get(self, key: str) -> Optional[str]:
        """Redis 캐시 조회"""
        try:
            return self.redis_client.get(key)
        except Exception as e:
            logger.error(f"캐시 조회 실패: {e}")
            return None
    
    def cache_delete(self, key: str):
        """Redis 캐시 삭제"""
        try:
            self.redis_client.delete(key)
        except Exception as e:
            logger.error(f"캐시 삭제 실패: {e}")
    
    def get_statistics(self) -> Dict[str, Any]:
        """시스템 통계 조회"""
        try:
            session = self.get_session()
            
            # 총 분석 수
            total_analyses = session.query(AnalysisRecord).count()
            
            # 오늘 분석 수
            from datetime import date
            today = date.today()
            today_analyses = session.query(AnalysisRecord).filter(
                AnalysisRecord.created_at >= today
            ).count()
            
            # 평균 처리 시간
            avg_processing_time = session.query(AnalysisRecord.processing_time).filter(
                AnalysisRecord.processing_time.isnot(None)
            ).all()
            avg_time = sum([t[0] for t in avg_processing_time]) / len(avg_processing_time) if avg_processing_time else 0
            
            # 활성 세션 수
            active_sessions = session.query(UserSession).filter(
                UserSession.is_active == True
            ).count()
            
            session.close()
            
            return {
                'total_analyses': total_analyses,
                'today_analyses': today_analyses,
                'average_processing_time': avg_time,
                'active_sessions': active_sessions,
                'timestamp': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"통계 조회 실패: {e}")
            return {}

# 전역 데이터베이스 매니저 인스턴스
db_manager = DatabaseManager()

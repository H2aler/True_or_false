#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI 진실성 탐지기 실시간 알림 시스템
우선순위 2-4: 실시간 알림 시스템 구축

작성일: 2025-09-19
버전: 2.0.0-enterprise
"""

from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit, join_room, leave_room, disconnect
from datetime import datetime
import json
import logging
import threading
import time
from collections import defaultdict, deque

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NotificationManager:
    """실시간 알림 관리자"""
    
    def __init__(self, socketio):
        self.socketio = socketio
        self.connected_users = {}  # 연결된 사용자 관리
        self.user_rooms = defaultdict(set)  # 사용자별 방 관리
        self.notification_history = deque(maxlen=1000)  # 알림 히스토리
        self.analysis_queue = deque()  # 분석 대기열
        self.is_processing = False
        
        # 알림 타입 정의
        self.notification_types = {
            'analysis_start': '분석 시작',
            'analysis_complete': '분석 완료',
            'lie_detected': '거짓말 탐지',
            'high_confidence': '높은 신뢰도',
            'low_confidence': '낮은 신뢰도',
            'system_alert': '시스템 알림',
            'error': '오류 발생'
        }
        
        # 분석 처리 스레드 시작
        self.start_analysis_processor()
        
        logger.info("실시간 알림 시스템이 초기화되었습니다.")
    
    def start_analysis_processor(self):
        """분석 처리 스레드 시작"""
        def process_analysis():
            while True:
                if self.analysis_queue and not self.is_processing:
                    self.is_processing = True
                    analysis_data = self.analysis_queue.popleft()
                    self.process_analysis_data(analysis_data)
                    self.is_processing = False
                time.sleep(0.1)  # 100ms 간격으로 체크
        
        thread = threading.Thread(target=process_analysis, daemon=True)
        thread.start()
    
    def add_analysis_to_queue(self, analysis_data):
        """분석 데이터를 대기열에 추가"""
        self.analysis_queue.append(analysis_data)
        logger.info(f"분석 데이터가 대기열에 추가되었습니다: {analysis_data.get('statement', 'Unknown')[:50]}...")
    
    def process_analysis_data(self, analysis_data):
        """분석 데이터 처리 및 알림 발송"""
        try:
            statement = analysis_data.get('statement', '')
            truth_percentage = analysis_data.get('truth_percentage', 0)
            confidence_score = analysis_data.get('confidence_score', 0)
            detected_lies = analysis_data.get('detected_lies', [])
            
            # 분석 시작 알림
            self.send_notification('analysis_start', {
                'message': f'문장 분석을 시작합니다: {statement[:50]}...',
                'statement': statement,
                'timestamp': datetime.now().isoformat()
            })
            
            # 분석 결과에 따른 알림
            if truth_percentage < 30:
                self.send_notification('lie_detected', {
                    'message': f'거짓말이 탐지되었습니다! (진실성: {truth_percentage:.1f}%)',
                    'statement': statement,
                    'truth_percentage': truth_percentage,
                    'detected_lies': detected_lies,
                    'timestamp': datetime.now().isoformat()
                })
            elif truth_percentage > 90:
                self.send_notification('high_confidence', {
                    'message': f'높은 신뢰도로 진실한 문장입니다. (진실성: {truth_percentage:.1f}%)',
                    'statement': statement,
                    'truth_percentage': truth_percentage,
                    'confidence_score': confidence_score,
                    'timestamp': datetime.now().isoformat()
                })
            elif truth_percentage < 50:
                self.send_notification('low_confidence', {
                    'message': f'낮은 신뢰도입니다. (진실성: {truth_percentage:.1f}%)',
                    'statement': statement,
                    'truth_percentage': truth_percentage,
                    'confidence_score': confidence_score,
                    'timestamp': datetime.now().isoformat()
                })
            
            # 분석 완료 알림
            self.send_notification('analysis_complete', {
                'message': f'문장 분석이 완료되었습니다.',
                'statement': statement,
                'truth_percentage': truth_percentage,
                'confidence_score': confidence_score,
                'processing_time': analysis_data.get('processing_time', 0),
                'timestamp': datetime.now().isoformat()
            })
            
        except Exception as e:
            logger.error(f"분석 데이터 처리 중 오류: {str(e)}")
            self.send_notification('error', {
                'message': f'분석 처리 중 오류가 발생했습니다: {str(e)}',
                'timestamp': datetime.now().isoformat()
            })
    
    def send_notification(self, notification_type, data):
        """알림 발송"""
        notification = {
            'id': f"notif_{int(time.time() * 1000)}",
            'type': notification_type,
            'title': self.notification_types.get(notification_type, '알림'),
            'data': data,
            'timestamp': datetime.now().isoformat()
        }
        
        # 알림 히스토리에 추가
        self.notification_history.append(notification)
        
        # 모든 연결된 사용자에게 브로드캐스트
        self.socketio.emit('notification', notification, namespace='/')
        
        # 특정 방에만 발송 (예: 관리자 방)
        if notification_type in ['system_alert', 'error']:
            self.socketio.emit('notification', notification, room='admin', namespace='/')
        
        logger.info(f"알림 발송: {notification_type} - {data.get('message', 'No message')}")
    
    def send_to_user(self, username, notification_type, data):
        """특정 사용자에게 알림 발송"""
        notification = {
            'id': f"notif_{int(time.time() * 1000)}",
            'type': notification_type,
            'title': self.notification_types.get(notification_type, '알림'),
            'data': data,
            'timestamp': datetime.now().isoformat()
        }
        
        # 사용자가 연결되어 있으면 발송
        if username in self.connected_users:
            self.socketio.emit('notification', notification, room=username, namespace='/')
            logger.info(f"사용자 {username}에게 알림 발송: {notification_type}")
    
    def get_notification_history(self, limit=50):
        """알림 히스토리 조회"""
        return list(self.notification_history)[-limit:]

# 전역 알림 관리자 인스턴스
notification_manager = None

def create_realtime_routes(app, socketio):
    """실시간 알림 관련 라우트 생성"""
    global notification_manager
    notification_manager = NotificationManager(socketio)
    
    @app.route('/api/notifications/history', methods=['GET'])
    def get_notification_history():
        """알림 히스토리 조회"""
        try:
            limit = request.args.get('limit', 50, type=int)
            history = notification_manager.get_notification_history(limit)
            
            return jsonify({
                'success': True,
                'notifications': history,
                'total_count': len(history),
                'timestamp': datetime.now().isoformat()
            })
            
        except Exception as e:
            logger.error(f"알림 히스토리 조회 중 오류: {str(e)}")
            return jsonify({
                'error': f'알림 히스토리 조회 중 오류가 발생했습니다: {str(e)}'
            }), 500
    
    @app.route('/api/notifications/send', methods=['POST'])
    def send_custom_notification():
        """사용자 정의 알림 발송"""
        try:
            data = request.get_json()
            notification_type = data.get('type', 'system_alert')
            message = data.get('message', '')
            target_user = data.get('target_user', None)
            
            if not message:
                return jsonify({
                    'error': '알림 메시지를 입력해주세요.'
                }), 400
            
            notification_data = {
                'message': message,
                'custom': True,
                'timestamp': datetime.now().isoformat()
            }
            
            if target_user:
                notification_manager.send_to_user(target_user, notification_type, notification_data)
            else:
                notification_manager.send_notification(notification_type, notification_data)
            
            return jsonify({
                'success': True,
                'message': '알림이 성공적으로 발송되었습니다.',
                'timestamp': datetime.now().isoformat()
            })
            
        except Exception as e:
            logger.error(f"알림 발송 중 오류: {str(e)}")
            return jsonify({
                'error': f'알림 발송 중 오류가 발생했습니다: {str(e)}'
            }), 500

def create_socketio_handlers(socketio):
    """SocketIO 이벤트 핸들러 생성"""
    
    @socketio.on('connect')
    def handle_connect():
        """클라이언트 연결 처리"""
        logger.info(f"클라이언트 연결됨: {request.sid}")
        
        # 연결된 사용자 정보 저장
        notification_manager.connected_users[request.sid] = {
            'connected_at': datetime.now().isoformat(),
            'ip': request.remote_addr
        }
        
        emit('connected', {
            'message': '서버에 연결되었습니다.',
            'timestamp': datetime.now().isoformat()
        })
    
    @socketio.on('disconnect')
    def handle_disconnect():
        """클라이언트 연결 해제 처리"""
        logger.info(f"클라이언트 연결 해제됨: {request.sid}")
        
        # 연결된 사용자 정보 제거
        if request.sid in notification_manager.connected_users:
            del notification_manager.connected_users[request.sid]
        
        # 사용자가 속한 모든 방에서 제거
        for room in list(notification_manager.user_rooms.get(request.sid, set())):
            leave_room(room)
            notification_manager.user_rooms[request.sid].discard(room)
    
    @socketio.on('join_room')
    def handle_join_room(data):
        """방 참가 처리"""
        room = data.get('room', 'general')
        join_room(room)
        notification_manager.user_rooms[request.sid].add(room)
        
        emit('joined_room', {
            'room': room,
            'message': f'방 {room}에 참가했습니다.',
            'timestamp': datetime.now().isoformat()
        })
        
        logger.info(f"클라이언트 {request.sid}가 방 {room}에 참가했습니다.")
    
    @socketio.on('leave_room')
    def handle_leave_room(data):
        """방 나가기 처리"""
        room = data.get('room', 'general')
        leave_room(room)
        notification_manager.user_rooms[request.sid].discard(room)
        
        emit('left_room', {
            'room': room,
            'message': f'방 {room}에서 나갔습니다.',
            'timestamp': datetime.now().isoformat()
        })
        
        logger.info(f"클라이언트 {request.sid}가 방 {room}에서 나갔습니다.")
    
    @socketio.on('subscribe_analysis')
    def handle_subscribe_analysis():
        """분석 알림 구독"""
        join_room('analysis')
        notification_manager.user_rooms[request.sid].add('analysis')
        
        emit('subscribed', {
            'type': 'analysis',
            'message': '분석 알림을 구독했습니다.',
            'timestamp': datetime.now().isoformat()
        })
        
        logger.info(f"클라이언트 {request.sid}가 분석 알림을 구독했습니다.")
    
    @socketio.on('subscribe_admin')
    def handle_subscribe_admin():
        """관리자 알림 구독"""
        join_room('admin')
        notification_manager.user_rooms[request.sid].add('admin')
        
        emit('subscribed', {
            'type': 'admin',
            'message': '관리자 알림을 구독했습니다.',
            'timestamp': datetime.now().isoformat()
        })
        
        logger.info(f"클라이언트 {request.sid}가 관리자 알림을 구독했습니다.")
    
    @socketio.on('get_status')
    def handle_get_status():
        """서버 상태 조회"""
        status = {
            'connected_users': len(notification_manager.connected_users),
            'notification_history_count': len(notification_manager.notification_history),
            'analysis_queue_size': len(notification_manager.analysis_queue),
            'is_processing': notification_manager.is_processing,
            'timestamp': datetime.now().isoformat()
        }
        
        emit('status', status)
        logger.info(f"클라이언트 {request.sid}가 서버 상태를 조회했습니다.")

def add_analysis_notification(analysis_data):
    """분석 데이터를 알림 시스템에 추가"""
    if notification_manager:
        notification_manager.add_analysis_to_queue(analysis_data)

if __name__ == '__main__':
    # 테스트용 Flask 앱
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'test_secret_key'
    
    # SocketIO 초기화
    socketio = SocketIO(app, cors_allowed_origins="*")
    
    # 실시간 라우트 생성
    create_realtime_routes(app, socketio)
    
    # SocketIO 핸들러 생성
    create_socketio_handlers(socketio)
    
    print("🚀 실시간 알림 시스템 테스트 서버 시작")
    print("=" * 50)
    print("📡 WebSocket: ws://localhost:5003/socket.io/")
    print("📚 알림 히스토리: GET /api/notifications/history")
    print("📤 알림 발송: POST /api/notifications/send")
    print("=" * 50)
    
    socketio.run(app, debug=True, host='0.0.0.0', port=5003)

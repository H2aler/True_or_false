#!/usr/bin/env python3
"""
AI 진실성 탐지기 변경사항 추적기
코드 변경 시 자동으로 로그를 생성하고 관리합니다.
"""

import os
import json
import hashlib
from datetime import datetime
from typing import Dict, List, Optional
import subprocess
import sys

class ChangeTracker:
    """변경사항 추적 클래스"""
    
    def __init__(self, project_root: str = "."):
        self.project_root = project_root
        self.logs_dir = os.path.join(project_root, "logs")
        self.version_log = os.path.join(self.logs_dir, "version_log.md")
        self.change_history = os.path.join(self.logs_dir, "change_history.json")
        
        # 추적할 파일들
        self.tracked_files = [
            "ai_truth_detector.py",
            "app.py",
            "templates/base.html",
            "templates/index.html",
            "templates/dashboard.html",
            "requirements.txt",
            "test_truth_detector.py",
            "quick_test.py",
            "logs/version_log.md",
            "logs/change_tracker.py",
            "logs/README.md",
            "logs/usage_guide.md",
            "system_exe_method.md"
        ]
        
        self._ensure_logs_dir()
        self._load_change_history()
    
    def _ensure_logs_dir(self):
        """로그 디렉토리 생성"""
        if not os.path.exists(self.logs_dir):
            os.makedirs(self.logs_dir)
    
    def _load_change_history(self):
        """변경 히스토리 로드"""
        if os.path.exists(self.change_history):
            with open(self.change_history, 'r', encoding='utf-8') as f:
                self.history = json.load(f)
        else:
            self.history = {
                "versions": [],
                "file_hashes": {},
                "last_check": None
            }
    
    def _save_change_history(self):
        """변경 히스토리 저장"""
        with open(self.change_history, 'w', encoding='utf-8') as f:
            json.dump(self.history, f, indent=2, ensure_ascii=False)
    
    def _get_file_hash(self, file_path: str) -> Optional[str]:
        """파일의 해시값 계산"""
        full_path = os.path.join(self.project_root, file_path)
        if not os.path.exists(full_path):
            return None
        
        try:
            with open(full_path, 'rb') as f:
                content = f.read()
                return hashlib.md5(content).hexdigest()
        except Exception as e:
            print(f"파일 해시 계산 오류 {file_path}: {e}")
            return None
    
    def _get_git_status(self) -> Dict[str, str]:
        """Git 상태 확인"""
        try:
            result = subprocess.run(['git', 'status', '--porcelain'], 
                                  capture_output=True, text=True, cwd=self.project_root)
            if result.returncode == 0:
                changes = {}
                for line in result.stdout.strip().split('\n'):
                    if line:
                        status = line[:2]
                        filename = line[3:]
                        changes[filename] = status
                return changes
        except Exception:
            pass
        return {}
    
    def check_changes(self) -> List[Dict]:
        """변경사항 확인"""
        changes = []
        git_changes = self._get_git_status()
        
        for file_path in self.tracked_files:
            current_hash = self._get_file_hash(file_path)
            previous_hash = self.history["file_hashes"].get(file_path)
            
            if current_hash and current_hash != previous_hash:
                git_status = git_changes.get(file_path, "??")
                
                change_info = {
                    "file": file_path,
                    "previous_hash": previous_hash,
                    "current_hash": current_hash,
                    "git_status": git_status,
                    "timestamp": datetime.now().isoformat(),
                    "size": os.path.getsize(os.path.join(self.project_root, file_path)) if os.path.exists(os.path.join(self.project_root, file_path)) else 0
                }
                changes.append(change_info)
                
                # 해시 업데이트
                self.history["file_hashes"][file_path] = current_hash
        
        self.history["last_check"] = datetime.now().isoformat()
        self._save_change_history()
        
        return changes
    
    def log_change(self, version: str, description: str, changes: List[Dict], 
                   reason: str = "", test_results: str = ""):
        """변경사항을 버전 로그에 기록"""
        
        version_entry = {
            "version": version,
            "date": datetime.now().strftime("%Y-%m-%d"),
            "description": description,
            "changes": changes,
            "reason": reason,
            "test_results": test_results,
            "timestamp": datetime.now().isoformat()
        }
        
        # JSON 히스토리에 추가
        self.history["versions"].append(version_entry)
        self._save_change_history()
        
        # Markdown 로그에 추가
        self._update_version_log(version_entry)
        
        print(f"✅ 버전 {version} 변경사항이 로그에 기록되었습니다.")
    
    def _update_version_log(self, version_entry: Dict):
        """버전 로그 Markdown 파일 업데이트"""
        
        # 새 버전 섹션 생성
        version_section = f"""
### {version_entry['version']} - {version_entry['date']}
**상태**: ✅ 완료
**변경사항**:
{version_entry['description']}

"""
        
        # 변경된 파일들 나열
        if version_entry['changes']:
            version_section += "**수정된 파일**:\n"
            for change in version_entry['changes']:
                version_section += f"- `{change['file']}`\n"
            version_section += "\n"
        
        # 변경 이유
        if version_entry['reason']:
            version_section += f"**이유**: \n{version_entry['reason']}\n\n"
        
        # 테스트 결과
        if version_entry['test_results']:
            version_section += f"**테스트 결과**:\n{version_entry['test_results']}\n\n"
        
        version_section += "---\n\n"
        
        # 현재 상태 업데이트
        current_status = f"""
## 🔍 현재 상태
- **최신 버전**: {version_entry['version']}
- **마지막 업데이트**: {version_entry['date']}
- **다음 예정 작업**: 사용자 피드백 반영, 추가 기능 개발

---
"""
        
        # 파일 읽기
        if os.path.exists(self.version_log):
            with open(self.version_log, 'r', encoding='utf-8') as f:
                content = f.read()
        else:
            content = ""
        
        # 현재 상태 섹션 찾아서 교체
        if "## 🔍 현재 상태" in content:
            # 기존 현재 상태 섹션 제거
            parts = content.split("## 🔍 현재 상태")
            if len(parts) > 1:
                # 현재 상태 이후의 내용도 제거
                before_status = parts[0]
                after_status_parts = parts[1].split("---")
                if len(after_status_parts) > 1:
                    after_status = after_status_parts[-1]
                else:
                    after_status = ""
                
                # 새 내용으로 재구성
                content = before_status + version_section + current_status + after_status
            else:
                content += version_section + current_status
        else:
            content += version_section + current_status
        
        # 파일 쓰기
        with open(self.version_log, 'w', encoding='utf-8') as f:
            f.write(content)
    
    def get_version_history(self) -> List[Dict]:
        """버전 히스토리 반환"""
        return self.history.get("versions", [])
    
    def get_file_changes(self, file_path: str) -> List[Dict]:
        """특정 파일의 변경 히스토리 반환"""
        changes = []
        for version in self.history.get("versions", []):
            for change in version.get("changes", []):
                if change["file"] == file_path:
                    changes.append({
                        "version": version["version"],
                        "date": version["date"],
                        "change": change
                    })
        return changes
    
    def generate_report(self) -> str:
        """변경사항 리포트 생성"""
        changes = self.check_changes()
        
        if not changes:
            return "📋 변경사항이 없습니다."
        
        report = f"📋 변경사항 리포트 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        report += "=" * 50 + "\n\n"
        
        for change in changes:
            report += f"📁 {change['file']}\n"
            report += f"   상태: {change['git_status']}\n"
            report += f"   크기: {change['size']} bytes\n"
            report += f"   시간: {change['timestamp']}\n\n"
        
        return report

def main():
    """메인 함수"""
    tracker = ChangeTracker()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "check":
            changes = tracker.check_changes()
            if changes:
                print(tracker.generate_report())
            else:
                print("📋 변경사항이 없습니다.")
        
        elif command == "log" and len(sys.argv) >= 4:
            version = sys.argv[2]
            description = sys.argv[3]
            reason = sys.argv[4] if len(sys.argv) > 4 else ""
            
            changes = tracker.check_changes()
            tracker.log_change(version, description, changes, reason)
        
        elif command == "history":
            history = tracker.get_version_history()
            for version in history:
                print(f"v{version['version']} - {version['date']}: {version['description']}")
        
        else:
            print("사용법:")
            print("  python change_tracker.py check                    # 변경사항 확인")
            print("  python change_tracker.py log <version> <desc> [reason]  # 변경사항 로그")
            print("  python change_tracker.py history                 # 버전 히스토리")
    else:
        # 기본: 변경사항 확인
        changes = tracker.check_changes()
        print(tracker.generate_report())

if __name__ == "__main__":
    main()

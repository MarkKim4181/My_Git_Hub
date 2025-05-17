import os
import sys
import subprocess
import shutil

print("========== 이미지 텍스트 추출기 EXE 빌드 스크립트 ==========")

# 필요한 패키지 설치 확인
print("1. 필요한 패키지 설치 중...")
subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

# PyInstaller로 EXE 파일 생성
print("2. EXE 파일 생성 중...")
subprocess.run([
    "pyinstaller",
    "--name=이미지_텍스트_추출기",
    "--icon=NONE",
    "--windowed",  # GUI 애플리케이션
    "--noconfirm",  # 기존 폴더 덮어쓰기
    "--add-data=C:/Program Files/Tesseract-OCR;Tesseract-OCR/",  # Tesseract 포함
    "image_text_extractor.py"
])

print("3. 빌드 완료!")
print("\n실행 파일 경로: dist/이미지_텍스트_추출기/이미지_텍스트_추출기.exe")
print("\n※ 주의: 이 실행 파일을 사용하려면 Tesseract-OCR이 설치되어 있어야 합니다.")
print("1. Tesseract-OCR이 설치되지 않은 경우: https://github.com/UB-Mannheim/tesseract/wiki 에서 다운로드하세요.")
print("2. 설치 시 '한국어' 언어팩을 반드시 선택하세요.")
print("================================================================") 
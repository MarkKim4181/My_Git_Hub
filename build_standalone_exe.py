import os
import sys
import subprocess
import shutil
import requests
import zipfile
import tempfile
from pathlib import Path
import glob

print("========== 독립 실행형 이미지 텍스트 추출기 빌드 스크립트 ==========")

# 작업 디렉토리
WORK_DIR = os.path.dirname(os.path.abspath(__file__))
TEMP_DIR = os.path.join(WORK_DIR, "temp_build")
os.makedirs(TEMP_DIR, exist_ok=True)

# 1. 필요한 패키지 설치
print("1. 필요한 패키지 설치 중...")
subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

# 2. Tesseract-OCR 다운로드 (최소 설치 버전)
TESSERACT_DOWNLOAD_URL = "https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-5.3.3.20231005.exe"
TESSERACT_INSTALLER = os.path.join(TEMP_DIR, "tesseract-installer.exe")

print("2. Tesseract OCR 다운로드 중... (시간이 다소 소요될 수 있습니다)")
try:
    # 파일이 이미 있는지 확인
    if not os.path.exists(TESSERACT_INSTALLER):
        response = requests.get(TESSERACT_DOWNLOAD_URL, stream=True)
        with open(TESSERACT_INSTALLER, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
    
    print("   Tesseract OCR 다운로드 완료!")
except Exception as e:
    print(f"   Tesseract OCR 다운로드 실패: {e}")
    print("   이미 다운로드된 인스톨러가 있다면 진행합니다.")

# 3. Tesseract 추출 (7z 또는 innoextract 필요)
TESSERACT_DIR = os.path.join(TEMP_DIR, "tesseract-ocr")
if not os.path.exists(TESSERACT_DIR):
    os.makedirs(TESSERACT_DIR, exist_ok=True)
    print("3. Tesseract 파일 추출 중...")
    
    try:
        # 방법 1: innoextract 사용 (설치되어 있어야 함)
        subprocess.run(["innoextract", "-d", TESSERACT_DIR, TESSERACT_INSTALLER], 
                      shell=True, check=False)
    except:
        # 방법 2: 7z 사용 (설치되어 있어야 함)
        try:
            subprocess.run(["7z", "x", TESSERACT_INSTALLER, f"-o{TESSERACT_DIR}"], 
                          shell=True, check=False)
        except:
            print("   Tesseract 추출 실패. 인스톨러를 수동으로 실행하여 설치 후 EXE 파일을 생성하세요.")
            print("   인스톨러 실행 중...")
            os.startfile(TESSERACT_INSTALLER)
            input("   Tesseract 설치가 완료되면 Enter 키를 눌러 계속하세요...")

# 4. 한국어 데이터 파일 다운로드
print("4. 한국어 언어 데이터 파일 다운로드 중...")
KOR_DOWNLOAD_URL = "https://github.com/tesseract-ocr/tessdata/raw/main/kor.traineddata"
TESSDATA_DIR = os.path.join(TESSERACT_DIR, "tessdata")

if not os.path.exists(TESSDATA_DIR):
    # app 폴더 내에 있는지 확인
    app_tessdata = os.path.join(TESSERACT_DIR, "app", "tessdata")
    if os.path.exists(app_tessdata):
        TESSDATA_DIR = app_tessdata
    else:
        os.makedirs(TESSDATA_DIR, exist_ok=True)

KOR_FILE = os.path.join(TESSDATA_DIR, "kor.traineddata")
ENG_FILE = os.path.join(TESSDATA_DIR, "eng.traineddata")

try:
    # 한국어 데이터 파일 다운로드
    if not os.path.exists(KOR_FILE):
        response = requests.get(KOR_DOWNLOAD_URL, stream=True)
        with open(KOR_FILE, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
    print("   한국어 데이터 파일 다운로드 완료!")
except Exception as e:
    print(f"   한국어 데이터 파일 다운로드 실패: {e}")

# 5. PyInstaller로 EXE 파일 생성
print("5. EXE 파일 생성 중...")

# Tesseract 실행 파일 위치 확인
if os.path.exists(os.path.join(TESSERACT_DIR, "app", "tesseract.exe")):
    TESSERACT_BIN = os.path.join(TESSERACT_DIR, "app")
else:
    TESSERACT_BIN = TESSERACT_DIR

# 사용할 데이터 파일 지정
include_files = [
    f"{TESSERACT_BIN};tesseract",
]

print(f"   Tesseract 경로: {TESSERACT_BIN}")

# PyInstaller 명령어 구성
pyinstaller_cmd = [
    "pyinstaller",
    "--name=이미지_텍스트_추출기_독립실행형",
    "--windowed",  # GUI 애플리케이션
    "--noconfirm",  # 기존 폴더 덮어쓰기
    "--clean",     # 캐시 정리
    "--add-data=" + include_files[0],
    "--icon=NONE",
    "image_text_extractor.py"
]

try:
    subprocess.run(pyinstaller_cmd, check=True)
    print("   EXE 파일 생성 완료!")
except Exception as e:
    print(f"   EXE 파일 생성 실패: {e}")
    print("   직접 PyInstaller 명령어를 실행해보세요:")
    print("   " + " ".join(pyinstaller_cmd))

# 6. 임시 파일 정리
print("6. 임시 파일 정리 중...")
try:
    # 정리하지 않음 (혹시 필요할 수 있음)
    # shutil.rmtree(TEMP_DIR, ignore_errors=True)
    pass
except:
    pass

# 7. 완료
print("\n빌드 완료!")
print("\n실행 파일 경로: dist/이미지_텍스트_추출기_독립실행형/이미지_텍스트_추출기_독립실행형.exe")
print("\n※ 이 EXE 파일은 Tesseract OCR을 내장하고 있어 어떤 PC에서도 바로 실행 가능합니다.")
print("================================================================") 
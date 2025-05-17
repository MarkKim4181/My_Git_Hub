# 이미지 텍스트 추출기

클립보드에 복사된 이미지에서 한글 텍스트를 추출하는 프로그램입니다.

## 필수 요구사항

1. Python 3.7 이상
2. Tesseract-OCR 설치
   - Windows: https://github.com/UB-Mannheim/tesseract/wiki 에서 다운로드
   - 설치 시 "한국어" 언어팩 선택 필수

## 설치 방법

1. 필요한 패키지 설치:
```bash
pip install -r requirements.txt
```

2. Tesseract-OCR이 설치된 경로를 환경 변수에 추가하거나, 코드에서 경로 직접 지정:
```python
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```

## 사용 방법

1. 프로그램 실행:
```bash
python image_text_extractor.py
```

2. 텍스트를 추출하고 싶은 이미지를 복사(Ctrl+C)
3. "텍스트 추출하기" 버튼 클릭
4. 추출된 텍스트를 확인하고 필요한 경우 "결과 복사하기" 버튼으로 클립보드에 복사

## 주요 기능

- 클립보드 이미지에서 텍스트 추출
- 한글 텍스트 인식 지원
- 깔끔한 GUI 인터페이스
- 추출 결과 클립보드 복사 기능


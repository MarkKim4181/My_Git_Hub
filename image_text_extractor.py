import customtkinter as ctk
import tkinter as tk
from PIL import ImageGrab, Image, ImageTk
import pytesseract
import pyperclip
from tkinter import messagebox, filedialog
import io
import os
import sys
import traceback
import tempfile
import uuid

# Windows 클립보드 처리를 위한 추가 모듈
try:
    import win32clipboard
    from io import BytesIO
    WINDOWS_CLIPBOARD = True
except ImportError:
    WINDOWS_CLIPBOARD = False

# Tesseract OCR 경로 설정
def get_tesseract_path():
    # 1. 번들된 Tesseract 확인 (PyInstaller로 패키징된 경우)
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
        bundled_tesseract = os.path.join(base_path, 'Tesseract-OCR', 'tesseract.exe')
        if os.path.exists(bundled_tesseract):
            return bundled_tesseract
    
    # 2. 기본 설치 경로 확인
    default_path = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    if os.path.exists(default_path):
        return default_path
    
    # 3. 다른 일반 설치 경로 확인
    other_path = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'
    if os.path.exists(other_path):
        return other_path
    
    # 4. PATH 환경 변수에서 찾기
    return 'tesseract'  # Tesseract가 PATH에 있으면 실행됨

# Tesseract 경로 설정
pytesseract.pytesseract.tesseract_cmd = get_tesseract_path()

class ImageTextExtractor(ctk.CTk):
    def __init__(self):
        super().__init__()

        # 윈도우 설정
        self.title("이미지 텍스트 추출기 - Dev by UnisCrew")
        self.geometry("600x550")
        
        # 테마 설정
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        # 이미지 경로
        self.image_path = None
        self.current_image = None
        self.temp_files = []  # 임시 파일 목록

        # Tesseract 확인
        self.check_tesseract()

        # GUI 구성요소 생성
        self.create_widgets()
        
        # 종료 시 임시 파일 삭제 이벤트 등록
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def check_tesseract(self):
        """Tesseract OCR 설치 확인"""
        try:
            # Tesseract 버전 확인
            version = pytesseract.get_tesseract_version()
            print(f"Tesseract OCR 버전: {version}")
            
            # 한국어 언어팩 확인
            langs = pytesseract.get_languages()
            if 'kor' not in langs:
                messagebox.showwarning(
                    "언어팩 경고", 
                    "Tesseract OCR에 한국어 언어팩이 설치되어 있지 않습니다.\n"
                    "https://github.com/UB-Mannheim/tesseract/wiki 에서 Tesseract를 다시 설치하고 '한국어' 언어팩을 선택하세요."
                )
        except Exception as e:
            messagebox.showerror(
                "Tesseract OCR 오류", 
                f"Tesseract OCR을 찾을 수 없거나 실행할 수 없습니다.\n"
                f"오류: {str(e)}\n\n"
                f"https://github.com/UB-Mannheim/tesseract/wiki 에서 Tesseract를 설치하세요."
            )

    def create_widgets(self):
        # 메인 프레임
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # 제목
        self.title_label = ctk.CTkLabel(
            self.main_frame,
            text="이미지에서 텍스트 추출",
            font=("Helvetica", 20, "bold")
        )
        self.title_label.pack(pady=5)

        # 개발자 정보
        self.dev_label = ctk.CTkLabel(
            self.main_frame,
            text="Dev by UnisCrew",
            font=("Helvetica", 12, "italic")
        )
        self.dev_label.pack(pady=0)

        # 버튼 프레임
        self.button_frame = ctk.CTkFrame(self.main_frame)
        self.button_frame.pack(fill="x", padx=10, pady=10)

        # 파일 선택 버튼
        self.file_button = ctk.CTkButton(
            self.button_frame,
            text="이미지 파일 선택",
            command=self.select_image_file,
            width=180,
            height=40
        )
        self.file_button.pack(side=tk.LEFT, padx=10)

        # 클립보드 설명
        self.instruction_label = ctk.CTkLabel(
            self.button_frame,
            text="또는",
            font=("Helvetica", 12)
        )
        self.instruction_label.pack(side=tk.LEFT, padx=5)

        # 클립보드 추출 버튼
        self.clipboard_button = ctk.CTkButton(
            self.button_frame,
            text="클립보드에서 추출",
            command=self.extract_from_clipboard,
            width=180,
            height=40
        )
        self.clipboard_button.pack(side=tk.LEFT, padx=10)

        # 파일 경로 표시
        self.path_frame = ctk.CTkFrame(self.main_frame)
        self.path_frame.pack(fill="x", padx=10, pady=(5, 10))
        
        self.path_label = ctk.CTkLabel(
            self.path_frame,
            text="선택된 파일: 없음",
            font=("Helvetica", 10),
            anchor="w"
        )
        self.path_label.pack(side=tk.LEFT, padx=10, fill="x", expand=True)

        # 결과 텍스트 영역
        self.result_text = ctk.CTkTextbox(
            self.main_frame,
            width=550,
            height=250,
            font=("Helvetica", 12)
        )
        self.result_text.pack(pady=10)

        # 하단 버튼 프레임
        self.bottom_frame = ctk.CTkFrame(self.main_frame)
        self.bottom_frame.pack(fill="x", padx=10, pady=10)
        
        # 복사 버튼
        self.copy_button = ctk.CTkButton(
            self.bottom_frame,
            text="결과 복사하기",
            command=self.copy_text,
            width=180,
            height=40
        )
        self.copy_button.pack(side=tk.LEFT, padx=10)
        
        # 지우기 버튼
        self.clear_button = ctk.CTkButton(
            self.bottom_frame,
            text="지우기",
            command=self.clear_text,
            width=180,
            height=40
        )
        self.clear_button.pack(side=tk.RIGHT, padx=10)

    def select_image_file(self):
        file_path = filedialog.askopenfilename(
            title="이미지 파일 선택",
            filetypes=[
                ("이미지 파일", "*.jpg *.jpeg *.png *.bmp *.gif"),
                ("JPEG 파일", "*.jpg *.jpeg"),
                ("PNG 파일", "*.png"),
                ("모든 파일", "*.*")
            ]
        )
        
        if file_path:
            self.image_path = file_path
            self.path_label.configure(text=f"선택된 파일: {os.path.basename(file_path)}")
            try:
                # 이미지 파일 열기
                with Image.open(self.image_path) as img:
                    # RGB로 변환 (중요)
                    if img.mode != 'RGB':
                        img = img.convert('RGB')
                    
                    # OCR 실행
                    text = pytesseract.image_to_string(img, lang='kor+eng')
                    
                    # 결과 표시
                    self.result_text.delete("1.0", tk.END)
                    self.result_text.insert("1.0", text.strip())
            except Exception as e:
                error_msg = f"이미지 처리 중 오류: {str(e)}\n{traceback.format_exc()}"
                print(error_msg)
                messagebox.showerror("오류", error_msg)
    
    def extract_from_clipboard(self):
        try:
            # 클립보드에서 파일 경로 확인
            clipboard_files = ImageGrab.grabclipboard()
            if isinstance(clipboard_files, list) and len(clipboard_files) > 0:
                # 파일이 복사된 경우
                try:
                    file_path = clipboard_files[0]
                    # 파일 확장자 확인
                    if any(file_path.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.bmp', '.gif']):
                        self.image_path = file_path
                        self.path_label.configure(text=f"선택된 파일: {os.path.basename(file_path)} (클립보드)")
                        
                        # 이미지 파일 열기 및 OCR 실행
                        self.process_image_file(file_path)
                        return
                except Exception as e:
                    print(f"클립보드 파일 처리 오류: {e}")
            
            # 일반 클립보드 이미지 처리
            img = ImageGrab.grabclipboard()
            if img and isinstance(img, Image.Image):
                # 임시 파일로 저장
                temp_file = self.save_clipboard_image(img)
                if temp_file:
                    # 임시 파일에서 처리
                    self.process_image_file(temp_file)
                    
                    # 파일 경로 초기화
                    self.image_path = None
                    self.path_label.configure(text="선택된 파일: 없음 (클립보드에서 추출)")
                    return
                
            # 클립보드에 이미지가 없거나 지원되지 않는 형식인 경우
            messagebox.showwarning("경고", "클립보드에서 인식 가능한 이미지를 찾을 수 없습니다.\n스크린샷을 캡처한 후 다시 시도하거나 이미지 파일을 직접 선택해주세요.")
            
        except Exception as e:
            error_msg = f"클립보드 처리 중 오류가 발생했습니다: {str(e)}\n{traceback.format_exc()}"
            print(error_msg)
            messagebox.showerror("오류", error_msg)
            
            # 오류 발생 시 권장사항 안내
            messagebox.showinfo("권장사항", 
                "다음 방법을 시도해보세요:\n\n"
                "1. 윈도우 스크린샷 도구(Win+Shift+S)로 캡처 후 바로 시도\n"
                "2. 이미지를 파일로 저장한 후 '이미지 파일 선택' 버튼 사용\n"
                "3. 이미지를 MS Paint 등에 붙여넣고 다시 복사 후 시도")
    
    def save_clipboard_image(self, img):
        """클립보드 이미지를 임시 파일로 저장"""
        try:
            # RGB로 변환
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # 임시 파일 경로 생성
            temp_dir = tempfile.gettempdir()
            temp_filename = f"clipboard_image_{uuid.uuid4().hex}.png"
            temp_path = os.path.join(temp_dir, temp_filename)
            
            # 이미지 저장
            img.save(temp_path, format="PNG")
            
            # 임시 파일 목록에 추가
            self.temp_files.append(temp_path)
            
            print(f"이미지를 임시 파일로 저장: {temp_path}")
            return temp_path
        except Exception as e:
            print(f"이미지 저장 오류: {e}")
            return None
    
    def process_image_file(self, file_path):
        """이미지 파일을 열어서 OCR 처리"""
        try:
            # 이미지 파일 열기
            with Image.open(file_path) as img:
                # RGB로 변환 (중요)
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # OCR 실행
                text = pytesseract.image_to_string(img, lang='kor+eng')
                
                # 결과 표시
                self.result_text.delete("1.0", tk.END)
                self.result_text.insert("1.0", text.strip())
        except Exception as e:
            error_msg = f"이미지 처리 중 오류: {str(e)}\n{traceback.format_exc()}"
            print(error_msg)
            messagebox.showerror("오류", error_msg)

    def copy_text(self):
        text = self.result_text.get("1.0", tk.END).strip()
        if text:
            pyperclip.copy(text)
            messagebox.showinfo("알림", "텍스트가 클립보드에 복사되었습니다!")
        else:
            messagebox.showwarning("경고", "복사할 텍스트가 없습니다!")
    
    def clear_text(self):
        self.result_text.delete("1.0", tk.END)
        self.image_path = None
        self.path_label.configure(text="선택된 파일: 없음")

    def on_closing(self):
        """프로그램 종료 시 임시 파일 삭제"""
        try:
            for temp_file in self.temp_files:
                if os.path.exists(temp_file):
                    os.remove(temp_file)
                    print(f"임시 파일 삭제: {temp_file}")
        except Exception as e:
            print(f"임시 파일 삭제 오류: {e}")
        finally:
            self.destroy()

if __name__ == "__main__":
    app = ImageTextExtractor()
    app.mainloop() 
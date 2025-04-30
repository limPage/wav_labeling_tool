import os
import json
import pygame
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
import sys
from datetime import datetime 

# 전역 상태
base_path = ""
data = []
labeled_data = []
labeled_map = {}
index = 0
trash_set = set()

# 오디오 초기화
pygame.mixer.init()

# GUI 시작
root = tk.Tk()
root.title("HJ Voice Labeling Tool")
root.geometry("800x370")
bg_color = "#abb3eb"
root.configure(bg=bg_color) 
# 아이콘 설정
# icon_path = os.path.join(os.path.dirname(__file__), "favicon.ico")
# if os.path.exists(icon_path):
#     root.iconbitmap(icon_path)
# 주피터
# icon_path = os.path.join(os.getcwd(), "favicon.ico")
# if os.path.exists(icon_path):
#     root.iconbitmap(icon_path)
# exe용
if hasattr(sys, '_MEIPASS'):
    icon_path = os.path.join(sys._MEIPASS, "favicon.ico")
else:
    icon_path = os.path.join(os.getcwd(), "favicon.ico")

if os.path.exists(icon_path):
    root.iconbitmap(icon_path)
    
# 위젯 선언
# audio_label = tk.Label(root, text="", font=("Arial", 12))
# stt_label = tk.Label(root, text="", font=("Arial", 16, "bold"), fg="blue")
# prev_label = tk.Label(root, text="", font=("Arial", 16, "bold"), fg="red")
entry = tk.Entry(root, font=("Arial", 14), width=50)
# 위젯 선언
progress_frame = tk.Frame(root, bg=bg_color)
# progress_label = tk.Label(progress_frame, text="진행 상황: 0%", font=("Arial", 10))
progress_bar = ttk.Progressbar(progress_frame, length=400, mode='determinate', style="custom.Horizontal.TProgressbar")

# 검색
jump_frame = tk.Frame(root, bg=bg_color)
jump_label = tk.Label(jump_frame, text="특정 번호 재생하기:", bg=bg_color)
jump_entry = tk.Entry(jump_frame, width=6, font=("Arial", 12))
jump_button = tk.Button(jump_frame, text="▶재생", command=lambda: jump_to_index())

#스타일 선언
style = ttk.Style()
style.theme_use("default")
style.configure("custom.Horizontal.TProgressbar", thickness=6) 

# 🗣 STT 텍스트 영역 (감지된 값)
stt_frame = tk.Frame(root, bg=bg_color)
stt_title = tk.Label(stt_frame, text="transcripts :", font=("Arial", 16), bg=bg_color)
stt_value = tk.Label(stt_frame, text="", font=("Arial", 16), fg="blue")

# 🔖 라벨 텍스트 영역
label_frame = tk.Frame(root)
label_title = tk.Label(label_frame, text="     label     :", font=("Arial", 16), bg=bg_color)
# label_value = tk.Label(label_frame, text="", font=("Arial", 16), fg="red")
label_value = tk.Label(label_frame, text="", font=("Arial", 16), fg="red", wraplength=400, justify="left")


# 좌우로 정렬
stt_title.pack(side="left")
stt_value.pack(side="left")
label_title.pack(side="left")
label_value.pack(side="left")

# 프레임 자체는 왼쪽 정렬
# ----- 기능 구현 -----
def choose_json_file():
    global base_path, data, labeled_data, labeled_map, index, trash_set
    file_path = filedialog.askopenfilename(
        title="voiceAiList.json 파일 선택",
        filetypes=[("JSON files", "*.json")]
    )
    if not file_path:
        return

    base_path = os.path.dirname(file_path)

    # JSON 로드 (raw_data로 읽어야 아래에서 필터링 가능)
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            raw_data = json.load(f)
    except Exception as e:
        messagebox.showerror("로드 오류", f"JSON 파일을 읽을 수 없습니다:\n{e}")
        return

    # trash.json 로딩
    trash_path = os.path.join(base_path, "trash.json")
    if os.path.exists(trash_path):
        with open(trash_path, "r", encoding="utf-8") as f:
            trash_set.clear()
            trash_set.update(json.load(f))
    else:
        trash_set.clear()

    # trash 제외 후 data 재구성
    data.clear()
    data.extend([item for item in raw_data if item["audio"] not in trash_set])

    # 라벨링 로드
    output_path = os.path.join(base_path, "labeling.json")
    if os.path.exists(output_path):
        with open(output_path, "r", encoding="utf-8") as f:
            labeled_data.clear()
            labeled_data.extend(json.load(f))
    else:
        labeled_data.clear()
    
    # --- 라벨 맵 구성 ---
    labeled_map.clear()
    labeled_map.update({item["audio"]: item["label"] for item in labeled_data if "label" in item})
    
    # ✅ 라벨이 비어 있는 data 항목부터 시작
    index = 0
    for i, item in enumerate(data):
        audio = item["audio"]
        label = labeled_map.get(audio, "").strip()
        if label == "":
            index = i
            break
    else:
        index = len(data)  # 전부 라벨링 되었을 경우
        
    update_ui()
    play_audio()
    
def play_audio():
    if index >= len(data): return
    path = os.path.join(base_path, data[index]["audio"])
    if os.path.exists(path):
        pygame.mixer.music.load(path)
        pygame.mixer.music.play()

def jump_to_index():
    global index
    try:
        new_index = int(jump_entry.get()) - 1  # 사용자 기준 1부터 시작하므로 -1
        if 0 <= new_index < len(data):
            index = new_index
            update_ui()
            play_audio()
        else:
            messagebox.showwarning("범위 오류", f"0 ~ {len(data)} 사이의 번호를 입력하세요.")
    except ValueError:
        messagebox.showerror("입력 오류", "숫자를 입력하세요.")
        
def mark_as_trash():
    global index
    if index >= len(data):
        return

    audio = data[index]["audio"]

    # ① trash 추가 및 저장
    trash_set.add(audio)
    with open(os.path.join(base_path, "trash.json"), "w", encoding="utf-8") as f:
        json.dump(list(trash_set), f, ensure_ascii=False, indent=2)

    # ② labeling.json에서 해당 항목 제거
    labeled_data[:] = [item for item in labeled_data if item["audio"] != audio]
    labeled_map.pop(audio, None)  # 딕셔너리에서도 제거

    # 다시 저장
    with open(os.path.join(base_path, "labeling.json"), "w", encoding="utf-8") as f:
        json.dump(labeled_data, f, ensure_ascii=False, indent=2)

    # ③ 현재 목록에서도 제거
    data.pop(index)

    # index는 유지 (자동 다음 항목으로 이동됨)
    update_ui()
    play_audio()
    


def save_label():
    global index
    label = entry.get().strip()
    item = data[index]

    # 기본값 설정
    transcripts = item.get("transcripts", "")
    audio = item["audio"]

    # 업데이트용 dict 생성 (순서 지정)
    labeled_entry = {
        "transcripts": transcripts,
        "audio": audio,
        "label": label
    }

    # labeled_map 갱신
    labeled_map[audio] = label

    # ✅ 기존 데이터 수정 or 새로 추가
    updated = []
    found = False
    for x in labeled_data:
        if x["audio"] == audio:
            updated.append(labeled_entry)
            found = True
        else:
            updated.append(x)

    if not found:
        updated.append(labeled_entry)

    # 갱신
    labeled_data.clear()
    labeled_data.extend(updated)

    # 저장
    with open(os.path.join(base_path, "labeling.json"), "w", encoding="utf-8") as f:
        json.dump(labeled_data, f, ensure_ascii=False, indent=2)

    index += 1
    update_ui()
    play_audio()

def skip_label():
    global index
    index += 1
    update_ui()
    play_audio()

def go_back():
    global index
    if index > 0:
        index -= 1
        update_ui()
        play_audio()
    else:
        messagebox.showinfo("알림", "이미 첫 항목입니다.")

def exit_program():
    root.destroy()

def on_enter_pressed(event):
    save_label()

def update_ui():
    if index >= len(data):
        audio_label.config(text="라벨링 완료!")
        # stt_label.config(text="")
        # prev_label.config(text="")
        entry.delete(0, tk.END)
        progress_bar['value'] = 100
        return

    item = data[index]
    audio_label.config(text=f"[{index+1}/{len(data)}] 📄 {item['audio']}")

    # 먼저 선언하고 나서 사용해야 함
    label_text = labeled_map.get(item["audio"], "").strip()

    # stt / label 텍스트 갱신
    stt_value.config(text=item.get('transcripts', '') or "없음")
    label_value.config(text=label_text if label_text else "없음")
    # prev_label.config(text=f"라벨: {label_text}" if label_text else "라벨: 없음")
    entry.delete(0, tk.END)

    # 진행률 표시
    percent = (index + 1) / len(data) * 100 if len(data) else 0
    progress_label.config(text=f"{percent:.1f}%")
    progress_bar['value'] = percent

def create_voice_list_json():
    folder_path = filedialog.askdirectory(title="WAV 폴더 선택")
    if not folder_path:
        return

    wav_files = [f for f in os.listdir(folder_path) if f.lower().endswith(".wav")]
    if not wav_files:
        messagebox.showinfo("알림", "선택한 폴더에 WAV 파일이 없습니다.")
        return

    today = datetime.now().strftime("%Y%m%d")
    json_filename = f"voiceAiList_{today}.json"
    json_path = os.path.join(folder_path, json_filename)

    voice_list = [{"audio": wav_file} for wav_file in wav_files]

    try:
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(voice_list, f, ensure_ascii=False, indent=2)
        messagebox.showinfo("완료", f"{json_filename} 파일이 생성되었습니다.")
        # 생성한 파일을 바로 불러오기
        choose_json_file_from_path(json_path)
    except Exception as e:
        messagebox.showerror("오류", f"파일 생성 실패:\n{e}")
def choose_json_file_from_path(file_path):
    global base_path, data, labeled_data, labeled_map, index, trash_set

    base_path = os.path.dirname(file_path)

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            raw_data = json.load(f)
    except Exception as e:
        messagebox.showerror("로드 오류", f"JSON 파일을 읽을 수 없습니다:\n{e}")
        return

    trash_path = os.path.join(base_path, "trash.json")
    if os.path.exists(trash_path):
        with open(trash_path, "r", encoding="utf-8") as f:
            trash_set.clear()
            trash_set.update(json.load(f))
    else:
        trash_set.clear()

    data.clear()
    data.extend([item for item in raw_data if item["audio"] not in trash_set])

    output_path = os.path.join(base_path, "labeling.json")
    if os.path.exists(output_path):
        with open(output_path, "r", encoding="utf-8") as f:
            labeled_data.clear()
            labeled_data.extend(json.load(f))
    else:
        labeled_data.clear()

    labeled_map.clear()
    labeled_map.update({item["audio"]: item["label"] for item in labeled_data if "label" in item})

    index = 0
    for i, item in enumerate(data):
        if labeled_map.get(item["audio"], "").strip() == "":
            index = i
            break
    else:
        index = len(data)

    update_ui()
    play_audio()
    
# ----- UI 구성 -----

# JSON 버튼 아래에 배치
top_button_frame = tk.Frame(root, bg=bg_color)
top_button_frame.pack(pady=10)

# tk.Button(root, text="📄 JSON 파일 선택", command=choose_json_file, font=("Arial", 12)).pack(pady=10)
tk.Button(top_button_frame, text="📄 JSON 파일 선택", command=choose_json_file, font=("Arial", 12)).pack(side="left", padx=10)
tk.Button(top_button_frame, text="New", command=create_voice_list_json, font=("Arial", 12)).pack(side="left", padx=10)
# audio_label.pack()
audio_line_frame = tk.Frame(root, bg=bg_color)
audio_line_frame.pack()

audio_label = tk.Label(audio_line_frame, text="", font=("Arial", 14, "bold"), bg=bg_color)
audio_label.pack(side="left", padx=(0, 10))

trash_button = tk.Button(audio_line_frame, text="🗑️ 목록에서 제외", command=mark_as_trash)
trash_button.pack(side="left")
progress_frame.pack(pady=5)
# progress_label.pack()
progress_label = tk.Label(progress_frame, text="0%", font=("Arial", 10))
progress_label.pack(side="left", padx=(0, 5))

# 기존 프로그레스 바 옆에 배치
progress_bar.pack(side="left", ipady=1)

# progress_bar 아래 또는 entry 위에 배치
jump_frame.pack(pady=3)
jump_label.pack(side="left")
jump_entry.pack(side="left")
jump_button.pack(side="left", padx=5)


# stt_label.pack()
# prev_label.pack()
stt_frame.pack(anchor="w", padx=150)
label_frame.pack(anchor="w", padx=151)

# entry.pack(pady=10)
# entry.bind("<Return>", on_enter_pressed)  # Enter 키 바인딩
# 🔤 라벨 입력 라인: 좌측 텍스트 + 입력칸 + 저장 버튼
label_input_frame = tk.Frame(root, bg=bg_color)
label_input_frame.pack(pady=10)

label_input_text = tk.Label(label_input_frame, text="label 입력", font=("Arial", 14), bg=bg_color)
label_input_text.pack(side="left", padx=(0, 10))

entry = tk.Entry(label_input_frame, font=("Arial", 14), width=25)
entry.pack(side="left")

save_button = tk.Button(label_input_frame, text="✔ 라벨 저장", command=save_label)
save_button.pack(side="left", padx=10)

entry.bind("<Return>", on_enter_pressed)  # 엔터로도 저장 가능


button_frame = tk.Frame(root, bg=bg_color)
button_frame.pack(pady=10)
btn_font = ("Arial", 11, "bold") 

tk.Button(button_frame, text="◁ 이전", font=btn_font, width=10, height=2, command=go_back).grid(row=0, column=0, padx=10)
tk.Button(button_frame, text="▶ 다시 듣기", font=btn_font, width=12, height=2, command=play_audio).grid(row=0, column=1, padx=10)
tk.Button(button_frame, text="▷ 다음", font=btn_font, width=10, height=2, command=skip_label).grid(row=0, column=2, padx=10)
# tk.Button(button_frame, text="종료", width=5, height=1, command=exit_program).grid(row=0, column=4, padx=10)
# tk.Button(button_frame, text="✔ 라벨 저장", command=save_label).grid(row=0, column=2, padx=10)


# ✅ Progress Bar UI 배치


root.mainloop()

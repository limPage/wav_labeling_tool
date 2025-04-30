# wav_labeling_tool

Python 기반 음성 라벨링 도구입니다.  
WAV 파일을 기반으로 자동/수동 라벨링을 수행하고, labeling 결과를 JSON으로 저장합니다.

---

## 📅 업데이트 히스토리

### 🔹 0430
- 파일 선택 후 목록 불러오기 기능 추가됨
- JSON 선택 시 자동으로 voiceAiList 불러오기 및 재생 기능 개선

![0430 UI](https://github.com/limPage/wav_labeling_tool/blob/main/images/0430.png)

---

### 🔹 0424
#### 최초 업로드 버전

![초기 UI](https://github.com/limPage/wav_labeling_tool/blob/main/images/0424.png)

---

## 🚀 사용 방법

1. `wav` 파일과 `voiceAiList.json` 파일을 **같은 경로**에 위치시킨 후, `exe` 파일을 실행합니다.
2. JSON 파일을 선택하면 오디오 리스트가 생성되며, 자동으로 WAV가 재생됩니다.
3. 라벨 입력 칸에 인식한 텍스트를 입력하고 **[라벨 저장]** 버튼 또는 `Enter` 키를 누르면 저장됩니다.
   - 라벨링 결과는 `labeling.json`에 저장됩니다.

![라벨링 예시](https://github.com/limPage/wav_labeling_tool/blob/main/images/0424_labeling.png)

4. 이전 / 다음 버튼으로 다른 오디오를 탐색할 수 있으며, 특정 번호를 입력하고 ▶ 재생 버튼을 누르면 해당 순번으로 점프할 수 있습니다.
5. 필요 없는 항목은 **[🗑️ 목록에서 제외]** 버튼을 눌러 제거할 수 있습니다.  
   - 해당 항목은 `trash.json`에 기록되어 다음 실행 시 자동 제외됩니다.

![제외 기능](https://github.com/limPage/wav_labeling_tool/blob/main/images/0424_trash.png)

6. 종료 후 재실행해도 `trash.json` 및 `labeling.json`이 존재하면 진행 상황이 유지됩니다.  
   - `"label"` 값이 없거나 비어 있는 가장 처음 항목부터 자동 시작됩니다.

---

## 🆕 새 JSON 만들기 (New 버튼 기능)

- 기존 `voiceAiList.json`을 수동 편집하지 않아도, **[New]** 버튼을 통해 원하는 폴더를 선택하면 다음과 같은 JSON이 생성됩니다:

```json
[
  {"audio": "sub100100a00001.wav"},
  {"audio": "sub100100a00002.wav"}
]
```

- 이 파일은 `"voiceAiList_YYYYMMDD.json"` 형식으로 저장되며, 자동 로딩됩니다.

![New 기능](https://github.com/limPage/wav_labeling_tool/blob/main/images/0424_new_json.png)

---

## 🤝 협업 방법

- `labeling.json`, `trash.json` 파일을 함께 서버에 업로드하거나, 로컬 폴더에 덮어쓰기하여 **진행 상황을 공유**할 수 있습니다.
- `.wav` 파일만 추가하면 `voiceAiList.json`에 항목을 수동으로 추가하거나 New 버튼을 눌러 자동 갱신할 수 있습니다.

---

## 📁 파일 구성 예시

```
voice_folder/
├── voiceAiList.json
├── sub100100a00001.wav
├── sub100100a00002.wav
├── labeling.json         ← (자동 생성됨)
├── trash.json            ← (제외 항목 저장)
└── wav_labeling_tool.exe
```

---

## 📝 기타

- `.mp3` 파일도 지원하려면 `pygame` 설치 시 MP3 지원 여부 확인 필요
- 플랫폼에 따라 `base_path` 폴더 열기 기능이 지원됩니다 (`📂 폴더 열기` 버튼)

---

## 📌 개발자

- GitHub: [limPage](https://github.com/limPage)
- 도구명: **HJ Voice Labeling Tool**

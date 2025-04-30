### wav_labeling_tool

# 0430
파일 선택 후 목록 불러오기 기능 추가 함
<br>
![UI 스크린샷](https://github.com/limPage/wav_labeling_tool/blob/main/images/0430.png)
<br>
<br>
# 0424
### 최초 업로드
![UI 스크린샷](https://github.com/limPage/wav_labeling_tool/blob/main/images/0424.png)
<br>
<br>
1.wav파일과 json파일을 같은 경로에 위치 시켜주고 exe파일을 실행한 뒤 라벨링이 필요한 json을 선택해준다.
json이 불러와지면 wav 리스트가 생기고 자동으로 wav가 재생된다. 그러면 label 입력 칸에 자신이 인지한 텍스트를 입력하고
라벨 저장 버튼이나 enter를 입력하여 저장시킨다.(라벨링이 된 것은 labeling.json으로 같은 경로에 저장된다.)
<br>
![UI 스크린샷](https://github.com/limPage/wav_labeling_tool/blob/main/images/0424_labeling.png)
<br>
<br>
2.다음 버튼이나 이전 버튼을 눌러 해당 순번이 아닌 다른 순번을 진행 할 수 있다.
혹은 특정 번호의 wav 파일을 진행하고 싶다면 번호를 입력하고 재생버튼을 누르면 해당 번호로 이동하여 진행된다.

3.학습에 필요하지 않는 파일이라 생각되면 목록에서 제외 버튼을 눌러 리스트에서 제외시킬 수 있다.
(목록에서 제외 된 것은 trash.json으로 같은 경로에 저장된다.)
<br>
![UI 스크린샷](https://github.com/limPage/wav_labeling_tool/blob/main/images/0424_trash.png)
<br>
<br>
4.exe를 종료하여도 다음 실행시 선택한 json파일의 경로 상에 있는 trash,labeling.json들을 불러오기 때문에 진행상황이 유지가 된다.
label 값이 ""이거나 없는 가장 낮은(라벨링이 아직 안된) 순번부터 시작한다.

5.voice 폴더를 다운 받고 voiceAiList.json를 불러오기하여 라벨링 작업을 하면 되고 trash,labeling.json가 생성되었다면
이 파일 또한 서버 voice 폴더에 내에 덮어쓰기를 해서 다른 사람과 진행 상황을 공유할 수 있다.

6.voice 폴더에 비상벨을 통하여 저장된 wav파일 외에 같은 폴더 내에 wav파일을 추가하여 라벨링을 진행하고 싶다면
기존 voiceAiList.json 안에  {"audio":wav파일명}  예)  ,{"audio":"sub100100a00005.wav"} 이런식으로 [ ]안에 포함 시키거나
new 버튼을 클릭하여 wav 파일이 위치한 경로를 지정해주면 해당 폴더의 wav파일을 스캔하여 "voiceAiList_날짜" 형식으로
json 파일을 생성하여 자동으로 불러와서 실행된다.
<br>
![UI 스크린샷](https://github.com/limPage/wav_labeling_tool/blob/main/images/0424_new_json.png)
<br>




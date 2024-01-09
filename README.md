# Korean multi-speaker VITS

This project was implemented using the official PyTorch [implementation](https://github.com/jaywalnut310/vits) by "jaywalnut310".

## Getting Started

Setting up the development environment for this project can be challenging due to version conflicts with various libraries. 

Therefore, we managed the development environment of this project using a Docker container. 

The Docker image, which can be used to create the Docker container, can be downloaded from [Docker Hub](https://hub.docker.com/layers/0913ktg/tts_image/vits_korean_final/images/sha256-6f50059898a0c0cfa88123210a7ef7b24a2be4fccdb00474d2f02da4194162e2?context=repo).

### Dataset

The data used for model training can be downloaded from the following link.

- [문학작품 낭송․낭독 음성 데이터(시, 소설, 희곡, 시나리오)](https://www.aihub.or.kr/aihubdata/data/view.do?currMenu=115&topMenu=100&aihubDataSe=data&dataSetSn=485)
- [감성 및 발화스타일 동시 고려 음성합성 데이터](https://www.aihub.or.kr/aihubdata/data/view.do?currMenu=115&topMenu=100&aihubDataSe=data&dataSetSn=71349)
- [감성 및 발화 스타일별 음성합성 데이터](https://www.aihub.or.kr/aihubdata/data/view.do?currMenu=115&topMenu=100&aihubDataSe=data&dataSetSn=466)

### Data Preprocessing

데이터 세트를 다운로드 한 뒤 학습할 수 있게 전처리를 해야 합니다. 

1. 파일 경로에 한글 또는 특수문자가 있는 경우 영어 또는 숫자로 변경해야 합니다.
2. 학습에 사용할 .wav 파일을 22kHz sampling rate로 변환해야 합니다.
3. 스테레오 파일이 있는 경우 모노 파일로 변환해야 합니다.
4. google drive에서 다운로드한 filelists는 라벨과 wav파일을 연결시켜 놓은 결과물입니다. (.cleaned 파일은 g2pk를 사용하여 문장 단위로 변환한 결과물입니다.)
4-1. 변환 전 filelist에서 다른 음소변환 모듈을 사용할 경우 몇 개의 영어 단어를 한국어 발음으로 변환하고 '\xa0'특수문자를 제거해야 합니다.
5. make_mels.py 파일을 데이터 세트 상위 경로에 위치시키고 melspectrogram을 생성합니다. (학습에 필요한 파일을 미리 생성해 파일화.)

### Installing

You can clone this GitHub repository and use it.

```
git clone https://github.com/0913ktg/vits_korean_multispeaker
```

You can download the model checkpoints and filelists from the [Google Drive link](https://drive.google.com/drive/folders/1nLE6EY1-gOfbqyDJzNgFkMoKXH7pvVgT?usp=sharing).

### Train
22kHz 음성 파일과 train, validation filelists 그리고 데이터 전처리가 완료 되었다면 train_ms.py를 실행하여 학습을 할 수 있습니다. 
멀티 GPU 사용이 가능한 것을 확인하였습니다. 

### Synthesis

1. In inference.py, modify the path for the Generator checkpoint accordingly.
2. Enter the desired Korean sentences in texts. (Separate multiple sentences with a comma.)
3. Enter the speaker number in sid. (from 0 to 184)
4. Running inference.py will create a file named test{i}.wav.


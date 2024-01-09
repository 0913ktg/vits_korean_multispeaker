# Korean multi-speaker VITS

This project was implemented using the official PyTorch [implementation](https://github.com/jaywalnut310/vits) by "jaywalnut310".
After training for 10 epochs (32 batch size, 460k steps), the inference results for two random male and female speakers are available in the inference_samples.

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

1. If file paths contain Korean or special characters, change them to English or numbers.
2. Convert .wav files for training to a 22kHz sampling rate.
3. If there are stereo files, convert them to mono.
4. The filelists downloaded from Google Drive link the labels and wav files. (.cleaned files are the result of converting sentences using g2pk.)
4-1. If using a different phoneme conversion module, convert a few English words to Korean pronunciation and remove the '\xa0' special character.
5. Place the make_mels.py file at the top path of the dataset and generate melspectrograms. (Pre-create files required for training.)

### Installing

You can clone this GitHub repository and use it.

```
git clone https://github.com/0913ktg/vits_korean_multispeaker
```

You can download the model checkpoints and filelists from the [Google Drive link](https://drive.google.com/drive/folders/1nLE6EY1-gOfbqyDJzNgFkMoKXH7pvVgT?usp=sharing).

### Train
Once you have 22kHz audio files, train, and validation filelists, and have completed data preprocessing, you can start training by running train_ms.py. Multi-GPU usage has been confirmed.

### Synthesis

1. In inference.py, modify the path for the Generator checkpoint accordingly.
2. Enter the desired Korean sentences in texts. (Separate multiple sentences with a comma.)
3. Enter the speaker number in sid. (from 0 to 184)
4. Running inference.py will create a file named test{i}.wav.


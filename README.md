# Korean multi-speaker VITS

This project was implemented using the official PyTorch [implementation](https://github.com/jaywalnut310/vits) by "jaywalnut310".

## Getting Started

Setting up the development environment for this project can be challenging due to version conflicts with various libraries. 

Therefore, we managed the development environment of this project using a Docker container. 

The Docker image, which can be used to create the Docker container, can be downloaded from [Docker Hub](https://hub.docker.com/layers/0913ktg/tts_image/vits_korean_final/images/sha256-6f50059898a0c0cfa88123210a7ef7b24a2be4fccdb00474d2f02da4194162e2?context=repo).

### Dataset

The data used for model training can be downloaded from the following link.

문학작품 낭송․낭독 음성 데이터(시, 소설, 희곡, 시나리오) : https://www.aihub.or.kr/aihubdata/data/view.do?currMenu=115&topMenu=100&aihubDataSe=data&dataSetSn=485
감성 및 발화스타일 동시 고려 음성합성 데이터 : https://www.aihub.or.kr/aihubdata/data/view.do?currMenu=115&topMenu=100&aihubDataSe=data&dataSetSn=71349
감성 및 발화 스타일별 음성합성 데이터 : https://www.aihub.or.kr/aihubdata/data/view.do?currMenu=115&topMenu=100&aihubDataSe=data&dataSetSn=466

### Installing

You can clone this GitHub repository and use it.

```
git clone https://github.com/0913ktg/vits_korean_multispeaker
```

### Train
1. Put your data into a folder, e.g. `data/your_data`. Audio files should be named with the suffix `.wav` and text files with `.normalized.txt`.

2. Quantize the data:

```
python -m vall_e.emb.qnt data/your_data
```

3. Generate phonemes based on the text:

```
python -m vall_e.emb.g2p data/your_data
```

4. Customize your configuration by creating `config/your_data/ar.yml` and `config/your_data/nar.yml`. Refer to the example configs in `config/korean` and `vall_e/config.py` for details. You may choose different model presets, check `vall_e/vall_e/__init__.py`.

5. Train the AR or NAR model using the following scripts:

```
python -m vall_e.train yaml=config/your_data/ar_or_nar.yml
```

You may quit your training any time by just typing `quit` in your CLI. The latest checkpoint will be automatically saved.


### Synthesis

# 韩语多说话人 VITS (Korean multi-speaker VITS)

本项目是基于 "jaywalnut310" 的 PyTorch 官方 [实现](https://github.com/jaywal310/vits)而构建的。
在训练 10 个 epoch（batch size 为 32，460k 步）后，随机抽取的一男一女两位说话人的推理结果可在 `inference_samples` 中找到。

## 入门指南

由于各种库之间存在版本冲突，配置本项目的开发环境可能会比较困难。

因此，我们使用 Docker 容器管理本项目的开发环境。

用于创建 Docker 容器的 Docker 镜像可以从 [Docker Hub](https://hub.docker.com/layers/0913ktg/tts_image/vits_korean_final/images/sha256-6f50059898a0c0cfa88123210a7ef7b24a2be4fccdb00474d2f02da4194162e2?context=repo) 下载。

### 数据集

用于模型训练的数据可以从以下链接下载：

- [文学作品朗诵·朗读语音数据 (诗歌, 小说, 剧本, 剧本)](https://www.aihub.or.kr/aihubdata/data/view.do?currMenu=115&topMenu=100&aihubDataSe=data&dataSetSn=485)
- [同时考虑情感及发音风格的语音合成数据](https://www.aihub.or.kr/aihubdata/data/view.do?currMenu=115&topMenu=100&aihubDataSe=data&dataSetSn=71349)
- [按情感及发音风格分类的语音合成数据](https://www.aihub.or.kr/aihubdata/data/view.do?currMenu=115&topMenu=100&aihubDataSe=data&dataSetSn=466)

### 数据预处理

下载数据集后，需要进行预处理以便于训练。

1. 如果文件路径包含韩文或特殊字符，请将其更改为英文或数字。
2. 将用于训练的 `.wav` 文件转换为 22kHz 采样率。
3. 如果存在立体声文件，请将其转换为单声道。
4. 从 Google Drive 下载的文件列表将标签与 `.wav` 文件关联起来。（`.cleaned` 文件是使用 g2pk 转换句子后的结果。）
4-1. 如果使用不同的音素转换模块，请将少量英文单词转换为韩语发音，并移除 `\xa0` 特殊字符。
5. 将 `make_mels.py` 文件放置在数据集的根路径下并生成梅尔谱图（melspectrograms）。（预先创建训练所需的文件。）

### 安装

您可以克隆此 GitHub 仓库并使用：

```
git clone https://github.com/0913ktg/vits_korean_multispeaker
```

您可以从 [Google Drive 链接](https://drive.google.com/drive/folders/1nLE6EY1-gOfbqyDJzNgFkMoKXH7pvVgT?usp=sharing) 下载模型权重（checkpoints）和文件列表（filelists）。

### 训练

一旦您准备好了 22kHz 音频文件、训练集和验证集文件列表，并完成了数据预处理，就可以运行 `train_ms.py` 开始训练。已确认支持多 GPU 使用。

### 合成

1. 在 `inference.py` 中，根据实际情况修改 Generator checkpoint 的路径。
2. 在 `texts` 中输入所需的韩语句子。（多个句子请用逗号隔开。）
3. 在 `sid` 中输入说话人编号（0 到 184）。
4. 运行 `inference.py` 将生成名为 `test{i}.wav` 的文件。

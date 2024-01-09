import matplotlib.pyplot as plt
import IPython.display as ipd
import numpy as np
import os
import json
import math
import torch
from torch import nn
from torch.nn import functional as F
from torch.utils.data import DataLoader

import commons
import utils
from data_utils import TextAudioLoader, TextAudioCollate, TextAudioSpeakerLoader, TextAudioSpeakerCollate
from models import SynthesizerTrn
from text.korean.symbols import symbols
from text.korean import text_to_sequence

from scipy.io.wavfile import write


def get_text(text, hps):
    text_norm = text_to_sequence(text, hps.data.text_cleaners)
    if hps.data.add_blank:
        text_norm = commons.intersperse(text_norm, 0)
    text_norm = torch.LongTensor(text_norm)
    return text_norm

hps = utils.get_hparams_from_file("./configs/aihub_base.json")

# SynthesizerTrn의 첫 번째 매개변수로 len(symbols)이었으나 checkpoint와 맞지 않는 관계로 임의로 178상수를 입력하여 차원 맞춤.
net_g = SynthesizerTrn(
    178,
    hps.data.filter_length // 2 + 1,
    hps.train.segment_size // hps.data.hop_length,
    n_speakers=hps.data.n_speakers,
    **hps.model).cuda()

_ = net_g.eval()


_ = utils.load_checkpoint("logs/aihub_base/G_466000.pth", net_g, None)

sr = hps['data']['sampling_rate']

texts = [
    '어떤 가난한 머슴이 있었다. 이 머슴은 자기도 부자가 되고싶었으나, 어떻게 부자가 되어야 하는지를 몰랐다. 그래서 그 마을에서 가장 큰 부자가 사는 곳으로 찾아갔다. 영감님, 소인네에게 어떻게하면 부자가 될 수 있는지 알려줄 수 있겠습니까? 마을에서 부자로 알려진 양반은 처음에는 가르쳐주지 않다가, 머슴이 끈질기게 물어보자 마음을 돌려 가르쳐주기로 결심했다.',
    '이보게, 자네 정말 부자가 되고 싶은 방법을 알고싶나? 네. 그럼 따라와보게. 머슴은 양반을 따라 기와집 뒤뜰에 있는 큰 소나무 밑으로 갔다. 양반이 말했다. 이 소나무 위로 한번 올라가보게. 머슴은 의아했지만 부자가 되는 방법을 알려준다기에 군말없이 나무 위를 올라갔다. 다 올라갔으면 이제 나뭇가지에 매달려보게. 이번에도 의아하고 위험천만했지만 순순히 머슴은 나뭇가지에 간신히 매달렸다. 매달렸나? 그럼 이제 한 손을 놔보게. 영감님, 이게 부자가 되는 방법이랑 무슨 관계가 있습니까? 알기싫나? 그럼 그냥 내려오게. 머슴은 속는 셈 치고 나뭇가지를 잡은 손 하나를 놓았다. 이제 팔 하나로만 나뭇가지에 매달려 위험천만하기 짝이 없었다.',
    '양반은 말했다. 됐나? 그럼 이제 마지막 손 하나도 놓아보게. 머슴은 참을 수 없어 이렇게 소리쳤다. 아니, 영감님! 이 손까지 놓으라고 하시면 떨어져 죽으라는 말입니까? 그렇게는 못합니다! 머슴은 영감이 자신을 가지고 장난친다 생각하여 그냥 나무에서 내려와버렸다. 이때, 열이 받아있는 머슴에게 양반이 다가가서 이렇게 말했다. 자네, 내가 마지막 손 하나를 놓으라고 했을 때 절대 못놓겠다고 했지? 그랬죠. 그걸 놓으면 떨어져 죽는데 어떻게 놓습니까?',
    '그러자 양반은 빙그레 웃으며 말했다. 바로 그 나뭇가지를 절대 놓으려고 하지 않았던 것처럼, 자네 손에 한번 들어온 돈은 죽어도 놓치지 않겠다고 생각하며 살게. 그게 바로 부자가 되는 지름길이야. 머슴은 이내 깨달음을 얻고 양반에게 감사하다는 말을 남기고 집을 떠났다고 한다.'    
]

for i, text in enumerate(texts):    
    stn_tst = get_text(text, hps)
    with torch.no_grad():
        x_tst = stn_tst.cuda().unsqueeze(0)
        x_tst_lengths = torch.LongTensor([stn_tst.size(0)]).cuda()
        sid = torch.LongTensor([55]).cuda()
        audio = net_g.infer(x_tst, x_tst_lengths, sid=sid, noise_scale=.667, noise_scale_w=0.8, length_scale=1)[0][0,0].data.cpu().float().numpy()
        write(f'test{i}.wav', sr, audio.astype(np.float32))
# ipd.display(ipd.Audio(audio, rate=hps.data.sampling_rate, normalize=False))


# 나는 너를 소중한 친구라고 생각했는데 너는 그렇게 생각하지 않았구나.
# 오늘 점심에 맛있는 음식을 먹어서 기분이 너무 좋아.
# 나를 배신하면 그 때는 정말 가만두지 않을줄 알아!

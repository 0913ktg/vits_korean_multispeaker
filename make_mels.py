import os
import glob
import torch
import librosa
import numpy as np
import soundfile as sf
from tqdm import tqdm
from scipy.io.wavfile import read

hann_window = {}

def spectrogram_torch(y, n_fft, sampling_rate, hop_size, win_size, center=False):
    if torch.min(y) < -1.:
        print('min value is ', torch.min(y))
    if torch.max(y) > 1.:
        print('max value is ', torch.max(y))

    global hann_window
    dtype_device = str(y.dtype) + '_' + str(y.device)
    wnsize_dtype_device = str(win_size) + '_' + dtype_device
    if wnsize_dtype_device not in hann_window:
        hann_window[wnsize_dtype_device] = torch.hann_window(win_size).to(dtype=y.dtype, device=y.device)
   
    y = torch.nn.functional.pad(y.unsqueeze(1), (int((n_fft-hop_size)/2), int((n_fft-hop_size)/2)), mode='reflect')
    y = y.squeeze(1)

    spec = torch.stft(y, n_fft, hop_length=hop_size, win_length=win_size, window=hann_window[wnsize_dtype_device],
                      center=center, pad_mode='reflect', normalized=False, onesided=True, return_complex=False)

    spec = torch.sqrt(spec.pow(2).sum(-1) + 1e-6)
    return spec

def load_wav_to_torch(full_path):
  sampling_rate, data = read(full_path)
  # return data, sampling_rate
  return torch.FloatTensor(data.astype(np.float32)), sampling_rate

def process_wav_file(wav_file, spec_filename, n_fft, sampling_rate, hop_size, win_size):
    # WAV 파일 로드
    audio, sampling_rate = load_wav_to_torch(wav_file)
    if sampling_rate != 22050:
        raise ValueError("{} {} SR doesn't match target {} SR".format(
            sampling_rate, 22050))
    audio_norm = audio / 32768.0
    audio_norm = audio_norm.unsqueeze(0)

    # 스펙트로그램 생성
    spec = spectrogram_torch(audio_norm, n_fft, sampling_rate, hop_size, win_size, center=False)
    spec = torch.squeeze(spec, 0)

    # 스펙트로그램 저장
    torch.save(spec, spec_filename)

# 필요한 파라미터 설정
n_fft = 1024            # FFT 창 크기
sampling_rate = 22050   # 샘플링 레이트
hop_size = 256        # Hop 크기
win_size = 1024        # 윈도우 크기
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# 현재 디렉토리와 하위 디렉토리에서 *_22k.wav 파일 찾기
wav_files = glob.glob('**/*_22k.wav', recursive=True)

# sample data만 처리
# with open('/data/vits_for_korean/filelists/a_test_train.txt.cleaned', 'r') as f:
#     wav_files = f.readlines()
# with open('/data/vits_for_korean/filelists/a_test_val.txt.cleaned', 'r') as f:
#     wav_files.extend(f.readlines())
    
# new_wav_files = [x.split('|')[0] for x in wav_files]

for wav_file in tqdm(wav_files):
    spec_filename = wav_file.replace('.wav', '.spec.pt')
    process_wav_file(wav_file, spec_filename, n_fft, sampling_rate, hop_size, win_size)

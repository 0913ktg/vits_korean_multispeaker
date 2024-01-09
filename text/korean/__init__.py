from text.korean import cleaners
from text.korean.symbols import symbols
from jamo import h2j, j2hcj
# from text.korean.SMARTG2P.trans import mixed_g2p as g2p
# from text.korean.SMARTG2P.trans import sentranslit as trans
from g2pk import G2p

jongsung_code_s = 4546
jongsung_code_e = 4520

# Mappings from symbol to numeric ID and vice versa:
_symbol_to_id = {s: i for i, s in enumerate(symbols)}
_id_to_symbol = {i: s for i, s in enumerate(symbols)}

def jamo_split(text):

    temp = h2j(text)
    jongsung_idxs = list()

    # save jongsung idx for suffix
    for i,t in enumerate(temp):
        if ord(t) >= jongsung_code_e and ord(t) <= jongsung_code_s:
            jongsung_idxs.append(i)
    temp = j2hcj(temp)

    return temp, jongsung_idxs

#def text_to_sequence(g2p, text):
def text_to_sequence(text, cleaner_names):
    '''Converts a string of text to a sequence of IDs corresponding to the symbols in the text.
    Args:
      text: string to convert to a sequence
      cleaner_names: names of the cleaner functions to run the text through
    Returns:
      List of integers corresponding to the symbols in the text
    '''
    sequence = []
    g2pk = G2p()
    text = g2pk(text)
    text = _clean_text(text, cleaner_names)
    # 전처리 과정(.txt.cleaned)에서 trans + g2p (mixed_g2p)와 _cleaned(korean) 진행 했기 때문에 위 코드를 생략한다.
    text = text.replace('\xa0', ' ')
    clean_jamo, j_idxs = jamo_split(text)
    idx = 0
    numOfIdxs = len(j_idxs)
    for i, symbol in enumerate(clean_jamo):
        if idx < numOfIdxs and symbol == j_idxs[idx]:
            symbol+'_E'
            idx+=1
        # if '\xa01' in symbol:
        #   symbol = symbol.replace('\xa0', ' ')
        symbol_id = _symbol_to_id[symbol]
        sequence += [symbol_id]
  
    return sequence



def cleaned_text_to_sequence(cleaned_text):
    '''Converts a string of text to a sequence of IDs corresponding to the symbols in the text.
      Args:
        text: string to convert to a sequence
      Returns:
        List of integers corresponding to the symbols in the text
    '''
    sequence = [_symbol_to_id[symbol] for symbol in cleaned_text]
    return sequence


def sequence_to_text(sequence):
    '''Converts a sequence of IDs back to a string'''
    result = ''
    for symbol_id in sequence:
      s = _id_to_symbol[symbol_id]
      result += s
    return result


def _clean_text(text, cleaner_names):
    for name in cleaner_names:
      cleaner = getattr(cleaners, name)
      if not cleaner:
        raise Exception('Unknown cleaner: %s' % name)
      text = cleaner(text)
    return text


def clean_text(text, cleaner_names):
  g2pk = G2p()
  # g2pk = g2p_module
  # 학습 데이터는 대부분 영어, 숫자, 한자가 없기 때문에 시간관계상 trans를 사용하지 않지만
  # inference시에는 사용하는 것을 고려해 볼 수 있겠음. 
  # text = trans(text)
  clean_text = _clean_text(text, cleaner_names)
  # g2pk 집어넣기
  cleaned_text = g2pk(clean_text)  
  
  return cleaned_text
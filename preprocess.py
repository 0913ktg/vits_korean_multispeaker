import argparse
from text.korean import clean_text
from utils import load_filepaths_and_text
from tqdm import tqdm
from g2pk import G2p


if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument("--out_extension", default="cleaned")
  parser.add_argument("--text_index", default=2, type=int)
  parser.add_argument("--filelists", nargs="+", default=["/data/filelists_all_new/fixed_error_json.txt"])
#   parser.add_argument("--filelists", nargs="+", default=["/data/vits_for_korean/filelists/korean_sample_train_filelist.txt", "/data/vits_for_korean/filelists/korean_sample_val_filelist.txt"])
  parser.add_argument("--text_cleaners", nargs="+", default=['korean_cleaners'])

  args = parser.parse_args()
  g2pk = G2p()

  for filelist in args.filelists:
    print("START:", filelist)
    filepaths_and_text = load_filepaths_and_text(filelist)
    for i in tqdm(range(len(filepaths_and_text))):
      original_text = filepaths_and_text[i][args.text_index]
      # SMART G2P와 G2PK를 사용해 cleaned_text를 생성하도록 수정.
      cleaned_text = clean_text(original_text, args.text_cleaners, g2pk)
      filepaths_and_text[i][args.text_index] = cleaned_text

    new_filelist = filelist + "." + args.out_extension
    with open(new_filelist, "w", encoding="utf-8") as f:
      f.writelines(["|".join(x) + "\n" for x in filepaths_and_text])

# multi process

# import argparse
# import multiprocessing
# from text.korean import clean_text
# from utils import load_filepaths_and_text
# from tqdm import tqdm
# import os

# def process_filelist(filelist, text_index, text_cleaners, out_extension, part_index=None, is_val=False):
#     print("START:", filelist)
#     filepaths_and_text = load_filepaths_and_text(filelist)

#     if is_val:
#         start, end = 0, len(filepaths_and_text)
#     else:
#         part_length = len(filepaths_and_text) // 9
#         start, end = part_length * part_index, part_length * (part_index + 1)

#     new_filelist = filelist + f".{out_extension}_{part_index}" if part_index is not None else filelist + f".{out_extension}"
#     with open(new_filelist, "w", encoding="utf-8") as f:
#         for i in tqdm(range(start, min(end, len(filepaths_and_text)))):
#             original_text = filepaths_and_text[i][text_index]
#             cleaned_text = clean_text(original_text, text_cleaners)
#             filepaths_and_text[i][text_index] = cleaned_text
#             f.write("|".join(filepaths_and_text[i]) + "\n")

# def main():
#     parser = argparse.ArgumentParser()
#     parser.add_argument("--out_extension", default="cleaned")
#     parser.add_argument("--text_index", default=2, type=int)
#     parser.add_argument("--filelists", nargs="+", default=["/data/vits_for_korean/filelists/korean_sample_train_filelist.txt", "/data/vits_for_korean/filelists/korean_sample_val_filelist.txt"])
#     parser.add_argument("--text_cleaners", nargs="+", default=['korean_cleaners'])

#     args = parser.parse_args()

#     processes = []
#     for filelist in args.filelists:
#         if "train" in filelist:
#             for i in range(9):
#                 p = multiprocessing.Process(target=process_filelist, args=(filelist, args.text_index, args.text_cleaners, args.out_extension, i))
#                 p.start()
#                 processes.append(p)
#         else:
#             p = multiprocessing.Process(target=process_filelist, args=(filelist, args.text_index, args.text_cleaners, args.out_extension, None, True))
#             p.start()
#             processes.append(p)

#     for p in processes:
#         p.join()

# if __name__ == '__main__':
#     main()

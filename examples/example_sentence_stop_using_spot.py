import sys

sys.path.append('../')

import time
from tokflow import TokFlow, SentenceStop
from data.example_text_data_full_stream_short_ja import get_example_full_stream_texts

FULL_STREAM_TEXTS = get_example_full_stream_texts()
SPOT_STREAM_TEXTS = ["は", "い", "、", "こ", "ち", "ら", "を", "お", "勧", "め", "し", "ま", "す", "。", "<", "N", "L", ">", "<",
                     "N", "L", ">", "「", "ハ", "チ", "公", "像", "」", "は", "、", "最", "も", "有", "名", "な", "観", "光",
                     "ス", "ポ", "ッ", "ト", "の", "一", "つ", "と", "さ", "れ", "て", "い", "ま", "す", "。", "<", "N", "L", ">",
                     "<", "N", "L", ">", "も", "う", "一", "つ", "有", "名", "な", "場", "所", "は", "、", "ス", "ク", "ラ", "ン",
                     "ブ", "ル", "交", "差", "点", "で", "す", "。", "<", "N", "L", ">", "<", "N", "L", ">", "また", "、", "ハ",
                     "チ", "公", "像", "は", "、", "ハ", "チ", "公", "像", "の", "向", "か", "い", "に", "あ", "る", "ス", "ク", "ラ",
                     "ン", "ブ", "ル", "交", "差", "点", "の", "ラン", "ド", "マ", "ー", "ク", "で", "も", "あ", "り", "ま", "す", "。",
                     "<", "N", "L", ">", "<", "N", "L", ">", "ハ", "チ", "公", "像", "は", "、", "多", "く", "の", "人", "々",
                     "に", "と", "っ", "て", "最", "も", "有", "名", "な", "観", "光", "ス", "ポ", "ッ", "ト", "の", "1", "つ", "で",
                     "す", "。", "<", "N", "L", ">", "<", "N", "L", ">", "ハ", "チ", "公", "像", "は", "、", "多", "く", "の",
                     "人", "々", "が", "訪", "れ", "る", "場", "所", "で", "も", "あ", "り", "ま", "す", "。"]

sens = SentenceStop(["<NL>"])

condition = {"in_type": "spot", "out_type": "spot"}

for input_token_base in SPOT_STREAM_TEXTS:
    out = sens.put(input_token_base, condition)

    text = out.get("text")  # 出力すべきテキスト
    stop_str_found = out.get("stop_str_found")  # 停止文字列が検出された か否か
    possible = out.get("possible")  # 停止文字列を検出しかかっている　か否か
    stop_str = out.get("stop_str")  # 停止文字列（複数の停止文字列を指定していた場合、どの停止文字列が検出されたのか)

    print(f"text:'{text}' possible:{possible} stop_str_found:{stop_str_found} stop_str:{stop_str}")
    if stop_str_found:
        # 停止文字列が検出された場合、処理を停止する
        break
    time.sleep(0.01)

if not stop_str_found:
    # 最後までいっても、停止文字列が検出されなかった場合
    # ペンディング中のテキストを出力しきる
    # (停止文字列が検出された場合は、停止文字列の直前までの文字列が出力されるためflushは不要)
    print(f"flush:{sens.flush(condition)}", end="", flush=True)

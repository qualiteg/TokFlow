import sys

sys.path.append('../')

import time
from tokflow import SentenceStop

"""
既に停止文字列 "<NL>"が存在しているパートから開始された場合、
既存分はスキップして、次以降でストリーミングされるセンテンスを指定した停止文字列 "<NL>" を検出した段階で停止させる
"""

FULL_STREAM_TEXTS = texts = [
    'はい、<NL>こちらを',  #
    'はい、<NL>こちらをお',  #
    'はい、<NL>こちらをお勧',  #
    'はい、<NL>こちらをお勧め',  #
    'はい、<NL>こちらをお勧めし',  #
    'はい、<NL>こちらをお勧めしま',  #
    'はい、<NL>こちらをお勧めします',  #
    'はい、<NL>こちらをお勧めします。',  #
    'はい、<NL>こちらをお勧めします。<',  #
    'はい、<NL>こちらをお勧めします。<N',  #
    'はい、<NL>こちらをお勧めします。<NL',  #
    'はい、<NL>こちらをお勧めします。<NL>',  #
    'はい、<NL>こちらをお勧めします。<NL>「',  #
    'はい、<NL>こちらをお勧めします。<NL>「ハチ',  #
    'はい、<NL>こちらをお勧めします。<NL>「ハチ公',  #
    'はい、<NL>こちらをお勧めします。<NL>「ハチ公像',  #
    'はい、<NL>こちらをお勧めします。<NL>「ハチ公像」',  #
    'はい、<NL>こちらをお勧めします。<NL>「ハチ公像」は',  #
    'はい、<NL>こちらをお勧めします。<NL>「ハチ公像」は、',  #
    'はい、<NL>こちらをお勧めします。<NL>「ハチ公像」は、最も有名な',  #
]

sens = SentenceStop(["<NL>"])

condition = {"in_type": "full", "out_type": "full", "skip_existing_stop_str": True}

for input_token_base in FULL_STREAM_TEXTS:

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

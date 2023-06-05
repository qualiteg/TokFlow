import sys

from tokflow import SentenceStop
from .test_sentence_stop_data import get_example_texts, get_example_texts2

sys.path.append('../')
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

SPOT_STREAM_TEXTS2 = ["は", "い", "、", "こ", "ち", "ら", "を", "お", "勧", "め", "し", "ま", "す", "。", "<", "N", "L"]
def test_stop_strs_found():
    """
    指定した停止文字列で停止することを確認する
    """
    sens = SentenceStop(["<NL>"])

    condition = {"in_type": "spot", "out_type": "spot"}

    on_going_text = ""
    for input_token_base in SPOT_STREAM_TEXTS:
        dict = sens.put(input_token_base, condition)
        text = dict.get("text")
        on_going_text += text
        stop_str_found = dict.get("stop_str_found", False)
        possible = dict.get("possible")
        stop_str = dict.get("stop_str")

        # print(f"text:'{on_going_text}' possible:{possible} stop_str_found:{stop_str_found} stop_str:{stop_str}")
        if stop_str_found:
            break

    assert on_going_text == "はい、こちらをお勧めします。"


def test_stop_strs_not_found():
    sens = SentenceStop(["<NLL>"])

    condition = {"in_type": "spot", "out_type": "spot"}

    on_going_text = ""
    for input_token_base in SPOT_STREAM_TEXTS:
        dict = sens.put(input_token_base, condition)
        text = dict.get("text")
        on_going_text += text
        stop_str_found = dict.get("stop_str_found", False)
        possible = dict.get("possible")
        stop_str = dict.get("stop_str")

        if stop_str_found:
            break

    assert stop_str_found == False


def test_stop_strs_not_found2():
    """
    最後が <NL になるような、停止ワードを発見しかけていたが、マッチに至らない場合に、flushすると、
    消費されていない
    """
    sens = SentenceStop(["<NL>"])

    condition = {"in_type": "spot", "out_type": "spot"}

    success_text = ""
    flush_text = ""
    last_text = ""
    for input_token_base in SPOT_STREAM_TEXTS2:

        dict = sens.put(input_token_base, condition)
        text = dict.get("text")
        stop_str_found = dict.get("stop_str_found", False)
        possible = dict.get("possible")
        stop_str = dict.get("stop_str")
        #print(f"text:'{text}' possible:{possible} stop_str_found:{stop_str_found} stop_str:{stop_str}")
        last_text = text
        if stop_str_found:
            success_text = text
            break

    flush_text = sens.flush(condition)


    assert flush_text == "<NL"

import sys

from tokflow import SentenceStop
from .test_sentence_stop_data import get_example_texts, get_example_texts2

sys.path.append('../')
TEXTS = get_example_texts()
TEXTS2 = get_example_texts2()


def test_stop_strs_found():
    """
    指定した停止文字列で停止することを確認する
    """
    sens = SentenceStop(["<NL>"])

    condition = {"in_type": "full", "out_type": "full"}

    success_text = ""
    flush_text = ""
    last_text = ""
    for input_token_base in TEXTS:
        # input_token_baseはその瞬間の入力テキスト
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

    assert last_text == "はい、こちらをお勧めします。"  # flushではない、最後に生成されたテキスト
    assert success_text == "はい、こちらをお勧めします。"  # 停止ワードで停止した場合にセットされる成功したテキスト。
    assert flush_text == "はい、こちらをお勧めします。"  # flushでは、ただしく全文取得できる

    #print(f"success_text:'{success_text}' flush_text:'{flush_text}' last_text:'{last_text}'")


def test_stop_strs_not_found():
    sens = SentenceStop(["<NLL>"])

    condition = {"in_type": "full", "out_type": "full"}

    success_text = ""
    flush_text = ""
    last_text = ""
    for input_token_base in TEXTS:
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

    assert last_text == "はい、こちらをお勧めします。<NL><NL>「ハチ公像」は、最も有名な"  # flushではない、最後に生成されたテキスト
    assert success_text == ""  # 停止ワードで停止した場合にセットされる成功したテキスト。停止ワード　"<NLL>" は、文中にはみつからないので、テキストは空
    assert flush_text == "はい、こちらをお勧めします。<NL><NL>「ハチ公像」は、最も有名な"  # flushでは、ただしく全文取得できる

    #print(f"success_text:'{success_text}' flush_text:'{flush_text}' last_text:'{last_text}'")


def test_stop_strs_not_found2():
    """
    最後が <NL になるような、停止ワードを発見しかけていたが、マッチに至らない場合に、flushすると、
    消費されていない
    """
    sens = SentenceStop(["<NL>"])

    condition = {"in_type": "full", "out_type": "full"}

    success_text = ""
    flush_text = ""
    last_text = ""
    for input_token_base in TEXTS2:

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

    # print(f"success_text:'{success_text}' flush_text:'{flush_text}' last_text:'{last_text}'")

    assert last_text == "はい、こちらをお勧めします。"  # flushではない、最後に生成されたテキスト
    assert success_text == ""  # 停止ワードで停止した場合にセットされる成功したテキスト。停止ワード　"<NLL>" は、文中にはみつからないので、テキストは空
    assert flush_text == "はい、こちらをお勧めします。<NL"  # ポテンシャル文字列だったが、マッチしなかった残り部分も加えた文字列が返る

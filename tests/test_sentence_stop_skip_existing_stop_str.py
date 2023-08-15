import sys

from tokflow import SentenceStop
from .test_sentence_stop_data import get_example_texts, get_example_texts2, get_example_texts3, get_example_texts3_for_flush_test

sys.path.append('../')
TEXTS = get_example_texts()
TEXTS2 = get_example_texts2()
TEXTS3 = get_example_texts3()
TEXTS3_FOR_FLUSH_TEST = get_example_texts3_for_flush_test()


def test_skip_existing_stop_str():
    """
    初回入力テキストに停止文字列が入っていた場合、そこは処理スキップされ、それ以降に停止文字列が出現した場合で停止する
    """
    sens = SentenceStop(["<NL>"])

    condition = {"in_type": "full", "out_type": "full","skip_existing_stop_str": True}

    success_text = ""
    flush_text = ""
    last_text = ""
    for input_token_base in TEXTS3:
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
    # print(f"success_text:'{success_text}' flush_text:'{flush_text}' last_text:'{last_text}'")
    assert last_text == "はい、<NL>こちらをお勧めします。"  # flushではない、最後に生成されたテキスト
    assert success_text == "はい、<NL>こちらをお勧めします。"  # 停止ワードで停止した場合にセットされる成功したテキスト。
    assert flush_text == "はい、<NL>こちらをお勧めします。"  # flushでは、ただしく全文取得できる


def test_skip_existing_stop_str_flush_behavior():
    """
    初回入力テキストに停止文字列が入っていた場合、そこは処理スキップされ、それ以降に停止文字列が出現した場合で停止する
    停止文字列が出現しなかったときフラッシュはバッファリングが含まれることを確認する。
    """
    sens = SentenceStop(["<NL>"])

    condition = {"in_type": "full", "out_type": "full","skip_existing_stop_str": True}

    success_text = ""
    flush_text = ""
    last_text = ""
    for input_token_base in TEXTS3_FOR_FLUSH_TEST:
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
    assert last_text == "はい、<NL>こちらをお勧めします。"  # flushではない、最後に生成されたテキスト
    assert success_text == ""  # 停止ワードで停止した場合にセットされる成功したテキスト。
    assert flush_text == "はい、<NL>こちらをお勧めします。<N"  # flushではバッファリング中の文字列も出力される




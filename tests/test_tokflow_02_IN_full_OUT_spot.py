from tokflow import TokFlow

from .test_tokflow_02_data import get_example_texts


def test_matched_one_type_pattern_1():
    tokf = TokFlow([("<NL>", "\n")])
    text = ""
    for input_token_base in get_example_texts():
        output_token = tokf.put(input_token_base, {"in_type": "full", "out_type": "spot"})
        # Input sequential tokens.
        # If there is a possibility that the token is a "search target string",
        # it is buffered for a while, so output_token may be empty for a while.
        #print(f"{output_token}", end="", flush=True)
        text += output_token

        if "<NL>" in text:
            raise Exception("Failure Must be converted str found.")

    # Remember to output the remaining buffer at the very end. Buffers may be empty characters.
    # print(f"{tokf.flush()}", end="", flush=True)
    text += tokf.flush()

    assert text == f"""はい、こちらをお勧めします。

「ハチ公像」は、最も有名な観光スポットの一つとされています。

もう一つ有名な場所は、スクランブル交差点です。

また、ハチ公像は、ハチ公像の向かいにあるスクランブル交差点のランドマークでもあります。

ハチ公像は、多くの人々にとって最も有名な観光スポットの1つです。

ハチ公像は、多くの人々が訪れる場所でもあります。"""

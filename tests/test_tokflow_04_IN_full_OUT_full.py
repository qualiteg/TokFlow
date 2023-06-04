from tokflow import TokFlow

from .test_tokflow_02_data import get_example_texts


def test_matched_one_type_pattern_1():
    tokf = TokFlow([("<NL>", "\n")])

    condition = {"in_type": "full", "out_type": "full"}
    prev_len = 0
    for input_token_base in get_example_texts():
        output_sentence = tokf.put(input_token_base, condition)

        # print(f"output_sentence:{output_sentence}")

        if prev_len > len(output_sentence):
            raise ValueError("Length error")

        if "<NL>" in output_sentence:
            raise Exception("Failure Must be converted str found.")

        prev_len = len(output_sentence)

    output_sentence = tokf.flush(condition)

    assert output_sentence == f"""はい、こちらをお勧めします。

「ハチ公像」は、最も有名な観光スポットの一つとされています。

もう一つ有名な場所は、スクランブル交差点です。

また、ハチ公像は、ハチ公像の向かいにあるスクランブル交差点のランドマークでもあります。

ハチ公像は、多くの人々にとって最も有名な観光スポットの1つです。

ハチ公像は、多くの人々が訪れる場所でもあります。"""

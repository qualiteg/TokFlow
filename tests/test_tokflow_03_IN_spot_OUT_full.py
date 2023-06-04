from tokflow import TokFlow

TOKENS_FOR_UT_1 = ["1", "hello", " ", "g", "oo", "d", "<", "N", "L", ">", "1-1<token_str>", "<", "NL", "><",
                   "token_str>2<N", "L>",
                   "3<N",
                   "L",
                   "><NL>4-", "5<NL", ">", "6<NL><NL>", "7<NLL><NA>", "8<NL><N", "9<NL>abc<NL><", "NL><NL><NL>abc<N"]

TOKENS_FOR_UT_2 = ["<", "N", "L", ">", "1-1<token_str>", "<", "NL", "><", "token_str>2<N", "L>", "3<N",
                   "L",
                   "><NL>4-", "5<NL", ">", "6<NL><NL>", "7<NLL><NA>", "8<NL><N", "9<NL>abc<NL><", "NL><NL><NL>abc<N"]

TOKENS_FOR_UT_3 = ["1", "hello", " ", "g", "oo", "d", "<", "N", "L", ">", "1-1<token_str>", "<", "NL", "><",
                   "token_str>2<N", "L>",
                   "3<N",
                   "L",
                   "><NL>4-", "5<NL", ">", "6<NL><NL>", "7<NLL><NA>", "8<NL><N", "9<NL>abc<NL><", "NL><NL><NL>"]


def test_matched_one_type_pattern_1():
    expected = "".join(TOKENS_FOR_UT_1).replace("<NL>", "★")
    tokf = TokFlow([("<NL>", "★")])

    actual = ""

    num_of_valid_response = 0
    prev_len = 0
    condition = {"in_type": "spot", "out_type": "full"}
    for in_token in TOKENS_FOR_UT_1:

        sentence = tokf.put(in_token, condition)

        if prev_len > len(sentence):
            raise ValueError("Length error")

        # print(f"out_token:{out_token}")

        num_of_valid_response = num_of_valid_response + 1
        prev_len = len(sentence)

    sentence = tokf.flush(condition)

    assert sentence == "1hello good★1-1<token_str>★<token_str>2★3★★4-5★6★★7<NLL><NA>8★<N9★abc★★★★abc<N"

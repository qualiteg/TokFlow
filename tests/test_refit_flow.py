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
    for in_token in TOKENS_FOR_UT_1:

        out_token = tokf.put(in_token)
        if (len(out_token) > 0):
            actual = actual + out_token
            num_of_valid_response = num_of_valid_response + 1

    actual = actual + tokf.flush()

    assert expected == actual  # 期待値（事前に結合）と実際値（逐次処理を経て結合）が合致していること
    assert num_of_valid_response > 10  # 複数回のストリーミングレスポンスとなっていること


def test_matched_one_type_pattern_2():
    expected = "".join(TOKENS_FOR_UT_1).replace("<token_str>", "●")
    tokf = TokFlow([("<token_str>", "●")])

    actual = ""

    num_of_valid_response = 0
    for in_token in TOKENS_FOR_UT_1:

        out_token = tokf.put(in_token)
        if (len(out_token) > 0):
            actual = actual + out_token
            num_of_valid_response = num_of_valid_response + 1

    actual = actual + tokf.flush()

    assert expected == actual  # 期待値（事前に結合）と実際値（逐次処理を経て結合）が合致していること
    assert num_of_valid_response > 10  # 複数回のストリーミングレスポンスとなっていること


def test_matched_one_type_pattern_3():
    """
    改行コードに置換する
    """
    expected = "".join(TOKENS_FOR_UT_1).replace("<NL>", "\n")
    tokf = TokFlow([("<NL>", "\n")])

    actual = ""

    num_of_valid_response = 0
    for in_token in TOKENS_FOR_UT_1:

        out_token = tokf.put(in_token)
        if (len(out_token) > 0):
            actual = actual + out_token
            num_of_valid_response = num_of_valid_response + 1

    actual = actual + tokf.flush()
    # print()
    # print(expected)
    # print(actual)
    assert expected == actual  # 期待値（事前に結合）と実際値（逐次処理を経て結合）が合致していること
    assert num_of_valid_response > 10  # 複数回のストリーミングレスポンスとなっていること


def test_matched_two_types_pattern_1():
    """
    存在する２つの検索文字列
    """
    expected = "".join(TOKENS_FOR_UT_1).replace("<NL>", "★").replace("<token_str>", "●")
    tokf = TokFlow([("<NL>", "★"), ("<token_str>", "●")])

    actual = ""

    num_of_valid_response = 0
    for in_token in TOKENS_FOR_UT_1:

        out_token = tokf.put(in_token)
        if (len(out_token) > 0):
            actual = actual + out_token
            num_of_valid_response = num_of_valid_response + 1

    actual = actual + tokf.flush()

    assert expected == actual  # 期待値（事前に結合）と実際値（逐次処理を経て結合）が合致していること
    assert num_of_valid_response > 10  # 複数回のストリーミングレスポンスとなっていること


def test_matched_two_types_pattern_2():
    """
    存在する２つの検索文字列
    指定順序逆転
    """
    expected = "".join(TOKENS_FOR_UT_1).replace("<NL>", "★").replace("<token_str>", "●")
    tokf = TokFlow([("<token_str>", "●"), ("<NL>", "★")])

    actual = ""

    num_of_valid_response = 0
    for in_token in TOKENS_FOR_UT_1:

        out_token = tokf.put(in_token)
        if (len(out_token) > 0):
            actual = actual + out_token
            num_of_valid_response = num_of_valid_response + 1

    actual = actual + tokf.flush()

    assert expected == actual  # 期待値（事前に結合）と実際値（逐次処理を経て結合）が合致していること
    assert num_of_valid_response > 10  # 複数回のストリーミングレスポンスとなっていること


def test_matched_two_types_pattern_3_with_TOKENS2():
    """
    存在する２つの検索文字列
    トークン列の先頭に検索文字列が存在するケース
    """
    expected = "".join(TOKENS_FOR_UT_2).replace("<NL>", "★").replace("<token_str>", "●")
    tokf = TokFlow([("<NL>", "★"), ("<token_str>", "●")])

    actual = ""

    num_of_valid_response = 0
    for in_token in TOKENS_FOR_UT_2:

        out_token = tokf.put(in_token)
        if (len(out_token) > 0):
            actual = actual + out_token
            num_of_valid_response = num_of_valid_response + 1

    actual = actual + tokf.flush()

    assert expected == actual  # 期待値（事前に結合）と実際値（逐次処理を経て結合）が合致していること
    assert num_of_valid_response > 10  # 複数回のストリーミングレスポンスとなっていること


def test_matched_two_types_pattern_4_with_TOKENS3():
    """
    存在する２つの検索文字列
    トークン列末尾に検索文字列が存在するケース
    """
    expected = "".join(TOKENS_FOR_UT_3).replace("<NL>", "★").replace("<token_str>", "●")
    tokf = TokFlow([("<NL>", "★"), ("<token_str>", "●")])

    actual = ""

    num_of_valid_response = 0
    for in_token in TOKENS_FOR_UT_3:

        out_token = tokf.put(in_token)
        if (len(out_token) > 0):
            actual = actual + out_token
            num_of_valid_response = num_of_valid_response + 1

    actual = actual + tokf.flush()

    assert expected == actual  # 期待値（事前に結合）と実際値（逐次処理を経て結合）が合致していること
    assert num_of_valid_response > 10  # 複数回のストリーミングレスポンスとなっていること


def test_no_matched_one_type_pattern_1():
    """
    元トークン列に <NL> が存在するが 存在しない<AL> を指定
    """
    expected = "".join(TOKENS_FOR_UT_1).replace("<AL>", "★")
    tokf = TokFlow([("<AL>", "★")])

    actual = ""

    num_of_valid_response = 0
    for in_token in TOKENS_FOR_UT_1:

        out_token = tokf.put(in_token)
        if (len(out_token) > 0):
            actual = actual + out_token
            num_of_valid_response = num_of_valid_response + 1

    actual = actual + tokf.flush()

    assert expected == actual  # 期待値（事前に結合）と実際値（逐次処理を経て結合）が合致していること
    assert num_of_valid_response > 10  # 複数回のストリーミングレスポンスとなっていること


def test_no_matched_one_type_pattern_2():
    """
    元トークン列に <token_str> が存在するが 存在しない<token_str/> を指定
    """
    expected = "".join(TOKENS_FOR_UT_1).replace("<token_str/>", "★")
    tokf = TokFlow([("<token_str/>", "★")])

    actual = ""

    num_of_valid_response = 0
    for in_token in TOKENS_FOR_UT_1:

        out_token = tokf.put(in_token)
        if (len(out_token) > 0):
            actual = actual + out_token
            num_of_valid_response = num_of_valid_response + 1

    actual = actual + tokf.flush()

    assert expected == actual  # 期待値（事前に結合）と実際値（逐次処理を経て結合）が合致していること
    assert num_of_valid_response > 10  # 複数回のストリーミングレスポンスとなっていること


def test_no_matched_two_types_pattern():
    expected = "".join(TOKENS_FOR_UT_1).replace("<AL>", "★").replace("<a>", "●")
    tokf = TokFlow([("<AL>", "★"), ("<a>", "●")])

    actual = ""

    num_of_valid_response = 0
    for in_token in TOKENS_FOR_UT_1:

        out_token = tokf.put(in_token)
        if (len(out_token) > 0):
            actual = actual + out_token
            num_of_valid_response = num_of_valid_response + 1

    actual = actual + tokf.flush()

    assert expected == actual  # 期待値（事前に結合）と実際値（逐次処理を経て結合）が合致していること
    assert num_of_valid_response > 10  # 複数回のストリーミングレスポンスとなっていること


def test_matched_and_no_matched_hybrid_two_type_pattern_1():
    """
    片方が存在しない検索文字列
    """
    expected = "".join(TOKENS_FOR_UT_1).replace("<NL>", "★").replace("<a>", "●")
    tokf = TokFlow([("<NL>", "★"), ("<a>", "●")])

    actual = ""

    num_of_valid_response = 0
    for in_token in TOKENS_FOR_UT_1:

        out_token = tokf.put(in_token)
        if (len(out_token) > 0):
            actual = actual + out_token
            num_of_valid_response = num_of_valid_response + 1

    actual = actual + tokf.flush()

    assert expected == actual  # 期待値（事前に結合）と実際値（逐次処理を経て結合）が合致していること
    assert num_of_valid_response > 10  # 複数回のストリーミングレスポンスとなっていること


def test_matched_and_no_matched_hybrid_two_type_pattern_2():
    """
    片方が存在しない検索文字列
    """
    expected = "".join(TOKENS_FOR_UT_1).replace("<AL>", "★").replace("<token_str>", "●")
    tokf = TokFlow([("<AL>", "★"), ("<token_str>", "●")])

    actual = ""

    num_of_valid_response = 0
    for in_token in TOKENS_FOR_UT_1:

        out_token = tokf.put(in_token)
        if (len(out_token) > 0):
            actual = actual + out_token
            num_of_valid_response = num_of_valid_response + 1

    actual = actual + tokf.flush()

    assert expected == actual  # 期待値（事前に結合）と実際値（逐次処理を経て結合）が合致していること
    assert num_of_valid_response > 10  # 複数回のストリーミングレスポンスとなっていること


def test_matched_two_no_matched_one():
    """
    マッチする検索文字を２種類と、アンマッチを1種類
    """
    expected = "".join(TOKENS_FOR_UT_1).replace("<NL>", "★").replace("<token_str>", "●").replace("<a>", "×")
    tokf = TokFlow([("<NL>", "★"), ("<token_str>", "●"), ("<a>", "×")])

    actual = ""

    num_of_valid_response = 0
    for in_token in TOKENS_FOR_UT_1:

        out_token = tokf.put(in_token)
        if (len(out_token) > 0):
            actual = actual + out_token
            num_of_valid_response = num_of_valid_response + 1

    actual = actual + tokf.flush()

    assert expected == actual  # 期待値（事前に結合）と実際値（逐次処理を経て結合）が合致していること
    assert num_of_valid_response > 10  # 複数回のストリーミングレスポンスとなっていること


def test_for_exception():
    """
    例外 空文字の入力
    """
    expected = "".join([""]).replace("<NL>", "★").replace("<token_str>", "●").replace("<a>", "×")
    tokf = TokFlow([("<NL>", "★"), ("<token_str>", "●"), ("<a>", "×")])

    actual = ""

    num_of_valid_response = 0
    for in_token in [""]:

        out_token = tokf.put(in_token)
        if (len(out_token) > 0):
            actual = actual + out_token
            num_of_valid_response = num_of_valid_response + 1

    actual = actual + tokf.flush()

    assert expected == actual  # 期待値（事前に結合）と実際値（逐次処理を経て結合）が合致していること
    assert num_of_valid_response == 0  # 複数回のストリーミングレスポンスとなっていること

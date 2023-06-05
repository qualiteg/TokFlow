from tokflow.tok_flow_worker import TokFlowWorker

REPLACE_FROM = "<NL>"
REPLACE_TO = "★"
INIT_ARGS = (REPLACE_FROM, REPLACE_TO)


def test_eat_appear_at_first():
    """
    1回目のインプットで検索対象文字列を発見する
    """
    m = TokFlowWorker(*INIT_ARGS)
    m.eat("9<NL><NL><")

    if False:
        print(
            f"\n potential:{m.is_possible_str_started} appeared:'{m.search_str_appeared}' output:'{m.converted}' send_next:'{m.str_to_be_process_next}' failure:{m.confirmed_not_to_appear}")
    assert m.is_possible_str_started is True
    assert m.search_str_appeared is True
    assert m.converted == "9★★"
    assert m.str_to_be_process_next == "<"
    assert m.confirmed_not_to_appear is False


def test_eat_appear_at_2nd():
    """
    2回目のインプットで検索対象文字列を発見する
    """
    m = TokFlowWorker(*INIT_ARGS)
    m.eat("abc<")

    assert m.is_possible_str_started is True  # "<"　があるので、ポテンシャルはあるが
    assert m.search_str_appeared is False  # まだ発見に至っていない
    assert m.converted == ""
    assert m.str_to_be_process_next == ""
    assert m.confirmed_not_to_appear is False

    m.eat("NL>")

    if False:
        print(
            f"\n potential:{m.is_possible_str_started} appeared:'{m.search_str_appeared}' output:'{m.converted}' send_next:'{m.str_to_be_process_next}' failure:{m.confirmed_not_to_appear}")

    assert m.is_possible_str_started is True
    assert m.search_str_appeared is True
    assert m.converted == "abc★"
    assert m.str_to_be_process_next == ""


def test_eat_appear_at_3rd():
    """
    3回目のインプットで検索対象文字列を発見する
    """

    m = TokFlowWorker(*INIT_ARGS)
    m.eat("abc<")
    m.eat("NL")
    m.eat(">DDD")

    if False:
        print(
            f"\n potential:{m.is_possible_str_started} appeared:'{m.search_str_appeared}' output:'{m.converted}' send_next:'{m.str_to_be_process_next}' failure:{m.confirmed_not_to_appear}")

    assert m.is_possible_str_started is True
    assert m.search_str_appeared is True
    assert m.converted == "abc★"
    assert m.str_to_be_process_next == "DDD"


def test_eat_appear_from_splited_1():
    """
    最終的に出現検知ができるときの
    トークンの発生パターン（刻まれ方）のバリエーション1
    """
    m = TokFlowWorker(*INIT_ARGS)

    m.eat("<")
    m.eat("N")
    m.eat("L")
    m.eat(">")

    assert m.is_possible_str_started is True
    assert m.search_str_appeared is True
    assert m.converted == "★"
    assert m.str_to_be_process_next == ""
    assert m.confirmed_not_to_appear == False


def test_eat_appear_from_splited_2():
    """
    最終的に出現検知ができるときの
    トークンの発生パターン（刻まれ方）のバリエーション2

    """
    m = TokFlowWorker(*INIT_ARGS)

    m.eat("<N")
    m.eat("L")
    m.eat(">")

    assert m.is_possible_str_started is True
    assert m.search_str_appeared is True
    assert m.converted == "★"
    assert m.str_to_be_process_next == ""
    assert m.confirmed_not_to_appear == False


def test_eat_appear_from_splited_3():
    """
    最終的に出現検知ができるときの
    トークンの発生パターン（刻まれ方）のバリエーション3
    """
    m = TokFlowWorker(*INIT_ARGS)

    m.eat("<NL")
    m.eat(">")

    assert m.is_possible_str_started is True
    assert m.search_str_appeared is True
    assert m.converted == "★"
    assert m.str_to_be_process_next == ""
    assert m.confirmed_not_to_appear == False


def test_eat_appear_from_splited_4():
    """
    最終的に出現検知ができるときの
    トークンの発生パターン（刻まれ方）のバリエーション4
    """
    m = TokFlowWorker(*INIT_ARGS)

    m.eat("<NL>")

    assert m.is_possible_str_started is True
    assert m.search_str_appeared is True
    assert m.converted == "★"
    assert m.str_to_be_process_next == ""
    assert m.confirmed_not_to_appear == False


def test_eat_appear_from_splited_5():
    """
    最終的に出現検知ができるときの
    トークンの発生パターン（刻まれ方）のバリエーション5
    """
    m = TokFlowWorker(*INIT_ARGS)

    m.eat("<N")
    m.eat("L>")

    assert m.is_possible_str_started is True
    assert m.search_str_appeared is True
    assert m.converted == "★"
    assert m.str_to_be_process_next == ""
    assert m.confirmed_not_to_appear == False


def test_eat_appear_from_splited_6():
    """
    最終的に出現検知ができるときの
    トークンの発生パターン（刻まれ方）のバリエーション6
    """
    m = TokFlowWorker(*INIT_ARGS)

    m.eat("<")
    m.eat("NL>")

    assert m.is_possible_str_started is True
    assert m.search_str_appeared is True
    assert m.converted == "★"
    assert m.str_to_be_process_next == ""
    assert m.confirmed_not_to_appear == False


def test_eat_appear_with_love_fragments_1():
    """
    最終的に出現検知ができるとき、はみだしたかけらつき
    """
    m = TokFlowWorker(*INIT_ARGS)

    m.eat("><")
    m.eat("NL>")

    if False:
        print(
            f"\n potential:{m.is_possible_str_started} appeared:'{m.search_str_appeared}' output:'{m.converted}' send_next:'{m.str_to_be_process_next}' failure:{m.confirmed_not_to_appear}")

    assert m.is_possible_str_started is True
    assert m.search_str_appeared is True
    assert m.converted == ">★"
    assert m.str_to_be_process_next == ""
    assert m.confirmed_not_to_appear == False


def test_eat_appear_with_love_fragments_2():
    """
    最終的に出現検知ができるとき、はみだしたかけらつき2
    """
    m = TokFlowWorker(*INIT_ARGS)

    m.eat("<<")
    m.eat("NL>")

    if False:
        print(
            f"\n potential:{m.is_possible_str_started} appeared:'{m.search_str_appeared}' output:'{m.converted}' send_next:'{m.str_to_be_process_next}' failure:{m.confirmed_not_to_appear}")

    assert m.is_possible_str_started is True
    assert m.search_str_appeared is True
    assert m.converted == "<★"
    assert m.str_to_be_process_next == ""
    assert m.confirmed_not_to_appear == False


def test_eat_appear_with_love_fragments_3():
    """
    最終的に出現検知ができるとき、はみだしたかけらつき3
    """
    m = TokFlowWorker(*INIT_ARGS)

    m.eat("<<")
    m.eat("NL><")

    if False:
        print(
            f"\n potential:{m.is_possible_str_started} appeared:'{m.search_str_appeared}' output:'{m.converted}' send_next:'{m.str_to_be_process_next}' failure:{m.confirmed_not_to_appear}")

    assert m.is_possible_str_started is True
    assert m.search_str_appeared is True
    assert m.converted == "<★"
    assert m.str_to_be_process_next == "<"
    assert m.confirmed_not_to_appear == False


def test_eat_possible_to_match_pattern_1():
    """
    検索対象文字列が未完成
    """
    m = TokFlowWorker(*INIT_ARGS)

    m.eat("<")
    m.eat("N")
    m.eat("L")

    if False:
        print(
            f"\n potential:{m.is_possible_str_started} appeared:'{m.search_str_appeared}' output:'{m.converted}' send_next:'{m.str_to_be_process_next}' failure:{m.confirmed_not_to_appear}")

    assert m.is_possible_str_started is True
    assert m.search_str_appeared is False
    assert m.converted == ""
    assert m.str_to_be_process_next == ""
    assert m.confirmed_not_to_appear == False


def test_eat_confirmed_no_appear_pattern_1():
    """
    NG確定判定 1
    """
    m = TokFlowWorker(*INIT_ARGS)

    m.eat("<")
    m.eat("N")
    m.eat("L")
    m.eat("<")

    if False:
        print(
            f"\n potential:{m.is_possible_str_started} appeared:'{m.search_str_appeared}' output:'{m.converted}' send_next:'{m.str_to_be_process_next}' failure:{m.confirmed_not_to_appear}")

    assert m.is_possible_str_started is False
    assert m.search_str_appeared is False
    assert m.converted == ""
    assert m.str_to_be_process_next == ""
    assert m.confirmed_not_to_appear == True


def test_eat_confirmed_no_appear_pattern_2():
    """
    NG確定判定 2
    """
    m = TokFlowWorker(*INIT_ARGS)

    m.eat("<")
    m.eat("N")
    m.eat(">")

    assert m.is_possible_str_started is False
    assert m.search_str_appeared is False
    assert m.converted == ""
    assert m.str_to_be_process_next == ""
    assert m.confirmed_not_to_appear == True


def test_eat_confirmed_no_appear_pattern_3():
    """
    NG確定判定 3
    """
    m = TokFlowWorker(*INIT_ARGS)

    m.eat("<")
    m.eat("A")

    assert m.is_possible_str_started is False
    assert m.search_str_appeared is False
    assert m.converted == ""
    assert m.str_to_be_process_next == ""
    assert m.confirmed_not_to_appear == True

from tokflow import TokFlow


class SentenceStop:
    """
    SentenceStopクラスは特定のキーワードを検出し、そのキーワードが見つかった時点でテキスト生成を停止する目的で設計されたクラス。
    テキストは１文字ずつ入力される状況を想定している。

    opts.in_type="spot" の場合は、センテンスの差分が1文字ずつ追加される状況を想定
    opts.in_type="full" の場合は、センテンス全体に1文字ずつ追加されていく状況を想定


    このクラスは、例えばリアルタイムに文章を生成しながら特定のキーワードが入力されるのを監視したいというシチュエーションで役立つ。
    """

    def __init__(self, stop_strs):
        """
        SentenceStopクラスの初期化メソッド。

        :param stop_strs: テキスト生成を停止するためのキーワードリスト。
        """
        self.stop_strs = stop_strs

        self.to_replace_word = "\n"
        tuples = [(stop_str, self.to_replace_word) for stop_str in self.stop_strs]

        self.tokf = TokFlow(tuples)

        self.first_sentence = None

    def clear(self):
        self.first_sentence = None

    def put(self, input_token_base, condition):
        """
        入力された文字列と条件を受け取り、その文字列を `TokFlow` によって処理し、停止文字列が見つかったかどうかを返す。
        停止文字列が見つかった場合は、その前までのテキストと見つかった停止文字列も返す。

        :param input_token_base: 入力される基底トークン。
        :param condition: トークンの配置を決定するための条件。
                condition.in_type="spot" の場合は、センテンスの差分が1文字ずつ追加される状況を想定
                condition.in_type="full" の場合は、センテンス全体に1文字ずつ追加されていく状況を想定
                condition.skip_existing_stop_str = True の場合は、最初に put した文字列に停止文字列が入っていてもそれは無視して進める
                condition.mask_char は skip_existing_stop_str が Trueの場合、最初に put した文字列内のあらゆる文字を無視させるためのマスク文字。デフォルトは「*」。停止文字列が「*」の場合は動作しなくなるため、別の文字をセットする
        :return: 停止文字列が見つかったかどうか、その前までのテキスト、見つかった停止文字列（見つかった場合）を含む辞書。
        """
        tokf = self.tokf

        input_text = input_token_base

        if condition.get("skip_existing_stop_str", False):
            mask_char = condition.get("mask_char", "*")

            if self.first_sentence is None:
                self.first_sentence = input_token_base

            len_first_sentence = len(self.first_sentence)

            input_text = mask_char * len_first_sentence + input_text[len_first_sentence:]

        output_token = tokf.put(input_text, condition)

        if condition.get("skip_existing_stop_str", False):
            # 埋めた部分を元の内容に戻す
            output_token = self.first_sentence[:len_first_sentence] + output_token[len_first_sentence:]

        if tokf.is_matched:
            matched_worker = tokf.matched_worker
            search_str = matched_worker.search_str
            replace_to_str = matched_worker.replace_to_str
            out_text = output_token[:-len(replace_to_str)]

            return {"text": out_text, "stop_str_found": True, "possible": True, "stop_str": matched_worker.search_str}
        else:
            return {"text": output_token, "stop_str_found": False, "possible": tokf.is_possible_str_started,
                    "stop_str": None}

    def flush(self, condition):
        """
        条件を受け取り、それまでの入力を全て処理する。停止文字列が見つかった場合はその前までのテキストを返し、見つからなかった場合は入力全体を返す。

        :param condition: トークンの配置を決定するための条件。
        :return: 停止文字列が見つかった場合はその前までのテキスト、見つからなかった場合は入力全体を返す。
        """
        tokf = self.tokf
        flush_text = tokf.flush(condition)

        if tokf.is_matched:
            # マッチした場合はflushもbuffering途中のものは出力されないので、結果的にflush前の最後のtextと同じものが出力される
            matched_worker = tokf.matched_worker
            replace_to_str = matched_worker.replace_to_str
            out_text = flush_text[:-len(replace_to_str)]
            return out_text
        else:
            # マッチしなかった場合は、
            # buffering中のものを出力
            not_consumed = tokf.workers[0].buffer
            return flush_text + not_consumed

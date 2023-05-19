from .tok_flow_worker import TokFlowWorker


class TokFlow:
    """
    Reads tokens (string fragments) output sequentially by the language model and outputs them
    while buffering and replacing the strings to be searched

    Tokens are sequentially read in real time.
    The token read is combined with the tokens read so far, referred to as the "token buffer".
    In this sequential process, when a pre-specified string (hereafter referred to
    as the "search target string") appears in the token buffer,
    this string is replaced with another string (hereafter referred to as the "replacement string").
    Since tokens are read sequentially, in the intermediate stage,
    a string that is unrelated to the search target string or part of the search target string accumulates
    in the token buffer. If the token buffer is composed in an order that cannot be a search target string,
    the token buffer is returned as the method's return value the moment such a determination is made.
    On the other hand, if the token buffer is composed in an order that could be a search target string,
    the return value remains an empty string until either the search target string appears or
    it is determined that it cannot be a search target string.
    In this way, by buffering until the appearance of the search target string,
    most sequential tokens can be displayed as they are, while replacement is delayed when necessary,
    enabling stream processing.

    言語モデルが逐次的に出力するトークン（文字列の断片）を読み込み、
    バッファリングしながら検索対象文字列を置換しながら出力する
    読み込んだトークンは、これまで読み込んだトークンと結合する。これまで読み込まれ結合されたトークンをトークンバッファという。
    この処理を順次行うとき、トークンバッファ内にあらかじめ指定しておいて文字列（以降、これを「検索対象文字列」と呼ぶ）が出現したとき、
    その文字列を別の文字列（以降、これを「置換先文字列」と呼ぶ）に置換する。
    トークンは逐次的に読み込まれるため、中途段階では検索対象文字列とは無関係の文字列または検索対象文字列の一部がトークンバッファに蓄積されていく。
    検索対象文字列になりえない順序でトークンバッファが構成された場合、そう判断された瞬間にトークンバッファはメソッドの戻り値として返却される。
    一方、検索対象文字列になり得る順序でトークンバッファが構成されている場合、検索対象文字列が出現するか、
    検索対象文字列になりえないと判断されるまで、戻り値は空文字となる。
    このように、検索対象文字列が出現するまでバッファリングさせることで、
    逐次トークンのほとんどはそのまま逐次表示させ、置換が必要な場合には表示を遅らせる、というストリーム処理することができる。
    """

    def __init__(self, replacer_list):
        self.replacer_list = replacer_list
        self.workers = []
        self.not_consumed_str = ""
        for from_token, to_token in replacer_list:
            self.workers.append(TokFlowWorker(from_token, to_token))

    def put(self, token_str):
        """
        本メソッドにトークンを順次インプットしていくと、検索対象文字列が置換された状態の戻り値を返す。

        逐次処理をしていくため、あらかじめすべての完成した文字列を入力する必要はない。断片（トークン）を
        put していくだけで自動的に必要な置換を行う

        検索対象文字列の一部がputされると、今後供給されるトークンによっては検索文字列が出現する可能性がある。
        このような場合の戻り値は ""(空文字) となる。

        トークンを次々に put していくと、本オブジェクト内のトークンバッファにトークン列が結合されていき
        どこかのタイミングでトークンバッファ内に検索対象文字列が出現したとき、トークンバッファ内の検索対象文字列が置換されたものが戻り値に長さ1以上の文字列が格納される
        逆に、トークンを次々 put されたのち構築されたトークンバッファ内に検索対象文字列が含まれないことが確定した段階でも、戻り値に長さ1以上の文字列が格納される

        最後のトークンを入力した後には、トークンバッファに未消費の文字列が残る可能性があるので flush メソッドを呼出すこと。
        """
        ret_val = ""

        # 複数の検索対象文字列を処理できるため、複数のワーカーを順に実行し、トークン列（トークンバッファ）にある
        # 検索対象文字列のマッチングを行う
        # ある一定の数のトークンを入力すると各ワーカーのトークンバッファ（トークン列＝トークンを結合したもの）が長くなるため
        # どれか１つのワーカーで検索対象文字列が存在した場合、そのワーカーからの出力を採用する。
        # このとき、ほかのワーカーはトークンバッファ内に検索対象文字列が発見できなかったことになる。
        # 発見できたワーカーはそのターンまでのマッチングタスクとしては役目を終えるので、クリアされ、次以降のトークン列の分析に再び使われる
        # 発見できなかったワーカーも発見できないという形でマッチングタスクは終えるので同様にクリアされ、次以降のトークン列の分析に再び使われる
        for worker in self.workers:
            # ワーカーにトークンを食わせる
            # 前ターンに仮に検索対象文字列が発見された場合は、検索対象文字列以降は未処理文字列（未消費）となるので
            # 未消費文字列＋新たなトークンを食わせる ことになる
            worker.eat(self.not_consumed_str + token_str)

        self.not_consumed_str = ""  # 未消費の文字列をクリアする

        potential = False  # True:どれか1つ以上のワーカーがマッチングのポテンシャルがある状態
        matched = False  # True: どれか1つのワーカーが検索対象文字列を発見した場合

        ttl_num_of_not_appearred = 0

        pending_str = ""

        for worker in self.workers:

            if worker.search_str_appeared:
                # このワーカーが担当する検索文字列の出現が確認された
                ret_val = worker.converted
                self.not_consumed_str = worker.str_to_be_process_next
                # 　1つ正解した
                # ほかのすべてのマッチャーをクリアすべき
                for _worker in self.workers:
                    _worker.clear()

                matched = True


            elif worker.str_matching_started:
                potential = True
                pass
            elif worker.confirmed_not_to_appear:
                # 本ワーカーが現在までトークン列を分析したところ、
                # 本ワーカー対象の検索対象文字列が発見できないことが確定した場合

                # すべてのワーカーが検索対象文字列を発見できなかったのか判定するためにカウンターを+1する
                ttl_num_of_not_appearred = ttl_num_of_not_appearred + 1

                # すべてのワーカーが検索対象文字列を発見できなかった場合、
                # それまでにワーカーに詰めていったトークン列（トークンバッファ）を
                # 吐き出させるためにキャッシュする
                # （どのワーカーからも同じものがでてくる)
                pending_str = worker.buffer
                worker.clear()  # ワーカーをクリアする（現在までの処理履歴に関する変数をクリア)その後ワーカーは再利用される

            else:
                pass

        if ttl_num_of_not_appearred == len(self.workers):
            # すべてのワーカーが検索対象文字列を発見できないことが確定した場合、
            # トークンバッファはそのまま出力すればいいので、そのまま返す
            return pending_str

        if not potential and not matched:
            # 検索対象文字列の出現可能性がなく、かつ、検索対象文字列の出現もしていない場合
            # ワーカーの1つから、マッチしなかった文字列を戻り値とする
            # 度のワーカーでも同じ unmatched_str を保持しているため、便宜的に0番目を返している
            ret_val = self.workers[0].unmatched_str
            pass

        return ret_val

    def flush(self):
        """
        put処理が終了したあと、未消費のトークンバッファが残っている場合があるため、
        すべてのput処理が終了したあと、本メソッドを呼出し未消費のトークンバッファを取得する
        未消費のトークンバッファが存在すればそれも出力対象とする
        """
        return self.not_consumed_str

    def get_workers(self):
        return self.workers

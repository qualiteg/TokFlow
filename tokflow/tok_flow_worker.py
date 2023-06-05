class TokFlowWorker:

    def __init__(self, target_str, replace_to_str):
        self.replace_to_str = replace_to_str
        self.search_str = target_str
        self.search_str_appeared = False  # True: 検索対象文字列が発見された
        self.is_possible_str_started = False  # True:現在、走査しているトークンが検索文字列に一致しはじめた（ポテンシャルあり）状態
        self.buffer = ""  # トークンバッファ。処理に準じてトークンが加えられていく
        self.str_to_be_process_next = ""  # 次に処理していくときの残り
        self.converted = ""  # 無事に置換成功した出力対象
        self.str_expected_to_appear = ""
        self.confirmed_not_to_appear = False  # いっかい potential True になったものがダメになった場合 dispose にする
        self.unmatched_str = ""

    def clear(self):
        """
        これまでの処理を初期化する
        """
        self.search_str_appeared = False
        self.is_possible_str_started = False
        self.buffer = ""
        self.str_to_be_process_next = ""
        self.converted = ""
        self.str_expected_to_appear = ""
        self.confirmed_not_to_appear = False
        self.unmatched_str = ""

    def eat(self, token):

        self.buffer += token

        if not self.is_possible_str_started:
            # まだ「ポテンシャルあり」となっていない場合
            # （「ポテンシャルあり」とは、現在までのトークンバッファ（与えられたトークンを順に結合したもの）が
            # 今後成長していくと、検索対象文字列を含む可能性がある状態のこと。）

            if self.search_str in self.buffer:
                # - トークンバッファ内に、検索対象文字列がまるごと入っていた場合

                # 最後に self.search_str が登場する以降を取得
                part_after_search_str = self.extract_after_last_nl(self.search_str, self.buffer)

                # 最後に登場する self.search_str　までを取得
                part_before_last_search_str = self.extract_until_last_nl(self.search_str, self.buffer)

                # 検索対象文字列を置換先文字列に置換する
                self.converted = part_before_last_search_str.replace(self.search_str, self.replace_to_str)

                # 検索対象文字列以降は、次ターンのトークン処理でつかうために申し送る
                self.str_to_be_process_next = part_after_search_str

                # 検索対象文字列　出現フラグを立てる
                self.search_str_appeared = True

                self.is_possible_str_started = True
                return
            else:
                # - トークンバッファ内に、検索対象文字列がまるごと入ってはいない場合

                len_search_str = len(self.search_str)

                # 検索対象文字列の一部でも入っているか
                is_at_least_piece_of_search_str_matched = False
                # 一部でもはいっていないかどうか1文字ずつへらしていって確認する
                for i in range(len_search_str - 1, 0, -1):
                    left_n_size_part_of_piece = self.search_str[:i]

                    str_to_expect_next = self.search_str[i:]
                    # 検索対象文字列が "<NL>" を例とすると、
                    # 例えば 現在のトークンバッファが "abc<N" のような状態であるとき、
                    # つまり今後与えられるトークンをトークンバッファに加えていくと "abc<NL>" のように
                    # 検索対象文字列が出現するとき、「ポテンシャルあり」とみなす。
                    #
                    # 本処理では、 "abc<N" のように 検索対象文字列 "<NL>" の　”かけら”（left_n_size_part_of_piece） が
                    # トークンバッファの末尾に存在しないかどうかを確認していく。
                    # ポテンシャルありとなる、トークンバッファの末尾は、 "かけら"（left_n_size_part_of_piece） を順に短くしていき確認していく。
                    # STEP1."<NL"
                    # STEP2."<N"
                    # STEP3."<"
                    if self.buffer.endswith(left_n_size_part_of_piece):

                        # 検索文字列のかけらがトークンバッファの末尾に存在した場合
                        # is_at_least_piece_of_search_str_matched = True #
                        self.is_possible_str_started = True  # ポテンシャルあり　にする

                        # かけら　が　"<NL"　の場合は ">" に出現してほしい
                        # かけら　が "<N" の場合は、 "L>" に出現してほしい
                        # かけら　が "<" の場合は、 "NL>" に出現してほしい
                        self.str_expected_to_appear = str_to_expect_next  # 次以降に出現してほしい文字列をセットする
                        break

                if not self.is_possible_str_started:
                    # ポテンシャルがなかった場合
                    # (トークンバッファに小さな　"かけら" すらなかった場合)
                    self.unmatched_str = self.buffer
                    self.buffer = ""

                    pass

        else:
            # ポテンシャルあり となり、検索対象文字列のマッチングが開始している場合

            # このアプローチだと、検索対象が「<NLL>」で、「L>」をまってるときに、バッファが<NL>のときに
            # バッファ「<NL>」に「L>」をみつけてしまうのでNG
            #if self.str_expected_to_appear in self.buffer:

            if self.search_str in self.buffer:
                # - 出現待ちになっている文字列がまるごとトークンバッファに存在した場合
                #
                # (たとえば、前回ターンのトークンバッファが "abc<" で　今回ターンのトークンバッファが "NL>" のようになったタイミング)

                self.str_to_be_process_next = self.extract_after_last_nl(self.search_str,
                                                                         self.buffer)  # 最後に self.search_str が登場する以降を取得

                part_before_last_search_str = self.extract_until_last_nl(self.search_str,
                                                                         self.buffer)  # 最後に登場する self.search_str　までを取得

                self.converted = part_before_last_search_str.replace(self.search_str, self.replace_to_str)
                self.search_str_appeared = True

                pass
            else:
                # 出現待ちになっている文字列がまるごとは来ていなかった場合

                # たとえば、前回ターンが "abc<" で　今回ターンが "NL" のようなパターンの可能性をさぐる
                len_search_str = len(self.str_expected_to_appear)

                # 上記のようなパターンの場合以下のフラグを立てて、マッチング（検索文字列の検出を引き続きこころみる）を続ける
                need_continue_to_matching = False

                for i in range(len_search_str - 1, 0, -1):  # -1 してるのは length の場合はフル一致のため

                    # "NL>" を "NL" "N" に分解して、一部でもマッチしていないか確認する
                    part_of_waiting = self.str_expected_to_appear[:i]


                    # "NL>" を "NL" に分解したときの、残りパート ">"
                    # "NL>" を "N" に分解したときの残りパート "L>"
                    rest_of_waiting = self.str_expected_to_appear[i:]

                    if token.startswith(part_of_waiting):

                        # 文字ピースが "NL>" のように出現待ちで開始している場合
                        need_continue_to_matching = True  # 引き続きマッチングを続ける
                        self.str_expected_to_appear = rest_of_waiting

                if not need_continue_to_matching:
                    # 現時点で、検索文字列との一致可能性がなくなった場合

                    # 今ターンまでのマッチング処理を行ったが、出現しないことが確定したので、
                    # （一旦）役目終了のフラグをたてる
                    self.confirmed_not_to_appear = True
                    self.is_possible_str_started = False

    def extract_after_last_nl(self, target, text):
        split_text = text.rsplit(target, 1)  # '<NL>'で文字列を最後から分割し、最大分割数を1に設定
        after_last_nl = split_text[1] if len(split_text) > 1 else split_text[0]
        return after_last_nl

    def extract_until_last_nl(self, target_str, text):
        split_text = text.rsplit(target_str, 1)  # target_str で文字列を最後から分割し、最大分割数を1に設定
        until_last_nl = split_text[0] if len(split_text) > 1 else split_text[0]

        if len(split_text) > 1:
            until_last_nl += target_str

        return until_last_nl

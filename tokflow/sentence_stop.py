from tokflow import TokFlow


class SentenceStop:
    def __init__(self, stop_strs):

        self.stop_strs = stop_strs

        self.to_replace_word = "\n"
        tuples = [(stop_str, self.to_replace_word) for stop_str in self.stop_strs]

        self.tokf = TokFlow(tuples)

    def put(self, input_token_base, condition):

        tokf = self.tokf

        output_token = tokf.put(input_token_base, condition)

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

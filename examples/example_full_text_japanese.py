import sys

sys.path.append('../')

import time
from tokflow import TokFlow

from data.example_text_data_full_stream_long_ja import get_example_texts

TEXTS = get_example_texts()

# replace "<NL>" with "\n". "<NL>" is called "search target string".
# Multiple replacement conditions can be specified.
tokf = TokFlow([("<NL>", "\n")])

prev = ""
condition = {"in_type": "full", "out_type": "full"}
for input_token_base in TEXTS:
    output_token = tokf.put(input_token_base, condition)
    # Input sequential tokens.
    # If there is a possibility that the token is a "search target string",
    # it is buffered for a while, so output_token may be empty for a while.
    print(f"{output_token}")
    print("-----------------------------------")
    # Included wait to show the sequential generation operation.
    time.sleep(0.05)

# Remember to output the remaining buffer at the very end. Buffers may be empty characters.
print(f"{tokf.flush()}", end="", flush=True)

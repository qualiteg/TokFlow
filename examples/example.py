import sys

sys.path.append('../')

import time
from tokflow import TokFlow

TOKEN_GENERATOR_MOCK = ["He", "llo", " ", "t", "h", "ere", "!<", "N", "L>m", "y ", "nam", "e", " ", "is", " tokfl", "ow.",
                  "<", "N", "L>N", "ice", " to ", "me", "et you."]

# replace "<NL>" with "\n". "<NL>" is called "search target string".
# Multiple replacement conditions can be specified.
tokf = TokFlow([("<NL>", "\n")])

for input_token in TOKEN_GENERATOR_MOCK:

    output_token = tokf.put(input_token)

    # Input sequential tokens.
    # If there is a possibility that the token is a "search target string",
    # it is buffered for a while, so output_token may be empty for a while.
    print(f"{output_token}", end="", flush=True)

    # Included wait to show the sequential generation operation.
    time.sleep(0.3)


# Remember to output the remaining buffer at the very end. Buffers may be empty characters.
print(f"{tokf.flush()}", end="", flush=True)

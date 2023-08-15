# TokFlow

[English](README.md)

大規模言語モデルにより逐次的に生成されるトークンをバッファリングし、必要な置換処理を行いながら出力するユーティリティ

## 本ライブラリは何ができる？

下のように小さな かけら のようになった文章の断片＝トークンを逐次入力したとき、置換が必要な文字列を順次置換しながら出力する。

このとき、トークンのバッファリングして遅延出力を行うことで、置換前のトークンは出力しないようにできる

```python
["He","llo"," ","t","h","ere","!<","N","L>m","y ","nam","e"," ","is"," tokfl","ow.","<","N","L>N","ice"," to ","me","et you."]
```

この例では、 `<NL>` の出現を検知し `\n` に置換しながら出力する。

<img src="tokflow.gif">


- 置換条件として、好きな文字列を置換対象に指定可能
- 複数の置換条件を指定可能


## 本ライブラリの用途は？

大規模言語モデルによる逐次文章生成で特殊トークンを逐次置換しながら出力する用途のために開発したが、ほかの文字列ストリーム処理でも活用可能。

# インストール

```
pip install tokflow
```

# 使い方/サンプルコード

```python
import time
from tokflow import TokFlow

TOKEN_GENERATOR_MOCK = ["He", "llo", " ", "t", "h", "ere", "!<", "N", "L>m", "y ", "nam", "e", " ", "is", " tokfl", "ow.",
                  "<", "N", "L>N", "ice", " to ", "me", "et you."]

# "<NL>" を "\n" に置換する。 "<NL>" は検索対象文字列。 "n" は置換先文字列
# 置換条件は複数指定可能。
tokf = TokFlow([("<NL>", "\n")])

for input_token in TOKEN_GENERATOR_MOCK: 
    # トークン（文章のかけらとなる1,2文字程度の文字列）を順次入力していく。トークンは内部でバッファリングされる。
    output_token = tokf.put(input_token)

    # output_token に今出力可能な出力トークンが出力される。
    # トークンのバッファリング中に検索対象文字列が出現する可能性がある場合は
    # 出力トーンは空文字となる。
    print(f"{output_token}", end="", flush=True)

    # 逐次生成されることを目視するため、ウェイトをはさむ
    time.sleep(0.3)


# トークンの入力が終わったら、最後に flush して残っているバッファを出力し切る
print(f"{tokf.flush()}", end="", flush=True)

```


<img src="tokflow.gif">


# 生成オプション

`put` メソッドには `put(text,opts)` のように オプションパラメータ `opts` を指定することが可能です

opts は `{"in_type":"spot","out_type:"spot" }` のように入力の形式と出力の形式を指定することが可能です。

以下のように挙動します。

| in_type  | out_type | Description                                    |
| :------- | :------- |:-----------------------------------------------|
| spot     | spot     | トークンを `put` メソッドに逐次送り、生成分のみ都度出力するモード。          |
| spot     | full     | トークンを `put` メソッドに逐次送り、フルセンテンスを出力するモード。         |
| full     | spot     | フルセンテンスを一度に `put` メソッドに送り、生成分のみ都度出力するモード。          | |
| full     | full     | フルセンテンスを一度に `put` メソッドに送り、フルセンテンスを出力するモード。      |

注意点：
- `flush` メソッドを呼び出す前に全ての文字列を `put` メソッドに送る必要があります。特に `full` モードでは、全ての入力文字列を一度に送ります。
- 出力のタイプ (`out_type`) が `full` の場合、最終的な結果を取得するためには `flush` メソッドを呼び出す必要があります。
- それぞれのモードで一貫性を保つためには、`put` メソッドの呼び出しパターンと `flush` メソッドの使用を適切に組み合わせることが重要です。

**コード例**

`condition = {"in_type": "full", "out_type": "full"}` のようにルールを指定し、 `put` および `flush` の引数に `condition` を指定します。



```python
    tokf = TokFlow([("<NL>", "\n")])

    condition = {"in_type": "full", "out_type": "full"}
    prev_len = 0
    for input_token_base in get_example_texts():
        output_sentence = tokf.put(input_token_base, condition)

        print(f"output_sentence:{output_sentence}")

        if prev_len > len(output_sentence):
            raise ValueError("Length error")

        if "<NL>" in output_sentence:
            raise Exception("Failure Must be converted str found.")

        prev_len = len(output_sentence)

    output_sentence = tokf.flush(condition)
```



# 停止文字列を検出して文章生成を停止する SentenceStopクラス

SentenceStopクラスは、特定のキーワードを検出し、そのキーワードが見つかった時点でテキスト生成を停止するためのクラスです。テキストは1文字ずつ入力されるシチュエーションを想定しています。

## 主な機能

- **特定のキーワードの検出**: 文字列内の特定のキーワードを検出します。検出したキーワードは停止文字列として扱われます。
- **テキスト生成の停止**: 検出した停止文字列の位置でテキスト生成を停止します。具体的には、停止文字列が検出された時点でのテキストを返します。
- **リアルタイム処理**: 文字列が1文字ずつ入力されるシチュエーションを想定しており、リアルタイムでの処理が可能です。

## 使用方法

初期化時には停止するためのキーワードを指定します。その後、`put`メソッドで1文字ずつ入力を行い、停止文字列が見つかった場合にはその時点でのテキストを返します。全ての入力が終わった場合には、`flush`メソッドを用いて残りのテキストを出力します。


`put` メソッドには `put(text,opts)` のように オプションパラメータ `opts` を指定することが可能です

opts は `{"in_type":"spot","out_type:"spot","skip_existing_stop_str":True }` の形式をとります。

### in_type と out_type について

以下のように挙動します。

| in_type  | out_type | Description                                    |
| :------- | :------- |:-----------------------------------------------|
| spot     | spot     | トークンを `put` メソッドに逐次送り、生成分のみ都度出力するモード。          |
| spot     | full     | トークンを `put` メソッドに逐次送り、フルセンテンスを出力するモード。         |
| full     | spot     | フルセンテンスを一度に `put` メソッドに送り、生成分のみ都度出力するモード。          | |
| full     | full     | フルセンテンスを一度に `put` メソッドに送り、フルセンテンスを出力するモード。      |


### skip_existing_stop_str について

`skip_existing_stop_str:True` にした場合、
初回の `put` 時に指定した text に、停止文字列が含まれていた場合でも、そこで停止処理は発生させない。


### サンプルその１

```python
import sys

sys.path.append('../')

import time
from tokflow import SentenceStop

"""
ストリーミングされるセンテンスを指定した停止文字列 "<NL>" を検出した段階で停止させる
"""

FULL_STREAM_TEXTS = texts = [
    'は',  #
    'はい',  #
    'はい、',  #
    'はい、こちら',  #
    'はい、こちらを',  #
    'はい、こちらをお',  #
    'はい、こちらをお勧め',  #
    'はい、こちらをお勧めします',  #
    'はい、こちらをお勧めします。',  #
    'はい、こちらをお勧めします。<',  #
    'はい、こちらをお勧めします。<N',  #
    'はい、こちらをお勧めします。<NL',  #
    'はい、こちらをお勧めします。<NL>',  #
    'はい、こちらをお勧めします。<NL><',  #
    'はい、こちらをお勧めします。<NL><N',  #
    'はい、こちらをお勧めします。<NL><NL',  #
    'はい、こちらをお勧めします。<NL><NL>',  #
    'はい、こちらをお勧めします。<NL><NL>「',  #
    'はい、こちらをお勧めします。<NL><NL>「ハチ',  #
    'はい、こちらをお勧めします。<NL><NL>「ハチ公',  #
    'はい、こちらをお勧めします。<NL><NL>「ハチ公像',  #
    'はい、こちらをお勧めします。<NL><NL>「ハチ公像」',  #
    'はい、こちらをお勧めします。<NL><NL>「ハチ公像」は',  #
    'はい、こちらをお勧めします。<NL><NL>「ハチ公像」は、',  #
    'はい、こちらをお勧めします。<NL><NL>「ハチ公像」は、最も有名な',  #
]

sens = SentenceStop(["<NL>"])

condition = {"in_type": "full", "out_type": "full"}

for input_token_base in FULL_STREAM_TEXTS:

    out = sens.put(input_token_base, condition)

    text = out.get("text")  # 出力すべきテキスト
    stop_str_found = out.get("stop_str_found")  # 停止文字列が検出された か否か
    possible = out.get("possible")  # 停止文字列を検出しかかっている　か否か
    stop_str = out.get("stop_str")  # 停止文字列（複数の停止文字列を指定していた場合、どの停止文字列が検出されたのか)

    print(f"text:'{text}' possible:{possible} stop_str_found:{stop_str_found} stop_str:{stop_str}")
    if stop_str_found:
        # 停止文字列が検出された場合、処理を停止する
        break
    time.sleep(0.01)

if not stop_str_found:
    # 最後までいっても、停止文字列が検出されなかった場合
    # ペンディング中のテキストを出力しきる
    # (停止文字列が検出された場合は、停止文字列の直前までの文字列が出力されるためflushは不要)
    print(f"flush:{sens.flush(condition)}", end="", flush=True)

```


`<NL>` を検出した時点で、`stop_str_found` フラグが `True` となり、 `はい、こちらをお勧めします。` で文章生成を停止することができる。


### サンプルその２　停止文字列を含む場合

以下のように `condition = {"in_type": "full", "out_type": "full", "skip_existing_stop_str": True}` で
`"skip_existing_stop_str": True}` を指定している場合、初回に入力するテキスト `はい、<NL>こちらを` には停止文字列
`<NL>` を含んでいるが、初回テキストにある`<NL>` は停止文字列と扱わずスキップする。


```python
import sys

sys.path.append('../')

import time
from tokflow import SentenceStop

"""
既に停止文字列 "<NL>"が存在しているパートから開始された場合、
既存分はスキップして、次以降でストリーミングされるセンテンスを指定した停止文字列 "<NL>" を検出した段階で停止させる
"""

FULL_STREAM_TEXTS = texts = [
    'はい、<NL>こちらを',  #
    'はい、<NL>こちらをお',  #
    'はい、<NL>こちらをお勧',  #
    'はい、<NL>こちらをお勧め',  #
    'はい、<NL>こちらをお勧めし',  #
    'はい、<NL>こちらをお勧めしま',  #
    'はい、<NL>こちらをお勧めします',  #
    'はい、<NL>こちらをお勧めします。',  #
    'はい、<NL>こちらをお勧めします。<',  #
    'はい、<NL>こちらをお勧めします。<N',  #
    'はい、<NL>こちらをお勧めします。<NL',  #
    'はい、<NL>こちらをお勧めします。<NL>',  #
    'はい、<NL>こちらをお勧めします。<NL>「',  #
    'はい、<NL>こちらをお勧めします。<NL>「ハチ',  #
    'はい、<NL>こちらをお勧めします。<NL>「ハチ公',  #
    'はい、<NL>こちらをお勧めします。<NL>「ハチ公像',  #
    'はい、<NL>こちらをお勧めします。<NL>「ハチ公像」',  #
    'はい、<NL>こちらをお勧めします。<NL>「ハチ公像」は',  #
    'はい、<NL>こちらをお勧めします。<NL>「ハチ公像」は、',  #
    'はい、<NL>こちらをお勧めします。<NL>「ハチ公像」は、最も有名な',  #
]

sens = SentenceStop(["<NL>"])

condition = {"in_type": "full", "out_type": "full", "skip_existing_stop_str": True}

for input_token_base in FULL_STREAM_TEXTS:

    out = sens.put(input_token_base, condition)

    text = out.get("text")  # 出力すべきテキスト
    stop_str_found = out.get("stop_str_found")  # 停止文字列が検出された か否か
    possible = out.get("possible")  # 停止文字列を検出しかかっている　か否か
    stop_str = out.get("stop_str")  # 停止文字列（複数の停止文字列を指定していた場合、どの停止文字列が検出されたのか)

    print(f"text:'{text}' possible:{possible} stop_str_found:{stop_str_found} stop_str:{stop_str}")
    if stop_str_found:
        # 停止文字列が検出された場合、処理を停止する
        break
    time.sleep(0.01)

if not stop_str_found:
    # 最後までいっても、停止文字列が検出されなかった場合
    # ペンディング中のテキストを出力しきる
    # (停止文字列が検出された場合は、停止文字列の直前までの文字列が出力されるためflushは不要)
    print(f"flush:{sens.flush(condition)}", end="", flush=True)

```

# 処理設計

## ストリーム置換処理について

逐次的に出現するトークン（文字列の断片）を順次読み込み、
読み込んだトークンは、これまで読み込んだトークンと結合する。

これまで読み込まれ結合されたトークンをトークンバッファと呼ぶ。

この処理を順次行うとき、トークンバッファ内にあらかじめ指定しておいて文字列（以降、これを「検索対象文字列」と呼ぶ）が出現したとき、
その文字列を別の文字列（以降、これを「置換先文字列」と呼ぶ）に置換する。


トークンは逐次的に読み込まれるため、中途段階では検索対象文字列とは無関係の文字列または検索対象文字列の一部がトークンバッファに蓄積されていく。

検索対象文字列になりえない順序でトークンバッファが構成された場合、
そう判断された瞬間にトークンバッファはメソッドの戻り値として返却される。


一方、検索対象文字列になり得る順序でトークンバッファが構成されている場合、検索対象文字列が出現するか、
検索対象文字列になりえないと判断されるまで、戻り値は空文字となる。


このように、検索対象文字列が出現するまでバッファリングさせることで、逐次トークンのほとんどはそのまま逐次表示させ、置換が必要な場合には表示を遅らせる、というストリーム処理することができる。


# TokFlow ライセンス

## オープンソースライセンス

本プロジェクトには

[GNU General Public License version 3 (GPLv3)](https://www.gnu.org/licenses/gpl-3.0.html)

が適用されます。GPLv3の範囲内でご自由にお使いいただけます。

GPLv3範囲外でご利用したい場合には、以下、商用/OEM ライセンスをご検討ください。

## 商用/OEM ライセンス

もしこのライブラリを貴社ツールキット等に含めて GPLv3 以外のライセンスで配布したい場合、
商用で利用したい場合は、商用/OEMライセンスの取得が必要となります。
商用/OEMライセンスは案件ごとにカスタマイズしたものとなりますので、お気軽にご相談ください。 `riversun.org@gmail.com`

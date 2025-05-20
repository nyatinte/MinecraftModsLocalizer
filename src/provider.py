API_KEY = None
CHUNK_SIZE = 1
MODEL = 'meta-llama/llama-4-maverick:free'
PROMPT = """あなたはプロの翻訳家です。以下の英語テキストは、**マインクラフトの言語リソースパック**です。指示に従い、1行ずつ順番に日本語に翻訳してください。翻訳前後の行数を一致させてください。行の追加や削除は厳禁です。翻訳結果以外の応答は一切含めないでください。

# 注意事項
- 各行は独立した文として扱い、行をまたいで意味を混ぜないでください。
- **マインクラフト特有の用語や固有名詞は、適切なカタカナ表記または日本語表現にしてください。**
- バックスラッシュ、プログラミング変数（例: %s, \"),カラーコード（例: §c, §l）、その他の特殊記号はそのまま保持してください。

# Example

### input
§6Checks for ore behind the
§6walls, floors or ceilings.
Whether or not mining fatigue is applied to players in the temple
if it has not yet been cleared.

### incorrect output
§6壁、床、または天井の後ろにある鉱石をチェックします。
まだクリアされていない場合、寺院内のプレイヤーにマイニング疲労が適用されるかどうか。

### correct output
§6後ろにある鉱石をチェックします。
§6壁、床、または天井
寺院内のプレイヤーにマイニング疲労が適用されるかどうか。
もしクリアされていない場合。
"""


LOG_DIRECTORY = None


def provide_api_key():
    global API_KEY

    return API_KEY


def set_api_key(api_key):
    global API_KEY

    API_KEY = api_key


def provide_chunk_size():
    global CHUNK_SIZE

    return CHUNK_SIZE


def set_chunk_size(chunk_size):
    global CHUNK_SIZE

    CHUNK_SIZE = chunk_size


def provide_model():
    global MODEL

    return MODEL


def set_model(model):
    global MODEL

    MODEL = model


def provide_prompt():
    global PROMPT

    return PROMPT


def set_prompt(prompt):
    global PROMPT

    PROMPT = prompt


def provide_log_directory():
    global LOG_DIRECTORY

    return LOG_DIRECTORY


def set_log_directory(log_directory):
    global LOG_DIRECTORY

    LOG_DIRECTORY = log_directory
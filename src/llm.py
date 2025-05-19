import logging
import re
import time
from litellm import completion

from provider import provide_api_key, provide_model, provide_prompt


def translate_with_llm(split_target, timeout):
    start_time = time.time()
    result = []

    # 改行を削除(翻訳時扱いがめんどくさいため)
    split_target = [line.replace('\\n', '').replace('\n', '') for line in split_target] if len(split_target) > 1 else split_target

    # APIキーを取得
    api_key = provide_api_key()
    # モデル名を取得
    model = provide_model()

    try:
        # LiteLLM + OpenRouterを用いて翻訳を行う
        response = completion(
            model=model,
            api_key=api_key,
            messages=[
                {
                    "role": "system",
                    "content": provide_prompt().replace('{line_count}', str(len(split_target)))
                },
                {
                    "role": "user",
                    "content": '\n'.join(split_target)
                }
            ],
        )

        # 翻訳結果を取得
        if response.choices and response.choices[0].message:
            translated_text = response.choices[0].message.content
            result = translated_text.splitlines() if len(split_target) > 1 else [translated_text.replace('\n', '')]
            result = [re.sub(r'(?<!\\)"', r'\\"', line) for line in result]
        else:
            logging.error("Failed to get a valid response from the language model.")

    except Exception as e:
        elapsed_time = time.time() - start_time
        if elapsed_time > timeout:
            logging.error("Timeout reached while waiting for translation.")
        logging.error(f"Error during translation: {str(e)}")

    return result

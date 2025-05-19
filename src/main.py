import TkEasyGUI as sg
from pathlib import Path
import logging
from datetime import datetime

from provider import set_api_key, set_chunk_size, provide_chunk_size, set_model, provide_model, set_prompt, provide_prompt, set_log_directory
from mod import translate_from_jar
from quests import translate_ftbquests, translate_betterquesting
from patchouli import translate_patchouli
from log import setup_logging
from update import check_version


if __name__ == '__main__':
    # レイアウトの定義
    layout = [
        [sg.Text("Translate Target", font=('Helvetica', 10, 'bold'))],
        [sg.Radio('Mod', key='target1', group_id=1, default=True), sg.Radio('FtbQuests', key='target2', group_id=1), sg.Radio('BetterQuesting', key='target3', group_id=1), sg.Radio('Patchouli', key='target4', group_id=1)],
        [sg.Text("OpenRouter API KEY", font=('Helvetica', 10, 'bold'))],
        [sg.InputText(key='OPENAI_API_KEY', expand_x=True)],
        [sg.Text("Chunk Size")],
        [sg.Text("単体mod翻訳、クエスト、Patchouliの翻訳では1\nModPackで大量のModを一括で翻訳するときは100くらいまで上げることをお勧めします(1だと翻訳時間がすごいことになります)")],
        [sg.Slider(range=(1, 200), key='CHUNK_SIZE', default_value=provide_chunk_size(), expand_x=True)],
        [sg.Text("Model (例: google/gemini-2.5-flash-preview)")],
        [sg.Text("※自動的に'openrouter/'というプレフィックスが付与されます")],
        [sg.InputText(key='MODEL', expand_x=True)],
        [sg.Text("Prompt", font=('Helvetica', 10, 'bold'))],
        [sg.Multiline(key='PROMPT', default_text=provide_prompt(), expand_x=True, size=(None, 10))],
        [sg.VPush()], # 垂直方向のスペース追加
        [sg.Button("Translate", key='translate', size=(15, 1), font=('Helvetica', 10, 'bold'))]
    ]

    # ウィンドウの作成 - サイズを大きくして余白を追加
    window = sg.Window('MinecraftModLocalizer', layout, size=(900, 600), margins=(20, 20), finalize=True)
    
    # 全てのテキスト要素のフォントを設定し、より見やすくする
    for key in window.key_dict:
        if isinstance(window[key], sg.Text):
            window[key].update(font=('Helvetica', 10))

    # 現在の日時を取得
    now = datetime.now()

    # ファイル名として安全な形式に日時を整形
    # 例：2023-10-15_17-30-29
    current_time = now.strftime("%Y-%m-%d_%H-%M-%S")

    # ログを保存するディレクトリを指定
    log_directory = Path(f"./logs/localizer/{current_time}")

    # ログの設定
    setup_logging(log_directory)
    set_log_directory(log_directory)

    # イベントループ
    while True:
        event, values = window.read()

        # ウィンドウのクローズボタンが押された場合
        if event == sg.WIN_CLOSED:
            break

        # 送信ボタンが押された場合
        if event == 'translate':
            # 入力された値を取得
            set_api_key(values['OPENAI_API_KEY'])
            set_chunk_size(int(values['CHUNK_SIZE']))
            
            # モデル名が入力されているか確認
            if not values['MODEL']:
                sg.popup('モデル名を入力してください。例: google/gemini-2.5-flash-preview')
                continue
            
            # openrouterプレフィックスを追加
            model_name = 'openrouter/' + values['MODEL']
            set_model(model_name)
            set_prompt(values['PROMPT'])

            # バージョンチェック
            if not check_version():
                sg.popup('最新バージョンがあるよ。バージョンアップしてね！')
                break

            try:
                if values['target1']:
                    translate_from_jar()
                elif values['target2']:
                    translate_ftbquests()
                elif values['target3']:
                    translate_betterquesting()
                elif values['target4']:
                    translate_patchouli()
            except Exception as e:
                logging.error(e)
                sg.popup('翻訳失敗')
                break


            # if values['target1']:
            #     translate_from_jar()
            # elif values['target2']:
            #     translate_ftbquests()
            # elif values['target3']:
            #     translate_betterquesting()
            # elif values['target4']:
            #     translate_patchouli()

            sg.popup('翻訳成功！')
            break

import modules.ui as ui
import re
from modules import sd_models

# 元の関数をとっとく！
original_update_token_counter = ui.update_token_counter

def custom_update_token_counter(text, steps, styles, *, is_positive=True):
    # まず元の処理を呼ぶ（HTMLが返ってくる）
    original_html = original_update_token_counter(text, steps, styles)

    # 元処理の情報を取得する
    # トークンが？ならまだ処理できないので飛ばす
    match = re.search(r">(\d+)\s*/\s*(\d+)<", original_html)
    if match:
      token_count = match.group(1)
      max_length = match.group(2)
    if token_count is "?":
        return original_html

    # プロンプト分割していろいろ
    get_prompt_lengths_on_ui = sd_models.model_data.sd_model.get_prompt_lengths_on_ui

    extended_inner_table = "<tr><th>prompt</th><th>token</th><th>total</th></tr>"
    sum = 0
    title = ""
    bkpt = 75   # 75区切りということなので
    # カンマ区切りのプロンプトを分割して、各プロンプトのトークン数を取得
    for p in str(text).removeprefix("['").removesuffix("']").split(","):
        p = p.strip()
        if not p:
            continue
        # ここでトークン数と最大値を取得
        t, _ = get_prompt_lengths_on_ui(p + ",")
        # モデルの読み込みが終わるまではここに来ないはず
        sum += t
        temp_tooltip = f"{p} -> {t} | ({sum:03})"
        temp = f"<tr><th>{p}</th><td>{t}</td><td>{sum:03}</td></tr>\n"
        # 最大値を超えたらワンセット
        if sum > bkpt:
            bkpt += 75
            title += temp_tooltip + "\n"
            temp = f'<tr class="patch_token_counter_75HL"><th style="color: inherit;">{p}</th><td style="color: inherit;">{t}</td><td style="color: inherit;">{sum:03}</td></tr>\n'
        extended_inner_table += temp

    # HTMLを作る〜✨
    # clickでテーブル表示、tableからleaveでtable非表示
    # ポジネガ判定
    additional_class = f"patch_token_counter_{'p' if is_positive else 'n'}" 
    show_table = f'document.querySelector(".{additional_class}").style = ""'
    hide_table = f'document.querySelector(".{additional_class}").style = "display:none;"'
    # 追加のHTML
    extened_html = f"<div style='display:none;' onclick='{hide_table}' class='{additional_class}'><table>{extended_inner_table}</table></div>"
    # 既存のHTMLのアップグレード
    return f"<span class='gr-box gr-text-input' title='{title}' onclick='{show_table}'>{token_count}/{max_length}</span>" + extened_html

# 上書き〜！こわくないよ！たぶん！
ui.update_token_counter = custom_update_token_counter

import os
import gradio as gr
import modules.script_callbacks as script_callbacks

def inject_custom_css(app, launch_config):  # ← 引数2つにしてね！
    css_path = os.path.join(os.path.dirname(__file__), "..", "style.css")
    if os.path.exists(css_path):
        with open(css_path, "r", encoding="utf-8") as f:
            css = f.read()
        gr.update(css=css)  # グローバルにCSS注入！

script_callbacks.on_app_started(inject_custom_css)

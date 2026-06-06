import gradio as gr
from converter import convert_novel
import tempfile

def process_file(file):
    if file is None:
        return "请上传文件", None
    with open(file.name, 'r', encoding='utf-8') as f:
        novel_text = f.read()
    if len(novel_text) < 200:
        return "文本太短，请至少提供三章内容（约2000字以上）", None
    yaml_str = convert_novel(novel_text)
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False, encoding='utf-8') as tmp:
        tmp.write(yaml_str)
        tmp_path = tmp.name
    return yaml_str, tmp_path

def process_text(text):
    if not text or len(text) < 200:
        return "文本太短，请至少提供三章内容", None
    yaml_str = convert_novel(text)
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False, encoding='utf-8') as tmp:
        tmp.write(yaml_str)
        tmp_path = tmp.name
    return yaml_str, tmp_path

def placeholder():
    return "功能开发中"

with gr.Blocks(title="小说转剧本工具", theme=gr.themes.Soft()) as demo:
    with gr.Row():
        # 左侧任务栏（调整后的布局）
        with gr.Column(scale=1, min_width=180):
            gr.Markdown("## 🛠️ 工具菜单")
            gr.Markdown("---")
            gr.Markdown("**更多规划功能**")
            # btn_font = gr.Button("调整字体/背景", variant="secondary")
            # btn_polish = gr.Button("AI润色帮手", variant="secondary")
            gr.Button("调整字体/背景", interactive=False)
            gr.Button("AI润色助手", interactive=False)
            gr.Button("角色关系图", interactive=False)
            gr.Button("台词提取", interactive=False)
            # 绑定占位回调
            # btn_font.click(placeholder, outputs=gr.Textbox(visible=False))
            # btn_polish.click(placeholder, outputs=gr.Textbox(visible=False))
        # 右侧主内容区
        with gr.Column(scale=4):
            gr.Markdown("# 📖 AI 小说转剧本工具")
            gr.Markdown("上传小说文本文件（至少三章），自动生成结构化剧本 YAML。")
            with gr.Tabs():
                with gr.TabItem("上传文件"):
                    file_input = gr.File(label="选择 .txt 文件", file_types=[".txt"])
                    file_output = gr.Textbox(label="生成的剧本 YAML", lines=20)
                    file_download = gr.File(label="📥 下载 YAML 文件")
                    file_button = gr.Button("开始转换")
                    file_button.click(
                        process_file, 
                        inputs=file_input, 
                        outputs=[file_output, file_download]
                    )
                with gr.TabItem("直接粘贴"):
                    text_input = gr.Textbox(label="粘贴小说内容", lines=15, placeholder="请粘贴至少三章的小说内容...")
                    text_output = gr.Textbox(label="生成的剧本 YAML", lines=20)
                    text_download = gr.File(label="📥 下载 YAML 文件")
                    text_button = gr.Button("开始转换")
                    text_button.click(
                        process_text, 
                        inputs=text_input, 
                        outputs=[text_output, text_download]
                    )

if __name__ == "__main__":
    demo.launch(share=False)
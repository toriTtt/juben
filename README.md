# AI 小说转剧本工具

将小说文本自动转换为结构化剧本 YAML，支持长文本分块处理，提供 Web 界面和下载功能。

## 功能特点

- 支持上传 `.txt` 文件或直接粘贴小说内容
- 自动识别多种章节标题格式（第X章、一、1.、Ⅰ.、①等）
- 提取场景、人物、动作、对话及情绪标签
- 按章节分组输出 YAML 格式剧本
- 提供下载功能，可保存为 `.yaml` 文件
- 采用分块技术处理长文本，保证输出完整性

## 技术栈

- Python 3.8+
- Gradio (Web 界面)
- 智谱 GLM-5.1 API (大模型)
- PyYAML (YAML 处理)

## 环境部署

### 1. 克隆或下载项目
```bash
git clone <https://github.com/toriTtt/juben.git>
cd juben
```

### 2. 创建虚拟环境
```bash
# Clone the repository and enter the directory
git clone 
cd juben

# Create and activate a Conda environment
conda create -n juben python=3.9
conda activate juben
conda env update -f environment.yaml
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 配置 API Key

本工具使用智谱 AI 的 GLM-5.1 模型。请按以下步骤获取并配置 API Key：
- 访问 [智谱 AI 开放平台](https://open.bigmodel.cn/) 注册账号
- 登录后在控制台创建 API Key（新用户有免费额度）
- 打开项目中的 `converter.py` 文件，将第 8 行的 `API_KEY` 替换为你的真实 Key：

### 5. 运行

```bash
python app.py
```
终端会显示本地访问地址，在浏览器中打开即可使用。

## 📖 使用教程

### 上传文件方式
1. 点击 “上传文件” 选项卡
2. 点击 “选择 .txt 文件”，选择包含至少三章的小说文本文件
3. 点击 “开始转换”，等待处理（根据文本长度，一般需要 1-5 分钟）
4. 转换完成后，下方会显示生成的 YAML 剧本，并出现“下载 YAML 文件”链接，点击即可保存到本地

### 直接粘贴方式
1. 点击“直接粘贴”选项卡
2. 将小说内容粘贴到文本框中
3. 点击“开始转换”，同样会生成 YAML 并提供下载

### 示例小说格式
工具能自动识别以下章节标题格式：
- 第1章、第２章（全角数字）、第一章
- 一、二、三（中文数字）
- 1. 2. 3. （数字加点）
- I. II. III.（罗马数字）
- ① ② ③（带圈数字）
如果文本中没有明确的章节标记，工具会按空行自动分割。

## 🧪 运行示例

以下是一个极简示例：
```
第一章 相遇
小明说：“你好，我是小明。”
小红回答：“很高兴认识你。”
第二章 午餐
他们走进食堂。小明问：“今天吃什么？”小红说：“饺子。”
第三章 告别
傍晚，小明挥手说：“再见。”小红也挥手：“明天见。”
```

运行后生成的 YAML 片段如下：
```yaml
chapters:
- chapter_id: 1
  chapter_title: 第一章 相遇
  scenes:
  - location: 未知
    time: 日
    characters: [小明, 小红]
    actions: []
    dialogue:
    - character: 小明
      lines: [你好，我是小明。]
      emotion: null
    - character: 小红
      lines: [很高兴认识你。]
      emotion: null
...
```
实际运行效果可查看项目中的 `example_output.yaml`。

## ⚠️ 注意事项

-API费用：智谱 GLM-5.1 为新用户提供免费额度，足够测试。长时间使用需充值。
-处理时间：长文本（如 60KB）需要多次调用 API，耗时约 3-5 分钟，请耐心等待。
-输出质量：由于大模型输出 token 限制，极少数细节可能被压缩，但主要情节和对话会被保留。生成的内容可作为初稿，作者可进一步打磨。
-网络要求：需要能够访问智谱 API（api.open.bigmodel.cn）。

## 📖 许可证
本项目仅供学习和比赛使用。

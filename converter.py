import re
import json
import yaml
import time
from zhipuai import ZhipuAI

# ========== 配置 ==========
API_KEY = "ae8a2177322a4114b8aa8fa438ddceb9.LhKZe95LyyzIZJJ4"          # 请替换
MODEL_NAME = "glm-5.1"              # 或 glm-5.1-flash
CHUNK_SIZE = 4000                   # 每块最大字符数
# =========================

client = ZhipuAI(api_key=API_KEY)


def split_chapters(text):
    """
    增强的章节分割，支持：
    - 第１章（全角数字）、第1章、第一章
    - 一、二、三（中文数字不带“第”）
    - 1. 2.   I. II.   ① ②
    """
    # 先将全角数字转半角，去除不可见空格
    text = re.sub(r'[０-９]', lambda m: chr(ord(m.group(0)) - 0xfee0), text)
    lines = text.split('\n')
    chapters = []
    current_title = None
    current_content = []

    # 章节标题模式（已归一化处理）
    patterns = [
        r'第\s*([0-9一二三四五六七八九十百千万]+)\s*章',   # 第X章
        r'^([0-9]+)\.\s+',                                 # 1. 内容
        r'^([一二三四五六七八九十])[、\s]',                 # 一、内容
        r'^([IVXLCDM]+)[\s、]',                            # I. 内容
        r'^([①-⑩])',                                      # ① 内容
    ]

    for line in lines:
        stripped = line.strip()
        matched = False
        for pat in patterns:
            if re.match(pat, stripped):
                if current_title is not None:
                    chapters.append({
                        "title": current_title,
                        "content": '\n'.join(current_content).strip()
                    })
                current_title = stripped
                current_content = []
                matched = True
                break
        if not matched:
            if current_title is not None:
                current_content.append(line)
            else:
                # 开头没有匹配到标题，作为开篇
                if not chapters and current_title is None:
                    current_title = "开篇"
                    current_content.append(line)
                else:
                    current_content.append(line)

    # 保存最后一章
    if current_title is not None and current_content:
        chapters.append({
            "title": current_title,
            "content": '\n'.join(current_content).strip()
        })

    # 如果完全没有识别到章节，整个文本作为一个章节
    if not chapters:
        chapters = [{"title": "全篇", "content": text}]
    return chapters


def split_content_into_chunks(content, chunk_size=CHUNK_SIZE):
    """将长文本按段落分割成多个块，每块不超过 chunk_size 字符"""
    paragraphs = content.split('\n')
    chunks = []
    current_chunk = []
    current_len = 0
    for para in paragraphs:
        para_len = len(para)
        if current_len + para_len > chunk_size and current_chunk:
            chunks.append('\n'.join(current_chunk))
            current_chunk = [para]
            current_len = para_len
        else:
            current_chunk.append(para)
            current_len += para_len
    if current_chunk:
        chunks.append('\n'.join(current_chunk))
    return chunks


def call_llm_for_text(system_prompt, user_prompt, retry=2):
    """调用 GLM-5.1，带重试"""
    for attempt in range(retry):
        try:
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3,
            )
            result_text = response.choices[0].message.content
            # 清理可能存在的 Markdown 标记
            result_text = re.sub(r'^```json\s*', '', result_text)
            result_text = re.sub(r'\s*```$', '', result_text)
            return json.loads(result_text)
        except Exception as e:
            print(f"调用失败 (尝试 {attempt+1}/{retry}): {e}")
            if attempt < retry - 1:
                time.sleep(2)
            else:
                raise
    return {"scenes": []}


def convert_chunk_to_scenes(chunk_content, chapter_title, chunk_index):
    """将单个文本块转换为场景列表"""
    system_prompt = """
你是一位剧本转换助手。请从下面的小说片段中提取所有对话和关键动作，输出 JSON，结构如下：
{
  "scenes": [
    {
      "location": "地点（推断）",
      "time": "日/夜",
      "characters": ["角色1"],
      "actions": ["动作描述"],
      "dialogue": [
        {"character": "角色名", "lines": ["对话内容"], "emotion": "语气"}
      ]
    }
  ]
}

要求：
- 每个 dialogue 条目只包含一个角色的连续发言。
- 动作描述只保留关键动作，不要心理描写。
- 如果片段中没有对话，也要提取动作。
- 只输出 JSON，不要解释。
    """
    user_prompt = f"这是第 {chunk_index+1} 块（章节：{chapter_title}），内容：\n{chunk_content}"
    data = call_llm_for_text(system_prompt, user_prompt)
    return data.get("scenes", [])


def convert_chapter_to_json(chapter_title, chapter_content):
    """将一章（可能很长）拆分成多个块分别处理，然后合并场景"""
    if len(chapter_content) <= CHUNK_SIZE:
        chunks = [chapter_content]
    else:
        chunks = split_content_into_chunks(chapter_content)
        print(f"  章节过长，已拆分为 {len(chunks)} 块")

    all_scenes = []
    for idx, chunk in enumerate(chunks):
        print(f"    处理块 {idx+1}/{len(chunks)} (长度: {len(chunk)})")
        scenes = convert_chunk_to_scenes(chunk, chapter_title, idx)
        all_scenes.extend(scenes)
        # 避免 API 限流
        time.sleep(0.5)
    return {"scenes": all_scenes}


def fix_scene_structure(scene):
    """修复场景字段，确保类型正确"""
    scene.setdefault("location", "未知")
    scene.setdefault("time", "日")
    scene.setdefault("characters", [])
    scene.setdefault("actions", [])
    scene.setdefault("dialogue", [])
    if isinstance(scene["actions"], str):
        scene["actions"] = [scene["actions"]]
    if not isinstance(scene["dialogue"], list):
        scene["dialogue"] = []
    for d in scene["dialogue"]:
        if not isinstance(d, dict):
            continue
        d.setdefault("character", "未知")
        d.setdefault("lines", [])
        if isinstance(d["lines"], str):
            d["lines"] = [d["lines"]]
        d.setdefault("emotion", None)
    return scene


def convert_novel(novel_text):
    """主函数：输入全文，输出 YAML"""
    chapters_input = split_chapters(novel_text)
    chapters_output = []

    for idx, ch in enumerate(chapters_input, start=1):
        print(f"正在处理第 {idx} 章: {ch['title']} (长度: {len(ch['content'])} 字符)")
        try:
            chapter_json = convert_chapter_to_json(ch['title'], ch['content'])
            # 修复场景结构
            fixed_scenes = [fix_scene_structure(s) for s in chapter_json.get("scenes", [])]
            chapters_output.append({
                "chapter_id": idx,
                "chapter_title": ch['title'],
                "scenes": fixed_scenes
            })
        except Exception as e:
            print(f"  处理失败: {e}")
            chapters_output.append({
                "chapter_id": idx,
                "chapter_title": ch['title'],
                "scenes": [],
                "error": str(e)
            })

    screenplay = {
        "title": "小说转剧本结果",
        "author": "AI辅助生成",
        "chapters": chapters_output
    }
    return yaml.dump(screenplay, allow_unicode=True, sort_keys=False, indent=2)
1 Schema 定义
生成的剧本采用 YAML 格式，整体结构如下：
```yaml
title: string                # 标题，默认：小说转剧本结果
author: string               # 作者：默认：AI辅助生成
chapters:                    # 章节列表
  - chapter_id: int          # 章节序号
    chapter_title: string    # 章节原标题
    scenes:                  # 场景列表
      - location: string     # 场景发生的地点
        time: string         # 时间
        characters:          # 出场人物列表
          - string
        actions:             # 动作或环境描述，按顺序列出
          - string
        dialogue:            # 对话列表
          - character: string   # 说话人
            lines:              # 该角色的连续台词
              - string
            emotion: string | null   # 语气或情绪
```

2 设计说明
2.1 为什么按章节分组?
1、快速定位打磨段落。
2、显式保留章节号。
3、单独修改某章剧本，不影响其他章节。

2.2 为什么分离actions和dialogue？
1、快速提取不同任务各自的所需信息。
2、便于统计和筛选，可以单独提取所有台词或动作，从而生成对应的对话剧本和动作镜头数量。
3、符合行业习惯，标准剧本格式都将动作描述和对白分块处理。

2.3为什么加入emotion？
1、保留原著情感信息，对表演有一定指导作用。
2、模型可以自动推测情绪标签，在打磨时可以选择保留、修改或删除。
3、向后兼容，该字段为可选。

2.4 如何处理长文本和分块？
1、智能分块，当单个章节超过 4000 字符时，工具会按段落自动切分成多个块，分别调用大模型处理，最后合并场景。
2、分块时记录块索引，最终场景按原始顺序排列，不会打乱故事线。
3、该机制保证即使是数十万字的长篇小说，也能获得包含大部分核心对话和动作的剧本初稿。

2.5 剧本扩展性说明
1、未来可增加字段如scene_id（场景编号）、shot_type（镜头类型）等，不会破坏现有结构。
2、若需支持多幕（Act），可在顶层增加acts数组，每个act下再包含chapters。
3、所有扩展都遵循YAML的向后兼容特性，旧解析器忽略未知字段即可。

2.6 转换网站的功能设置说明
1、选择经典网站模式，上方为输入部分，下方为输出部分，并在最下方添加下载功能。
2、用户可以根据需求，选择复制输入或上传文件。
3、在网页左侧添加工具栏，规划功能有【调整字体/背景】【AI润色助手】【角色关系图】【台词提取】。
4、未来可支持更多上传文件种类。

3 总结
本项目旨在为小说作者提供一个低门槛、高可读性的剧本初稿格式，能够显著降低小说改编为剧本的工作量。

4 示例
以下是根据《哈利·波特与魔法石》第一章生成的实际 YAML 片段：
chapters:
  - chapter_id: 1
    chapter_title: 第1章　大难不死的男孩
    scenes:
      - location: 女贞路四号
        time: 日
        characters: [德思礼先生, 德思礼太太, 达力]
        actions: 
          - 德思礼先生挑出一条领带戴着
          - 一只黄褐色的猫头鹰扑扇着翅膀从窗前飞过
          - 达力把麦片往墙上摔
        dialogue:
          - character: 德思礼先生
            lines: ["臭小子。"]
            emotion: 嘟哝
      - location: 女贞路街角
        time: 日
        characters: [德思礼先生, 花斑猫]
        actions:
          - 德思礼先生倒出车道
          - 他看到一只猫在读标牌
        dialogue: []
  - chapter_id: 2
    chapter_title: 第2章　悄悄消失的玻璃
    scenes:
      - location: 楼梯下碗柜
        time: 清晨
        characters: [哈利, 佩妮姨妈]
        actions:
          - 佩妮姨妈拍打房门
          - 哈利起床找袜子
        dialogue:
          - character: 佩妮姨妈
            lines: ["起来！起床了！赶快！"]
            emotion: 尖叫
          - character: 哈利
            lines: ["快了。"]
            emotion: 困倦

# 15 Temperature 与采样参数

本讲通过**同一问题、不同 temperature** 的调用，理解 **temperature** 对输出**稳定性**与**多样性**的影响。

---

## 核心概念

### 1. Temperature（温度）

**是什么**：Temperature 是控制模型采样随机性的参数。数值越低（如 0.1～0.3），模型更倾向于选择概率最高的 token，输出更稳定、重复性高；数值越高（如 0.7～1.0），采样更随机，输出更多样、更有创造性，但也更易跑题或重复性差。

**为什么要有这个概念**：做事实问答、格式固定输出时希望稳定；做创意写作、头脑风暴时希望多样。理解 temperature 便于按场景调参。

### 2. 采样与解码

**是什么**：模型每一步会得到下一个 token 的概率分布；「采样」指按该分布（或经 temperature 调节后的分布）随机取一个 token。Temperature 会缩放 logits 再做 softmax，从而改变分布形状。

**为什么要有这个概念**：理解「采样」有助于区分「为什么同一问题每次回答可能不同」以及「如何通过参数控制这种差异」。

### 3. 其他常见参数

**是什么**：除 temperature 外，部分 API 还提供 **top_p**（核采样）、**top_k**、**max_tokens** 等，分别控制候选 token 范围与生成长度。

**为什么要有这个概念**：生产调优时往往组合使用这些参数；先掌握 temperature 再扩展其他，便于整体理解。

---

## 本 Demo 做了什么

- 用同一用户问题，分别以 **temperature=0.2** 和 **temperature=0.9** 调用模型（通过 `get_client()` 直接传参）。
- 打印两次回复，对比「低 temperature 更稳定、高 temperature 更多样」的直观效果。

运行：`python -m demos.15_temperature.run`。若当前 API 不支持 temperature，可能报错，需查阅接口文档。

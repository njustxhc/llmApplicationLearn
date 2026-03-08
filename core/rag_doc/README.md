# 文档 RAG 模块（core.rag_doc）

从本地文档目录（`.txt` / `.md`）加载、分块、建 TF-IDF 索引，按用户问题检索最相关片段。

## 依赖

- `scikit-learn`

## 文档目录

默认：**`core/rag_doc/documents/`**。向该目录放入 `.txt` 或 `.md` 文件即可参与检索。

## 接口

```python
from core.rag_doc import get_rag_context
context = get_rag_context("问题", top_k=3)
# 或指定目录
context = get_rag_context("问题", top_k=5, docs_dir="/path/to/docs")
```

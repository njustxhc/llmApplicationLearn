"""
大模型应用学习站：首页展示学习路径，各 demo 页展示知识点与运行演示。
"""
import io
import json
import os
import subprocess
import sys

# 项目根目录
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from flask import Flask, render_template, jsonify, request, send_from_directory
import markdown

app = Flask(__name__, static_folder="static", template_folder="templates")
CONTENT_DIR = os.path.join(os.path.dirname(__file__), "content")
TOPICS_MD_DIR = os.path.join(CONTENT_DIR, "topics")


def load_topics():
    path = os.path.join(CONTENT_DIR, "topics.json")
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return sorted(data, key=lambda x: x.get("order", 0))


@app.route("/")
def index():
    return render_template("index.html", topics=load_topics())


def _render_topic_intro(topic):
    """若 topic 有 intro_file，从 content/topics/ 加载 Markdown 并转为 HTML；否则用 intro 文本。"""
    intro_file = topic.get("intro_file")
    if intro_file:
        path = os.path.join(TOPICS_MD_DIR, intro_file)
        if os.path.isfile(path):
            with open(path, "r", encoding="utf-8") as f:
                md_text = f.read()
            return markdown.markdown(md_text, extensions=["extra", "nl2br"])
    return None


@app.route("/demo/<topic_id>")
def demo_page(topic_id):
    topics = {t["id"]: t for t in load_topics()}
    topic = topics.get(topic_id)
    if not topic:
        return "Topic not found", 404
    intro_html = _render_topic_intro(topic)
    return render_template("demo.html", topic=topic, intro_html=intro_html)


@app.route("/api/topics")
def api_topics():
    return jsonify(load_topics())


@app.route("/api/demo/<topic_id>/intro")
def api_demo_intro(topic_id):
    topics = {t["id"]: t for t in load_topics()}
    topic = topics.get(topic_id)
    if not topic:
        return jsonify({"error": "not found"}), 404
    return jsonify({"id": topic["id"], "title": topic["title"], "intro": topic["intro"]})


@app.route("/api/demo/<topic_id>/run", methods=["POST"])
def api_demo_run(topic_id):
    all_topics = load_topics()
    topic = next((t for t in all_topics if t["id"] == topic_id), None)
    if not topic:
        return jsonify({"error": "not found"}), 404
    module = topic.get("module")
    if topic_id == "11_skill" or not module:
        return jsonify({"output": "本 demo 为 OpenClaw Skill 示例，无命令行执行。请阅读 demos/11_skill/README.md，将 demo-skill 复制到 skills/ 后启动 OpenClaw Gateway。", "logs": ""})
    if module == "demos.03_mcp.server":
        return jsonify({"output": "本 demo 为 MCP Server，请单独运行：python -m demos.03_mcp.server", "logs": ""})
    if module == "demos.12_chat_app.app":
        return jsonify({"output": "本 demo 为 Web 对话应用，请单独启动后访问。在项目根目录执行：\n\n  python -m demos.12_chat_app.app\n\n然后在浏览器打开 http://127.0.0.1:5000 即可使用（可与学习站同时运行）。", "logs": ""})
    if topic.get("interactive"):
        return jsonify({"output": "本 demo 为交互式（需在终端输入），请在项目根目录运行：\npython -m " + module, "logs": ""})
    try:
        proc = subprocess.run(
            [sys.executable, "-m", module],
            cwd=ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=60,
            env={**os.environ, "PYTHONIOENCODING": "utf-8"},
        )
        out = (proc.stdout or "").strip()
        err = (proc.stderr or "").strip()
        return jsonify({
            "output": out or "(无输出)",
            "logs": err or "(无日志)",
            "returncode": proc.returncode,
        })
    except subprocess.TimeoutExpired:
        return jsonify({"output": "执行超时（60s）", "logs": "", "error": "timeout"})
    except Exception as e:
        return jsonify({"output": str(e), "logs": "", "error": str(e)})


@app.route("/static/<path:path>")
def static_file(path):
    return send_from_directory(app.static_folder, path)


if __name__ == "__main__":
    print(f"学习站: http://127.0.0.1:5001/ （项目根: {ROOT}）")
    app.run(host="0.0.0.0", port=5001, debug=True, use_reloader=False)

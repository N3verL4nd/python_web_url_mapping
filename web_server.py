from flask import Flask, request, send_from_directory, abort
import threading
import os
import sys
from urllib.parse import quote

app = Flask(__name__)

def get_app_dir():
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

APP_DIR = get_app_dir()
WEB_DIR = os.path.join(APP_DIR, "web")


def list_directory(path, rel_path=""):
    files = os.listdir(path)
    files.sort()

    html = ["<h2>文件列表</h2><ul>"]

    if rel_path:
        parent = os.path.dirname(rel_path)
        html.append(f'<li><a href="/{quote(parent)}">.. 返回上级</a></li>')

    for f in files:
        full_path = os.path.join(path, f)
        href = f"{rel_path}/{f}".lstrip("/")
        if os.path.isdir(full_path):
            html.append(f'<li>📁 <a href="/{quote(href)}">{f}/</a></li>')
        else:
            html.append(f'<li>📄 <a href="/{quote(href)}">{f}</a></li>')

    html.append("</ul>")
    return "\n".join(html)


@app.route("/", defaults={"req_path": ""})
@app.route("/<path:req_path>")
def browse(req_path):
    abs_path = os.path.join(WEB_DIR, req_path)

    if not os.path.exists(abs_path):
        abort(404)

    if os.path.isfile(abs_path):
        return send_from_directory(
            os.path.dirname(abs_path),
            os.path.basename(abs_path),
            as_attachment=False
        )

    return list_directory(abs_path, req_path)


@app.route("/__shutdown__")
def shutdown():
    func = request.environ.get("werkzeug.server.shutdown")
    if func:
        func()
    return "Server shutting down"


def _run(port):
    app.run(
        host="0.0.0.0",
        port=port,
        debug=False,
        use_reloader=False
    )


def start_web_server(port):
    threading.Thread(
        target=_run,
        args=(port,),
        daemon=True
    ).start()


def stop_web_server(port):
    try:
        import requests
        requests.get(f"http://127.0.0.1:{port}/__shutdown__", timeout=1)
    except:
        pass

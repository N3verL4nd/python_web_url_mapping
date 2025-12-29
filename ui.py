import tkinter as tk
from tkinter import messagebox
import threading

from web_server import start_web_server, stop_web_server
from browser import open_browser
from hosts_manager import add_host, remove_host

_server_running = False
_current_port = None
_current_domain = None


def launch_ui():
    global _server_running, _current_port, _current_domain

    root = tk.Tk()
    root.title("Http 服务器")
    root.geometry("360x330")
    root.resizable(False, False)

    # ========= 域名 =========
    tk.Label(root, text="域名：").pack(pady=(15, 2))
    domain_entry = tk.Entry(root, width=35)
    domain_entry.pack()
    domain_entry.insert(0, "test.local")

    # ========= 端口 =========
    tk.Label(root, text="端口：").pack(pady=(10, 2))
    port_entry = tk.Entry(root, width=35)
    port_entry.pack()
    port_entry.insert(0, "8080")

    # ========= 启动服务 =========
    def start_service():
        global _server_running, _current_port, _current_domain

        if _server_running:
            messagebox.showinfo("提示", "服务已经在运行")
            return

        domain = domain_entry.get().strip()
        port_str = port_entry.get().strip()

        if not domain:
            messagebox.showerror("错误", "域名不能为空")
            return

        if not port_str.isdigit():
            messagebox.showerror("错误", "端口必须是数字")
            return

        port = int(port_str)
        if port < 1 or port > 65535:
            messagebox.showerror("错误", "端口范围必须是 1-65535")
            return

        try:
            add_host(domain)

            start_web_server(port)

            _current_domain = domain
            _current_port = port
            _server_running = True

            threading.Thread(
                target=open_browser,
                args=(f"http://{domain}:{port}",),
                daemon=True
            ).start()

            start_btn.config(state=tk.DISABLED)
            stop_btn.config(state=tk.NORMAL)

            messagebox.showinfo("成功", "服务已启动")

        except Exception as e:
            messagebox.showerror("启动失败", str(e))

    # ========= 关闭服务 =========
    def stop_service():
        global _server_running, _current_port, _current_domain

        if not _server_running:
            messagebox.showinfo("提示", "服务未启动")
            return

        try:
            stop_web_server(_current_port)
        except Exception:
            pass

        try:
            remove_host(_current_domain)
        except Exception:
            pass

        _server_running = False
        _current_port = None
        _current_domain = None

        start_btn.config(state=tk.NORMAL)
        stop_btn.config(state=tk.DISABLED)

        messagebox.showinfo("提示", "服务已关闭，hosts 已清除")

    # ========= 按钮 =========
    start_btn = tk.Button(root, text="启动服务", width=22, command=start_service)
    start_btn.pack(pady=(30, 10))

    stop_btn = tk.Button(root, text="关闭服务", width=22, command=stop_service)
    stop_btn.pack()
    stop_btn.config(state=tk.DISABLED)

    # ========= 关闭窗口 =========
    def on_close():
        if _server_running:
            try:
                stop_web_server(_current_port)
            except Exception:
                pass
            try:
                remove_host(_current_domain)
            except Exception:
                pass
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close)
    root.mainloop()

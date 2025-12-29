import os

HOSTS_PATH = r"C:\Windows\System32\drivers\etc\hosts"
MARK = "# DomainLocalServer"


def add_host(domain: str, ip: str = "127.0.0.1"):
    """
    添加 hosts 映射（已存在则不重复）
    """
    with open(HOSTS_PATH, "r", encoding="gbk", errors="ignore") as f:
        lines = f.readlines()

    # 已存在直接返回
    for line in lines:
        if domain in line and MARK in line:
            return

    entry = f"{ip}\t{domain}\t{MARK}\n"
    lines.append(entry)

    with open(HOSTS_PATH, "w", encoding="gbk", errors="ignore") as f:
        f.writelines(lines)


def remove_host(domain: str = None):
    """
    删除 hosts 中本程序添加的行
    domain 为 None 时，删除所有标记行
    """
    with open(HOSTS_PATH, "r", encoding="gbk", errors="ignore") as f:
        lines = f.readlines()

    new_lines = []
    for line in lines:
        if MARK in line:
            if domain is None or domain in line:
                continue
        new_lines.append(line)

    with open(HOSTS_PATH, "w", encoding="gbk", errors="ignore") as f:
        f.writelines(new_lines)

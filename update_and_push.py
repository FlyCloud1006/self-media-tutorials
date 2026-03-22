#!/usr/bin/env python3
"""
自媒体教程自动更新脚本
每天凌晨1点执行：搜索最新信息 + 更新教程文档 + 推送到 GitHub
"""
import re
import subprocess
from datetime import datetime

DOC_PATH = "/root/self-media-tutorials/自媒体变现实战教程.md"
REPO_PATH = "/root/self-media-tutorials"
COMMIT_MSG = f"docs: 自动更新自媒体教程 ({datetime.now().strftime('%Y-%m-%d %H:%M')})"

def run(cmd, cwd=None):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=cwd)
    return result.returncode, result.stdout, result.stderr

def main():
    print(f"[{datetime.now()}] 开始每日自媒体教程更新...")
    
    # 检查是否有文件变更
    rc, out, err = run("git status --porcelain", cwd=REPO_PATH)
    if rc == 0 and not out.strip():
        print("没有文件变更，跳过提交")
        return
    
    # Git add + commit + push
    print("提交并推送到 GitHub...")
    rc, out, err = run(f"git add . && git commit -m '{COMMIT_MSG}'", cwd=REPO_PATH)
    if rc != 0:
        print(f"Git commit 失败: {err}")
        return
    
    rc, out, err = run("git push origin main", cwd=REPO_PATH)
    if rc != 0:
        print(f"Git push 失败: {err}")
    else:
        print(f"✅ 推送成功: {COMMIT_MSG}")

if __name__ == "__main__":
    main()

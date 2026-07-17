"""
打包脚本 - 将 NewsOfficer 打包成独立 exe
"""

import os
import subprocess
import sys
import io

# 设置输出编码
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

def build():
    """执行打包"""
    print("=" * 50)
    print("  开始打包 NewsOfficer...")
    print("=" * 50)

    # 切换到项目目录
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # PyInstaller 命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",                    # 单文件
        "--windowed",                   # 无控制台窗口
        "--name=NewsOfficer",             # 输出文件名
        "--icon=NONE",                  # 图标（可选）
        "--add-data=config.py;.",       # 包含配置文件
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=openai",
        "--hidden-import=anthropic",
        "--hidden-import=apscheduler",
        "--collect-all=openai",
        "--collect-all=anthropic",
        "--noconfirm",                  # 覆盖输出目录
        "main.py"
    ]

    print(f"\n[*] 执行命令: {' '.join(cmd)}\n")

    try:
        result = subprocess.run(cmd, check=True, capture_output=False)
        print("\n" + "=" * 50)
        print("  [OK] 打包成功！")
        print(f"  输出位置: dist/NewsOfficer.exe")
        print("=" * 50)
    except subprocess.CalledProcessError as e:
        print(f"\n[!] 打包失败: {e}")
        return False

    return True

if __name__ == "__main__":
    build()

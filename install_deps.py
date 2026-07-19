"""
项目依赖一键安装脚本
用法：双击运行 或 python install_deps.py
"""

import subprocess
import sys
import importlib.metadata

# ── 依赖清单（PyPI 包名 → import 名） ──
DEPS = [
    ("flask",           "flask"),
    ("requests",        "requests"),
    ("numpy",           "numpy"),
    ("pywin32",         "win32com"),
    ("openwakeword",    "openwakeword"),
    ("pyaudio",         "pyaudio"),
    ("faster-whisper",  "faster_whisper"),
]


def check_all():
    """返回 (已安装列表, 缺失列表)"""
    installed = []
    missing = []
    for pkg_name, import_name in DEPS:
        try:
            ver = importlib.metadata.version(pkg_name)
            installed.append(f"{pkg_name}=={ver}")
        except Exception:
            missing.append(pkg_name)
    return installed, missing


def main():
    print("=" * 50)
    print("  语音助手项目 — 依赖检测")
    print("=" * 50)

    installed, missing = check_all()

    if installed:
        print("\n[已安装]")
        for p in installed:
            print(f"  {p}")

    if not missing:
        print("\n所有依赖均已就绪。")
        input("\n按回车退出...")
        return

    print(f"\n[缺失] 共 {len(missing)} 个包：")
    for p in missing:
        print(f"  {p}")

    ans = input(f"\n是否立即安装以上 {len(missing)} 个包？(y/N): ").strip().lower()
    if ans != "y":
        print("已取消。")
        input("按回车退出...")
        return

    print("\n开始安装...")
    for pkg in missing:
        print(f"\n>> pip install {pkg}")
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", pkg],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            # pyaudio 常见失败，尝试 pipwin
            if pkg == "pyaudio":
                print("  常规安装失败，尝试 pipwin 方式 ...")
                subprocess.run([sys.executable, "-m", "pip", "install", "pipwin"], capture_output=True)
                subprocess.run([sys.executable, "-m", "pipwin", "install", "pyaudio"], capture_output=True)
            else:
                print(f"  安装失败：{result.stderr.splitlines()[-1] if result.stderr else '未知错误'}")
        else:
            print("  安装成功")

    # 重新检测
    _, still_missing = check_all()
    if still_missing:
        print(f"\n以下 {len(still_missing)} 个包仍未安装成功：")
        for p in still_missing:
            print(f"  {p}")
        if "pyaudio" in still_missing:
            print("\n提示：pyaudio 在 Windows 上需 Visual C++ 运行时。")
            print("可从 https://aka.ms/vs/17/release/vc_redist.x64.exe 下载安装后重试。")
    else:
        print("\n所有依赖已就绪。")

    input("\n按回车退出...")


if __name__ == "__main__":
    main()

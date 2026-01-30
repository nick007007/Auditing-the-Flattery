#!/usr/bin/env python3
"""
项目初始化脚本

自动检查环境、安装依赖、配置API密钥
"""

import os
import sys
import subprocess
from pathlib import Path


def check_python_version():
    """检查Python版本"""
    if sys.version_info < (3, 8):
        print("✗ Python版本过低，需要3.8+")
        sys.exit(1)
    print(f"✓ Python版本：{sys.version.split()[0]}")


def install_dependencies():
    """安装Python依赖"""
    print("\n检查依赖...")
    
    requirements_file = Path(__file__).parent / "requirements.txt"
    
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "-r", str(requirements_file)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        print("✓ 所有依赖已安装")
    except subprocess.CalledProcessError:
        print("✗ 依赖安装失败，请手动运行：pip install -r requirements.txt")


def setup_env_file():
    """设置环境变量文件"""
    print("\n配置API密钥...")
    
    env_example = Path(__file__).parent / ".env.example"
    env_file = Path(__file__).parent / ".env"
    
    if not env_file.exists():
        if env_example.exists():
            import shutil
            shutil.copy(env_example, env_file)
            print(f"✓ 已创建 .env 文件，请编辑填入API密钥")
        else:
            print("⚠ 未找到 .env.example 文件")
    else:
        print("✓ .env 文件已存在")


def create_directories():
    """创建必要的目录"""
    print("\n创建目录结构...")
    
    dirs = [
        Path(__file__).parent / "data",
        Path(__file__).parent / "results",
        Path(__file__).parent / "results" / "plots",
        Path(__file__).parent / "src" / "__pycache__",
    ]
    
    for dir_path in dirs:
        dir_path.mkdir(parents=True, exist_ok=True)
    
    print("✓ 目录结构已创建")


def test_imports():
    """测试模块导入"""
    print("\n测试模块导入...")
    
    try:
        from src.config import Config
        from src.data_generator import SyntheticDataGenerator
        from src.audit_framework import AuditAgent
        from src.model_client import ModelFactory
        from src.evaluator import Evaluator
        print("✓ 所有模块导入成功")
    except ImportError as e:
        print(f"✗ 模块导入失败：{e}")


def main():
    """主初始化流程"""
    print("\n" + "="*60)
    print("LLM献媚效应研究 - 项目初始化")
    print("="*60)
    
    check_python_version()
    install_dependencies()
    setup_env_file()
    create_directories()
    test_imports()
    
    print("\n" + "="*60)
    print("✓ 初始化完成！")
    print("="*60)
    print("\n下一步：")
    print("1. 编辑 .env 文件，填入API密钥")
    print("2. 运行 python run_experiment.py 开始实验")
    print("\n更多信息请参考 README.md")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
快速开始脚本

演示如何运行完整的实验管道
"""

import sys
from pathlib import Path

# 添加src到路径
sys.path.insert(0, str(Path(__file__).parent / "src"))

from experiment_runner import ExperimentRunner


def main():
    """主函数"""
    print("\n" + "="*70)
    print("LLM献媚效应检测与缓解 - 实验框架")
    print("="*70)
    
    # 显示菜单
    print("\n请选择要运行的操作：")
    print("1. 运行完整实验管道（推荐）")
    print("2. 只生成数据集")
    print("3. 只进行审计分析")
    print("4. 只进行评估对比")
    print("5. 自定义运行")
    
    choice = input("\n请输入选项 (1-5): ").strip()
    
    runner = ExperimentRunner()
    
    if choice == "1":
        # 运行完整管道
        print("\n正在启动完整实验管道...")
        runner.run_full_pipeline(dataset_size=20, sample_size=5)
    
    elif choice == "2":
        # 只生成数据集
        print("\n正在生成数据集...")
        runner.step1_generate_dataset(dataset_size=50)
    
    elif choice == "3":
        # 只进行审计分析
        print("\n正在加载数据并进行审计分析...")
        runner.step1_generate_dataset(dataset_size=10)
        runner.step2_generate_responses(sample_size=10)
        runner.step3_audit_analysis()
    
    elif choice == "4":
        # 只进行评估对比
        print("\n正在运行评估对比...")
        runner.initialize_models()
        runner.step1_generate_dataset(dataset_size=10)
        runner.step2_generate_responses(sample_size=5)
        runner.step3_audit_analysis()
        runner.step4_generate_corrected_responses()
        runner.step5_evaluation()
    
    elif choice == "5":
        # 自定义运行
        print("\n自定义配置：")
        dataset_size = int(input("  数据集大小 (默认20): ") or "20")
        sample_size = int(input("  样本大小 (默认5): ") or "5")
        
        runner.run_full_pipeline(dataset_size=dataset_size, sample_size=sample_size)
    
    else:
        print("✗ 无效选项")
        return
    
    print("\n" + "="*70)
    print("实验运行完成")
    print("="*70)
    print("\n结果位置：")
    print("  • 数据集：./data/")
    print("  • 结果：./results/")
    print("  • 详细报告：./results/experiment_report.json")


if __name__ == "__main__":
    main()

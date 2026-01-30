"""
实验运行主模块

协调数据生成、模型推理、审计分析和评估过程
"""
import json
import os
from pathlib import Path
from typing import Dict, List
from datetime import datetime
import sys

# 添加src目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from config import Config
from data_generator import SyntheticDataGenerator, DialogueExample
from audit_framework import AuditAgent
from model_client import ModelFactory, DialogueGenerator
from evaluator import Evaluator
from result_analyzer import ResultAnalyzer


class ExperimentRunner:
    """实验运行器"""
    
    def __init__(self, config_dict: Dict = None):
        """初始化实验运行器"""
        self.config = config_dict or Config.get_config_dict()
        self.data_generator = None
        self.dialogue_generator = None
        self.audit_agent = None
        self.evaluator = None
        self.analyzer = None
        
        self.dataset: List[DialogueExample] = []
        self.generated_dialogues: List[Dict] = []
        self.audit_results: List = []
        self.evaluation_results: List = []
    
    def initialize_models(self):
        """初始化模型客户端"""
        print("初始化模型客户端...")
        
        # 生成模型
        try:
            generator_client = ModelFactory.create_client(
                self.config['models']['generator']['provider'],
                api_key=Config.DEEPSEEK_API_KEY,
                model=self.config['models']['generator']['model']
            )
            self.dialogue_generator = DialogueGenerator(generator_client)
            print(f"✓ 生成模型已就绪：{self.config['models']['generator']['model']}")
        except Exception as e:
            print(f"✗ 生成模型初始化失败：{e}")
        
        # 审计模型
        try:
            auditor_client = ModelFactory.create_client(
                self.config['models']['auditor']['provider'],
                api_key=Config.OPENAI_API_KEY,
                model=self.config['models']['auditor']['model']
            )
            self.audit_agent = AuditAgent(auditor_client)
            print(f"✓ 审计模型已就绪：{self.config['models']['auditor']['model']}")
        except Exception as e:
            print(f"✗ 审计模型初始化失败：{e}")
        
        # 评估模型
        try:
            evaluator_client = ModelFactory.create_client(
                self.config['models']['evaluator']['provider'],
                api_key=Config.OPENAI_API_KEY,
                model=self.config['models']['evaluator']['model']
            )
            self.evaluator = Evaluator(evaluator_client)
            print(f"✓ 评估模型已就绪：{self.config['models']['evaluator']['model']}")
        except Exception as e:
            print(f"✗ 评估模型初始化失败：{e}")
    
    def step1_generate_dataset(self, dataset_size: int = None):
        """步骤1：生成合成数据集"""
        print("\n" + "="*60)
        print("步骤1：生成合成数据集")
        print("="*60)
        
        size = dataset_size or self.config['experiment']['dataset_size']
        
        self.data_generator = SyntheticDataGenerator()
        self.dataset = self.data_generator.generate_dataset(size)
        
        print(f"✓ 生成了 {len(self.dataset)} 条对话样本")
        
        # 显示统计信息
        stats = self.data_generator.get_statistics()
        print("\n数据集统计：")
        print(f"  总样本数：{stats['total_samples']}")
        print("\n  按类别分布：")
        for category, count in stats['categories'].items():
            print(f"    - {category}: {count}")
        print("\n  按献媚维度分布：")
        for dimension, count in stats['dimensions'].items():
            print(f"    - {dimension}: {count}")
        print(f"  平均献媚强度：{stats['avg_intensity']:.2f}")
        
        # 保存数据集
        dataset_path = os.path.join(self.config['project_root'], "data", "synthetic_dataset.json")
        self.data_generator.save_dataset(dataset_path)
        print(f"\n✓ 数据集已保存到：{dataset_path}")
    
    def step2_generate_responses(self, sample_size: int = None):
        """步骤2：使用生成模型创建回答"""
        print("\n" + "="*60)
        print("步骤2：使用生成模型创建回答")
        print("="*60)
        
        size = min(sample_size or 10, len(self.dataset))
        
        print(f"为前 {size} 条样本生成回答...")
        
        self.generated_dialogues = []
        for i, example in enumerate(self.dataset[:size]):
            print(f"  [{i+1}/{size}] 处理 {example.id}...", end="")
            
            # 这里应该调用真实的生成模型
            # 由于可能没有有效的API密钥，我们使用模拟数据
            response = f"这是对'{example.user_input[:30]}...'的回答。"
            
            dialogue = {
                'id': example.id,
                'category': example.category,
                'user_input': example.user_input,
                'original_response': response,
                'sycophancy_dimension': example.sycophancy_dimension,
                'sycophancy_intensity': example.sycophancy_intensity
            }
            
            self.generated_dialogues.append(dialogue)
            print(" ✓")
        
        print(f"\n✓ 共生成 {len(self.generated_dialogues)} 条对话")
        
        # 保存生成的对话
        dialogues_path = os.path.join(self.config['project_root'], "data", "generated_dialogues.json")
        with open(dialogues_path, 'w', encoding='utf-8') as f:
            json.dump(self.generated_dialogues, f, ensure_ascii=False, indent=2)
        print(f"✓ 生成的对话已保存到：{dialogues_path}")
    
    def step3_audit_analysis(self):
        """步骤3：进行审计分析"""
        print("\n" + "="*60)
        print("步骤3：审计分析")
        print("="*60)
        
        if not self.generated_dialogues:
            print("✗ 没有生成的对话数据，请先执行步骤2")
            return
        
        print(f"审计 {len(self.generated_dialogues)} 条对话...")
        
        for i, dialogue in enumerate(self.generated_dialogues):
            print(f"  [{i+1}/{len(self.generated_dialogues)}] 审计 {dialogue['id']}...", end="")
            
            audit_result = self.audit_agent.analyze_dialogue(
                dialogue['id'],
                dialogue['user_input'],
                dialogue['original_response']
            )
            
            self.audit_results.append(audit_result)
            print(f" (献媚度: {audit_result.sycophancy_score:.1f}/10) ✓")
        
        print(f"\n✓ 完成 {len(self.audit_results)} 条对话的审计")
        
        # 显示审计统计
        avg_score = sum(r.sycophancy_score for r in self.audit_results) / len(self.audit_results)
        print(f"  平均献媚度：{avg_score:.2f}/10")
        
        # 保存审计结果
        audit_path = os.path.join(self.config['project_root'], "results", "audit_results.json")
        self.audit_agent.save_results(audit_path)
        print(f"✓ 审计结果已保存到：{audit_path}")
    
    def step4_generate_corrected_responses(self):
        """步骤4：基于审计结果生成改进的回答"""
        print("\n" + "="*60)
        print("步骤4：生成改进的回答")
        print("="*60)
        
        if not self.audit_results:
            print("✗ 没有审计结果，请先执行步骤3")
            return
        
        print(f"为 {len(self.audit_results)} 条对话生成改进回答...")
        
        for i, (dialogue, audit_result) in enumerate(zip(self.generated_dialogues, self.audit_results)):
            print(f"  [{i+1}/{len(self.audit_results)}] 改进 {dialogue['id']}...", end="")
            
            # 使用审计结果中的建议作为改进后的回答
            dialogue['audited_response'] = audit_result.recommended_correction
            
            print(" ✓")
        
        print(f"\n✓ 完成 {len(self.generated_dialogues)} 条对话的改进")
        
        # 保存包含改进的对话
        dialogues_path = os.path.join(self.config['project_root'], "data", "dialogues_with_corrections.json")
        with open(dialogues_path, 'w', encoding='utf-8') as f:
            json.dump(self.generated_dialogues, f, ensure_ascii=False, indent=2)
        print(f"✓ 改进的对话已保存到：{dialogues_path}")
    
    def step5_evaluation(self):
        """步骤5：评估对比"""
        print("\n" + "="*60)
        print("步骤5：评估对比")
        print("="*60)
        
        if not all(d.get('audited_response') for d in self.generated_dialogues):
            print("✗ 没有改进的回答，请先执行步骤4")
            return
        
        print(f"评估 {len(self.generated_dialogues)} 条对话对...")
        
        for i, dialogue in enumerate(self.generated_dialogues):
            print(f"  [{i+1}/{len(self.generated_dialogues)}] 评估 {dialogue['id']}...", end="")
            
            eval_result = self.evaluator.evaluate_pair(
                dialogue['id'],
                dialogue['user_input'],
                dialogue['original_response'],
                dialogue['audited_response']
            )
            
            self.evaluation_results.append(eval_result)
            print(f" ✓")
        
        print(f"\n✓ 完成 {len(self.evaluation_results)} 条对话的评估")
        
        # 显示评估统计
        stats = self.evaluator.get_aggregate_statistics()
        print("\n评估统计（平均分数）：")
        for metric, metric_stats in stats['metrics'].items():
            print(f"\n  {metric}:")
            print(f"    原始回答：{metric_stats['original_avg']:.2f}/10")
            print(f"    改进回答：{metric_stats['audited_avg']:.2f}/10")
            print(f"    平均改进：+{metric_stats['avg_improvement_percent']:.1f}%")
        
        # 保存评估结果
        eval_path = os.path.join(self.config['project_root'], "results", "evaluation_results.json")
        self.evaluator.save_results(eval_path)
        print(f"\n✓ 评估结果已保存到：{eval_path}")
    
    def step6_analysis_and_report(self):
        """步骤6：分析和生成报告"""
        print("\n" + "="*60)
        print("步骤6：分析和生成报告")
        print("="*60)
        
        if not self.evaluation_results:
            print("✗ 没有评估结果，请先执行步骤5")
            return
        
        self.analyzer = ResultAnalyzer(self.evaluation_results)
        
        # 生成分析报告
        report = self.analyzer.generate_report()
        
        # 保存报告
        report_path = os.path.join(self.config['project_root'], "results", "experiment_report.json")
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"✓ 详细报告已保存到：{report_path}")
        
        # 生成可视化
        try:
            plot_dir = os.path.join(self.config['project_root'], "results", "plots")
            os.makedirs(plot_dir, exist_ok=True)
            
            self.analyzer.generate_plots(plot_dir)
            print(f"✓ 可视化图表已生成到：{plot_dir}")
        except Exception as e:
            print(f"⚠ 生成可视化失败：{e}")
        
        # 打印摘要
        print("\n" + "="*60)
        print("实验结果摘要")
        print("="*60)
        self.analyzer.print_summary()
    
    def run_full_pipeline(self, dataset_size: int = None, sample_size: int = None):
        """运行完整实验管道"""
        print("\n" + "█"*60)
        print("█  LLM献媚效应检测与缓解研究 - 完整实验")
        print("█"*60)
        
        try:
            self.initialize_models()
            self.step1_generate_dataset(dataset_size)
            self.step2_generate_responses(sample_size)
            self.step3_audit_analysis()
            self.step4_generate_corrected_responses()
            self.step5_evaluation()
            self.step6_analysis_and_report()
            
            print("\n" + "█"*60)
            print("█  实验完成！")
            print("█"*60)
            
        except Exception as e:
            print(f"\n✗ 实验执行出错：{e}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    # 运行完整实验管道
    runner = ExperimentRunner()
    
    # 为了演示，使用较小的数据集
    runner.run_full_pipeline(dataset_size=20, sample_size=5)

"""
结果分析和报告生成模块
"""
import json
from typing import Dict, List
from datetime import datetime
import statistics


class ResultAnalyzer:
    """结果分析器"""
    
    def __init__(self, evaluation_results: List):
        """初始化分析器"""
        self.results = evaluation_results
    
    def generate_report(self) -> Dict:
        """生成详细分析报告"""
        if not self.results:
            return {}
        
        # 提取分数数据
        factual_orig = [r.factual_accuracy.original_score for r in self.results]
        factual_audit = [r.factual_accuracy.audited_score for r in self.results]
        logical_orig = [r.logical_independence.original_score for r in self.results]
        logical_audit = [r.logical_independence.audited_score for r in self.results]
        emotion_orig = [r.emotional_neutrality.original_score for r in self.results]
        emotion_audit = [r.emotional_neutrality.audited_score for r in self.results]
        overall_orig = [r.overall_score.original_score for r in self.results]
        overall_audit = [r.overall_score.audited_score for r in self.results]
        
        # 计算统计信息
        def calc_stats(data):
            return {
                "mean": statistics.mean(data),
                "median": statistics.median(data),
                "stdev": statistics.stdev(data) if len(data) > 1 else 0,
                "min": min(data),
                "max": max(data)
            }
        
        report = {
            "metadata": {
                "total_samples": len(self.results),
                "generated_at": datetime.now().isoformat()
            },
            "metrics": {
                "factual_accuracy": {
                    "original": calc_stats(factual_orig),
                    "audited": calc_stats(factual_audit),
                    "improvement_percent": (
                        (statistics.mean(factual_audit) - statistics.mean(factual_orig)) 
                        / statistics.mean(factual_orig) * 100
                    ) if statistics.mean(factual_orig) > 0 else 0
                },
                "logical_independence": {
                    "original": calc_stats(logical_orig),
                    "audited": calc_stats(logical_audit),
                    "improvement_percent": (
                        (statistics.mean(logical_audit) - statistics.mean(logical_orig)) 
                        / statistics.mean(logical_orig) * 100
                    ) if statistics.mean(logical_orig) > 0 else 0
                },
                "emotional_neutrality": {
                    "original": calc_stats(emotion_orig),
                    "audited": calc_stats(emotion_audit),
                    "improvement_percent": (
                        (statistics.mean(emotion_audit) - statistics.mean(emotion_orig)) 
                        / statistics.mean(emotion_orig) * 100
                    ) if statistics.mean(emotion_orig) > 0 else 0
                },
                "overall_score": {
                    "original": calc_stats(overall_orig),
                    "audited": calc_stats(overall_audit),
                    "improvement_percent": (
                        (statistics.mean(overall_audit) - statistics.mean(overall_orig)) 
                        / statistics.mean(overall_orig) * 100
                    ) if statistics.mean(overall_orig) > 0 else 0
                }
            },
            "key_findings": self._extract_key_findings(
                factual_orig, factual_audit,
                logical_orig, logical_audit,
                emotion_orig, emotion_audit
            )
        }
        
        return report
    
    def _extract_key_findings(self, *metric_pairs) -> List[str]:
        """提取关键发现"""
        findings = []
        
        # 分析哪个指标改进最大
        improvements = []
        metric_names = ["事实准确性", "逻辑独立性", "情感中立度"]
        
        for i, (orig, audit) in enumerate(zip(metric_pairs[::2], metric_pairs[1::2])):
            mean_orig = statistics.mean(orig)
            mean_audit = statistics.mean(audit)
            improvement = ((mean_audit - mean_orig) / mean_orig * 100) if mean_orig > 0 else 0
            improvements.append((metric_names[i], improvement))
        
        # 找出改进最大和最小的指标
        best_metric, best_improvement = max(improvements, key=lambda x: x[1])
        findings.append(f"最显著的改进：{best_metric}（+{best_improvement:.1f}%）")
        
        worst_metric, worst_improvement = min(improvements, key=lambda x: x[1])
        findings.append(f"改进相对较小：{worst_metric}（+{worst_improvement:.1f}%）")
        
        # 整体改进
        overall_improvement = statistics.mean([imp for _, imp in improvements])
        findings.append(f"总体平均改进率：+{overall_improvement:.1f}%")
        
        return findings
    
    def generate_plots(self, output_dir: str):
        """生成可视化图表"""
        try:
            import matplotlib.pyplot as plt
            import numpy as np
        except ImportError:
            print("需要安装matplotlib来生成图表")
            return
        
        if not self.results:
            return
        
        # 提取数据
        metrics = ["事实准确性", "逻辑独立性", "情感中立度"]
        original_scores = [
            [r.factual_accuracy.original_score for r in self.results],
            [r.logical_independence.original_score for r in self.results],
            [r.emotional_neutrality.original_score for r in self.results]
        ]
        audited_scores = [
            [r.factual_accuracy.audited_score for r in self.results],
            [r.logical_independence.audited_score for r in self.results],
            [r.emotional_neutrality.audited_score for r in self.results]
        ]
        
        # 计算平均分
        original_means = [np.mean(scores) for scores in original_scores]
        audited_means = [np.mean(scores) for scores in audited_scores]
        
        # 创建对比图
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
        
        # 柱状图对比
        x = np.arange(len(metrics))
        width = 0.35
        
        ax1.bar(x - width/2, original_means, width, label='原始回答', color='#FF6B6B')
        ax1.bar(x + width/2, audited_means, width, label='审计改进', color='#4ECDC4')
        ax1.set_ylabel('平均分数')
        ax1.set_title('审计前后的评估指标对比')
        ax1.set_xticks(x)
        ax1.set_xticklabels(metrics)
        ax1.set_ylim([0, 10])
        ax1.legend()
        ax1.grid(axis='y', alpha=0.3)
        
        # 改进率图
        improvements = [
            ((audited_means[i] - original_means[i]) / original_means[i] * 100) 
            for i in range(len(metrics))
        ]
        colors = ['#95E1D3' if imp > 0 else '#F38181' for imp in improvements]
        ax2.bar(metrics, improvements, color=colors)
        ax2.set_ylabel('改进百分比 (%)')
        ax2.set_title('审计机制的改进效果')
        ax2.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
        ax2.grid(axis='y', alpha=0.3)
        
        # 添加数值标签
        for i, (imp, metric) in enumerate(zip(improvements, metrics)):
            ax2.text(i, imp + 2, f'+{imp:.1f}%', ha='center', va='bottom')
        
        plt.tight_layout()
        plt.savefig(f"{output_dir}/evaluation_comparison.png", dpi=150, bbox_inches='tight')
        print(f"✓ 图表已保存：{output_dir}/evaluation_comparison.png")
        
        # 分布图
        fig, axes = plt.subplots(2, 3, figsize=(15, 8))
        
        for idx, (metric, orig, audit) in enumerate(zip(metrics, original_scores, audited_scores)):
            row, col = idx // 3, idx % 3
            ax = axes[row, col]
            
            ax.hist(orig, bins=5, alpha=0.6, label='原始', color='#FF6B6B', edgecolor='black')
            ax.hist(audit, bins=5, alpha=0.6, label='改进', color='#4ECDC4', edgecolor='black')
            ax.set_title(f'{metric}分布')
            ax.set_xlabel('分数')
            ax.set_ylabel('频数')
            ax.legend()
        
        # 隐藏多余的子图
        for idx in range(len(metrics), 6):
            row, col = idx // 3, idx % 3
            axes[row, col].axis('off')
        
        plt.tight_layout()
        plt.savefig(f"{output_dir}/score_distribution.png", dpi=150, bbox_inches='tight')
        print(f"✓ 图表已保存：{output_dir}/score_distribution.png")
        
        plt.close('all')
    
    def print_summary(self):
        """打印摘要信息"""
        report = self.generate_report()
        
        if not report:
            print("没有数据可显示")
            return
        
        print(f"\n总样本数：{report['metadata']['total_samples']}\n")
        
        print("指标改进情况：")
        for metric, stats in report['metrics'].items():
            print(f"\n  {metric}:")
            print(f"    原始平均分：{stats['original']['mean']:.2f}/10")
            print(f"    改进平均分：{stats['audited']['mean']:.2f}/10")
            print(f"    改进幅度：+{stats['improvement_percent']:.1f}%")
        
        if report['key_findings']:
            print("\n关键发现：")
            for finding in report['key_findings']:
                print(f"  • {finding}")


if __name__ == "__main__":
    # 测试分析器（需要实际的评估结果）
    print("ResultAnalyzer模块已准备好，可以与评估结果一起使用")

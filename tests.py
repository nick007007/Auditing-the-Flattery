"""
单元测试模块

测试各个核心组件的功能
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

import unittest
from src.data_generator import SyntheticDataGenerator, DialogueExample
from src.audit_framework import AuditAgent, AuditPromptBuilder
from src.evaluator import Evaluator, EvaluatorPromptBuilder


class TestDataGenerator(unittest.TestCase):
    """测试数据生成器"""
    
    def setUp(self):
        self.generator = SyntheticDataGenerator()
    
    def test_generate_dataset(self):
        """测试数据集生成"""
        dataset = self.generator.generate_dataset(10)
        self.assertEqual(len(dataset), 10)
        self.assertIsInstance(dataset[0], DialogueExample)
    
    def test_dataset_statistics(self):
        """测试统计信息"""
        self.generator.generate_dataset(20)
        stats = self.generator.get_statistics()
        
        self.assertEqual(stats['total_samples'], 20)
        self.assertIn('categories', stats)
        self.assertIn('dimensions', stats)
        self.assertGreater(stats['avg_intensity'], 0)


class TestAuditFramework(unittest.TestCase):
    """测试审计框架"""
    
    def setUp(self):
        self.agent = AuditAgent()
    
    def test_audit_prompt_building(self):
        """测试审计提示词构建"""
        prompt = AuditPromptBuilder.build_audit_prompt(
            "用户输入测试",
            "模型回答测试"
        )
        
        self.assertIn("审计维度一", prompt)
        self.assertIn("审计维度二", prompt)
        self.assertIn("审计维度三", prompt)
        self.assertIn("献媚程度评分", prompt)
    
    def test_dialogue_analysis(self):
        """测试对话分析"""
        result = self.agent.analyze_dialogue(
            "test_001",
            "全球气温在下降",
            "您这个观点很有见地"
        )
        
        self.assertEqual(result.dialogue_id, "test_001")
        self.assertGreater(result.sycophancy_score, 0)
        self.assertLessEqual(result.sycophancy_score, 10)


class TestEvaluator(unittest.TestCase):
    """测试评估模块"""
    
    def setUp(self):
        self.evaluator = Evaluator(None)
    
    def test_evaluation_prompt_building(self):
        """测试评估提示词构建"""
        prompt = EvaluatorPromptBuilder.build_evaluation_prompt(
            "用户输入",
            "原始回答",
            "改进回答"
        )
        
        self.assertIn("事实准确性", prompt)
        self.assertIn("逻辑独立性", prompt)
        self.assertIn("情感中立度", prompt)
    
    def test_pair_evaluation(self):
        """测试回答对评估"""
        result = self.evaluator.evaluate_pair(
            "test_001",
            "用户输入",
            "原始回答",
            "改进回答"
        )
        
        self.assertEqual(result.dialogue_id, "test_001")
        self.assertGreater(result.factual_accuracy.original_score, 0)
        self.assertGreater(result.factual_accuracy.audited_score, 0)


class TestStatistics(unittest.TestCase):
    """测试统计计算"""
    
    def test_improvement_calculation(self):
        """测试改进百分比计算"""
        from src.evaluator import EvaluationScore
        
        score = EvaluationScore(
            metric="test",
            original_score=6.0,
            audited_score=8.0,
            improvement=0  # 会被计算
        )
        
        # 计算改进
        improvement = (score.audited_score - score.original_score) / score.original_score * 100
        self.assertAlmostEqual(improvement, 33.33, places=1)


def run_tests():
    """运行所有测试"""
    # 创建测试套件
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TestDataGenerator))
    suite.addTests(loader.loadTestsFromTestCase(TestAuditFramework))
    suite.addTests(loader.loadTestsFromTestCase(TestEvaluator))
    suite.addTests(loader.loadTestsFromTestCase(TestStatistics))
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    print("="*60)
    print("运行单元测试")
    print("="*60)
    
    success = run_tests()
    
    print("\n" + "="*60)
    if success:
        print("✓ 所有测试通过")
    else:
        print("✗ 部分测试失败")
    print("="*60)
    
    sys.exit(0 if success else 1)

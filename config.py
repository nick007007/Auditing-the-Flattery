"""
配置管理模块
"""
import os
from pathlib import Path
from typing import Dict, Any
import yaml
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class Config:
    """全局配置类"""
    
    # 项目路径
    PROJECT_ROOT = Path(__file__).parent.parent
    DATA_DIR = PROJECT_ROOT / "data"
    RESULTS_DIR = PROJECT_ROOT / "results"
    MODELS_DIR = PROJECT_ROOT / "models"
    
    # 创建必要的目录
    for dir_path in [DATA_DIR, RESULTS_DIR, MODELS_DIR]:
        dir_path.mkdir(parents=True, exist_ok=True)
    
    # API配置
    DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    
    # 模型配置
    GENERATOR_MODEL = {
        "provider": "deepseek",
        "model": "deepseek-chat",
        "temperature": 0.7,
        "max_tokens": 2000,
    }
    
    AUDITOR_MODEL = {
        "provider": "openai",
        "model": "gpt-4",
        "temperature": 0.3,
        "max_tokens": 2000,
    }
    
    EVALUATOR_MODEL = {
        "provider": "openai",
        "model": "gpt-4",
        "temperature": 0.2,
        "max_tokens": 1000,
    }
    
    # 实验配置
    DATASET_SIZE = 100
    NUM_ROUNDS = 5
    DOUBLE_BLIND = True
    
    # 数据类别
    DATA_CATEGORIES = [
        "expert_fallacy",
        "extreme_emotion",
        "stance_fluctuation",
        "vague_advice"
    ]
    
    # 献媚维度
    SYCOPHANCY_DIMENSIONS = [
        "answer_sycophancy",
        "feedback_sycophancy",
        "emotional_validation",
        "imitation_sycophancy",
        "moral_sycophancy",
        "indirect_sycophancy"
    ]
    
    # 评估指标
    EVALUATION_METRICS = [
        "factual_accuracy",
        "logical_independence",
        "emotional_neutrality"
    ]
    
    @classmethod
    def load_yaml(cls, config_path: str) -> Dict[str, Any]:
        """加载YAML配置文件"""
        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    @classmethod
    def get_config_dict(cls) -> Dict[str, Any]:
        """获取完整配置字典"""
        return {
            "project_root": str(cls.PROJECT_ROOT),
            "data_dir": str(cls.DATA_DIR),
            "results_dir": str(cls.RESULTS_DIR),
            "models": {
                "generator": cls.GENERATOR_MODEL,
                "auditor": cls.AUDITOR_MODEL,
                "evaluator": cls.EVALUATOR_MODEL,
            },
            "experiment": {
                "dataset_size": cls.DATASET_SIZE,
                "num_rounds": cls.NUM_ROUNDS,
                "double_blind": cls.DOUBLE_BLIND,
            },
            "data_categories": cls.DATA_CATEGORIES,
            "sycophancy_dimensions": cls.SYCOPHANCY_DIMENSIONS,
            "evaluation_metrics": cls.EVALUATION_METRICS,
        }


if __name__ == "__main__":
    print(Config.get_config_dict())

"""
模块初始化文件
"""

__version__ = "1.0.0"
__author__ = "LLM Sycophancy Research Team"
__description__ = "LLM Sycophancy Detection and Mitigation Framework"

from .config import Config
from .data_generator import SyntheticDataGenerator
from .audit_framework import AuditAgent
from .model_client import ModelFactory
from .evaluator import Evaluator
from .result_analyzer import ResultAnalyzer
from .experiment_runner import ExperimentRunner

__all__ = [
    "Config",
    "SyntheticDataGenerator",
    "AuditAgent",
    "ModelFactory",
    "Evaluator",
    "ResultAnalyzer",
    "ExperimentRunner"
]

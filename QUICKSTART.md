# 快速命令参考

## 基本操作

### 初始化项目
```bash
python init.py
```

### 运行交互式实验
```bash
python run_experiment.py
```

### 运行单元测试
```bash
python tests.py
```

### 直接运行完整管道
```bash
cd src
python experiment_runner.py
```

## 常用命令

### 生成数据集
```bash
python -c "from src.data_generator import SyntheticDataGenerator; \
g = SyntheticDataGenerator(); \
d = g.generate_dataset(100); \
g.save_dataset('./data/dataset.json')"
```

### 仅进行审计分析
```bash
python -c "from src.audit_framework import AuditAgent; \
a = AuditAgent(); \
r = a.analyze_dialogue('test', 'input', 'response'); \
print(f'Sycophancy Score: {r.sycophancy_score}/10')"
```

### 进行评估对比
```bash
python -c "from src.evaluator import Evaluator; \
e = Evaluator(None); \
r = e.evaluate_pair('test', 'input', 'original', 'audited'); \
print(f'Improvement: +{r.factual_accuracy.improvement:.1f}%')"
```

## 环境变量

编辑 `.env` 文件：

```bash
DEEPSEEK_API_KEY=sk-xxx
OPENAI_API_KEY=sk-xxx
ANTHROPIC_API_KEY=sk-xxx
```

## 文件位置

- **数据文件**：`./data/`
- **结果文件**：`./results/`
- **代码模块**：`./src/`
- **配置文件**：`./config.yaml`

## 故障排除

### ImportError: No module named 'src'
```bash
# 添加当前目录到Python路径
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
python run_experiment.py
```

### API密钥无效
检查 `.env` 文件中的密钥是否正确填写

### 内存不足
减少 `config.yaml` 中的 `dataset_size` 参数

## 性能优化

- 使用本地模型以避免API调用：编辑 `config.yaml` 中的 provider
- 减少样本大小用于快速原型设计
- 使用 `--profile` 标志进行性能分析

## 输出示例

```
成功完成实验后，您将获得：

1. 合成数据集：
   - 总样本数：100
   - 按类别分布：25+25+25+25

2. 审计结果：
   - 平均献媚度：6.5/10
   - 识别出的献媚模式

3. 评估报告：
   - 事实准确性：+42.7%
   - 逻辑独立性：+52.6%
   - 情感中立度：+56.5%

4. 可视化图表：
   - evaluation_comparison.png
   - score_distribution.png
```

更多细节请参考 README.md

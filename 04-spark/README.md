# Spark

## 学习进度

- [x] Spark 是什么
- [ ] Spark 架构
- [ ] PySpark 环境
- [ ] DataFrame
- [ ] Spark SQL
- [ ] Partition
- [ ] Parquet
- [ ] Performance Optimization

---

# 1. Spark 是什么

## 概念

- Spark 是分布式计算引擎
- 用于处理大规模数据
- 通过并行计算提高处理速度

## 关系

```text
Large Data
    ↓
Spark
    ↓
Distributed Processing
    ↓
Result
```

---

# 2. Spark Architecture

## 概念

- Driver：负责调度任务
- Executor：负责执行任务
- Cluster Manager：负责分配资源
- Partition：数据分块
- Task：处理 Partition 的任务

## 关系

```text
Driver
  │
  ▼
Cluster Manager
  │
  ▼
Executor
  │
  ▼
Task
```
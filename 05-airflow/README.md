# Airflow

## 学习进度

- [x] Airflow 是什么
- [x] DAG
- [x] Task
- [x] Operator
- [x] BashOperator
- [x] PythonOperator
- [x] Task Dependency
- [x] Scheduling
- [x] Retry
- [x] Logs
- [x] Backfill / Catchup
- [x] 调度 Spark ETL 的思路
- [x] 业务日期 `{{ ds }}`
- [x] Sensor
- [x] XCom
- [x] Variables / Connections
- [x] Airflow Mini Project
- [x] Airflow 第一轮总结

---

# 1. Airflow 是什么

## 概念

Airflow 是一个工作流调度工具。

它解决的问题不是“怎么算数据”，而是：

```text
任务什么时候运行？
任务之间谁先谁后？
任务失败了怎么办？
任务日志在哪里看？
任务能不能自动重跑？
历史任务能不能补跑？
```

Spark 负责处理数据：

```text
Read CSV
    ↓
Clean / Filter
    ↓
Aggregation
    ↓
Write Parquet
```

Airflow 负责调度任务：

```text
每天凌晨 2 点运行 Spark ETL
失败后自动重试
先跑清洗任务，再跑汇总任务
查看任务日志
```

## Spark 和 Airflow 的关系

```text
Spark：干活的人
Airflow：安排活的人
```

更具体：

```text
Spark Job
    ↓
负责处理数据

Airflow DAG
    ↓
负责安排 Spark Job 什么时候跑、按什么顺序跑
```

## 重点

> Spark 是计算工具，Airflow 是调度工具。

---

# 2. Airflow 核心概念

## DAG

DAG 是一个工作流。

DAG 全称是：

```text
Directed Acyclic Graph
```

可以理解为：

```text
有方向、不能循环的任务流程图
```

比如：

```text
download_data
    ↓
clean_data
    ↓
aggregate_data
    ↓
check_result
```

这个完整流程就是一个 DAG。

---

## Task

Task 是 DAG 里面的一个具体任务。

例如：

```text
check_input
run_etl
check_output
```

关系：

```text
DAG
 ├── Task 1
 ├── Task 2
 └── Task 3
```

---

## Operator

Operator 决定一个 Task 怎么执行。

常见 Operator：

```text
BashOperator      执行 Linux 命令
PythonOperator    执行 Python 函数
Sensor            等待某个条件满足
```

可以这样理解：

```text
Task 是任务
Operator 是任务的执行方式
```

---

## Schedule

Schedule 表示 DAG 什么时候运行。

例如：

```text
手动运行
每天运行一次
每小时运行一次
每周运行一次
```

---

# 3. 第一个 DAG

## 示例

文件路径：

```text
05-airflow/dags/hello_airflow.py
```

代码：

```python
from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator


with DAG(
    dag_id="hello_airflow",
    start_date=datetime(2026, 7, 27),
    schedule=None,
    catchup=False,
    tags=["learning"],
) as dag:

    task_1 = BashOperator(
        task_id="say_hello",
        bash_command="echo 'Hello Airflow'",
    )

    task_2 = BashOperator(
        task_id="show_date",
        bash_command="date",
    )

    task_1 >> task_2
```

## 重点解释

```python
dag_id="hello_airflow"
```

表示 DAG 的名字。

```python
start_date=datetime(2026, 7, 27)
```

表示 DAG 从哪一天开始生效。

```python
schedule=None
```

表示不自动调度，只手动运行。

```python
catchup=False
```

表示不要自动补跑历史任务。

```python
task_1 >> task_2
```

表示 `task_1` 先执行，`task_2` 后执行。

## 重点

> DAG 是工作流，Task 是具体任务，Operator 决定任务怎么执行。

---

# 4. BashOperator

## 概念

BashOperator 用来执行 Shell 命令。

适合执行：

```text
echo
date
ls
test -f
spark-submit
docker run
```

## 示例

```python
from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator


with DAG(
    dag_id="bash_operator_basic",
    start_date=datetime(2026, 7, 27),
    schedule=None,
    catchup=False,
    tags=["learning"],
) as dag:

    say_hello = BashOperator(
        task_id="say_hello",
        bash_command="echo 'Hello Airflow'",
    )

    show_date = BashOperator(
        task_id="show_date",
        bash_command="date",
    )

    say_hello >> show_date
```

## 重点

> BashOperator 适合执行 Linux 命令，也适合用来调度 `spark-submit`。

---

# 5. PythonOperator

## 概念

PythonOperator 用来执行 Python 函数。

适合执行：

```text
数据检查
参数处理
简单 Python 逻辑
调用自定义函数
```

## 示例

```python
from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator


def say_hello():
    print("Hello Airflow from Python function")


def show_message():
    message = "This is a PythonOperator task"
    print(message)


with DAG(
    dag_id="python_operator_basic",
    start_date=datetime(2026, 7, 27),
    schedule=None,
    catchup=False,
    tags=["learning"],
) as dag:

    task_1 = PythonOperator(
        task_id="say_hello",
        python_callable=say_hello,
    )

    task_2 = PythonOperator(
        task_id="show_message",
        python_callable=show_message,
    )

    task_1 >> task_2
```

## 重点

这里要写：

```python
python_callable=say_hello
```

不要写成：

```python
python_callable=say_hello()
```

区别：

```text
say_hello      把函数交给 Airflow，等任务运行时再执行
say_hello()    现在立刻执行函数
```

---

# 6. PythonOperator 传参数

## 示例

```python
from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator


def print_city(city):
    print(f"Current city is {city}")


with DAG(
    dag_id="python_operator_with_params",
    start_date=datetime(2026, 7, 27),
    schedule=None,
    catchup=False,
    tags=["learning"],
) as dag:

    task = PythonOperator(
        task_id="print_city",
        python_callable=print_city,
        op_kwargs={
            "city": "Beijing"
        },
    )
```

## 重点

`op_kwargs` 用来给 Python 函数传参数。

---

# 7. Task Dependency 任务依赖

## 概念

任务依赖解决的问题是：

```text
哪个任务先执行？
哪个任务后执行？
哪个任务必须等前面的任务成功后才能执行？
```

## 最常见写法

```python
task_1 >> task_2
```

表示：

```text
task_1 先执行
task_2 后执行
```

## 示例

```python
from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator


with DAG(
    dag_id="task_dependency_basic",
    start_date=datetime(2026, 7, 27),
    schedule=None,
    catchup=False,
    tags=["learning"],
) as dag:

    check_input = BashOperator(
        task_id="check_input",
        bash_command="echo 'Checking input data...'",
    )

    run_etl = BashOperator(
        task_id="run_etl",
        bash_command="echo 'Running ETL job...'",
    )

    check_output = BashOperator(
        task_id="check_output",
        bash_command="echo 'Checking output data...'",
    )

    check_input >> run_etl >> check_output
```

## 分叉依赖

```python
extract_data >> [clean_orders, clean_customers]
[clean_orders, clean_customers] >> build_report
```

表示：

```text
extract_data
    ↓
clean_orders 和 clean_customers 可以并行
    ↓
两个都成功后
    ↓
build_report 才执行
```

## 数仓对应

```text
ODS
    ↓
DWD
    ↓
DWS
    ↓
ADS
```

Airflow 里可以写成：

```python
ods_task >> dwd_task >> dws_task >> ads_task
```

## 重点

> Airflow 用 `task_1 >> task_2` 表示任务依赖。

---

# 8. Scheduling 调度周期

## 概念

Scheduling 决定 DAG 什么时候自动运行。

例如：

```text
手动运行
每天运行一次
每小时运行一次
每周运行一次
```

## 不自动调度

```python
schedule=None
```

表示只手动运行。

学习阶段常用这个。

## 每天运行一次

```python
schedule="@daily"
```

## 常见预设

```text
@once       只运行一次
@hourly     每小时一次
@daily      每天一次
@weekly     每周一次
@monthly    每月一次
```

## cron 表达式

每天凌晨 2 点运行：

```python
schedule="0 2 * * *"
```

cron 结构：

```text
分 时 日 月 星期
```

常见例子：

```text
0 2 * * *      每天凌晨 2 点
0 9 * * *      每天上午 9 点
0 * * * *      每小时整点
30 1 * * *     每天凌晨 1:30
0 8 * * 1      每周一早上 8 点
```

## 示例

```python
from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator


with DAG(
    dag_id="daily_pipeline_basic",
    start_date=datetime(2026, 7, 27),
    schedule="@daily",
    catchup=False,
    tags=["learning"],
) as dag:

    start = BashOperator(
        task_id="start",
        bash_command="echo 'Start daily pipeline'",
    )

    run_etl = BashOperator(
        task_id="run_etl",
        bash_command="echo 'Run ETL job'",
    )

    end = BashOperator(
        task_id="end",
        bash_command="echo 'Finish daily pipeline'",
    )

    start >> run_etl >> end
```

## 重点

> `schedule` 决定 DAG 什么时候自动运行；学习阶段用 `schedule=None`，真实日任务常用 `@daily` 或 `"0 2 * * *"`。

---

# 9. Retry 失败重试

## 概念

Retry 表示任务失败后自动重试。

常见原因：

```text
源系统还没准备好数据
网络临时异常
文件还没到
数据库连接超时
Spark 任务偶发失败
```

## 基本写法

```python
retries=3
retry_delay=timedelta(minutes=5)
```

表示：

```text
失败后最多重试 3 次
每次重试间隔 5 分钟
```

## 示例

```python
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator


with DAG(
    dag_id="retry_basic",
    start_date=datetime(2026, 7, 27),
    schedule=None,
    catchup=False,
    tags=["learning"],
) as dag:

    unstable_task = BashOperator(
        task_id="unstable_task",
        bash_command="exit 1",
        retries=3,
        retry_delay=timedelta(minutes=5),
    )
```

## default_args

如果多个任务使用相同重试规则，可以放到 `default_args`。

```python
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator


default_args = {
    "retries": 3,
    "retry_delay": timedelta(minutes=5),
}


with DAG(
    dag_id="retry_with_default_args",
    start_date=datetime(2026, 7, 27),
    schedule=None,
    catchup=False,
    default_args=default_args,
    tags=["learning"],
) as dag:

    check_input = BashOperator(
        task_id="check_input",
        bash_command="echo 'checking input'",
    )

    run_etl = BashOperator(
        task_id="run_etl",
        bash_command="echo 'running etl'",
    )

    check_input >> run_etl
```

## 重点

> Retry 用来处理临时失败，常用参数是 `retries` 和 `retry_delay`。

---

# 10. Logs 日志

## 概念

Airflow 每个 Task 都有自己的日志。

日志里可以看到：

```text
任务什么时候开始
执行了什么命令
Python 函数打印了什么
报错原因是什么
任务是否重试
任务最终成功还是失败
```

## Web UI 查看日志流程

```text
进入 DAG
    ↓
点击某一次运行记录
    ↓
点击失败的 Task
    ↓
点击 Logs
```

## BashOperator 日志

```python
run_etl = BashOperator(
    task_id="run_etl",
    bash_command="echo 'Running ETL job...'",
)
```

日志里会看到：

```text
Running ETL job...
```

如果命令失败：

```python
bad_task = BashOperator(
    task_id="bad_task",
    bash_command="ls /not_exists_path",
)
```

日志里可能看到：

```text
ls: cannot access '/not_exists_path': No such file or directory
```

## PythonOperator 日志

```python
def check_input_file():
    print("Checking input file...")
    print("Input file exists")
```

`print()` 内容会进入 Task 日志。

## 失败排查顺序

```text
1. 哪个 DAG 失败了？
2. 哪个 Task 失败了？
3. 这个 Task 的 Logs 里最后一个 ERROR 是什么？
4. 是文件不存在、权限问题、SQL 报错，还是 Spark 报错？
5. 修复后重跑失败的 Task 或整个 DAG
```

## 重点

> Airflow 排查失败的第一步：先找到失败的 Task，再看这个 Task 的 Logs。

---

# 11. Backfill 和 Catchup

## 概念

Backfill 可以理解为：

```text
补跑历史日期的任务
```

比如一个 DAG：

```python
schedule="@daily"
start_date=datetime(2026, 7, 1)
```

如果今天是 2026-07-27，Airflow 可能会认为中间每天都应该运行一次。

如果允许补跑，就可能创建很多历史任务。

## catchup

```python
catchup=False
```

表示不要自动补跑历史任务。

```python
catchup=True
```

表示允许自动补跑历史任务。

## 示例

```python
from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator


with DAG(
    dag_id="catchup_basic",
    start_date=datetime(2026, 7, 1),
    schedule="@daily",
    catchup=False,
    tags=["learning"],
) as dag:

    print_date = BashOperator(
        task_id="print_date",
        bash_command="echo 'Run daily task'",
    )
```

## 真实数仓场景

正常运行：

```text
2026-07-25 02:00 → 处理 2026-07-24 的数据
2026-07-26 02:00 → 处理 2026-07-25 的数据
2026-07-27 02:00 → 处理 2026-07-26 的数据
```

如果某天失败，需要补跑历史日期，这就是 Backfill 的场景。

## 重点

> `catchup=False` 表示不要自动补跑历史任务；Backfill 是补跑历史日期的数据任务。

---

# 12. 业务日期 `{{ ds }}`

## 概念

Airflow 每次运行 DAG 时，都会有一个对应的调度日期。

常见模板变量：

```text
{{ ds }}
```

格式：

```text
YYYY-MM-DD
```

例如：

```text
2026-07-26
```

在数据工程里，这个日期经常作为业务日期传给 Spark、SQL 或 Hive。

## BashOperator 中使用

```python
bash_command="echo 'Current ds is {{ ds }}'"
```

运行时，Airflow 会把 `{{ ds }}` 替换成当前 DAG Run 的日期。

## 示例

```python
from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator


with DAG(
    dag_id="ds_basic",
    start_date=datetime(2026, 7, 27),
    schedule="@daily",
    catchup=False,
    tags=["learning"],
) as dag:

    print_ds = BashOperator(
        task_id="print_ds",
        bash_command="echo 'Current ds is {{ ds }}'",
    )
```

## 和 Spark ETL 结合

```python
run_spark_etl = BashOperator(
    task_id="run_spark_etl",
    bash_command="""
    spark-submit /app/etl.py --dt {{ ds }}
    """,
)
```

## 数仓对应

Hive 里常见：

```sql
WHERE dt = '${biz_date}'
```

Airflow + Spark 里：

```text
Airflow 的 {{ ds }}
    ↓
传给 Spark 参数 --dt
    ↓
Spark 处理对应 dt 分区
```

## 重点

> `{{ ds }}` 是 Airflow 常用的日期模板变量，可以把调度日期传给 Spark / SQL，用来处理指定业务日期的数据。

---

# 13. Sensor

## 概念

Sensor 用来等待某个条件满足。

常见用途：

```text
等待文件出现
等待某个目录生成
等待上游任务完成
等待某个分区数据到达
```

## 为什么需要 Sensor？

比如任务每天 2 点运行，但上游文件 2:05 才生成。

没有 Sensor：

```text
02:00 检查文件
文件不存在
任务失败
```

有 Sensor：

```text
02:00 检查文件，不存在
等待一会儿
02:02 再检查，不存在
等待一会儿
02:05 文件到了
继续执行后面的 ETL
```

## Sensor 和 Retry 的区别

```text
Retry：
检查失败 → Task 失败 → 等待 → 重试

Sensor：
检查失败 → Task 继续等待 → 再检查 → 条件满足后成功
```

## 简化代码理解

```python
wait_for_input = FileSensor(
    task_id="wait_for_input",
    filepath="/data/input/orders.csv",
    poke_interval=60,
    timeout=1800,
)
```

参数：

```text
filepath       等待哪个文件
poke_interval  每隔多少秒检查一次
timeout        最多等待多久
```

## DAG 中的位置

```python
wait_for_input >> run_spark_etl >> check_output
```

对应：

```text
等待输入文件
    ↓
运行 Spark ETL
    ↓
检查输出结果
```

## 重点

> Sensor 用来等待上游条件满足，比如等待文件到达；Sensor 是持续等待，Retry 是失败后重试。

---

# 14. XCom

## 概念

XCom 是 Airflow 里用来在 Task 之间传递小数据的机制。

XCom 全称：

```text
cross-communication
```

可以理解为：

```text
Task 之间传递小结果
```

## 适合传什么？

适合传小数据：

```text
日期
状态
文件路径
小字符串
小数字
少量参数
```

不适合传大数据：

```text
DataFrame
大文件
大量 JSON
上百万行数据
```

## PythonOperator 自动返回 XCom

```python
def get_biz_date():
    return "2026-07-26"
```

这个返回值可以被后面的 Task 使用。

## 示例

```python
from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator


def get_biz_date():
    biz_date = "2026-07-26"
    print(f"Business date is {biz_date}")
    return biz_date


def use_biz_date(ti):
    biz_date = ti.xcom_pull(task_ids="get_biz_date")
    print(f"Use business date: {biz_date}")


with DAG(
    dag_id="xcom_basic",
    start_date=datetime(2026, 7, 27),
    schedule=None,
    catchup=False,
    tags=["learning"],
) as dag:

    task_1 = PythonOperator(
        task_id="get_biz_date",
        python_callable=get_biz_date,
    )

    task_2 = PythonOperator(
        task_id="use_biz_date",
        python_callable=use_biz_date,
    )

    task_1 >> task_2
```

## 重点

```python
ti.xcom_pull(task_ids="get_biz_date")
```

表示从 `get_biz_date` 这个 Task 里取出 XCom 值。

## 注意

不要用 XCom 传 DataFrame。

正确方式：

```text
Task 1 处理数据并写到文件 / 表
Task 2 读取这个文件 / 表继续处理
```

## 重点

> XCom 用来在 Task 之间传递小数据，比如日期、路径、状态；不要用 XCom 传大数据或 DataFrame。

---

# 15. Variables 和 Connections

## 概念

Variables 和 Connections 用来管理配置，避免把参数、路径、账号密码都写死在 DAG 代码里。

---

## Variables

Variables 用来保存普通配置。

适合放：

```text
文件路径
环境名称
业务系统名称
普通参数
开关配置
```

例如：

```text
orders_input_path = /data/input/orders.csv
orders_output_path = /data/output/dws_city_sales_daily
```

DAG 里读取：

```python
from airflow.models import Variable

input_path = Variable.get("orders_input_path")
output_path = Variable.get("orders_output_path")
```

---

## Connections

Connections 用来保存外部系统连接信息。

适合放：

```text
MySQL
PostgreSQL
Hive
Spark Cluster
AWS
S3
FTP
HTTP API
```

一个数据库连接通常包含：

```text
host
port
username
password
database
```

---

## Variables vs Connections

| 类型 | 用来存什么 | 例子 |
|---|---|---|
| Variables | 普通配置 | 路径、环境名、业务参数 |
| Connections | 外部系统连接 | 数据库、S3、API、FTP |

## 重点

```text
Variables 管参数
Connections 管连接
```

---

# 16. 用 Airflow 调度 Spark ETL 的思路

## 整体关系

Spark 负责处理数据：

```text
spark-submit first_pyspark.py
```

Airflow 负责安排任务：

```text
check_input
    ↓
run_spark_etl
    ↓
check_output
```

也就是：

```text
Airflow DAG
    ↓
BashOperator
    ↓
执行 spark-submit 命令
    ↓
Spark ETL 处理数据
```

## 为什么用 BashOperator 调 Spark？

因为运行 Spark 脚本，本质上就是执行一条 Linux 命令。

例如：

```bash
spark-submit /app/first_pyspark.py
```

所以 Airflow 可以把它放进 `BashOperator`。

---

# 17. Airflow Mini Project

## 项目目标

用 Airflow 的思想组织一个完整数据任务流程：

```text
check_input
    ↓
run_spark_etl
    ↓
check_output
```

含义：

```text
检查输入文件是否存在
    ↓
运行 Spark ETL
    ↓
检查输出目录是否生成
```

---

## 项目结构

```text
05-airflow/
├── README.md
└── dags/
    └── spark_mini_etl_dag.py
```

---

## DAG 完整代码

```python
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator


default_args = {
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}


with DAG(
    dag_id="spark_mini_etl_pipeline",
    start_date=datetime(2026, 7, 27),
    schedule=None,
    catchup=False,
    default_args=default_args,
    tags=["spark", "etl", "learning"],
) as dag:

    check_input = BashOperator(
        task_id="check_input",
        bash_command=(
            "test -f "
            "/home/kevin/data-engineer-learning/04-spark/data/input/orders.csv"
        ),
    )

    run_spark_etl = BashOperator(
        task_id="run_spark_etl",
        bash_command="""
        sudo docker run --rm \
        -v /home/kevin/data-engineer-learning/04-spark/labs:/app \
        -v /home/kevin/data-engineer-learning/04-spark/data:/data \
        apache/spark-py:latest \
        /opt/spark/bin/spark-submit /app/first_pyspark.py
        """,
    )

    check_output = BashOperator(
        task_id="check_output",
        bash_command=(
            "test -d "
            "/home/kevin/data-engineer-learning/04-spark/data/output/dws_city_sales_daily"
        ),
    )

    check_input >> run_spark_etl >> check_output
```

---

## 代码拆解

### default_args

```python
default_args = {
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}
```

表示：

```text
每个任务失败后最多重试 2 次
每次重试间隔 5 分钟
```

### check_input

```python
test -f /home/kevin/data-engineer-learning/04-spark/data/input/orders.csv
```

表示检查输入文件是否存在。

### run_spark_etl

执行 Spark ETL 脚本。

本质上是把之前手动执行的 Docker + spark-submit 命令交给 Airflow。

### check_output

```python
test -d /home/kevin/data-engineer-learning/04-spark/data/output/dws_city_sales_daily
```

表示检查输出目录是否生成。

### 任务依赖

```python
check_input >> run_spark_etl >> check_output
```

表示：

```text
check_input 成功
    ↓
run_spark_etl 才能运行
    ↓
run_spark_etl 成功
    ↓
check_output 才能运行
```

---

## 真实数仓对应关系

```text
check_input
    ↓
检查 ODS 原始文件是否到达

run_spark_etl
    ↓
ODS → DWD → DWS

check_output
    ↓
检查 DWS 汇总结果是否生成
```

以后可以扩展成：

```text
wait_input_file
    ↓
ods_load
    ↓
dwd_clean
    ↓
dws_aggregate
    ↓
ads_report
    ↓
quality_check
```

---

# 18. Airflow 环境说明

## 当前环境情况

曾尝试使用官方 Docker Compose 启动 Airflow，但由于电脑物理内存只有 8GB，虚拟机分配 2GB 内存，完整 Airflow 多容器环境会触发 OOM。

报错现象：

```text
Out of memory
airflow-apiserver unhealthy
VS Code SSH 断开重连
```

## 当前学习策略

当前阶段先不强行运行完整 Airflow 环境，而是重点掌握：

```text
DAG 怎么写
Task 怎么定义
Operator 怎么用
任务依赖怎么组织
调度周期怎么理解
失败怎么重试
日志怎么排查
Spark ETL 怎么被 Airflow 调度
```

## 原因

真实公司里 Airflow 通常已经部署好，数据工程师更多负责：

```text
写 DAG
改 DAG
看日志
重跑任务
排查失败
维护任务依赖
```

不一定每个人都要从零部署 Airflow 集群。

---

# 19. 面试表达

## English

```text
Airflow is a workflow orchestration tool.

I use Airflow to define DAGs, manage task dependencies, schedule ETL jobs, configure retries, and check task logs.

In my learning project, I designed a DAG to orchestrate a Spark ETL pipeline. The DAG checks whether the input file exists, runs the Spark job with BashOperator, and validates whether the output directory is generated.

I also learned concepts such as schedule, catchup, retry, logs, sensors, XCom, variables, and connections.
```

## 中文理解

```text
Airflow 是工作流调度工具。

我用 Airflow 定义 DAG、管理任务依赖、调度 ETL 任务、配置失败重试，并通过日志排查任务失败原因。

在我的学习项目中，我设计了一个 DAG 来调度 Spark ETL。这个 DAG 先检查输入文件是否存在，然后通过 BashOperator 执行 Spark 任务，最后检查输出目录是否生成。

我也学习了 schedule、catchup、retry、logs、sensor、XCom、variables 和 connections 等概念。
```

---

# 20. Airflow 第一轮总结

## 已掌握内容

- Airflow 是工作流调度工具
- DAG 是工作流
- Task 是具体任务
- Operator 决定任务怎么执行
- BashOperator 用来执行 Shell 命令
- PythonOperator 用来执行 Python 函数
- `task_1 >> task_2` 表示任务依赖
- `schedule` 决定调度周期
- `retries` 和 `retry_delay` 用来失败重试
- Logs 用来排查任务失败原因
- `catchup=False` 表示不要自动补跑历史任务
- Backfill 表示补跑历史数据
- `{{ ds }}` 是常用业务日期模板变量
- Sensor 用来等待上游条件满足
- XCom 用来在任务之间传递小数据
- Variables 用来保存普通参数
- Connections 用来保存外部系统连接
- Airflow 可以通过 BashOperator 调度 Spark ETL

## 当前阶段目标

第一轮 Airflow 学习目标不是部署完整集群，而是：

```text
能看懂 DAG 文件
知道 Task 怎么定义
知道 Operator 是干什么的
知道任务依赖怎么写
知道 schedule / retry / logs / catchup 是什么
知道怎么用 Airflow 调度 Spark ETL
```

## 下一阶段

进入 AWS：

```text
06-aws
    ↓
IAM
S3
Glue
Glue Data Catalog
Athena
EC2
Redshift Basics
```

AWS 学习目标：

```text
理解云上数据工程基础
知道数据如何存到 S3
知道如何用 Athena 查询 S3 数据
知道 IAM 权限的基本作用
知道 Glue / Data Catalog 在数据平台中的位置
```
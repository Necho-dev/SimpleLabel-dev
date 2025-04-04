# SimpleLabel

`simplelabel` 是一个使用 Python 编写的工具，它可以根据规则轻松地对文件进行标注，同时也支持根据规则快速生成 SQL 语句。

## 安装
首先，确保你已经安装了 Python 3.6 或更高版本（推荐Python 3.8及以上）。然后，你可以使用以下命令安装 `simplelabel`：

```bash
pip install simplelabel
```

## 命令行使用方法

### 显示版本信息
如果你想查看 `simplelabel` 的版本信息，可以使用以下命令：
```bash
simplelabel --version
```

### 快速完成数据标注
使用 `--label` 指令可以快速完成数据标注，该指令需要输入规则文件地址和原始待标注的数据文件地址，同时通过 `-o` 标识指定数据输出地址。示例如下：
```bash
simplelabel --label rule_file.csv data_file.csv -o output_labeled_data.csv
```

### 快速完成 SQL 语句生成
使用 `--generate` 指令可以快速完成 SQL 语句生成，该指令需要输入规则文件地址，同时通过 `-o` 标识指定 SQL 文件输出地址。示例如下：
```bash
simplelabel --generate rule_file.csv -o output_sql.txt
```

## Python 使用方法
`simplelabel` 也提供了 Python API，你可以使用以下代码来完成数据标注和 SQL 语句生成：

```python
from simplelabel import FieldMap, FieldsIdentifier
from simplelabel import DataLabelEngine, SQLGenerator

if __name__ == '__main__':
    rule_file_path = 'data/rules_zfb.csv'
    bill_file_path = 'data/bills_zfb.csv'
    labeled_file_path = 'data/bills_zfb_labeled.csv'
    sql_file_path = 'data/bills_zfb_sql.sql'

    field_map = FieldMap(
        field1='筛选字段1',
        condition1='筛选条件1',
        keyword1='关键字1',
        logic='关联条件',
        field2='（可选）筛选字段2',
        condition2='（可选）筛选条件2',
        keyword2='（可选）关键字2',
        label='账单类别'
    )

    # 根据规则标注数据
    label_engine = DataLabelEngine.init(rule_file_path, field_map)
    label_engine.label(bill_file_path, labeled_file_path)

    field_identifier = FieldsIdentifier({
        '业务类型': 'yw_type',
        '业务描述': 'yw_desc',
        '备注': 'remark'
    }).init()

    # 根据规则生成 SQL 语句
    sql_generator = SQLGenerator.init(rule_file_path, field_map)
    sql_generator.generate(sql_file_path, field_identifier)

```

### 代码解读
- `FieldMap` 类用于定义规则文件中的列名映射关系，包括筛选字段、筛选条件、关键字、关联条件、筛选字段2、筛选条件2、关键字2和账单类别等。

```python
# 默认列名映射关系
# DEFAULT_FIELD_MAP
field1='筛选字段1',
condition1='筛选条件1',
keyword1='关键字1',
logic='关联条件',
field2='（可选）筛选字段2',
condition2='（可选）筛选条件2',
keyword2='（可选）关键字2',
label='账单类别'
```

- `FieldsIdentifier` 类用于定义需标注数据的字段标识和字段名称的对应关系，包括业务类型、业务描述和备注等。
- `DataLabelEngine` 类用于根据规则对数据进行标注，包括初始化规则、数据标注和输出标注结果等方法。
- `SQLGenerator` 类用于根据规则生成 SQL 语句，包括初始化规则、生成SQL语句和输出SQL文件等方法。 

在上述代码中，`rule_file_path` 是标注规则文件路径，`bill_file_path` 是原始待标注的数据文件路径，`labeled_file_path` 是标注后的数据文件路径，`sql_file_path` 是 SQL 语句文件路径。

我们首先实例化 `FieldMap` 对象，接着使用 `DataLabelEngine` 类根据标注规则对原始数据进行标注，输出标注结果文件，最后使用 `SQLGenerator` 类生成 SQL 语句，输出SQL文件。
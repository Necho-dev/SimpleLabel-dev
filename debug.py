from typing import Dict
from simplelabel import *


def record_to_dict(data) -> Dict[str, str]:
    if isinstance(data, dict):
        records = data.get('record', {})
        field_mapping = data.get('field_mapping', {})
    elif hasattr(data, 'record') and hasattr(data, 'field_mapping'):
        records = data.record
        field_mapping = data.field_mapping
    else:
        raise ValueError("Unsupported input data structure")

    result = {}
    for field_name, field_identifier in field_mapping.items():
        if field_identifier in records:
            result[field_name] = str(records[field_identifier]).strip()
        else:
            result[field_name] = ''
    return result


record = {
    'record': {
        'sxzd1': "'",
        'sxtj1': "'",
        'gjz1': "'",
        'kxsxzd2': '动账摘要',
        'kxsxtj2': '包含',
        'kxgjz2': '预扣费；操作费；配送费；拦截费',
        'zdlb': '偏远地区物流费服务费'
    },
    'field_mapping': {
        '筛选字段1': 'sxzd1',
        '筛选条件1': 'sxtj1',
        '关键字1': 'gjz1',
        '关联条件': 'gltj',
        '（可选）筛选字段2': 'kxsxzd2',
        '（可选）筛选条件2': 'kxsxtj2',
        '（可选）关键字2': 'kxgjz2',
        '账单类别': 'zdlb'
    }
}
rules = [
    {
        '筛选字段1': "'",
        '筛选条件1': "'",
        '关键字1': "'",
        '（可选）筛选字段2': '动账摘要',
        '（可选）筛选条件2': '包含',
        '（可选）关键字2': '预扣费；操作费；配送费；拦截费',
        '账单类别': '偏远地区物流费服务费'
    }
]

rules = [record_to_dict(rules)]
print(RuleParser(rules).parse())

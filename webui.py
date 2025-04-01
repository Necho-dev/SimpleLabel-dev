import gradio as gr
import pandas as pd
from typing import Union, List


DEFAULT_CONDITION_CHOICES = [
    '',
    '等于', '不等于',
    '为空', '不为空',
    '大于', '大于等于',
    '小于', '小于等于',
    '包含', '不包含',
    '开头是', '开头不是',
    '结尾是', '结尾不是',
    '正则匹配', '正则不匹配'
]

css = """
.md-title {
    margin: 1px 0px 6px 0px
}
.table {
    scrollbar-width: thin;
    scrollbar-color: var(--button-primary-background-fill) rgba(0, 0, 0, 0);
    overflow-x: auto;
}
.table td {
    white-space: pre-warp;
}
"""


def create_rule_form(visible: bool = False):
    """
    新建数据标注规则配置表单
    """
    with gr.Accordion("数据标注规则配置(新增/更新)", open=True, visible=visible) as form_accord:
        with gr.Row():
            field1 = gr.Textbox(label="筛选字段1", placeholder="数据字段名称", interactive=True)
            condition1 = gr.Dropdown(DEFAULT_CONDITION_CHOICES, label="筛选条件1", interactive=True, value='')
            keyword1 = gr.Textbox(label="关键字1", placeholder="匹配关键词", interactive=True)
            logic = gr.Dropdown(["", "且", "或"], label="关联条件", interactive=True, value='')
            field2 = gr.Textbox(label="（可选）筛选字段2", interactive=True)
            condition2 = gr.Dropdown(DEFAULT_CONDITION_CHOICES, label="（可选）筛选条件2", interactive=True, value='')
            keyword2 = gr.Textbox(label="（可选）关键字2", interactive=True)
            label = gr.Textbox(label="类别标签", placeholder="账单/订单类别名称", interactive=True)
    return form_accord, field1, condition1, keyword1, logic, field2, condition2, keyword2, label


def on_select_row(event: gr.SelectData):
    """
    选择行时返回索引
    """
    if event.index is None:
        return None
    return event.index[0]


def fill_rule_form(data: pd.DataFrame, index) -> Union[List, None]:
    """
    根据指定数据和索引返回规则实例
    :param data: 数据
    :param index: 索引
    :return: List[]或None
    """
    # 索引为空或超出范围时返回None
    if index is None or index >= len(data):
        return None
    # 根据索引获取数据行
    row = data.iloc[index]
    if row is None:
        return None
    # 返回规则数据
    return [
        row["筛选字段1"],
        row["筛选条件1"],
        row["关键字1"],
        row["关联条件"],
        row["（可选）筛选字段2"],
        row["（可选）筛选条件2"],
        row["（可选）关键字2"],
        row["类别标签"]
    ]


def create_identifier_inputs():
    with gr.Accordion("字段标识配置 (用于SQL语句生成)", open=True):
        for i in range(1, 10):
            with gr.Row():
                inputs = {
                    "数据字段名称": gr.Textbox(
                        label="数据字段名称",
                        value="value",
                        interactive=False
                    ),
                    "字段标识": gr.Textbox(
                        label="字段标识",
                        value="字段标识",
                        interactive=True
                    )
                }
    return inputs


def dataframe(value=None, max_height: int = 1000, interactive: bool = False, wrap: bool = False, visible: bool = False):
    return gr.Dataframe(
        value=value,
        interactive=interactive,
        max_height=max_height,
        wrap=wrap,
        visible=visible
    )


def preview_file(file):
    if file is None:
        return None
    try:
        df = pd.read_csv(file.name)
        # df.columns = ["筛选字段1", "筛选条件1", "关键字1", "关联条件", "筛选字段2", "筛选条件2", "关键字2", "类别标签"]
        return df
        # return dataframe(df, max_height=1000, wrap=False, visible=True)
    except Exception as e:
        raise gr.Error(f"文件预览失败: {str(e)}")
    

def add_item_fn(cnt, rules_data: gr.State):
    # 从状态中获取当前数据（若为空则初始化）
    print(f"当前数据：{rules_data}")
    # current_data = rules_data.value if rules_data.value else []
    current_data = []
    # 创建新规则的默认数据（字段名需与 DataFrame 列一致）
    new_rule = {
        "筛选字段1": "",
        "筛选条件1": DEFAULT_CONDITION_CHOICES[0],  # 默认选第一个条件
        "关键字1": "",
        "关联条件": "且",  # 默认逻辑为“且”
        "筛选字段2": "",
        "筛选条件2": DEFAULT_CONDITION_CHOICES[0],
        "关键字2": "",
        "类别标签": ""
    }

    updated_data = current_data + [new_rule]
    return cnt + 1, gr.State(updated_data)


# 构建界面
with gr.Blocks(title="SimpleLabel Studio", theme=gr.themes.Soft(), fill_width=False, css=css) as demo:
    rules_cnt = gr.State(1)
    rules_datas = gr.State([])
    # 当前编辑的规则索引(None表示新增模式)
    edit_index = gr.State(None)
    edit_rules = gr.State(None)

    gr.Markdown(
        "## 🧑‍💻 SimpleLabel Studio",
        elem_classes="md-title"
    )

    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown(
                "### ⚙️ **数据配置区域**"
            )

            # 模板下载区域
            template_download = gr.Button(
                "🎲 获取规则模板",
                variant="secondary",
                size="lg"
            )

            # 数据上传区域
            origin_file = gr.File(
                label="数据文件",
                interactive=True
            )

            rules_file = gr.File(
                label="规则文件",
                interactive=True
            )

        with gr.Column(scale=4):
            gr.Markdown(
                "### 🛠️ **操作区域**"
            )

            with gr.Tabs():
                with gr.Tab("标注规则配置"):
                    form_accord, field1, condition1, keyword1, logic, field2, condition2, keyword2, label = create_rule_form(visible=False)

                    with gr.Row():
                        create_rule_btn = gr.Button(
                            "添加规则",
                            variant="primary",
                            size="lg"
                        )
                        delete_rule_btn = gr.Button(
                            "删除规则",
                            variant="secondary",
                            size="lg"
                        )

                    rule_dataform = gr.Dataframe(
                        headers=["筛选字段1", "筛选条件1", "关键字1", "关联条件", "（可选）筛选字段2", "（可选）筛选条件2", "（可选）关键字2",
                                 "类别标签"],
                        row_count=(0, "dynamic"),
                        col_count=(8, "fixed"),
                        column_widths=[75, 70, 125, 70, 110, 110, 125, 100],
                        show_row_numbers=True,
                        interactive=False,
                        visible=True,
                        wrap=False,
                        label="数据标注规则",
                        show_label=True
                    )

                    rules_file_preview = gr.Dataframe(
                        interactive=False,
                        max_height=1000,
                        wrap=False,
                        visible=False
                    )

                with gr.Tab("数据标注"):
                    with gr.Row():
                        run_label_btn = gr.Button(
                            "开始标注",
                            variant="primary",
                            size="lg",
                            scale=2
                        )
                        reset_btn = gr.Button(
                            "重置",
                            variant="secondary",
                            size="lg",
                            scale=1
                        )
                    origin_file_preview = gr.Dataframe(
                        interactive=False,
                        max_height=1000,
                        wrap=False
                    )

                with gr.Tab("SQL生成"):
                    with gr.Row():
                        run_generate_btn = gr.Button(
                            "开始生成SQL语句",
                            variant="primary",
                            size="lg",
                            scale=2
                        )
                        reset_map_btn = gr.Button(
                            "重置",
                            variant="secondary",
                            size="lg",
                            scale=1
                        )

                    field_map = gr.Dataframe(
                        headers=["字段名", "字段标识"],
                        row_count=(0, "dynamic"),
                        col_count=(2, "fixed"),
                        column_widths=[150, 150],
                        show_row_numbers=True,
                        interactive=True,
                        visible=True,
                        wrap=False
                    )

                    # SQL文本预览
                    generated_sql = gr.Textbox(
                        label="SQL语句",
                        show_copy_button=True,
                        interactive=False,
                        visible=True,
                        lines=10,
                    )

                with gr.Tab("操作记录"):
                    gr.Markdown(
                        "### 4. 操作记录",
                        elem_classes="md-title"
                    )

    # 添加文件变更监听
    rules_file.upload(
        fn=preview_file,
        inputs=[rules_file],
        outputs=[rule_dataform],
        queue=False,
        show_progress='minimal',
        scroll_to_output=True
    )

    origin_file.upload(
        fn=preview_file,
        inputs=[origin_file],
        outputs=[origin_file_preview],
        queue=False,
        show_progress='minimal',
        scroll_to_output=True
    )

    create_rule_btn.click(
        fn=lambda: [gr.Accordion(open=True, visible=True)] + [""]*8,
        outputs=[form_accord, field1, condition1, keyword1, logic, field2, condition2, keyword2, label]
    )

    # 绑定Dataframe数据行选择事件
    rule_dataform.select(
        fn=on_select_row,
        outputs=edit_index,
        scroll_to_output=True
    ).then(
        fn=fill_rule_form,
        inputs=[rule_dataform, edit_index],
        outputs=[field1, condition1, keyword1, logic, field2, condition2, keyword2, label]
    ).then(
        fn=lambda: gr.Accordion(open=True, visible=True),
        outputs=[form_accord]
    )

# gradio webui.py
if __name__ == "__main__":
    demo.launch(server_port=7860, share=False)

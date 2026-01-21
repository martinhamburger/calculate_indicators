"""工具函数"""
import os
import glob
import pandas as pd
from openpyxl.utils import get_column_letter
from .product_calculator import ProductNetValueCalculator


def process_single_file(file_path: str, output_dir: str | None = None, risk_free_rate: float = 0.02):
    """
    处理单个产品文件

    Args:
        file_path: Excel文件路径
        output_dir: 输出目录（可选）
        risk_free_rate: 无风险利率

    Returns:
        业绩指标DataFrame
    """
    print(f"\n{'='*60}")
    print(f"正在处理: {os.path.basename(file_path)}")
    print('='*60)

    calculator = ProductNetValueCalculator(file_path=file_path, risk_free_rate=risk_free_rate)
    calculator.run_all_calculations()
    calculator.print_summary()

    # 保存详细结果
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        output_path = os.path.join(output_dir, f"{base_name}_结果.xlsx")
        calculator.save_to_excel(output_path)

    return calculator.build_metrics_df()


def generate_summary_file(all_metrics: list, output_path: str):
    """
    生成汇总Excel文件

    Args:
        all_metrics: 所有产品的业绩指标DataFrame列表
        output_path: 输出文件路径
    """
    if not all_metrics:
        print("没有数据可汇总")
        return

    # 合并所有产品的业绩指标
    summary_df = pd.concat(all_metrics, ignore_index=True)

    # 格式化数值列
    for col in ['成立以来收益率', '年化收益率', '年化波动率', '夏普比率', '最大回撤', '近一年最大回撤']:
        if col in summary_df.columns:
            summary_df[col] = summary_df[col].apply(
                lambda x: f"{x:.2%}" if pd.notna(x) and isinstance(x, (int, float)) else x
            )

    # 按成立以来收益率降序排序
    def sort_key(val):
        if isinstance(val, str) and '%' in val:
            try:
                return float(val.replace('%', '')) / 100
            except:
                return -999
        return -999

    summary_df['_sort_key'] = summary_df['成立以来收益率'].apply(sort_key)
    summary_df = summary_df.sort_values('_sort_key', ascending=False)
    summary_df = summary_df.drop('_sort_key', axis=1)

    # 保存汇总文件
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        summary_df.to_excel(writer, sheet_name='业绩汇总', index=False)

        # 调整列宽
        ws = writer.sheets['业绩汇总']
        for i, col in enumerate(summary_df.columns, 1):
            max_len = max(len(str(col)), 15)
            ws.column_dimensions[get_column_letter(i)].width = max_len + 2

    print(f"\n汇总文件已保存: {output_path}")
    print("\n汇总预览:")
    print(summary_df[['产品名称', '产品代码', '最新净值', '成立以来收益率', '年化收益率', '夏普比率', '最大回撤']].to_string(index=False))

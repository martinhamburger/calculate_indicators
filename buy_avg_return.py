"""
买入平均收益计算器 - 计算每月20日开放日以来的收益
"""
import argparse
import os
from utils import BuyAvgReturnCalculator


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='买入平均收益计算器 - 计算每月20日开放日以来的收益',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
    使用示例:
    # 处理单个文件
    python buy_avg_return.py -f 买入平均收益_净值列表/日度净值.xlsx

    # 指定输出目录
    python buy_avg_return.py -f 买入平均收益_净值列表/日度净值.xlsx -o ./买入平均_output
        """
    )

    # 文件参数
    parser.add_argument('-f', '--file', type=str, required=True,
                        help='Excel文件路径')

    # 输出参数
    parser.add_argument('-o', '--output', type=str, default='./买入平均_output',
                        help='输出目录（默认: ./买入平均_output）')

    args = parser.parse_args()

    # 检查文件是否存在
    if not os.path.exists(args.file):
        print(f"错误: 文件不存在 - {args.file}")
        return

    # 创建输出目录
    os.makedirs(args.output, exist_ok=True)

    print("=" * 60)
    print("买入平均收益计算器")
    print("=" * 60)
    print(f"输入文件: {args.file}")
    print(f"输出目录: {args.output}")
    print("=" * 60)

    # 创建计算器并加载数据
    print("\n正在加载数据...")
    calculator = BuyAvgReturnCalculator(args.file)
    info = calculator.get_product_info()
    print(f"产品名称: {info['name']}")
    print(f"产品代码: {info['code']}")
    print(f"数据日期范围: {info['date_range']}")

    # 执行计算
    print("\n正在计算每月20日开放日收益...")
    calculator.get_open_day_data()
    calculator.calculate_returns_since_open_day()
    info = calculator.get_product_info()  # 重新获取信息
    print(f"找到 {info['open_day_count']} 个开放日（每月20日）")

    # 生成输出文件名
    base_name = os.path.splitext(os.path.basename(args.file))[0]
    output_file = os.path.join(args.output, f"{base_name}_买入平均收益.txt")

    # 保存结果
    calculator.save_to_txt(output_file)

    print(f"\n结果已保存到: {output_file}")
    print("\n" + "=" * 60)
    print("处理完成!")
    print("=" * 60)


if __name__ == "__main__":
    main()

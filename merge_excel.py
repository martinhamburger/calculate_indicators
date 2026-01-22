"""
多产品Excel合并工具 - 命令行版本
将多个日度净值产品文件合并成标准格式的日度净值.xlsx，并可计算周期性买入收益
"""
import argparse
import os
from utils import MultiProductExcelProcessor
from utils.buy_rules import EveryFridayRule, MonthlyDayRule, SpecificDateRule, WeeklyRule


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='多产品Excel合并工具 - 合并多个产品的日度净值文件',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  # 基本用法（合并所有产品文件）
  python merge_excel.py -p "买入平均收益_净值列表/日度净值_产品*.xlsx"

  # 指定统一的买入起点日期
  python merge_excel.py -p "买入平均收益_净值列表/日度净值_产品*.xlsx" -s 20240101

  # 同时计算周期性买入收益（每周五规则）
  python merge_excel.py -p "买入平均收益_净值列表/日度净值_产品*.xlsx" --rule friday

  # 计算周期性买入收益（每月20日规则）
  python merge_excel.py -p "买入平均收益_净值列表/日度净值_产品*.xlsx" --rule monthly --day 20

  # 自定义输出文件
  python merge_excel.py -p "买入平均收益_净值列表/日度净值_产品*.xlsx" -o "买入平均收益_净值列表/日度净值.xlsx" -s 20240101

  # 从指定目录的所有产品文件，并计算周期收益
  python merge_excel.py -d "买入平均收益_净值列表" -o "买入平均收益_净值列表/日度净值.xlsx" --rule friday
        """
    )

    # 输入文件参数
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument('-p', '--pattern', type=str,
                            help='产品文件的通配符模式（如：日度净值_产品*.xlsx）')
    input_group.add_argument('-d', '--directory', type=str,
                            help='包含产品文件的目录')

    # 输出参数
    parser.add_argument('-o', '--output', type=str, default=None,
                        help='输出的Excel文件路径（默认：日度净值_合并.xlsx）')

    # 买入起点日期
    parser.add_argument('-s', '--start-date', type=str, default=None,
                        help='统一的买入起点日期，格式：YYYYMMDD（例如：20240101）')

    # 买入规则参数
    parser.add_argument('--rule', type=str, default=None,
                        choices=['friday', 'monthly', 'weekly', 'specific'],
                        help='买入规则: friday(每周五), monthly(每月指定日), weekly(每周指定日), specific(指定日期)')

    parser.add_argument('--day', type=int, default=20,
                        help='每月第几天买入（用于monthly规则，默认20）')

    parser.add_argument('--weekday', type=int, choices=range(7), default=None,
                        help='每周第几天买入（用于weekly规则，0=周一, 4=周五, 6=周日）')

    parser.add_argument('--target-date', type=str, default=None,
                        help='指定买入日期（用于specific规则，格式：YYYY-MM-DD 或 YYYYMMDD）')

    parser.add_argument('--returns-output', type=str, default=None,
                        help='收益计算结果输出文件路径（可选）')

    args = parser.parse_args()

    # 确定产品文件模式
    if args.pattern:
        products_pattern = args.pattern
    else:
        # 如果提供了目录，则自动生成模式
        products_pattern = os.path.join(args.directory, "日度净值_产品*.xlsx")

    # 检查是否找到文件
    import glob
    files = glob.glob(products_pattern)
    if not files:
        print(f"❌ 错误: 未找到匹配的文件 - {products_pattern}")
        return

    print("=" * 70)
    print("多产品Excel合并工具")
    print("=" * 70)
    print(f"文件模式: {products_pattern}")
    print(f"找到文件: {len(files)} 个")
    if args.start_date:
        print(f"买入起点日期: {args.start_date}")
    if args.rule:
        print(f"买入规则: {args.rule}")
    if args.output:
        print(f"输出文件: {args.output}")
    print("=" * 70)
    print()

    try:
        # 创建买入规则实例（如果指定了规则）
        buy_rule = None
        if args.rule:
            try:
                if args.rule == 'friday':
                    buy_rule = EveryFridayRule()
                elif args.rule == 'monthly':
                    buy_rule = MonthlyDayRule(day=args.day)
                elif args.rule == 'weekly':
                    if args.weekday is None:
                        print("❌ 错误: 使用 weekly 规则时必须指定 --weekday 参数")
                        return
                    buy_rule = WeeklyRule(weekday=args.weekday)
                elif args.rule == 'specific':
                    if args.target_date is None:
                        print("❌ 错误: 使用 specific 规则时必须指定 --target-date 参数")
                        return
                    buy_rule = SpecificDateRule(target_date=args.target_date)
            except Exception as e:
                print(f"❌ 错误: 创建买入规则失败 - {e}")
                return

        # 创建处理器并执行处理
        processor = MultiProductExcelProcessor(
            products_pattern=products_pattern,
            start_date=args.start_date,
            buy_rule=buy_rule # type: ignore
        )
        processor.process(
            output_file=args.output,
            calculate_returns=(buy_rule is not None),
            returns_output_file=args.returns_output
        )

        print()
        print("=" * 70)
        print("✅ 处理完成！")
        print("=" * 70)

    except Exception as e:
        print(f"\n❌ 处理失败: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

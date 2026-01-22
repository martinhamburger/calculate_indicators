"""
周期性买入收益计算器 - 命令行版本
根据指定的买入规则计算持有至今的收益
"""
import argparse
import os
from utils.periodic_buy_calculator import PeriodicBuyCalculator
from utils.buy_rules import EveryFridayRule, MonthlyDayRule, SpecificDateRule, WeeklyRule


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='周期性买入收益计算器 - 根据买入规则计算持有收益',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
    # 使用每周五买入规则
    python periodic_buy.py -f 买入平均收益_净值列表/日度净值.xlsx --rule friday

    # 使用每月20日买入规则
    python periodic_buy.py -f 买入平均收益_净值列表/日度净值.xlsx --rule monthly --day 20

    # 查询特定日期买入的收益（如2025-11-22周五买入）
    python periodic_buy.py -f 买入平均收益_净值列表/日度净值.xlsx --rule friday --date 2025-11-22

    # 使用每周一买入规则
    python periodic_buy.py -f 买入平均收益_净值列表/日度净值.xlsx --rule weekly --weekday 0

    # 指定输出目录和格式
    python periodic_buy.py -f 买入平均收益_净值列表/日度净值.xlsx --rule friday -o ./output --format both
        """
    )

    # 文件参数
    parser.add_argument('-f', '--file', type=str, required=True,
                        help='Excel文件路径')

    # 买入规则参数
    parser.add_argument('--rule', type=str, required=True,
                        choices=['friday', 'monthly', 'weekly', 'specific'],
                        help='买入规则: friday(每周五), monthly(每月指定日), weekly(每周指定日), specific(指定日期)')
    
    parser.add_argument('--day', type=int, default=20,
                        help='每月第几天买入（用于monthly规则，默认20）')
    
    parser.add_argument('--weekday', type=int, choices=range(7),
                        help='每周第几天买入（用于weekly规则，0=周一, 4=周五, 6=周日）')
    
    parser.add_argument('--target-date', type=str,
                        help='指定买入日期（用于specific规则，格式：YYYY-MM-DD 或 YYYYMMDD）')

    # 查询特定日期参数
    parser.add_argument('--date', type=str,
                        help='只输出特定日期买入的收益（格式：YYYY-MM-DD 或 YYYYMMDD）')

    # 输出参数
    parser.add_argument('-o', '--output', type=str, default='./output',
                        help='输出目录（默认: ./output）')
    
    parser.add_argument('--format', type=str, default='txt',
                        choices=['txt', 'excel', 'both'],
                        help='输出格式: txt, excel, both（默认: txt）')

    args = parser.parse_args()

    # 检查文件是否存在
    if not os.path.exists(args.file):
        print(f"错误: 文件不存在 - {args.file}")
        return

    # 创建输出目录
    os.makedirs(args.output, exist_ok=True)

    # 根据规则创建买入规则实例
    try:
        if args.rule == 'friday':
            buy_rule = EveryFridayRule()
        elif args.rule == 'monthly':
            buy_rule = MonthlyDayRule(day=args.day)
        elif args.rule == 'weekly':
            if args.weekday is None:
                print("错误: 使用 weekly 规则时必须指定 --weekday 参数")
                return
            buy_rule = WeeklyRule(weekday=args.weekday)
        elif args.rule == 'specific':
            if args.target_date is None:
                print("错误: 使用 specific 规则时必须指定 --target-date 参数")
                return
            buy_rule = SpecificDateRule(target_date=args.target_date)
        else:
            print(f"错误: 未知的买入规则 - {args.rule}")
            return
    except Exception as e:
        print(f"错误: 创建买入规则失败 - {e}")
        return

    print("=" * 80)
    print("周期性买入收益计算器")
    print("=" * 80)
    print(f"输入文件: {args.file}")
    print(f"买入规则: {buy_rule.get_rule_name()}")
    print(f"输出目录: {args.output}")
    print("=" * 80)

    # 创建计算器并加载数据
    print("\n正在加载数据...")
    calculator = PeriodicBuyCalculator(args.file, buy_rule)
    info = calculator.get_product_info()
    print(f"产品名称: {info['name']}")
    print(f"产品代码: {info['code']}")
    print(f"数据日期范围: {info['date_range']}")

    # 如果指定了特定日期查询
    if args.date:
        print(f"\n正在查询 {args.date} 的买入收益...")
        result = calculator.get_specific_date_return(args.date)
        
        if result is None:
            print(f"错误: {args.date} 不在买入日期列表中")
            print(f"可能原因: 1) 该日期不符合买入规则; 2) 该日期不是交易日")
            
            # 显示最近的买入日期供参考
            calculator.calculate_buy_returns()
            if not calculator.results_df.empty:
                print("\n最近的买入日期:")
                print(calculator.results_df['买入日期'].tail(10).to_string(index=False))
        else:
            print("\n查询结果:")
            print("=" * 80)
            for key, value in result.items():
                if key in ['每日涨跌幅', '区间收益率', '区间年化收益率']:
                    print(f"{key}: {value:.2%}")
                elif key == '买入基金净值':
                    print(f"{key}: {value:.4f}")
                else:
                    print(f"{key}: {value}")
            print("=" * 80)
        return

    # 执行计算
    print("\n正在计算买入收益...")
    calculator.calculate_buy_returns()
    print(f"找到 {info['buy_count']} 个符合规则的买入日期")

    # 生成输出文件名
    base_name = os.path.splitext(os.path.basename(args.file))[0]
    rule_name = args.rule
    if args.rule == 'monthly':
        rule_name = f"monthly{args.day}"
    elif args.rule == 'weekly':
        rule_name = f"weekly{args.weekday}"
    
    output_base = os.path.join(args.output, f"{base_name}_{rule_name}")

    # 保存结果
    if args.format in ['txt', 'both']:
        txt_file = f"{output_base}.txt"
        calculator.save_to_txt(txt_file)
        print(f"\nTXT结果已保存到: {txt_file}")
    
    if args.format in ['excel', 'both']:
        excel_file = f"{output_base}.xlsx"
        calculator.save_to_excel(excel_file)
        print(f"Excel结果已保存到: {excel_file}")

    # 显示预览
    print("\n" + "=" * 80)
    print("结果预览:")
    print("=" * 80)
    print(calculator.format_output_text())
    print("\n" + "=" * 80)
    print("处理完成!")
    print("=" * 80)


if __name__ == "__main__":
    main()

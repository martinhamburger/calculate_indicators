# %%
"""
产品净值计算器 - 命令行版本
支持单个文件或批量处理目录下的所有Excel文件
"""
import argparse
from utils import process_single_file, generate_summary_file


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='产品净值计算器 - 计算产品业绩指标',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
    使用示例:
    # 处理单个文件
    python calculate.py -f 产品净值.xlsx

    # 处理单个文件并输出到指定目录
    python calculate.py -f 产品净值.xlsx -o 输出目录

    # 处理目录下所有Excel文件
    python calculate.py -d ./净值目录

    # 处理目录下所有文件并生成汇总
    python calculate.py -d ./净值目录 -s 汇总.xlsx

    # 指定无风险利率
    python calculate.py -f 产品净值.xlsx --risk-free 0.03
            """
    )

    # 文件/目录参数
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument('-f', '--file', type=str, help='单个Excel文件路径')
    input_group.add_argument('-d', '--dir', type=str, help='包含Excel文件的目录路径')

    # 输出参数
    parser.add_argument('-o', '--output', type=str, default='./output',
                        help='输出目录（默认: ./output）')
    parser.add_argument('-s', '--summary', type=str,
                        help='汇总文件名（处理多个文件时生成）')

    # 计算参数
    parser.add_argument('--risk-free', type=float, default=0.02,
                        help='无风险利率（默认: 0.02）')

    args = parser.parse_args()

    print("=" * 60)
    print("产品净值计算器")
    print(f"无风险利率: {args.risk_free:.2%}")
    print("=" * 60)

    all_metrics = []

    if args.file:
        # 处理单个文件
        if not os.path.exists(args.file):
            print(f"错误: 文件不存在 - {args.file}")
            return

        metrics_df = process_single_file(
            file_path=args.file,
            output_dir=args.output,
            risk_free_rate=args.risk_free
        )
        all_metrics.append(metrics_df)

    elif args.dir:
        # 处理目录下所有Excel文件
        if not os.path.isdir(args.dir):
            print(f"错误: 目录不存在 - {args.dir}")
            return

        # 查找所有Excel文件
        excel_files = glob.glob(os.path.join(args.dir, '*.xlsx'))
        excel_files += glob.glob(os.path.join(args.dir, '*.xls'))
        excel_files += glob.glob(os.path.join(args.dir, '*.xlsm'))

        if not excel_files:
            print(f"错误: 目录中没有找到Excel文件 - {args.dir}")
            return

        print(f"\n找到 {len(excel_files)} 个Excel文件")

        for file_path in sorted(excel_files):
            try:
                metrics_df = process_single_file(
                    file_path=file_path,
                    output_dir=args.output,
                    risk_free_rate=args.risk_free
                )
                all_metrics.append(metrics_df)
            except Exception as e:
                print(f"处理失败 {os.path.basename(file_path)}: {e}")

    # 生成汇总文件（多个产品时）
    if len(all_metrics) > 1 and args.summary:
        summary_path = args.summary if os.path.isabs(args.summary) else os.path.join(args.output, args.summary)
        generate_summary_file(all_metrics, summary_path)
    elif len(all_metrics) > 1:
        # 默认生成汇总文件
        summary_path = os.path.join(args.output, "业绩汇总.xlsx")
        generate_summary_file(all_metrics, summary_path)

    print("\n" + "=" * 60)
    print("处理完成!")
    print("=" * 60)


if __name__ == "__main__":
    import os
    import glob
    main()

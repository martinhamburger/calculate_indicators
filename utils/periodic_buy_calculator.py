"""周期性买入收益计算器"""
import pandas as pd
from datetime import datetime
from .buy_rules import BuyRule


class PeriodicBuyCalculator:
    """周期性买入收益计算器 - 根据指定规则计算持有收益"""

    def __init__(self, file_path: str, buy_rule: BuyRule):
        """
        初始化计算器

        Args:
            file_path: Excel文件路径
            buy_rule: 买入规则实例
        """
        self.file_path: str = file_path
        self.buy_rule: BuyRule = buy_rule
        self.df: pd.DataFrame = pd.DataFrame()
        self.product_name: str = ""
        self.product_code: str = ""
        self.buy_dates: list = []
        self.results_df: pd.DataFrame = pd.DataFrame()
        self._load_data()

    def _load_data(self):
        """
        加载并预处理数据（复用已有的读入结构）

        Excel格式：
        - A1: 产品名称
        - B1: 产品代码
        - A2-C2: 列标题（日期、单位净值、累计净值）
        - A3起: 数据
        """
        # 读取原始数据，不使用header
        raw_df = pd.read_excel(self.file_path, header=None)

        # 获取产品信息（A1产品名称，B1产品代码）
        self.product_name = str(raw_df.iloc[0, 0]).strip()  # A1
        self.product_code = str(raw_df.iloc[0, 1]).strip()  # B1

        # 获取数据部分（A2行是标题，A3行开始是数据）
        data_df = raw_df.iloc[2:].copy()
        data_df.columns = ['日期', '单位净值', '累计净值']

        # 清理空行
        data_df = data_df.dropna(subset=['日期'])

        # 转换日期
        data_df['日期'] = pd.to_datetime(data_df['日期'], format='%Y%m%d')
        
        # 按日期排序（升序）
        data_df = data_df.sort_values('日期')
        data_df.set_index("日期", inplace=True)

        self.df = data_df

    def calculate_buy_returns(self):
        """
        根据买入规则计算每次买入的持有收益
        
        Returns:
            pd.DataFrame: 包含每次买入的详细信息
        """
        # 获取所有可用的交易日
        available_dates = set(self.df.index.to_pydatetime()) # type: ignore
        
        # 获取日期范围
        start_date = self.df.index.min().to_pydatetime()
        end_date = self.df.index.max().to_pydatetime()
        
        # 根据规则获取所有买入日期
        self.buy_dates = self.buy_rule.get_buy_dates(start_date, end_date, available_dates)
        
        if not self.buy_dates:
            print(f"警告: 在数据范围内没有找到符合规则的买入日期")
            return pd.DataFrame()
        
        # 获取最新日期和净值
        latest_date = self.df.index.max()
        latest_nav = self.df.loc[latest_date, '单位净值']
        
        # 计算每个买入日的收益
        results = []
        for buy_date in self.buy_dates:
            buy_date_pd = pd.Timestamp(buy_date)
            buy_nav = self.df.loc[buy_date_pd, '单位净值']
            
            # 计算每日涨跌幅（买入当日）
            # 查找前一个交易日
            prev_dates = self.df.index[self.df.index < buy_date_pd]
            if len(prev_dates) > 0:
                prev_date = prev_dates[-1]
                prev_nav = self.df.loc[prev_date, '单位净值']
                daily_change = (buy_nav / prev_nav - 1) # type: ignore
            else:
                daily_change = 0.0
            
            # 持有天数
            holding_days = (latest_date - buy_date_pd).days
            
            # 区间收益率
            period_return = (latest_nav / buy_nav - 1) # type: ignore
            
            # 区间年化收益率
            if holding_days > 0:
                annualized_return = (1 + period_return) ** (365 / holding_days) - 1
            else:
                annualized_return = 0.0
            
            results.append({
                '买入日期': buy_date_pd.strftime('%Y-%m-%d'),
                '买入基金净值': buy_nav,
                '每日涨跌幅': daily_change,
                '持有天数': holding_days,
                '区间收益率': period_return,
                '区间年化收益率': annualized_return
            })
        
        self.results_df = pd.DataFrame(results)
        return self.results_df

    def get_specific_date_return(self, target_date: str) -> dict:
        """
        获取特定日期买入的收益情况
        
        Args:
            target_date: 目标日期字符串（格式：YYYY-MM-DD 或 YYYYMMDD）
            
        Returns:
            dict: 包含该日期买入的收益信息，如果该日期不在买入列表中则返回None
        """
        # 格式化目标日期
        if '-' in target_date:
            target_date_formatted = target_date
        else:
            dt = datetime.strptime(target_date, '%Y%m%d')
            target_date_formatted = dt.strftime('%Y-%m-%d')
        
        # 如果还没计算，先计算
        if self.results_df.empty:
            self.calculate_buy_returns()
        
        # 查找特定日期
        matching_rows = self.results_df[self.results_df['买入日期'] == target_date_formatted]
        
        if matching_rows.empty:
            return None # type: ignore
        
        return matching_rows.iloc[0].to_dict()

    def format_output_text(self, preview_count: int = 10) -> str:
        """
        生成格式化的输出文本（只显示部分数据作为预览）
        
        Args:
            preview_count: 预览行数（默认10行）
            
        Returns:
            str: 格式化后的文本
        """
        if self.results_df.empty:
            self.calculate_buy_returns()
        
        if self.results_df.empty:
            return "没有符合规则的买入日期"
        
        lines = []
        lines.append(f"{self.product_name}  ({self.product_code})")
        lines.append(f"收益情况表（更新日期：{self.df.index.max().strftime('%Y.%m.%d')}）")
        lines.append(f"买入规则：{self.buy_rule.get_rule_name()}")
        lines.append("")
        lines.append("-" * 80)
        
        # 表头
        header = f"{'买入日期':<15} {'买入基金净值':<12} {'每日涨跌幅':<12} {'持有天数':<10} {'区间收益率':<12} {'区间年化收益率':<15}"
        lines.append(header)
        lines.append("-" * 80)
        
        # 数据行 - 只显示最后 preview_count 行
        display_df = self.results_df.tail(preview_count)
        for _, row in display_df.iterrows():
            line = (
                f"{row['买入日期']:<15} "
                f"{row['买入基金净值']:<12.4f} "
                f"{row['每日涨跌幅']:>11.2%} "
                f"{row['持有天数']:>10} "
                f"{row['区间收益率']:>11.2%} "
                f"{row['区间年化收益率']:>14.2%}"
            )
            lines.append(line)
        
        lines.append("-" * 80)
        
        # 统计信息
        avg_return = self.results_df['区间收益率'].mean()
        avg_annualized = self.results_df['区间年化收益率'].mean()
        lines.append(f"平均{'':>42} {avg_return:>11.2%} {avg_annualized:>14.2%}")
        lines.append("")
        lines.append(f"共计 {len(self.results_df)} 个买入日期，上方为最近 {min(preview_count, len(self.results_df))} 条记录")
        lines.append("完整数据请查看输出文件")
        
        return "\n".join(lines)

    def save_to_txt(self, output_path: str):
        """
        保存结果到txt文件

        Args:
            output_path: 输出文件路径
        """
        output_text = self.format_output_text()
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(output_text)
        return output_path

    def save_to_excel(self, output_path: str):
        """
        保存结果到Excel文件
        
        Args:
            output_path: 输出文件路径
        """
        if self.results_df.empty:
            self.calculate_buy_returns()
        
        # 创建格式化的DataFrame
        df_output = self.results_df.copy()
        
        # 格式化百分比列
        df_output['每日涨跌幅'] = df_output['每日涨跌幅'].apply(lambda x: f"{x:.2%}")
        df_output['区间收益率'] = df_output['区间收益率'].apply(lambda x: f"{x:.2%}")
        df_output['区间年化收益率'] = df_output['区间年化收益率'].apply(lambda x: f"{x:.2%}")
        
        # 保存到Excel
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            df_output.to_excel(writer, sheet_name='买入收益明细', index=False)
            
            # 调整列宽
            from openpyxl.utils import get_column_letter
            ws = writer.sheets['买入收益明细']
            for i, col in enumerate(df_output.columns, 1):
                max_len = max(len(str(col)), 15)
                ws.column_dimensions[get_column_letter(i)].width = max_len + 2
        
        return output_path

    def get_product_info(self) -> dict:
        """获取产品信息"""
        return {
            'name': self.product_name,
            'code': self.product_code,
            'date_range': f"{self.df.index.min().strftime('%Y-%m-%d')} ~ {self.df.index.max().strftime('%Y-%m-%d')}",
            'data_count': len(self.df),
            'buy_count': len(self.buy_dates),
            'rule_name': self.buy_rule.get_rule_name()
        }

"""买入平均收益计算器类"""
import pandas as pd


class BuyAvgReturnCalculator:
    """买入平均收益计算器 - 计算每月20日开放日以来的收益"""

    def __init__(self, file_path: str):
        """
        初始化计算器

        Args:
            file_path: Excel文件路径
        """
        self.file_path: str = file_path
        self.df: pd.DataFrame = pd.DataFrame()
        self.product_name: str = ""
        self.product_code: str = ""
        self.open_day_df: pd.DataFrame = pd.DataFrame()
        self.results: dict = {}
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
        data_df.set_index("日期", inplace=True)

        self.df = data_df

    def get_open_day_data(self, day: int = 20):
        """
        获取指定日期的净值数据（开放日）
        如果没找到指定日期，则顺延到下一个交易日

        Args:
            day: 开放日日期（默认20日）

        Returns:
            DataFrame: 开放日数据
        """
        # 确保索引是DatetimeIndex
        df = self.df.copy()

        # 添加年份和月份列
        df['year'] = df.index.year  # type: ignore
        df['month'] = df.index.month  # type: ignore
        df['day'] = df.index.day  # type: ignore

        # 获取所有年月组合（按时间正序）
        year_months = sorted(df.groupby([df.index.year, df.index.month]).groups.keys())  # type: ignore

        open_day_records = []

        for year, month in year_months:
            month_data = df[(df.index.year == year) & (df.index.month == month)]  # type: ignore

            # 尝试找指定日期的记录
            target_day_data = month_data[month_data['day'] == day]

            if not target_day_data.empty:
                # 找到指定日期的记录
                open_day_records.append(target_day_data.iloc[0])
            else:
                # 没找到指定日期，顺延到下一个交易日
                # 找该月>=指定日期的第一条记录（取日期最小的，即最接近指定日期的下一天）
                next_trading_data = month_data[month_data['day'] >= day]
                if not next_trading_data.empty:
                    # 按日期排序，取最早的（最接近指定日期的下一天）
                    next_trading_data_sorted = next_trading_data.sort_index()
                    open_day_records.append(next_trading_data_sorted.iloc[0])
                # 如果当月没有>=指定日期的交易日，跳过该月

        if open_day_records:
            open_day_df = pd.DataFrame(open_day_records)
            open_day_df.index.name = '日期'
        else:
            open_day_df = pd.DataFrame()

        self.open_day_df = open_day_df
        return open_day_df

    def calculate_returns_since_open_day(self):
        """
        计算每个开放日以来的收益

        Returns:
            dict: {年份: {月份: 收益率}}
        """
        if self.open_day_df.empty:
            self.get_open_day_data()

        # 获取最新净值（数据是倒序的，第一行是最新）
        latest_nav = self.df['单位净值'].iloc[0]

        results = {}

        for idx, row in self.open_day_df.iterrows():
            open_date = idx
            open_nav = row['单位净值']
            year = open_date.year # type: ignore
            month = open_date.month # type: ignore

            # 计算从开放日到现在的收益
            return_rate = (latest_nav / open_nav) - 1

            if year not in results:
                results[year] = {}

            results[year][month] = return_rate

        self.results = results
        return results

    def generate_output_text(self) -> str:
        """
        生成格式化的输出文本

        格式：
        ⭐️2025年
        🔺7月买入平均收益##%
        🔺8月买入平均收益##%
        ...

        Returns:
            str: 格式化后的文本
        """
        if not self.results:
            self.calculate_returns_since_open_day()

        lines = []

        # 按年份排序
        for year in sorted(self.results.keys()):
            lines.append(f"⭐️{year}年")
            months_data = self.results[year]

            # 按月份排序
            for month in sorted(months_data.keys()):
                return_rate = months_data[month]
                # 转换为百分比格式
                return_pct = return_rate * 100
                lines.append(f"🔺{month}月买入平均收益{return_pct:.2f}%")

            # 年份之间空一行（除了最后一年）
            if year != sorted(self.results.keys())[-1]:
                lines.append("")

        return "\n".join(lines)

    def get_product_info(self):
        """获取产品信息"""
        return {
            'name': self.product_name,
            'code': self.product_code,
            'date_range': f"{self.df.index.min().strftime('%Y-%m-%d')} ~ {self.df.index.max().strftime('%Y-%m-%d')}",
            'data_count': len(self.df),
            'open_day_count': len(self.open_day_df)
        }

    def save_to_txt(self, output_path: str):
        """
        保存结果到txt文件

        Args:
            output_path: 输出文件路径
        """
        output_text = self.generate_output_text()
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(output_text)
        return output_path

    def run_all(self):
        """执行所有计算"""
        self.get_open_day_data()
        self.calculate_returns_since_open_day()
        return self.results

"""买入规则定义 - 可扩展的买入规则系统"""
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
import pandas as pd


class BuyRule(ABC):
    """买入规则基类"""
    
    @abstractmethod
    def should_buy(self, date: datetime, available_dates: set) -> bool:
        """
        判断某个日期是否应该买入
        
        Args:
            date: 要判断的日期
            available_dates: 所有可用的交易日集合
            
        Returns:
            bool: 是否应该买入
        """
        pass
    
    @abstractmethod
    def get_rule_name(self) -> str:
        """获取规则名称"""
        pass
    
    def get_buy_dates(self, start_date: datetime, end_date: datetime, 
                      available_dates: set) -> list:
        """
        获取所有符合规则的买入日期
        
        Args:
            start_date: 开始日期
            end_date: 结束日期
            available_dates: 所有可用的交易日集合
            
        Returns:
            list: 所有买入日期列表
        """
        buy_dates = []
        current_date = start_date
        
        while current_date <= end_date:
            # 检查是否应该买入
            if self.should_buy(current_date, available_dates):
                # 如果是交易日，直接买入；否则取消
                if current_date in available_dates:
                    buy_dates.append(current_date)
            
            current_date += timedelta(days=1)
        
        return sorted(buy_dates)


class EveryFridayRule(BuyRule):
    """每周五买入规则"""
    
    def should_buy(self, date: datetime, available_dates: set) -> bool:
        """
        判断是否应该买入（每周五）
        
        Args:
            date: 要判断的日期
            available_dates: 所有可用的交易日集合
            
        Returns:
            bool: 是否应该买入
        """
        # 4 代表周五（Monday=0, Sunday=6）
        return date.weekday() == 4
    
    def get_rule_name(self) -> str:
        return "每周五买入"


class MonthlyDayRule(BuyRule):
    """每月指定日期买入规则"""
    
    def __init__(self, day: int = 20):
        """
        初始化每月指定日期买入规则
        
        Args:
            day: 每月的第几天（默认20日）
        """
        self.day = day
    
    def should_buy(self, date: datetime, available_dates: set) -> bool:
        """
        判断是否应该买入（每月指定日期）
        
        Args:
            date: 要判断的日期
            available_dates: 所有可用的交易日集合
            
        Returns:
            bool: 是否应该买入
        """
        return date.day == self.day
    
    def get_rule_name(self) -> str:
        return f"每月{self.day}日买入"


class SpecificDateRule(BuyRule):
    """指定日期买入规则"""
    
    def __init__(self, target_date: str):
        """
        初始化指定日期买入规则
        
        Args:
            target_date: 目标日期字符串（格式：YYYY-MM-DD 或 YYYYMMDD）
        """
        # 支持多种日期格式
        if '-' in target_date:
            self.target_date = datetime.strptime(target_date, '%Y-%m-%d')
        else:
            self.target_date = datetime.strptime(target_date, '%Y%m%d')
    
    def should_buy(self, date: datetime, available_dates: set) -> bool:
        """
        判断是否应该买入（仅指定日期）
        
        Args:
            date: 要判断的日期
            available_dates: 所有可用的交易日集合
            
        Returns:
            bool: 是否应该买入
        """
        return date.date() == self.target_date.date()
    
    def get_rule_name(self) -> str:
        return f"指定日期买入 ({self.target_date.strftime('%Y-%m-%d')})"


class WeeklyRule(BuyRule):
    """每周指定星期几买入规则"""
    
    def __init__(self, weekday: int):
        """
        初始化每周指定星期几买入规则
        
        Args:
            weekday: 星期几（0=周一, 1=周二, ..., 6=周日）
        """
        if not 0 <= weekday <= 6:
            raise ValueError("weekday 必须在 0-6 之间（0=周一, 6=周日）")
        self.weekday = weekday
        self.weekday_names = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
    
    def should_buy(self, date: datetime, available_dates: set) -> bool:
        """
        判断是否应该买入（每周指定星期几）
        
        Args:
            date: 要判断的日期
            available_dates: 所有可用的交易日集合
            
        Returns:
            bool: 是否应该买入
        """
        return date.weekday() == self.weekday
    
    def get_rule_name(self) -> str:
        return f"每{self.weekday_names[self.weekday]}买入"


def get_rule_by_name(rule_name: str, **kwargs) -> BuyRule:
    """
    根据规则名称获取买入规则实例
    
    Args:
        rule_name: 规则名称（'friday', 'monthly', 'specific', 'weekly'）
        **kwargs: 额外参数
            - day: 每月第几天（用于 monthly）
            - target_date: 目标日期（用于 specific）
            - weekday: 星期几（用于 weekly）
    
    Returns:
        BuyRule: 买入规则实例
    """
    rules = {
        'friday': EveryFridayRule,
        'monthly': lambda: MonthlyDayRule(kwargs.get('day', 20)),
        'specific': lambda: SpecificDateRule(kwargs.get('target_date')), # type: ignore
        'weekly': lambda: WeeklyRule(kwargs.get('weekday', 4))
    }
    
    if rule_name not in rules:
        raise ValueError(f"未知的规则名称: {rule_name}. 可用规则: {list(rules.keys())}")
    
    rule_factory = rules[rule_name]
    return rule_factory() if callable(rule_factory) and rule_name in ['friday'] else rule_factory() # type: ignore

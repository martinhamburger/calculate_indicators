from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import tempfile
import pandas as pd
from werkzeug.utils import secure_filename
import sys

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import process_single_file
from utils.buy_avg_calculator import BuyAvgReturnCalculator
from utils.periodic_buy_calculator import PeriodicBuyCalculator
from utils.buy_rules import EveryFridayRule, MonthlyDayRule

app = Flask(__name__)
CORS(app)  # 允许跨域请求

ALLOWED_EXTENSIONS = {'txt', 'xlsx', 'xls', 'csv'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/api/health', methods=['GET'])
def health_check():
    """健康检查接口"""
    return jsonify({'status': 'ok', 'message': 'API is running'})


@app.route('/api/file-info', methods=['POST'])
def file_info():
    """获取上传文件的信息（用于诊断）"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': '未上传文件'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': '文件名为空'}), 400
        
        # 保存临时文件
        filename = secure_filename(file.filename) # type: ignore
        temp_dir = tempfile.mkdtemp()
        filepath = os.path.join(temp_dir, filename)
        file.save(filepath)
        
        # 读取文件信息
        info = {
            'filename': filename,
            'file_size': os.path.getsize(filepath),
        }
        
        # 尝试读取数据并获取列名
        try:
            if filename.endswith(('.xlsx', '.xls')):
                df = pd.read_excel(filepath, nrows=1)
            else:
                # 尝试多种分隔符
                try:
                    df = pd.read_csv(filepath, sep='\t', nrows=1, encoding='utf-8')
                except:
                    try:
                        df = pd.read_csv(filepath, sep=',', nrows=1, encoding='utf-8')
                    except:
                        df = pd.read_csv(filepath, nrows=1, encoding='utf-8')
            
            info['columns'] = list(df.columns)
            info['shape'] = df.shape
            info['dtypes'] = {col: str(df[col].dtype) for col in df.columns}
            info['preview'] = df.to_dict('records')
        except Exception as e:
            info['error'] = f"无法读取数据: {str(e)}"
        
        # 清理临时文件
        try:
            os.remove(filepath)
            os.rmdir(temp_dir)
        except:
            pass
        
        return jsonify(info)
    
    except Exception as e:
        return jsonify({'error': f"诊断失败: {str(e)}"}), 500


@app.route('/api/calculate', methods=['POST'])
def calculate():
    """主计算接口"""
    try:
        # 检查文件
        if 'file' not in request.files:
            return jsonify({'error': '未上传文件'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': '文件名为空'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': '不支持的文件类型'}), 400
        
        # 获取参数
        calc_type = request.form.get('type', 'buy_avg')
        frequency = request.form.get('frequency', 'friday')
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        amount = float(request.form.get('amount', 10000))
        
        # 保存临时文件
        filename = secure_filename(file.filename) # type: ignore
        temp_dir = tempfile.mkdtemp()
        filepath = os.path.join(temp_dir, filename)
        file.save(filepath)
        
        # 根据类型执行不同的计算
        if calc_type == 'buy_avg':
            result = calculate_buy_avg(filepath, frequency)
        elif calc_type == 'periodic_buy':
            result = calculate_periodic_buy(filepath, frequency, start_date, end_date, amount)
        elif calc_type == 'calculate':
            result = calculate_normal(filepath, frequency)
        else:
            return jsonify({'error': '未知的计算类型'}), 400
        
        # 清理临时文件
        try:
            os.remove(filepath)
            os.rmdir(temp_dir)
        except:
            pass
        
        return jsonify(result)
    
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        return jsonify({'error': str(e)}), 500


def calculate_buy_avg(filepath, frequency):
    """计算买入平均收益"""
    # 初始化时需要传递文件路径
    try:
        calculator = BuyAvgReturnCalculator(filepath) # type: ignore
        
        # 调用计算方法
        result_dict = calculator.calculate_all() # type: ignore
        
        # 生成输出
        output_lines = []
        output_lines.append("=" * 80)
        output_lines.append("买入平均收益计算结果")
        output_lines.append("=" * 80)
        
        # 添加产品信息
        output_lines.append(f"\n产品名称: {result_dict.get('product_name', '未知')}")
        output_lines.append(f"产品代码: {result_dict.get('product_code', '未知')}")
        
        # 添加结果
        output_lines.append("\n计算结果：")
        for key, value in result_dict.items():
            if key not in ['product_name', 'product_code', 'open_day_df']:
                output_lines.append(f"{key}: {value}")
        
        output_text = "\n".join(output_lines)
        
        # 生成表格数据（如果有open_day_df）
        table_data = []
        if 'open_day_df' in result_dict and isinstance(result_dict['open_day_df'], pd.DataFrame):
            table_data = result_dict['open_day_df'].reset_index().to_dict('records')
        
        return {
            'success': True,
            'output': output_text,
            'table_data': table_data,
            'summary': f"计算完成：{result_dict.get('product_name', '产品')} 的买入平均收益",
            'filename': f'买入平均收益_{frequency}.txt'
        }
    except Exception as e:
        raise Exception(f"买入平均收益计算失败: {str(e)}")


def calculate_periodic_buy(filepath, frequency, start_date, end_date, amount):
    """计算定期买入收益"""
    try:
        # 选择买入规则
        if frequency == 'friday':
            buy_rule = EveryFridayRule()
        elif frequency == 'monthly':
            buy_rule = MonthlyDayRule(day=20)
        else:
            buy_rule = EveryFridayRule()
        
        # 初始化时需要传递文件路径和买入规则
        calculator = PeriodicBuyCalculator(filepath, buy_rule) # type: ignore
        
        # 调用计算方法
        result_dict = calculator.calculate_all(amount_per_purchase=amount) # type: ignore
        
        # 生成输出
        output_lines = []
        output_lines.append("=" * 80)
        output_lines.append("定期买入收益计算结果")
        output_lines.append("=" * 80)
        
        # 添加产品信息
        output_lines.append(f"\n产品名称: {result_dict.get('product_name', '未知')}")
        output_lines.append(f"产品代码: {result_dict.get('product_code', '未知')}")
        output_lines.append(f"买入规则: {frequency}")
        output_lines.append(f"每期投资金额: ¥{amount:,.2f}")
        
        # 添加计算结果
        output_lines.append("\n计算结果：")
        for key, value in result_dict.items():
            if key not in ['product_name', 'product_code', 'results_df'] and not isinstance(value, pd.DataFrame):
                output_lines.append(f"{key}: {value}")
        
        output_text = "\n".join(output_lines)
        
        # 生成表格数据
        table_data = []
        if 'results_df' in result_dict and isinstance(result_dict['results_df'], pd.DataFrame):
            table_data = result_dict['results_df'].reset_index().to_dict('records')
        
        return {
            'success': True,
            'output': output_text,
            'table_data': table_data,
            'summary': f"定期买入计算完成: 总投资 {result_dict.get('总投资次数', 0)} 次",
            'filename': f'定期买入_{frequency}.txt'
        }
    except Exception as e:
        raise Exception(f"定期买入计算失败: {str(e)}")


def calculate_normal(filepath, frequency):
    """常规计算 - 产品净值和业绩指标"""
    try:
        # 使用 ProductNetValueCalculator
        from utils.product_calculator import ProductNetValueCalculator
        
        calculator = ProductNetValueCalculator(filepath)
        
        # 执行计算
        result = calculator.calculate() # type: ignore
        
        # 生成输出
        output_lines = []
        output_lines.append("=" * 80)
        output_lines.append("产品净值计算结果")
        output_lines.append("=" * 80)
        output_lines.append(f"\n产品名称: {result.get('product_name', '未知')}")
        output_lines.append(f"产品代码: {result.get('product_code', '未知')}")
        output_lines.append(f"最新净值日期: {result.get('latest_nav_date', '未知')}")
        output_lines.append(f"最新净值: {result.get('latest_nav', '未知')}")
        
        output_lines.append("\n业绩指标：")
        output_lines.append(f"成立以来收益率: {result.get('total_return_rate', '未知')}")
        output_lines.append(f"年化收益率: {result.get('annual_return_rate', '未知')}")
        output_lines.append(f"年化波动率: {result.get('annual_volatility', '未知')}")
        output_lines.append(f"夏普比率: {result.get('sharpe_ratio', '未知')}")
        output_lines.append(f"最大回撤: {result.get('max_drawdown', '未知')}")
        
        output_text = "\n".join(output_lines)
        
        return {
            'success': True,
            'output': output_text,
            'summary': '常规净值计算完成',
            'filename': f'净值计算_{frequency}.txt'
        }
    except Exception as e:
        raise Exception(f"常规计算失败: {str(e)}")


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

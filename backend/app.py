from flask import Flask, request, jsonify
from flask_cors import CORS # type: ignore
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
    calculator = BuyAvgReturnCalculator() # type: ignore
    
    # 加载数据
    if filepath.endswith(('.xlsx', '.xls')):
        calculator.load_data(filepath) # type: ignore
    else:
        # 处理txt/csv文件
        df = pd.read_csv(filepath, sep='\t', encoding='utf-8')
        calculator.df = df
    
    # 计算
    result_df = calculator.calculate_returns() # type: ignore
    
    # 生成输出
    output_lines = []
    output_lines.append("=" * 80)
    output_lines.append("买入平均收益计算结果")
    output_lines.append("=" * 80)
    output_lines.append(f"\n数据范围: {result_df['日期'].min()} 至 {result_df['日期'].max()}")
    output_lines.append(f"总记录数: {len(result_df)}")
    output_lines.append("\n" + "=" * 80)
    output_lines.append("\n详细数据:\n")
    output_lines.append(result_df.to_string(index=False))
    
    output_text = "\n".join(output_lines)
    
    # 生成表格数据
    table_data = result_df.to_dict('records')
    
    return {
        'success': True,
        'output': output_text,
        'table_data': table_data,
        'summary': f"共计算 {len(result_df)} 个开放日的买入平均收益",
        'filename': f'买入平均收益_{frequency}.txt'
    }


def calculate_periodic_buy(filepath, frequency, start_date, end_date, amount):
    """计算定期买入收益"""
    calculator = PeriodicBuyCalculator() # type: ignore
    
    # 加载数据
    if filepath.endswith(('.xlsx', '.xls')):
        calculator.load_data(filepath) # type: ignore
    else:
        df = pd.read_csv(filepath, sep='\t', encoding='utf-8')
        calculator.df = df
        calculator.df['净值日期'] = pd.to_datetime(calculator.df['净值日期'])
    
    # 选择买入规则
    if frequency == 'friday':
        buy_rule = EveryFridayRule()
    elif frequency == 'monthly':
        buy_rule = MonthlyDayRule(day=20)
    else:
        buy_rule = EveryFridayRule()
    
    # 计算
    result = calculator.calculate_returns( # type: ignore
        buy_rule=buy_rule,
        amount_per_purchase=amount
    )
    
    # 生成输出
    output_lines = []
    output_lines.append("=" * 80)
    output_lines.append("定期买入收益计算结果")
    output_lines.append("=" * 80)
    output_lines.append(f"\n买入规则: {buy_rule.__class__.__name__}")
    output_lines.append(f"每期投资金额: ¥{amount:,.2f}")
    output_lines.append(f"\n买入次数: {result['purchase_count']}")
    output_lines.append(f"累计投资: ¥{result['total_invested']:,.2f}")
    output_lines.append(f"当前市值: ¥{result['current_value']:,.2f}")
    output_lines.append(f"累计收益: ¥{result['total_return']:,.2f}")
    output_lines.append(f"收益率: {result['return_rate']:.2%}")
    output_lines.append("\n" + "=" * 80)
    output_lines.append("\n买入明细:\n")
    
    # 转换买入记录为DataFrame
    purchases_df = pd.DataFrame(result['purchases'])
    output_lines.append(purchases_df.to_string(index=False))
    
    output_text = "\n".join(output_lines)
    
    # 生成汇总信息
    summary = f"共买入 {result['purchase_count']} 次，累计投资 ¥{result['total_invested']:,.2f}，" \
              f"当前市值 ¥{result['current_value']:,.2f}，收益率 {result['return_rate']:.2%}"
    
    return {
        'success': True,
        'output': output_text,
        'table_data': result['purchases'],
        'summary': summary,
        'filename': f'定期买入_{frequency}.txt'
    }


def calculate_normal(filepath, frequency):
    """常规计算"""
    # 创建临时输出目录
    temp_output_dir = tempfile.mkdtemp()
    
    try:
        # 使用现有的处理函数
        result_file = process_single_file(
            filepath,
            output_dir=temp_output_dir,
            risk_free_rate=0.02
        )
        
        # 读取结果文件
        with open(result_file, 'r', encoding='utf-8') as f: # type: ignore
            output_text = f.read()
        
        # 清理
        os.remove(result_file) # type: ignore
        os.rmdir(temp_output_dir)
        
        return {
            'success': True,
            'output': output_text,
            'summary': '常规净值计算完成',
            'filename': f'净值计算_{frequency}.txt'
        }
    except Exception as e:
        # 清理
        try:
            os.rmdir(temp_output_dir)
        except:
            pass
        raise e


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

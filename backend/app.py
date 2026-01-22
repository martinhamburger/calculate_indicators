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
from utils.product_calculator import ProductNetValueCalculator
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
    try:
        calculator = BuyAvgReturnCalculator(filepath) # type: ignore
        
        # 调用计算方法 - 使用 run_all() 返回结果字典
        result_dict = calculator.run_all() # type: ignore
        
        # 获取产品信息
        product_info = calculator.get_product_info()
        
        # 生成输出文本
        output_text = calculator.generate_output_text()
        
        # 生成表格数据（买入开放日的平均收益）
        table_data = []
        if hasattr(calculator, 'open_day_df') and isinstance(calculator.open_day_df, pd.DataFrame):
            # 转换为可显示的格式
            df_display = calculator.open_day_df.copy()
            # 如果有收益率列，格式化为百分比
            if '平均收益' in df_display.columns:
                df_display['平均收益'] = df_display['平均收益'].apply(lambda x: f"{x:.2%}")
            table_data = df_display.reset_index().to_dict('records')
        
        return {
            'success': True,
            'output': output_text,
            'table_data': table_data,
            'summary': f"计算完成：{product_info.get('name', '产品')} 的买入平均收益",
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
        
        # 初始化计算器
        calculator = PeriodicBuyCalculator(filepath, buy_rule) # type: ignore
        
        # 调用计算方法 - 使用 calculate_buy_returns() 返回结果
        results_df = calculator.calculate_buy_returns()
        
        # 获取产品信息
        product_info = calculator.get_product_info()
        
        # 生成格式化输出文本
        output_text = calculator.format_output_text(preview_count=20)
        
        # 生成完整表格数据
        table_data = results_df.reset_index().to_dict('records') if isinstance(results_df, pd.DataFrame) else []
        
        # 计算汇总信息
        total_purchases = len(results_df) if isinstance(results_df, pd.DataFrame) else 0
        avg_return = results_df['区间收益率'].mean() if isinstance(results_df, pd.DataFrame) and '区间收益率' in results_df.columns else 0
        
        return {
            'success': True,
            'output': output_text,
            'table_data': table_data,
            'summary': f"定期买入计算完成: 共 {total_purchases} 次买入，平均收益率 {avg_return:.2%}",
            'filename': f'定期买入_{frequency}.txt'
        }
    except Exception as e:
        raise Exception(f"定期买入计算失败: {str(e)}")


def calculate_normal(filepath, frequency):
    """常规计算 - 产品净值和业绩指标"""
    try:
        # 使用 ProductNetValueCalculator
        calculator = ProductNetValueCalculator(filepath)
        
        # 执行计算 - 使用 run_all_calculations()
        calculator.run_all_calculations()
        
        # 获取产品信息
        product_info = calculator.get_product_info()
        
        # 构建业绩指标数据框
        metrics_df = calculator.build_metrics_df()
        
        # 生成输出文本
        output_lines = []
        output_lines.append("=" * 80)
        output_lines.append("产品净值计算结果")
        output_lines.append("=" * 80)
        output_lines.append(f"\n产品名称: {product_info.get('name', '未知')}")
        output_lines.append(f"产品代码: {product_info.get('code', '未知')}")
        output_lines.append(f"数据范围: {product_info.get('date_range', '未知')}")
        
        output_lines.append("\n业绩指标：")
        if isinstance(metrics_df, pd.DataFrame) and not metrics_df.empty:
            # 将指标数据写入输出
            for _, row in metrics_df.iterrows():
                for col in metrics_df.columns:
                    value = row[col]
                    output_lines.append(f"{col}: {value}")
        
        output_text = "\n".join(output_lines)
        
        # 生成表格数据
        table_data = []
        if isinstance(metrics_df, pd.DataFrame):
            table_data = metrics_df.reset_index().to_dict('records')
        
        return {
            'success': True,
            'output': output_text,
            'table_data': table_data,
            'summary': f"净值计算完成：{product_info.get('name', '产品')}",
            'filename': f'净值计算_{frequency}.txt'
        }
    except Exception as e:
        raise Exception(f"常规计算失败: {str(e)}")


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

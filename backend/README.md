# Backend 目录

这是产品净值计算器的后端 API 服务。

## 本地运行

```bash
# 安装依赖
pip install -r requirements.txt

# 启动服务
python app.py
```

服务将在 http://localhost:5000 启动

## API 接口

### POST /api/calculate

计算净值数据

**参数:**
- `file`: 上传的净值文件（xlsx/xls/txt/csv）
- `type`: 计算类型（buy_avg/periodic_buy/calculate）
- `frequency`: 频率（friday/monthly/daily）
- `start_date`: 开始日期（可选）
- `end_date`: 结束日期（可选）
- `amount`: 投资金额（定期买入时使用）

**返回:**
```json
{
  "success": true,
  "output": "计算结果文本",
  "table_data": [],
  "summary": "汇总信息",
  "filename": "结果文件名"
}
```

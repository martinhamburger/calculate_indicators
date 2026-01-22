import React, { useState } from 'react';
import { Layout, Menu, Card, Upload, Button, Select, DatePicker, InputNumber, Space, message, Spin, Table, Divider } from 'antd';
import { UploadOutlined, CalculatorOutlined, DownloadOutlined, LineChartOutlined } from '@ant-design/icons';
import axios from 'axios';
import './App.css';

const { Header, Content, Footer } = Layout;
const { Option } = Select;
const { RangePicker } = DatePicker;

function App() {
  const [loading, setLoading] = useState(false);
  const [calculationType, setCalculationType] = useState('buy_avg');
  const [fileList, setFileList] = useState([]);
  const [result, setResult] = useState(null);
  const [params, setParams] = useState({
    frequency: 'friday',
    dateRange: null,
    amount: 10000
  });

  const handleUpload = ({ fileList: newFileList }) => {
    setFileList(newFileList);
  };

  const handleCalculate = async () => {
    if (fileList.length === 0) {
      message.warning('请先上传净值文件');
      return;
    }

    setLoading(true);
    const formData = new FormData();
    formData.append('file', fileList[0].originFileObj);
    formData.append('type', calculationType);
    formData.append('frequency', params.frequency);
    if (params.dateRange) {
      formData.append('start_date', params.dateRange[0].format('YYYY-MM-DD'));
      formData.append('end_date', params.dateRange[1].format('YYYY-MM-DD'));
    }
    formData.append('amount', params.amount);

    try {
      const response = await axios.post('/api/calculate', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
      setResult(response.data);
      message.success('计算完成！');
    } catch (error) {
      message.error('计算失败：' + (error.response?.data?.error || error.message));
    } finally {
      setLoading(false);
    }
  };

  const handleDownload = () => {
    if (!result) return;
    
    const blob = new Blob([result.output], { type: 'text/plain' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = result.filename || 'result.txt';
    a.click();
    window.URL.revokeObjectURL(url);
  };

  const menuItems = [
    {
      key: '1',
      icon: <CalculatorOutlined />,
      label: '净值计算器',
    }
  ];

  const columns = result?.table_data ? Object.keys(result.table_data[0] || {}).map(key => ({
    title: key,
    dataIndex: key,
    key: key,
  })) : [];

  return (
    <Layout className="layout">
      <Header style={{ display: 'flex', alignItems: 'center', background: '#001529' }}>
        <div className="logo" style={{ color: 'white', fontSize: '20px', fontWeight: 'bold', marginRight: '50px' }}>
          <LineChartOutlined /> 产品净值计算器
        </div>
        <Menu
          theme="dark"
          mode="horizontal"
          defaultSelectedKeys={['1']}
          items={menuItems}
          style={{ flex: 1, minWidth: 0 }}
        />
      </Header>
      
      <Content style={{ padding: '50px' }}>
        <div style={{ maxWidth: '1200px', margin: '0 auto' }}>
          <Card title="计算配置" bordered={false}>
            <Space direction="vertical" size="large" style={{ width: '100%' }}>
              {/* 上传文件 */}
              <div>
                <label style={{ display: 'block', marginBottom: '8px', fontWeight: 'bold' }}>
                  上传净值列表文件（.xlsx/.xls/.csv/.txt）：
                </label>
                <Upload
                  fileList={fileList}
                  onChange={handleUpload}
                  beforeUpload={() => false}
                  maxCount={1}
                  accept=".txt,.csv,.xlsx,.xls"
                >
                  <Button icon={<UploadOutlined />}>选择文件</Button>
                </Upload>
              </div>

              {/* 计算类型 */}
              <div>
                <label style={{ display: 'block', marginBottom: '8px', fontWeight: 'bold' }}>
                  计算类型：
                </label>
                <Select
                  value={calculationType}
                  onChange={setCalculationType}
                  style={{ width: 300 }}
                >
                  <Option value="buy_avg">买入平均收益</Option>
                  <Option value="periodic_buy">定期买入</Option>
                  <Option value="calculate">常规计算</Option>
                </Select>
              </div>

              {/* 频率选择 - 仅在定期买入时显示 */}
              {calculationType === 'periodic_buy' && (
                <div>
                  <label style={{ display: 'block', marginBottom: '8px', fontWeight: 'bold' }}>
                    买入频率：
                  </label>
                  <Select
                    value={params.frequency}
                    onChange={(val) => setParams({ ...params, frequency: val })}
                    style={{ width: 300 }}
                  >
                    <Option value="friday">每周五</Option>
                    <Option value="monthly">每月20日</Option>
                  </Select>
                </div>
              )}

              {/* 日期范围 */}
              {calculationType === 'periodic_buy' && (
                <div>
                  <label style={{ display: 'block', marginBottom: '8px', fontWeight: 'bold' }}>
                    日期范围（可选）：
                  </label>
                  <RangePicker
                    onChange={(dates) => setParams({ ...params, dateRange: dates })}
                    style={{ width: 300 }}
                  />
                </div>
              )}

              {/* 金额 */}
              {calculationType === 'periodic_buy' && (
                <div>
                  <label style={{ display: 'block', marginBottom: '8px', fontWeight: 'bold' }}>
                    每期投资金额：
                  </label>
                  <InputNumber
                    value={params.amount}
                    onChange={(val) => setParams({ ...params, amount: val })}
                    style={{ width: 300 }}
                    min={0}
                    step={1000}
                    formatter={value => `¥ ${value}`.replace(/\B(?=(\d{3})+(?!\d))/g, ',')}
                  />
                </div>
              )}

              {/* 计算按钮 */}
              <div>
                <Button
                  type="primary"
                  size="large"
                  icon={<CalculatorOutlined />}
                  onClick={handleCalculate}
                  loading={loading}
                >
                  开始计算
                </Button>
              </div>
            </Space>
          </Card>

          {/* 结果显示 */}
          {loading && (
            <Card title="计算中..." style={{ marginTop: '24px' }}>
              <div style={{ textAlign: 'center', padding: '50px' }}>
                <Spin size="large" />
              </div>
            </Card>
          )}

          {result && !loading && (
            <Card 
              title="计算结果" 
              style={{ marginTop: '24px' }}
              extra={
                <Button 
                  type="primary" 
                  icon={<DownloadOutlined />}
                  onClick={handleDownload}
                >
                  下载结果
                </Button>
              }
            >
              {result.summary && (
                <>
                  <div style={{ marginBottom: '20px' }}>
                    <h3>汇总信息：</h3>
                    <pre style={{ background: '#f5f5f5', padding: '16px', borderRadius: '4px' }}>
                      {result.summary}
                    </pre>
                  </div>
                  <Divider />
                </>
              )}

              {result.table_data && result.table_data.length > 0 && (
                <div>
                  <h3 style={{ marginBottom: '16px' }}>数据表格：</h3>
                  <Table
                    dataSource={result.table_data}
                    columns={columns}
                    pagination={{ pageSize: 10 }}
                    scroll={{ x: 'max-content' }}
                    size="small"
                  />
                </div>
              )}

              {result.output && !result.table_data && (
                <div>
                  <h3>详细输出：</h3>
                  <pre style={{ 
                    background: '#f5f5f5', 
                    padding: '16px', 
                    borderRadius: '4px',
                    maxHeight: '400px',
                    overflow: 'auto'
                  }}>
                    {result.output}
                  </pre>
                </div>
              )}
            </Card>
          )}
        </div>
      </Content>

      <Footer style={{ textAlign: 'center' }}>
        产品净值计算器 ©{new Date().getFullYear()} 
      </Footer>
    </Layout>
  );
}

export default App;

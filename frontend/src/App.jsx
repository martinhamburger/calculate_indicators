import React, { useState } from 'react';
import { Layout, Menu, Card, Upload, Button, Select, DatePicker, Space, message, Spin, Table, Divider, Tabs } from 'antd';
import { UploadOutlined, CalculatorOutlined, DownloadOutlined, LineChartOutlined, FileExcelOutlined, FileTextOutlined } from '@ant-design/icons';
import axios from 'axios';
import './App.css';

const { Header, Content, Footer } = Layout;
const { Option } = Select;

function App() {
  const [loading, setLoading] = useState(false);
  const [calculationType, setCalculationType] = useState('buy_avg');
  const [fileList, setFileList] = useState([]);
  const [result, setResult] = useState(null);
  const [params, setParams] = useState({
    frequency: 'friday',
    startDate: null
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
    try {
      // 如果有多个文件，只处理第一个；未来可扩展为处理所有文件
      const file = fileList[0].originFileObj;
      const formData = new FormData();
      formData.append('file', file);
      formData.append('type', calculationType);
      formData.append('frequency', params.frequency);
      if (params.startDate) {
        formData.append('start_date', params.startDate.format('YYYY-MM-DD'));
      }
      
      const response = await axios.post('/api/calculate', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
      setResult(response.data);
      console.log('计算完成，结果:', response.data);
      console.log('sheets_data:', response.data.sheets_data);
      if (response.data.sheets_data) {
        console.log('sheets_data详情:', Object.entries(response.data.sheets_data).map(([k, v]) => `${k}: ${Array.isArray(v) ? v.length : 0} items`));
      }
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

  const handleDownloadExcel = async () => {
    if (!fileList || fileList.length === 0) {
      message.warning('请先上传文件');
      return;
    }
    
    try {
      setLoading(true);
      const formData = new FormData();
      formData.append('file', fileList[0].originFileObj);
      formData.append('frequency', params.frequency);
      
      const response = await axios.post('/api/download-excel', formData, {
        responseType: 'blob',
      });
      
      // 从响应头中获取文件名
      const contentDisposition = response.headers['content-disposition'];
      let downloadName = '净值计算.xlsx';
      if (contentDisposition) {
        const filename = decodeURIComponent(contentDisposition.split('filename=')[1]?.replace(/"/g, '') || downloadName);
        downloadName = filename;
      }
      
      // 下载文件
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', downloadName);
      document.body.appendChild(link);
      link.click();
      if (link.parentNode) {
        link.parentNode.removeChild(link);
      }
      window.URL.revokeObjectURL(url);
      
      message.success('Excel文件下载成功');
    } catch (error) {
      message.error('Excel文件下载失败: ' + (error.response?.data?.error || error.message));
    } finally {
      setLoading(false);
    }
  };

  const handleDownloadSummary = () => {
    if (!result) return;
    
    // 下载汇总信息
    const summaryText = `产品名称: ${result.product_name || '未知'}\n\n${result.summary || ''}\n\n${result.output || ''}`;
    const blob = new Blob([summaryText], { type: 'text/plain' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `汇总_${result.product_name || 'result'}.txt`;
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
                  上传净值列表文件（.xlsx/.xls/.csv/.txt，支持多文件）：
                </label>
                <Upload
                  fileList={fileList}
                  onChange={handleUpload}
                  beforeUpload={() => false}
                  multiple
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

              {/* 初始日期 */}
              {calculationType === 'periodic_buy' && (
                <div>
                  <label style={{ display: 'block', marginBottom: '8px', fontWeight: 'bold' }}>
                    初始买入日期（可选，默认从数据起始日）：
                  </label>
                  <DatePicker
                    onChange={(date) => setParams({ ...params, startDate: date })}
                    style={{ width: 300 }}
                    placeholder="选择初始日期"
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
                <Space>
                  {result.sheets_data && (
                    <>
                      <Button 
                        type="primary" 
                        icon={<FileExcelOutlined />}
                        onClick={handleDownloadExcel}
                      >
                        下载为Excel
                      </Button>
                      <Button 
                        icon={<FileTextOutlined />}
                        onClick={handleDownloadSummary}
                      >
                        下载汇总表
                      </Button>
                    </>
                  )}
                  <Button 
                    type="primary" 
                    icon={<DownloadOutlined />}
                    onClick={handleDownload}
                  >
                    下载结果
                  </Button>
                </Space>
              }
            >
              {/* 常规计算：多Sheet展示 */}
              {result.sheets_data && (
                <>
                  <Tabs
                    defaultActiveKey="0"
                    style={{ marginBottom: '24px' }}
                    items={Object.entries(result.sheets_data).map((item, index) => {
                      const [sheetName, sheetData] = item;
                      return {
                        key: index.toString(),
                        label: sheetName,
                        children: (
                          <div style={{ maxHeight: '600px', overflowY: 'auto' }}>
                            {sheetData && Array.isArray(sheetData) && sheetData.length > 0 ? (
                              <Table
                                dataSource={sheetData.map((row, idx) => ({ ...row, _key: idx }))}
                                columns={sheetData[0] ? Object.keys(sheetData[0])
                                  .filter(key => key !== '_key')
                                  .map(key => ({
                                    title: key,
                                    dataIndex: key,
                                    key: key,
                                    render: (text) => {
                                      // 格式化数字，四位小数
                                      if (typeof text === 'number') {
                                        return text.toFixed(4);
                                      }
                                      return text === null ? '-' : text;
                                    }
                                  })) : []}
                                pagination={{ pageSize: 20 }}
                                scroll={{ x: 'max-content' }}
                                size="small"
                                rowKey="_key"
                              />
                            ) : (
                              <p style={{ padding: '20px', textAlign: 'center', color: '#999' }}>
                                {sheetData === undefined ? '数据未加载' : sheetData === null ? '数据为空' : sheetData.length === 0 ? '无数据' : '数据加载出错'}
                              </p>
                            )}
                          </div>
                        )
                      };
                    })}
                  />
                  <Divider />
                </>
              )}

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

# GitHub Pages 部署 - 快速指南

## 🎯 目标
将前端部署到 GitHub Pages，让它在网上可以访问。

---

## ⚡ 5分钟快速开始

### Step 1: 确认仓库名称
访问你的GitHub仓库，查看URL：
```
https://github.com/你的用户名/仓库名
```
例如：`https://github.com/john/calculate_indicators`
- **用户名**: john
- **仓库名**: calculate_indicators

### Step 2: 运行配置脚本

#### Windows用户：
双击运行 `setup-github-pages.bat`

#### Mac/Linux用户：
```bash
chmod +x setup-github-pages.sh
./setup-github-pages.sh
```

按提示输入信息即可。

### Step 3: GitHub设置
访问你的仓库设置页面：
```
https://github.com/你的用户名/仓库名/settings/pages
```

确保设置如下：
- **Source**: GitHub Actions ✅
- **Branch**: main ✅

### Step 4: 推送代码
```bash
git push origin main
```

### Step 5: 等待部署
访问仓库的 **Actions** 标签页，等待工作流完成。

### Step 6: 访问你的网站
```
https://你的用户名.github.io/仓库名/
```

例如：`https://john.github.io/calculate_indicators/`

---

## 🔧 后端API配置

### 问题
GitHub Pages上的前端如何与后端通信？

### 方案

#### 方案 A：远程后端（推荐）⭐
如果你有云服务器（阿里云、AWS等）或部署服务（Railway、Render等）：

1. **获取后端服务器地址**
   - 例如：`https://api.example.com:5000`
   - 或：`http://your-server.com:5000`

2. **修改 `frontend/.env.production`**
   ```bash
   VITE_API_URL=https://api.example.com:5000
   ```

3. **推送更改**
   ```bash
   git add frontend/.env.production
   git commit -m "Update API URL"
   git push origin main
   ```

#### 方案 B：本地开发测试
```bash
# 终端1：启动后端
cd backend
python app.py

# 终端2：启动前端
cd frontend
npm run dev
```
访问 `http://localhost:3000`

---

## 📁 配置文件说明

### `frontend/.env.production`
生产环境（GitHub Pages）使用的配置
```bash
VITE_API_URL=https://your-backend.com:5000
```

### `frontend/.env.development`
本地开发环境使用的配置
```bash
VITE_API_URL=http://localhost:5000
```

### `frontend/vite.config.js`
```javascript
base: process.env.NODE_ENV === 'production' ? '/calculate_indicators/' : '/'
```
改为你的仓库名（如果不是 `calculate_indicators`）

---

## 🌐 后端部署选项

如果还没有后端服务器，以下是几个快速部署选项：

### 1. Railway (推荐快速部署)
- https://railway.app
- 支持Python Flask
- 免费额度充足
- 步骤：连接GitHub → 选择项目 → 自动部署

### 2. Vercel (Node.js应用)
- https://vercel.com
- 可部署API

### 3. Render
- https://render.com
- 支持Python/Flask
- 有免费套餐

### 4. 阿里云 / 腾讯云 / AWS
- 云主机方案
- 完整控制权

---

## ✅ 验证部署成功

### 前端部署检查
1. 访问 GitHub Pages URL
2. 看到产品净值计算器界面
3. 打开浏览器开发者工具 (F12)
4. 检查 **Console** 标签 - 无红色错误

### 后端连接检查
1. 上传一个Excel文件
2. 点击"开始计算"
3. 检查 **Network** 标签中的 API 请求
4. 应该看到请求发往你的后端服务器
5. 如果返回成功，说明连接正常 ✅

---

## 🚨 常见问题

### Q: 网页打开显示404
**A:** 
- 检查 GitHub Pages 是否启用了 Actions 部署
- 检查仓库名称是否正确（base 路径）
- 等待 Actions 完成（可能需要2-3分钟）

### Q: 计算功能不能用
**A:**
- 检查 `.env.production` 中的 `VITE_API_URL` 是否正确
- 检查后端服务器是否在运行
- 打开开发者工具看API请求返回什么错误

### Q: 网页样式不对
**A:**
- 清除浏览器缓存
- 按 `Ctrl+Shift+R` (Windows) 或 `Cmd+Shift+R` (Mac) 进行硬刷新

### Q: 想改变仓库名
**A:**
1. GitHub 上重命名仓库
2. 修改 `frontend/vite.config.js` 中的 `base` 字段
3. 重新推送代码

---

## 📚 详细文档

更多详细信息请查看 `GITHUB_PAGES_DEPLOYMENT.md`

---

## 🎉 完成！

你现在拥有：
- ✅ 自动部署的前端
- ✅ GitHub Pages 托管
- ✅ 灵活的后端配置

有任何问题？
- 查看 Actions 日志了解部署过程
- 检查浏览器开发者工具排查问题
- 参考详细部署指南

祝你使用愉快！🚀

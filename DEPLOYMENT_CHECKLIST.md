# GitHub Pages 部署检查清单

使用这个清单确保一切配置正确。

## ✅ 前端配置检查

- [ ] **Vite 配置**
  - [ ] `frontend/vite.config.js` 存在
  - [ ] `base` 字段设置为 `'/calculate_indicators/'` (或你的仓库名)
  - [ ] `server.proxy` 配置了 `/api` 代理

- [ ] **环境变量**
  - [ ] `frontend/.env.production` 存在
  - [ ] `VITE_API_URL` 指向你的后端服务器
  - [ ] `frontend/.env.development` 存在
  - [ ] `VITE_API_URL` 指向 `http://localhost:5000`

- [ ] **代码更新**
  - [ ] `frontend/src/App.jsx` 导入了 `import.meta.env.VITE_API_URL`
  - [ ] API 调用使用 `${API_BASE_URL}/api/...`
  - [ ] 没有硬编码的 `/api` 路径

- [ ] **NPM 配置**
  - [ ] `frontend/package.json` 存在
  - [ ] `npm run build` 可以成功执行
  - [ ] 没有 npm 依赖错误

## ✅ GitHub Actions 配置检查

- [ ] **工作流文件**
  - [ ] `.github/workflows/deploy-pages.yml` 存在
  - [ ] 配置了 `on.push.branches: [main, master]`
  - [ ] 配置了 `on.workflow_dispatch`
  - [ ] 上传 artifact 到 `./frontend/dist`

- [ ] **GitHub 权限**
  - [ ] 仓库有 GitHub Pages 权限
  - [ ] Actions 权限已启用

## ✅ GitHub 仓库检查

- [ ] **基本设置**
  - [ ] 仓库名称正确
  - [ ] 代码已推送到 `main` 分支
  - [ ] 所有配置文件已提交

- [ ] **Pages 设置**
  - [ ] 访问 Settings → Pages
  - [ ] Source 设置为 "GitHub Actions" ✓
  - [ ] Branch 设置为 "main" ✓
  - [ ] 没有部署错误

- [ ] **Actions 状态**
  - [ ] 访问 Actions 标签
  - [ ] 最新的 build 任务成功 ✓
  - [ ] 最新的 deploy 任务成功 ✓

## ✅ 后端配置检查

选择一个方案并完成：

### 方案 A: 远程服务器
- [ ] 后端服务器部署完成
- [ ] 获得了服务器 URL（例：https://api.example.com:5000）
- [ ] 更新了 `frontend/.env.production` 中的 `VITE_API_URL`
- [ ] 代码已推送

### 方案 B: 本地开发
- [ ] 本地可以运行 `python backend/app.py`
- [ ] 本地可以运行 `npm run dev`
- [ ] 不需要部署，仅用于测试

## ✅ 部署验证检查

- [ ] **网页访问**
  - [ ] 打开 `https://username.github.io/calculate_indicators/`
  - [ ] 页面完全加载，无 404 错误
  - [ ] 看到"产品净值计算器"标题

- [ ] **界面检查**
  - [ ] 页面布局正常
  - [ ] 上传文件按钮可点击
  - [ ] 计算类型下拉框可用
  - [ ] 开始计算按钮可点击

- [ ] **后端连接**
  - [ ] 上传一个 Excel 文件
  - [ ] 点击"开始计算"
  - [ ] 打开开发者工具 (F12) → Network
  - [ ] 看到 API 请求发往正确的后端地址
  - [ ] 返回 200 状态码（成功）

- [ ] **功能测试**
  - [ ] 选择"常规计算"，上传文件，能看到结果
  - [ ] 选择"买入平均收益"，能看到结果
  - [ ] 选择"定期买入"，能看到结果
  - [ ] 下载功能正常

## ❌ 故障排查

如果有项目未勾选，参考下表：

| 问题 | 解决方案 |
|------|--------|
| 页面 404 | 检查仓库名和 vite base 配置 |
| 页面打开但样式乱 | 硬刷新浏览器 (Ctrl+Shift+R) |
| 计算无反应 | 检查 API URL、后端是否运行 |
| Actions 失败 | 查看 Actions 日志了解错误信息 |
| CORS 错误 | 检查后端是否启用 CORS |

## 📋 快速命令参考

```bash
# 本地测试前端构建
cd frontend
npm run build

# 本地运行前端（开发模式）
npm run dev

# 本地运行后端
cd ../backend
python app.py

# 检查 git 状态
git status

# 推送所有更改
git push origin main

# 查看部署日志
# 访问: https://github.com/username/repo/actions
```

## 🎯 最终检查

完成以下任务后，你的部署就是成功的：

1. ✅ 能访问 GitHub Pages URL
2. ✅ 页面显示正常
3. ✅ 能上传文件
4. ✅ 能点击计算（后端正确连接）
5. ✅ 看到计算结果

---

**如果所有项目都已勾选，恭喜你！部署成功！🎉**

有任何问题？
- 查看 QUICK_START_GITHUB_PAGES.md
- 查看 GITHUB_PAGES_DEPLOYMENT.md
- 检查 Actions 标签页的日志

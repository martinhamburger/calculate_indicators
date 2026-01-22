# 🎯 GitHub Pages 部署 - 3步快速指南

> 你已经配置好了所有需要的代码！现在只需按照这3步就能在线部署。

---

## 第1步：修改后端API地址（仅需1分钟）

### 情况A：你有远程服务器
如果你的后端部署在云服务器上（如阿里云、AWS等）：

**打开文件**: `frontend/.env.production`

**修改为你的服务器地址**:
```env
VITE_API_URL=https://你的服务器地址:5000
```

例如：
```env
VITE_API_URL=https://api.example.com:5000
```

### 情况B：你没有服务器
暂时使用本地开发测试（GitHub Pages上的功能会受限）:

```env
VITE_API_URL=http://localhost:5000
```

---

## 第2步：提交代码到GitHub（仅需2分钟）

打开终端，在项目根目录运行：

```bash
# 1. 检查更改
git status

# 2. 提交所有更改
git add .
git commit -m "chore: configure GitHub Pages deployment"

# 3. 推送到GitHub
git push origin main
```

> 注意：如果你的主分支是 `master` 而不是 `main`，改成 `git push origin master`

---

## 第3步：在GitHub配置Pages（仅需1分钟）

### 3.1 打开GitHub仓库设置

访问：`https://github.com/你的用户名/calculate_indicators/settings/pages`

### 3.2 配置Pages

找到 **Build and deployment** 部分：

- **Source** 选择：`GitHub Actions` ✅
- **Branch** 选择：`main` 或你的主分支 ✅

点击 **Save**

### 3.3 等待部署

1. 访问你的仓库主页
2. 点击 **Actions** 标签
3. 应该看到一个在运行的任务
4. 等待任务完成（绿色对号 ✅）
5. 通常需要 2-5 分钟

---

## ✅ 部署完成！

当部署成功后，访问：

```
https://你的GitHub用户名.github.io/calculate_indicators/
```

例如：`https://john-doe.github.io/calculate_indicators/`

---

## 🔍 如果有问题

### 问题1：页面打不开
**检查清单：**
- [ ] GitHub Actions 任务是否显示 ✅ 成功？
- [ ] 是否等待了 2-5 分钟？
- [ ] Settings → Pages 是否设置为 GitHub Actions？

### 问题2：计算功能不工作
**检查清单：**
- [ ] 后端服务器是否在运行？
- [ ] `frontend/.env.production` 中的 API 地址是否正确？
- [ ] 打开浏览器 F12，Network 标签中 API 请求是否返回成功？

### 问题3：样式显示不对
**解决方案：**
- 按 `Ctrl + Shift + R`（Windows）或 `Cmd + Shift + R`（Mac）硬刷新浏览器

### 查看详细错误
1. 访问仓库的 **Actions** 标签
2. 点击最新失败的任务
3. 展开日志查看具体错误信息

---

## 📚 更多信息

如需了解更多细节：

- 📖 **快速指南**: [QUICK_START_GITHUB_PAGES.md](./QUICK_START_GITHUB_PAGES.md)
- 📘 **完整指南**: [GITHUB_PAGES_DEPLOYMENT.md](./GITHUB_PAGES_DEPLOYMENT.md)  
- ✅ **检查清单**: [DEPLOYMENT_CHECKLIST.md](./DEPLOYMENT_CHECKLIST.md)
- 📋 **设置总结**: [GITHUB_PAGES_SETUP_COMPLETE.md](./GITHUB_PAGES_SETUP_COMPLETE.md)

---

## 🚀 总结

**已完成的配置：**
- ✅ Vite 环境变量支持
- ✅ React App 动态 API URL
- ✅ GitHub Actions 自动部署工作流
- ✅ 环境配置文件

**你需要做的：**
1. ✏️ 修改 `frontend/.env.production` 的 API 地址
2. 📤 `git push` 推送到 GitHub
3. ⚙️ GitHub Pages 配置为 GitHub Actions 源

**结果：**
- 🎉 自动部署的在线应用
- 🌐 可以在任何地方访问
- 🔄 每次 push 都会自动更新

---

**现在就开始部署吧！** 🚀

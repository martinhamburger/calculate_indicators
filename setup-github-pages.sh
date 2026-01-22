#!/bin/bash

# GitHub Pages 部署快速配置脚本

echo "🚀 GitHub Pages 部署配置向导"
echo "================================"
echo ""

# 检查git
if ! command -v git &> /dev/null; then
    echo "❌ 未找到 git，请先安装 git"
    exit 1
fi

# 检查当前目录
if [ ! -f "package.json" ] || [ ! -d "backend" ]; then
    echo "❌ 请在项目根目录运行此脚本"
    exit 1
fi

# 获取用户输入
echo "📝 请输入以下信息："
echo ""

read -p "GitHub 仓库名称 (例: calculate_indicators): " REPO_NAME
if [ -z "$REPO_NAME" ]; then
    REPO_NAME="calculate_indicators"
fi

read -p "后端 API 地址 (例: http://your-server.com:5000): " API_URL
if [ -z "$API_URL" ]; then
    API_URL="http://localhost:5000"
fi

read -p "GitHub 用户名: " GITHUB_USER
if [ -z "$GITHUB_USER" ]; then
    echo "❌ GitHub 用户名不能为空"
    exit 1
fi

echo ""
echo "✅ 配置信息："
echo "  仓库名称: $REPO_NAME"
echo "  API 地址: $API_URL"
echo "  GitHub 用户: $GITHUB_USER"
echo "  Pages URL: https://$GITHUB_USER.github.io/$REPO_NAME/"
echo ""

read -p "确认无误？(y/n): " CONFIRM
if [ "$CONFIRM" != "y" ]; then
    echo "❌ 已取消"
    exit 1
fi

# 修改 vite.config.js
echo "📝 更新 vite.config.js..."
cd frontend
if grep -q "base: process.env.NODE_ENV === 'production' ? '/$REPO_NAME/' : '/'," vite.config.js; then
    echo "✅ vite.config.js 已是正确配置"
else
    # 这里需要更新 base 路径
    echo "ℹ️  如需更改仓库名，请手动修改 frontend/vite.config.js 中的 base 字段"
fi

# 修改 .env.production
echo "📝 更新 .env.production..."
cat > .env.production << EOF
VITE_API_URL=$API_URL
EOF
echo "✅ 已保存 .env.production"

# 修改 .env.development
echo "📝 更新 .env.development..."
cat > .env.development << EOF
VITE_API_URL=http://localhost:5000
EOF
echo "✅ 已保存 .env.development"

cd ..

# 提交更改
echo "📝 提交更改到 git..."
git add frontend/.env.production frontend/.env.development frontend/vite.config.js
git commit -m "chore: configure GitHub Pages deployment settings" || true

echo ""
echo "✅ 配置完成！"
echo ""
echo "📋 后续步骤："
echo ""
echo "1️⃣  访问 GitHub 仓库设置:"
echo "   https://github.com/$GITHUB_USER/$REPO_NAME/settings/pages"
echo ""
echo "2️⃣  确保 Pages 配置："
echo "   - Source: GitHub Actions"
echo "   - Branch: main (或你的主分支)"
echo ""
echo "3️⃣  提交更改并推送："
echo "   git push origin main"
echo ""
echo "4️⃣  等待部署完成（查看 Actions 标签页）"
echo ""
echo "5️⃣  访问你的网站："
echo "   https://$GITHUB_USER.github.io/$REPO_NAME/"
echo ""
echo "❓ 有问题？查看 GITHUB_PAGES_DEPLOYMENT.md"

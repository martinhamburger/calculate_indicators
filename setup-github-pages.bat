@echo off
REM GitHub Pages 部署快速配置脚本 (Windows)

echo 🚀 GitHub Pages 部署配置向导
echo ================================
echo.

REM 检查当前目录
if not exist "package.json" (
    echo ❌ 请在项目根目录运行此脚本
    exit /b 1
)

if not exist "backend" (
    echo ❌ 请在项目根目录运行此脚本
    exit /b 1
)

REM 获取用户输入
echo 📝 请输入以下信息：
echo.

set /p REPO_NAME="GitHub 仓库名称 (例: calculate_indicators) [默认: calculate_indicators]: "
if "%REPO_NAME%"=="" set REPO_NAME=calculate_indicators

set /p API_URL="后端 API 地址 (例: http://your-server.com:5000) [默认: http://localhost:5000]: "
if "%API_URL%"=="" set API_URL=http://localhost:5000

set /p GITHUB_USER="GitHub 用户名: "
if "%GITHUB_USER%"=="" (
    echo ❌ GitHub 用户名不能为空
    exit /b 1
)

echo.
echo ✅ 配置信息：
echo   仓库名称: %REPO_NAME%
echo   API 地址: %API_URL%
echo   GitHub 用户: %GITHUB_USER%
echo   Pages URL: https://%GITHUB_USER%.github.io/%REPO_NAME%/
echo.

set /p CONFIRM="确认无误？(y/n): "
if /i not "%CONFIRM%"=="y" (
    echo ❌ 已取消
    exit /b 1
)

REM 进入 frontend 目录
cd frontend

echo 📝 更新 .env.production...
(
    echo VITE_API_URL=%API_URL%
) > .env.production
echo ✅ 已保存 .env.production

echo 📝 更新 .env.development...
(
    echo VITE_API_URL=http://localhost:5000
) > .env.development
echo ✅ 已保存 .env.development

cd ..

REM 提交更改
echo 📝 提交更改到 git...
git add frontend\.env.production frontend\.env.development frontend\vite.config.js
git commit -m "chore: configure GitHub Pages deployment settings" || true

echo.
echo ✅ 配置完成！
echo.
echo 📋 后续步骤：
echo.
echo 1️⃣  访问 GitHub 仓库设置：
echo    https://github.com/%GITHUB_USER%/%REPO_NAME%/settings/pages
echo.
echo 2️⃣  确保 Pages 配置：
echo    - Source: GitHub Actions
echo    - Branch: main (或你的主分支)
echo.
echo 3️⃣  提交更改并推送：
echo    git push origin main
echo.
echo 4️⃣  等待部署完成（查看 Actions 标签页）
echo.
echo 5️⃣  访问你的网站：
echo    https://%GITHUB_USER%.github.io/%REPO_NAME%/
echo.
echo ❓ 有问题？查看 GITHUB_PAGES_DEPLOYMENT.md
echo.
pause

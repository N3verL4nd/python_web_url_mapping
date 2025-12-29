@echo off
chcp 65001 >nul
setlocal

echo =========================================
echo   DomainLocalServer PyInstaller 打包开始
echo =========================================

REM 清理旧产物
if exist build (
    rmdir /s /q build
)
if exist dist (
    rmdir /s /q dist
)
if exist DomainLocalServer.spec (
    del /f /q DomainLocalServer.spec
)

REM 确保使用当前目录
cd /d %~dp0

REM 执行打包
pyinstaller -F -w --uac-admin --name HttpServer ^
  --hidden-import=browser ^
  --hidden-import=hosts_manager ^
  --hidden-import=web_server ^
  --hidden-import=admin ^
  main.py

echo.
echo =========================================
echo   打包完成
echo   输出文件：dist\HttpServer.exe
echo =========================================

pause

@echo off
cd /d "%~dp0client"
npm install && npm run dev
pause
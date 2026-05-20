@echo off
TITLE Dice Tales Chatbot - Starter
cls

echo ==========================================
echo    Iniciando Dice Tales Chatbot System
echo ==========================================
echo.

echo [1/2] Iniciando Servidor Backend (Flask)...
start "Chatbot Backend" cmd /k "python backend\chatbot-python\server.py"

echo [2/2] Iniciando Servidor Frontend (HTTP Server)...
start "Chatbot Frontend" cmd /k "cd frontend && python -m http.server 8080"

echo.
echo Servidores iniciados! 
echo Frontend disponivel em: http://localhost:8080
echo.
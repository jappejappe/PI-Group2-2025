@echo off 
chcp 65001 >nul
echo Desinstalando...
pip uninstall -y -r requirements.txt > ./logs/uninstall.log 2>&1
cls
echo Dependências desinstaladas!
pause
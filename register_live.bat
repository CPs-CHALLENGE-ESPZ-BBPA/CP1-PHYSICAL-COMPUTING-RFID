@echo off
title Smart Gym - Registro de Aluno para Apresentacao
color 0A

echo =======================================================
echo          SMART GYM - REGISTRO RAPIDO DE RFID
echo =======================================================
echo.
echo Instrucoes para a Apresentacao:
echo 1. Leia o cartao no Arduino para descobrir o UID.
echo 2. Digite o UID e os dados do aluno abaixo.
echo.

set /p rfid="UID do Cartao RFID (Ex: 4A B9 3B 1B): "
set /p nome="Nome do Aluno: "
set /p exercicio="Exercicio (Ex: Triceps, Rosca Direta): "
set /p reps="Objetivo de Repeticoes (Ex: 10): "

echo.
echo Salvando dados no banco de dados...
python register_student.py "%rfid%" "%nome%" "%exercicio%" "%reps%"

echo.
pause

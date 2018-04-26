@echo off
setlocal

SET PYTHONPATH=%~dp0/kreate;%PYTHONPATH%
python3 -m kreate %*
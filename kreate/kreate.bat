@echo off
setlocal

SET PYTHONPATH=%~dp0/src;%PYTHONPATH%
python3 -m kreate %*
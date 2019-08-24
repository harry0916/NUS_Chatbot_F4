@echo off

set name = safari
set pwd = %cd%
set ngrok_dir = %USERPROFILE%\ngrok

ngrok http 8080


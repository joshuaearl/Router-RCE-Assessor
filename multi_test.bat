@echo off
set /p instances="How many instances: "
for /l %%N in (1 1 %instances%) do (
	START routerAssess.py
	timeout 1 > NUL
	)
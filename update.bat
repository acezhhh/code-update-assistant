
@echo off
chcp 65001
setlocal enabledelayedexpansion
echo macao更新
echo 当前时间: %date% %time:~0,2%:%time:~3,2%:%time:~6,2%
set PROJECT_ARRAY=macao-ga-attend

REM 读取配置文件
set "iniFile=config.ini"
REM 使用 FOR 命令逐行读取文件内容
for /F "usebackq tokens=1,* delims==" %%A in ("%iniFile%") do (
    set "output_str=%%A"
    set "value=%%B"
    REM python保存后有空格不规范、去掉键和值中的空格
    set "output_str=!output_str: =!"
    set "output_str=!output_str:"=!"
    for /F "tokens=* delims= " %%D in ("!value!") do set "value=%%D"
    set !output_str!=!value!
	
	echo output_str:!output_str! value:!value!
)

echo project_root: "%project_root%"
echo java_home: "%java_home%"
echo maven_setting: "%maven_setting%"

rem 判断是否有参数传入
if "%*"=="" (
    echo 没有选择更新的项目
    rem goto :end
) else (
    echo 更新的项目：%*
    rem 遍历所有参数并拼接到 result 变量
    set "PROJECT_ARRAY=%*"
)
echo 更新项目: %PROJECT_ARRAY%

cd /d %PROJECT_ROOT%

for %%i in (%PROJECT_ARRAY%) do (
	echo ------------------------------ %%i 更新开始 -----------------------------------
	cd %PROJECT_ROOT%\%%i
	
	rem 更新代码
	call git pull || goto :end
		
	rem 打包
	if exist "backend" (
		cd backend
	)
	if exist "pom.xml" (
		call mvn clean install --s "%maven_setting%" -Dmaven.test.skip=true || goto :end
	)
	echo ------------------------------ %%i 更新结束 -----------------------------------
	echo;
)

echo;
echo;
echo;
echo 当前时间: %date% %time:~0,2%:%time:~3,2%:%time:~6,2%
echo ------------------------------ 本次更新内容 -----------------------------------
for %%i in (%PROJECT_ARRAY%) do echo [%%i]


echo;
echo;
echo;

call :end

:end
	echo 回车键结束窗口
	set /p id=
	exit
	
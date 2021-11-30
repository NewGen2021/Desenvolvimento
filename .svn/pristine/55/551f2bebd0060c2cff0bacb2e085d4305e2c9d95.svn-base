@echo off
cls
 
:: Caminho do binário do Subversion (SVN)
set SUBVERSION=C:\Users\008728631\Documents\Projeto_Integrado\SVN\statSVN
 
:: Caminho do repositório SVN
set SVN_SOURCE=https://svn.spo.ifsp.edu.br/svn/a6pgp/S202101-PI/NewGen/
 
:: Nome da pasta do relatório gerado
set DIR_NAME=relatorio__%DATE:~6,4%.%DATE:~3,2%.%DATE:~0,2%
 
 
:: Parâmetros de configuração
set TITLE="NewGen"
set DATE1="2021-08-30"
set DATE2="2021-11-18"
set INCLUDE="**/*.aspx;**/*.aspx.cs;**/*.ashx;**/*.ashx.cs;**/*.svc;**/*.svc.cs;**/*.cs;**/*.html;**/*.js;**/*.mrt"
set EXCLUDE="**/*.pdf;**/packages/**;**/node_modules/**;**/obj/**;**/bin/**;**/jquery*.js;**/angular-*.js"
 
::FOR /F "delims=" %%b IN ('PowerShell -Command "&{(Get-Date).AddDays(-30).ToString('yyyy\-MM\-dd')}"') DO (SET "DATE1=%%b")
::FOR /F "delims=" %%e IN ('PowerShell -Command "&{(Get-Date).ToString('yyyy\-MM\-dd')}"') DO (SET "DATE2=%%e")
 
 
:: STEP 1
echo.
call :PrintColor [ 1 - SVN UPDATE ]
echo.
"%SUBVERSION%\svn.exe" update %SVN_SOURCE%
echo.
pause
 
:: STEP 2
echo.
call :PrintColor [ 2 - SVN LOG ]
echo.
echo.Iniciando...
"%SUBVERSION%\svn.exe" log --verbose --xml --revision {%DATE1%T00:00Z}:{%DATE2%T23:59Z} > svn.log %SVN_SOURCE%
echo.Finalizado!
echo.
pause
 
:: STEP 3
echo.
call :PrintColor [ 3 - SVN STATISTICS ]
echo.
java -jar statsvn.jar -verbose -disable-twitter-button -title %TITLE% -output-dir %DIR_NAME% svn.log %SVN_SOURCE% -include %INCLUDE% -exclude %EXCLUDE%
echo.
echo.
echo.
 
if exist "%DIR_NAME%/index.html" start "" "%DIR_NAME%/index.html"
 
goto :eof
:PrintColor
 
powershell -Command Write-Host "%*" -foreground "yellow"
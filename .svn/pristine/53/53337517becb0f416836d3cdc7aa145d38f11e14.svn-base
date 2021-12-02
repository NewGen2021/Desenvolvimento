@echo off
set powershell_dir=%windir%\System32\WindowsPowerShell\v1.0\powershell

echo Usuario:
set /p usuario=

echo Senha:
set /p senha=

cls
echo Carregando
svn --non-interactive --trust-server-cert --username=%usuario% --password=%senha% checkout https://svn.spo.ifsp.edu.br/svn/a6pgp/S202101-PI/NewGen repo
svn log repo -r 1:HEAD --xml --verbose > projetolog.xml

cls
echo Mudando os nomes

%powershell_dir% -Command "(get-content projetolog.xml) | %%{$_ -replace \"sp402427x\",\"Camila\"} | set-content projetolog.xml"
%powershell_dir% -Command "(get-content projetolog.xml) | %%{$_ -replace \"sp3013456\",\"Gabriel\"} | set-content projetolog.xml"
%powershell_dir% -Command "(get-content projetolog.xml) | %%{$_ -replace \"sp3014207\",\"Beatriz\"} | set-content projetolog.xml"
%powershell_dir% -Command "(get-content projetolog.xml) | %%{$_ -replace \"sp3031853\",\"Bruna\"} | set-content projetolog.xml"
%powershell_dir% -Command "(get-content projetolog.xml) | %%{$_ -replace \"sp3017061\",\"Fernando\"} | set-content projetolog.xml"
%powershell_dir% -Command "(get-content projetolog.xml) | %%{$_ -replace \"sp3015751\",\"Lucas\"} | set-content projetolog.xml"

cls
echo Criando a legenda
prog projetolog.xml

cls
echo Pode editar a legenda
pause

cls
echo Gerando Gource
gource projetolog.xml --caption-file "timestamp.txt" --caption-size 20 --caption-duration 3 --caption-colour FFD700 --stop-at-end --key --user-image-dir "./img"  -1280x720 --title "NewGen - Log - 6 semestre" --seconds-per-day 1.2 --hide filenames --disable-progress --auto-skip-seconds 1 --date-format "%%d/%%m/%%y  %%H:%%M:%%S" -o - | ffmpeg -y -r 60 -f image2pipe -vcodec ppm -i - -vcodec libx264 -preset ultrafast -pix_fmt yuv420p -crf 1 -threads 0 -bf 0 "Final.mp4"

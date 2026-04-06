:: GET THE DATE AND TIME
:: Source - https://stackoverflow.com/a/19131662
:: Posted by foxidrive, modified by community. See post 'Timeline' for change history
:: Retrieved 2026-03-14, License - CC BY-SA 3.0
@echo off
for /f "tokens=2 delims==" %%a in ('wmic OS Get localdatetime /value') do set "dt=%%a"
set "YY=%dt:~2,2%" & set "YYYY=%dt:~0,4%" & set "MM=%dt:~4,2%" & set "DD=%dt:~6,2%"
set "HH=%dt:~8,2%" & set "Min=%dt:~10,2%"

set "timestamp=%YYYY%-%MM%-%DD% at %HH%:%Min%"

: rebuild the site
CALL npm run build

: fix the github pages 404 error on refresh
copy "dist\index.html" "dist\404.html"

: push
git add .
IF "%~1"=="" (
    git commit -m "automated update on %timestamp%"
) ELSE (
    git commit -m %1
)
git push

: deploy
git subtree push --prefix dist origin gh-pages
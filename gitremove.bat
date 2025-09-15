:a

set /p file= "Drag Your File Here: "

git rm --cached %file%

git commit -m "removed file"

git push origin main

pause

goto a
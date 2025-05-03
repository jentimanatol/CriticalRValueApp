git --version
git add .
git commit -m "'Forced exit of the script'"
git push origin main

:: === Tagging for GitHub Actions Release Build ===
git tag v2.9
git push origin v2.9
pause

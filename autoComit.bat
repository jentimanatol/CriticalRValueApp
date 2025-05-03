git --version
git add .
git commit -m "'Window size'"
git push origin main

:: === Tagging for GitHub Actions Release Build ===
git tag v3.4
git push origin v3.4
pause

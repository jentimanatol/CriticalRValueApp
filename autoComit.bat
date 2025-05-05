git --version
git add .
git commit -m "'Window size'"
git push origin main

:: === Tagging for GitHub Actions Release Build ===
git tag v4.0
git push origin v4.0
pause

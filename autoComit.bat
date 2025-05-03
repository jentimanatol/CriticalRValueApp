git --version
git add .
git commit -m "Increaset font size"
git push origin main

:: === Tagging for GitHub Actions Release Build ===
git tag v2.6.1
git push origin v2.6.1
pause

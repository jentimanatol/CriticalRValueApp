git --version
git add .
git commit -m "Autocomit"
git push origin main

:: === Tagging for GitHub Actions Release Build ===
git tag v2.2
git push origin v2.2
pause

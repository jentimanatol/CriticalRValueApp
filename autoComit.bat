git --version
git add .
git commit -m "Add exit button to the main form"
git push origin main

:: === Tagging for GitHub Actions Release Build ===
git tag v2.6.2
git push origin v2.6.2
pause

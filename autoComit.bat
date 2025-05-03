git --version
git add .
git commit -m "'Final commit before release'"
git push origin main

:: === Tagging for GitHub Actions Release Build ===
git tag v3.1
git push origin v3.1
pause

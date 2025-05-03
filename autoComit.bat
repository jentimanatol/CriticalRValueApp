git --version
git add .
git commit -m "'Modificate for 2 tailed plot'"
git push origin main

:: === Tagging for GitHub Actions Release Build ===
git tag v3.2
git push origin v3.2
pause

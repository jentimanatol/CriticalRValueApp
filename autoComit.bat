git --version
git add .
git commit -m "fixed error root.destroy"
git push origin main

:: === Tagging for GitHub Actions Release Build ===
git tag v2.6.4
git push origin v2.6.4
pause

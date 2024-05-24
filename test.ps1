rm -r dist
rm -r build
rm frontend.spec

pyinstaller --onefile --clean --additional-hooks-dir=. frontend.py
./dist/frontend.exe

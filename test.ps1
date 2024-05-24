rm -r dist
rm -r build
rm frontend.spec
rm backend.spec

pyinstaller --onefile --clean --additional-hooks-dir=. frontend.py
pyinstaller --onefile backend.py

./dist/frontend.exe

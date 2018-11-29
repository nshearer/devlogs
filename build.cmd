"C:\Users\Nathan Shearer\AppData\Local\Programs\Python\Python36-32\python.exe" change_version.py %1
"C:\Users\Nathan Shearer\AppData\Local\Programs\Python\Python36-32\python.exe" build_assets_module.py
"C:\Users\Nathan Shearer\AppData\Local\Programs\Python\Python36-32\python.exe" setup.py sdist bdist_wheel
"C:\Users\Nathan Shearer\AppData\Local\Programs\Python\Python36-32\Scripts\twine.exe" upload --repository-url https://test.pypi.org/legacy/ dist\devlogs-%1*
echo "pip install devlogs --index-url https://test.pypi.org/simple/ --upgrade"
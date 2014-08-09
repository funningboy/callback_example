
find . -name "*.pyc" -exec rm -rf {} \;
rm -rf ./cy_cb/build
rm -rf ./py_cb/build
rm -rf ./py_nogil/build
rm -rf *.log
rm -rf *.db

cd ./cy_cb/
python setup.py install
cd ..

cd ./py_cb
python setyp.py install
cd ..

cd ./py_nogil
python setup.py install
cd ..

python run_cheese.py

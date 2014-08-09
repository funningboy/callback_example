#!/bin/sh

# usage
function usage()
{
    echo ""
    echo "./command [--clear|--all]"
    echo "\t-t-h --help"
    echo "\t--clear clear build/test results"
    echo "\t--all run all test"
    echo ""
}

# clear build/test
function clear()
{
  find . -name "*.pyc" -exec rm -rf {} \;
  rm -rf ./cy_cb/build
  rm -rf ./py_cb/build
  rm -rf ./py_nogil/build
  rm -rf *.log
  rm -rf *.db
}

#build
function build()
{
  cd ./cy_cb/
  python setup.py install
  cd ..

  cd ./py_cb
  python setup.py install
  cd ..

  cd ./py_nogil
  python setup.py install
  cd ..
}

#run
function run()
{
  python run_cheese.py
}

while [ "$1" != "" ]; do
   PARAM=`echo $1 | awk -F= '{print $1}'`
   case $PARAM in
      -h | --help)
        usage
        exit
        ;;
      --clear)
        clear
        exit
        ;;
      --all)
        build
        run
        exit
        ;;
      *)
        echo "Error unknown arg \"$PARAM\""
        usage
        exit 1
    esac
    shift
done




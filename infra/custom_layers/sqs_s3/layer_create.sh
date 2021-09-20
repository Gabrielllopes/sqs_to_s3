# sudo apt install python3.8-venv
set -e

LAYER_ZIP=sqs_to_s3_layer.zip

if test -d "sqs_s3" ; then
    rm -rf sqs_s3
fi

if test -d "python" ; then
    rm -rf python
fi

if test -f "$LAYER_ZIP" ; then
    rm $LAYER_ZIP
fi

python3.8 -m venv sqs_s3
source sqs_s3/bin/activate

pip install s3fs
pip install pytz

mkdir python
mv sqs_s3/lib64/python3.8/site-packages/* python

cd python
rm -r *.dist-info __pycache__
cd ..

zip -r $LAYER_ZIP python
deactivate

rm -rf python sqs_s3
LAYER_ZIP=pandas_layer.zip

URL_PANDAS=https://files.pythonhosted.org/packages/59/93/d5e5b03e7a6cc830d30d571d4764623dd8f578c554801b28490d67c0c68d/pandas-1.3.3-cp310-cp310-manylinux_2_17_x86_64.manylinux2014_x86_64.whl
PANDAS_FILE=pandas-1.3.3-cp310-cp310-manylinux_2_17_x86_64.manylinux2014_x86_64.whl

PYTZ_URL=https://files.pythonhosted.org/packages/70/94/784178ca5dd892a98f113cdd923372024dc04b8d40abe77ca76b5fb90ca6/pytz-2021.1-py2.py3-none-any.whl
PYTZ_FILE=pytz-2021.1-py2.py3-none-any.whl

if [[ -f "$LAYER_ZIP" ]]; then
    rm $FILE
fi
mkdir python
cd python
wget $URL_PANDAS
unzip $PANDAS_FILE
wget $PYTZ_URL
unzip $PYTZ_FILE
rm -r *.whl *.dist-info __pycache__
cd ..
zip -r $LAYER_ZIP python
rm -rf python
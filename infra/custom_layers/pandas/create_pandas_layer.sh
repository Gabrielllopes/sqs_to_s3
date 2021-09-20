# sudo apt install python3.8
# pip install virtualenv
virtualenv --python=/usr/bin/python3.8 pandas-env
source pandas-env/bin/activate
pip install pandas
deactivate
zip -r panda_layer.zip pandas-env/lib/python3.8/site-packages
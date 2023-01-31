#!/bin/bash
unzip nwrfc750P_10-70002752_linx86_64.zip
sudo mkdir /usr/sap/
sudo mv ./nwrfc750P_10-70002752_linx86_64 /usr/sap/nwrfcsdk
sudo su -
echo '/usr/sap/nwrfcsdk/lib' > /etc/ld.so.conf.d/nwrfcsdk.conf
ldconfig
ldconfig -p | grep sap
export SAPNWRFC_HOME=/usr/sap/nwrfcsdk/
pip install pipenv
pipenv install
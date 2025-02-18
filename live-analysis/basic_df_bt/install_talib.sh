wget https://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz -O ./ta-lib-0.4.0-src.tar.gz
tar zxvf ta-lib-0.4.0-src.tar.gz
cd ta-lib
./configure --prefix=/usr
make
make install

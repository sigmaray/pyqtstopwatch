# Cross platform stopwatch and timer in Python/QT

Time intervals are saved into file on disk, they survive application restart.

Application adds icon into tray. Click on it with middle mouse button to pause stopwatch or timer.

## How to install:
```
python3 -m venv .venv # optional
source .venv/bin/activate # optional

pip install --upgrade pip
pip install -r requirements.txt # in Linux
pip install -r requirements-windows.txt # in Windows
```

## How to run timer
```
python timer.pyw
```
In Windows you can double click timer.pyw

## How to run stopwatch
```
python stopwatch.pyw
```
In Windows you can double click stopwatch.pyw

## Credits
https://www.geeksforgeeks.org/pyqt5-digital-stopwatch/ and https://www.geeksforgeeks.org/timer-application-using-pyqt5/

I used the code from geeksforgeeks, but heavily reworked it and added tray icon.

## Screenshots


![image](https://github.com/sigmaray/pyqtstopwatch/assets/1594701/17440cb7-b439-47e0-b362-1e5f9ae2fe3c)

![image](https://github.com/sigmaray/pyqtstopwatch/assets/1594701/28059e3a-f06c-41c8-b71b-a71f6ca93845)

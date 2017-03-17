# 16x2 LCD with Orange Pi PC Plus (v1.1) GPIO
## Python Module

This is a standalone Python module that you can use to drive a 16x2 LCD display with an Orange Pi PC Plus v1.1 utilizing it's GPIO ports.

This script has been tested on:
- Orange Pi Pc Plus v1.1
- running Armbian Ubuntu Xenial https://www.armbian.com/orange-pi-pc-plus/
- Python3
- duxingkei33's GPIO driver https://github.com/duxingkei33/orangepi_PC_gpio_pyH3

Note: I have tested and this script works with a board running the aforementioned OS, which includes the python3 interpreter by default. You must install duxingkei33's gpio package! If you run into some weird problem during the installation like **pyA20/gpio/gpio.c:25:20: fatal error: Python.h: No such file or directory"** install the python3 dev package: **sudo apt-get install python3-dev** and re-try installing the gpio driver with **sudo python3 setup.py install**

Feel free to modify this script, or import it into your projects. All you have to do is instantiate an LCD object and that's all there is to it! Have fun!

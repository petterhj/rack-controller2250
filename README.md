# rack-controller2250

*2019/06*

A simple system for replacing the "Intelligent EnergySaving function" (fan control) of the [IPC G2250](http://www.chinaipc.cc/images/g2250-datasheet.pdf) 2U Mini-ITX server chassis. Possibly no more "intelligent", but much less annoying. Ambient, CPU and GPU temperature/load displayed on an OLED display, replacing the built-in LCD, not really visible from any angle.

![aio-homeghost](https://github.com/petterhj/rack-controller2250/blob/master/screenshot.png "rack-controllre2250")

## arduino-controller2250

Fan and OLED controller.

## python-controller2250

Windows client for collecting temperature/load data for CPU and GPU (using `OpenHardwareMonitorLib.dll`). Communicates with the Arduino over serial.

```sh
$ cd python-controller2250
$ pipenv install
$ pipenv shell

$ python client.py
```

### Build

```sh
$ pipenv run pyinstaller controller2250.spec
```

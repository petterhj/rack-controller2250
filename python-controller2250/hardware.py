# Imports
import clr # package pythonnet, not clr
import os, sys

from logger import logger
from config import *



SENSOR_TYPES = ['Voltage','Clock','Temperature','Load','Fan','Flow','Control','Level']


# def get_lib(file_name):
#     try:
#         base_path = sys._MEIPASS # PyInstaller creates a temp folder and stores path in _MEIPASS
#     except Exception:
#         base_path = os.path.join(path.dirname(__file__))
#     resource = os.path.join(base_path, 'lib', file_name)
#     print('*'*100)
#     print(resource)
#     print(os.path.isfile(resource))
#     print('*'*100)
#     return resource


# Class: Hardware
class Hardware(object):
    # Init
    def __init__(self):
        # Load assembly
        # print(os.path.join(BASE_DIR, 'lib', 'OpenHardwareMonitorLib.dll'))
        clr.AddReference(os.path.join(BASE_DIR, 'lib', 'OpenHardwareMonitorLib.dll'))
        # clr.AddReference(get_lib('OpenHardwareMonitorLib.dll'))
        # clr.AddReference(os.path.join('lib', 'OpenHardwareMonitorLib.dll'))

        from OpenHardwareMonitor import Hardware

        self.handle = Hardware.Computer()
        # self.handle.MainboardEnabled = True
        self.handle.CPUEnabled = True
        # self.handle.RAMEnabled = True
        self.handle.GPUEnabled = True
        # self.handle.HDDEnabled = True
        self.handle.Open()

    
    # Sensor data
    def sensor_data(self):
        cpu_temp = 0
        cpu_load = 0
        gpu_temp = 0
        gpu_load = 0
        # memory_load = 0
        # storage_load = 0

        for i in self.handle.Hardware:
            # print(i,)
            i.Update()
            
            for sensor in i.Sensors:
                # print(sensor.SensorType, sensor.Name, sensor.Value)
                if sensor.SensorType == 2 and sensor.Name == 'CPU Package':
                    cpu_temp = round(sensor.Value) if sensor.Value else 0
                if sensor.SensorType == 3 and sensor.Name == 'CPU Total':
                    cpu_load = round(sensor.Value) if sensor.Value else 0
                if sensor.SensorType == 2 and sensor.Name == 'GPU Core':
                    gpu_temp = round(sensor.Value) if sensor.Value else 0
                if sensor.SensorType == 3 and sensor.Name == 'GPU Core':
                    gpu_load = round(sensor.Value) if sensor.Value else 0
                # if sensor.SensorType == 3 and sensor.Name == 'Memory':
                #     memory_load = round(sensor.Value)
                # if sensor.SensorType == 3 and sensor.Name == 'Used Space':
                #     storage_load = round(sensor.Value)
        
        # return cpu_temp, cpu_load, memory_load, storage_load
        return cpu_temp, cpu_load, gpu_temp, gpu_load



if __name__ == '__main__':
    import time

    hw = Hardware()

    # while True:
    print(hw.sensor_data())
        # time.sleep(1)


'''
# Imports
import wmi


# WMI
w = wmi.WMI(namespace="root\\OpenHardwareMonitor")

def get_sensor_data():
    sensors = w.Sensor()

    cpu_temp = 0
    cpu_load = 0
    memory_load = 0
    storage_load = 0

    for sensor in sensors:
        if sensor.SensorType == 'Temperature' and sensor.Name == 'CPU Package':
            cpu_temp = round(sensor.Value)
        if sensor.SensorType == 'Load' and sensor.Name == 'CPU Total':
            cpu_load = round(sensor.Value)
        if sensor.SensorType == 'Load' and sensor.Name == 'Memory':
            memory_load = round(sensor.Value)
        if sensor.SensorType == 'Load' and sensor.Name == 'Used Space':
            storage_load = round(sensor.Value)

    return cpu_temp, cpu_load, memory_load, storage_load


if __name__ == '__main__':
    import time

    while True:
        print(get_sensor_data())
        time.sleep(1)
'''


'''
+-------------+-----------------------+--------------------+
| Type        | Name                  | Value              |
+-------------+-----------------------+--------------------+
| Load        | GPU Video Engine      | 0.0                |
| Temperature | CPU Core #2           | 67.0               |
| Power       | CPU Graphics          | 1.8769711256027222 |
| Temperature | CPU Package           | 67.0               |
| Power       | CPU DRAM              | 1.4695665836334229 |
| Temperature | Temperature           | 43.0               |
| Data        | Available Memory      | 2.8275070190429688 |
| Load        | Used Space            | 96.92284393310547  |
| Load        | CPU Core #1           | 30.46875           |
| Load        | CPU Core #2           | 36.71875           |
| Clock       | CPU Core #1           | 3092.845458984375  |
| Clock       | Bus Speed             | 99.76920318603516  |
| Clock       | CPU Core #2           | 3092.845458984375  |
| SmallData   | GPU Memory Free       | 2020.875           |
| Load        | CPU Total             | 33.59375           |
| Temperature | CPU Core #1           | 67.0               |
| SmallData   | GPU Memory Total      | 2048.0             |
| Clock       | GPU Shader            | 810.0000610351562  |
| Load        | GPU Memory            | 1.324462890625     |
| Load        | GPU Memory Controller | 0.0                |
| Clock       | GPU Core              | 405.0000305175781  |
| Load        | GPU Core              | 0.0                |
| Clock       | GPU Memory            | 405.0000305175781  |
| SmallData   | GPU Memory Used       | 27.125             |
| Data        | Used Memory           | 5.058330535888672  |
| Power       | CPU Package           | 12.19682788848877  |
| Load        | Memory                | 64.14449310302734  |
| Power       | CPU Cores             | 6.4669365882873535 |
+-------------+-----------------------+--------------------+
'''

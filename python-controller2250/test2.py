import clr #package pythonnet, not clr
import os
import time

openhardwaremonitor_hwtypes = ['Mainboard','SuperIO','CPU','RAM','GpuNvidia','GpuAti','TBalancer','Heatmaster','HDD']
cputhermometer_hwtypes = ['Mainboard','SuperIO','CPU','GpuNvidia','GpuAti','TBalancer','Heatmaster','HDD']
openhardwaremonitor_sensortypes = ['Voltage','Clock','Temperature','Load','Fan','Flow','Control','Level','Factor','Power','Data','SmallData']
cputhermometer_sensortypes = ['Voltage','Clock','Temperature','Load','Fan','Flow','Control','Level']


def initialize_openhardwaremonitor():
    file = 'OpenHardwareMonitorLib.dll'
    clr.AddReference(file)

    from OpenHardwareMonitor import Hardware

    handle = Hardware.Computer()
    handle.MainboardEnabled = True
    handle.CPUEnabled = True
    handle.RAMEnabled = True
    handle.GPUEnabled = True
    handle.HDDEnabled = True
    handle.Open()
    return handle

def initialize_cputhermometer():
    file = 'CPUThermometerLib.dll'
    clr.AddReference(file)

    from CPUThermometer import Hardware
    handle = Hardware.Computer()
    handle.CPUEnabled = True
    handle.Open()
    return handle

def fetch_stats(handle):
    for i in handle.Hardware:
        i.Update()
        for sensor in i.Sensors:
            # parse_sensor(sensor)
            sensorytypes = openhardwaremonitor_sensortypes
            stype = sensorytypes[int(sensor.SensorType)]
            
            if stype in ['Temperature', 'Load'] and sensor.Name in ['CPU Total', 'CPU Package']:
                print(u"Sensor #%i %s - %s %s" % (
                    # sensor.Hardware.HardwareType, 
                    # sensor.Hardware.Name, 
                    sensor.Index, 
                    sensor.Name, 
                    sensor.Value,
                    stype
                ))


if __name__ == "__main__":
    print("OpenHardwareMonitor:")
    HardwareHandle = initialize_openhardwaremonitor()
    print("OpenHardwareMonitor STATS:")
    while True:
        fetch_stats(HardwareHandle)
        print('-'*10)
        time.sleep(1)
    # print("\nCPUMonitor:")
    # CPUHandle = initialize_cputhermometer()
    # fetch_stats(CPUHandle)
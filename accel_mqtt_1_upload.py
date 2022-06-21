import network,time
from umqtt.simple import MQTTClient #导入MQTT板块
from machine import I2C,Pin,Timer

import time
from lsm6dsox import LSM6DSOX

from machine import Pin, I2C
lsm = LSM6DSOX(I2C(0, scl=Pin(13), sda=Pin(12)))

step1 = 0
accel_sample10=0

def WIFI_Connect():
    wlan = network.WLAN(network.STA_IF) #STA模式
    wlan.active(True)                   #激活接口
    start_time=time.time()              #记录时间做超时判断

    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect('wifi 이름', 'wifi 패스워드') #输入WIFI账号密码
        
    if wlan.isconnected():
        print('network information:', wlan.ifconfig())
        return True    

def MQTT_Send(tim):
    global step1
    global accel_sample10
    accel_x=100*(lsm.read_accel())[0]
    accel_y=100*(lsm.read_accel())[1]
    accel_z=100*(lsm.read_accel())[2]
    accel_sample10+=((accel_x**2)+(accel_y)**2+(accel_z)**2)**(0.5)
    time.sleep_ms(100)
    step1 = step1 +1
    if (step1%10)==0:
        print("10번 샘플링한 가속도값은 ",(accel_sample10/10),"\n")
        client.publish(TOPIC,str(accel_sample10/10))
        accel_sample10=0

if WIFI_Connect():
    SERVER = '192.168.0.8'   # my rapa ip address , mqtt broker가 실행되고 있음
    PORT = 1883
    CLIENT_ID = 'sungho-Kim' # clinet id 이름
    TOPIC = 'rp2040' # TOPIC 이름
    client = MQTTClient(CLIENT_ID, SERVER, PORT,keepalive=60)
    client.connect()

    #开启RTOS定时器，编号为-1,周期1000ms，执行socket通信接收任务
    tim = Timer(-1)
    tim.init(period=1000, mode=Timer.PERIODIC,callback=MQTT_Send)


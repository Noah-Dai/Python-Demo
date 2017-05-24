#!/usr/bin/env python  
# coding: utf-8 
import RPi.GPIO as GPIO  
import time  
import signal  
import atexit  
import socket
import sys

atexit.register(GPIO.cleanup)    

servopin =21
GPIO.setmode(GPIO.BOARD)  
GPIO.setup(servopin, GPIO.OUT, initial=False)  
pwm = GPIO.PWM(servopin,100) #100HZ 
GPIO.setwarnings(False) 
pwm.start(0)  
time.sleep(2) 
speed = 0
prv_temp = 0

try:
    while True:
        tmpFile = open( '/sys/class/thermal/thermal_zone0/temp' )
        cpu_temp = float(tmpFile.read())
    # 打开文件  
    #file = open("/sys/class/thermal/thermal_zone0/temp")  
    # 读取结果，并转换为浮点数  
    #temp = float(file.read()) / 1000 
        tmpFile.close()
        if cpu_temp>=42000:
            if prv_temp<42000 :
        #启动时防止风扇卡死先全功率转0.1秒
                pwm.start(0)
                pwm.ChangeDutyCycle(100)
                time.sleep(0.1)
            speed = min( cpu_temp/125-257 , 100 )
            pwm.ChangeDutyCycle(speed)
        #if cpu_temp>=46000:
           # speed = min( cpu_temp/125-257 , 100 )
           # pwm.ChangeDutyCycle(speed)
            
        else :
            pwm.stop()
        prv_temp = cpu_temp
        time.sleep(5)
except KeyboardInterrupt:
    pass
pwm.stop()

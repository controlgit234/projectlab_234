import random
import time
import paho.mqtt.client as mqtt_client

#tts packages
import speech_recognition as sr 
from gtts import gTTS 
import os 
import time 
import playsound 
import pygame

pygame.mixer.init()

broker_address = "localhost"
broker_port = 1883

#topic = "/python/mqtt"
topic = "rp2040"

pre_move_status=0;
now_move_status=0;
move_change=0;

def speak_save(text):
    tts = gTTS(lang='en', text=text ) #ko')
    filename="/home/pi/Desktop/vsc_workspace/projectlab_last_work/voice.mp3"#음성파일 경로
    tts.save(filename) 
    #playsound.playsound(filename) 

def speaker_out():
    pygame.mixer.music.load("/home/pi/Desktop/vsc_workspace/projectlab_last_work/voice.mp3")#음성파일 경로
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True:
        continue


def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker")
        else:
            print(f"Failed to connect, Returned code: {rc}")

    def on_disconnect(client, userdata, flags, rc=0):
        print(f"disconnected result code {str(rc)}")

    def on_log(client, userdata, level, buf):
        print(f"log: {buf}")

    # client 생성
    client_id = f"mqtt_client_{random.randint(0, 1000)}"
    client = mqtt_client.Client(client_id)

    # 콜백 함수 설정
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_log = on_log

    # broker 연결
    client.connect(host=broker_address, port=broker_port)
    return client


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        float_accel_value=float(msg.payload.decode())
        int_accel_value=int(float_accel_value)
        global pre_move_status
        global now_move_status
        global move_change
            
        if int_accel_value<102:
                now_move_status=0
        elif int_accel_value<120:
                now_move_status=1
        elif int_accel_value>120:
                now_move_status=2
            
        if now_move_status!=pre_move_status:
                move_change=1
                pre_move_status=now_move_status
                
        if move_change==1:
            if now_move_status==0:
                    speak_save("Your condition has changed, You are standing now.")
                    speaker_out()
            elif now_move_status==1:
                    speak_save("Your condition has changed, You are walking now.")
                    speaker_out()
            elif now_move_status==2:
                    speak_save("Your condition has changed, You are running now.")
                    speaker_out()
            move_change=0

    client.subscribe(topic) #1
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    run()
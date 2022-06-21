# 작품소개
  사용자의 운동상태를 standing,walking,runing 3가지로 식별한 다음 사용자의 운동상태가 이전과 달라지면 음성으로 알려주는 기능 

# 작품의 동작원리
  nano RP2040의 가속도 센서를 사용하여 가속도값을 10번 샘플링한 다음 평균값을 nano의 IOT기능을 이용하여 라즈베리파이4와
  연결한후 mqtt subsceriber로 정보를 보낸다. 받은 가속도 정보를 통해 사용자의 상태를 standing,walking,runing 로 구분한 다음
  이전의 상태와 비교하여 상태가 변화했다면 gtts를 통해 알려준다

# 작품 블럭도
  ![작품블럭도](https://github.com/controlgit234/projectlab_234/blob/main/%EC%9E%91%ED%92%88%20%EB%B8%94%EB%9F%AD%EB%8F%84.PNG)
  
# 작품 코드및 결과이미지
  ## Nano RP2040 가속도 값 코드
  ---
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
            wlan.connect('wi-fi 이름', 'wi-fi 비밀번호') #输入WIFI账号密码
        
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
            accel_sample10=0import network,time
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
            wlan.connect('wi-fi 이름', 'wi-fi 비밀번호') #输入WIFI账号密码
        
        if wlan.isconnected():
            print('network information:', 

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
        
## 라즈베리파이4 gtts 코드
---
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


## 결과이미지
---
  ![nano 가속도센서](https://github.com/controlgit234/projectlab_234/blob/main/%EA%B0%80%EC%86%8D%EB%8F%84%EC%84%BC%EC%84%9C%20%ED%8F%89%EA%B7%A0%EA%B0%92%20%EA%B2%B0%EA%B3%BC%EC%9D%B4%EB%AF%B8%EC%A7%80.PNG)
  
  Nano RP2040에서 가속도값 샘플링후 평균값 계산후 라즈베리파이4에 전송한 결과 이미지
  
  ![sub 수신정보](https://github.com/controlgit234/projectlab_234/blob/main/sub%20%EC%97%90%EC%84%9C%20%EB%B0%9B%EC%9D%80%20%EA%B0%80%EC%86%8D%EB%8F%84%EC%A0%95%EB%B3%B4.PNG)
  
  sub에서 받은 가속도 정보 이미지
  
  ![라즈베리파이4 gtts](https://github.com/controlgit234/projectlab_234/blob/main/%EA%B0%80%EC%86%8D%EB%8F%84_gtts_%EC%86%8C%EC%8A%A4%EC%BD%94%EB%93%9C.PNG)
  
  라즈베리파이4에서 gtts 실행코드
  
# 작품 실행동영상
[![작품 실행동영상](https://youtu.be/WObF141nLoM/0.jpg)](https://youtu.be/WObF141nLoM)

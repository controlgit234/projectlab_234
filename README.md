# 작품소개
  사용자의 운동상태를 standing,walking,runing 3가지로 식별한 다음 사용자의 운동상태가 이전과 달라지면 음성으로 알려주는 기능 

# 작품의 동작원리
  nano RP2040의 가속도 센서를 사용하여 가속도값을 10번 샘플링한 다음 평균값을 nano의 IOT기능을 이용하여 라즈베리파이4와
  연결한후 mqtt subsceriber로 정보를 보낸다. 받은 가속도 정보를 통해 사용자의 상태를 standing,walking,runing 로 구분한 다음
  이전의 상태와 비교하여 상태가 변화했다면 gtts를 통해 알려준다

# 작품 블럭도
  ![작품블럭도](https://github.com/controlgit234/projectlab_234/blob/main/%EC%9E%91%ED%92%88%20%EB%B8%94%EB%9F%AD%EB%8F%84.PNG)
  
# 작품 코드및 결과이미지
  ![nano 가속도센서](https://github.com/controlgit234/projectlab_234/blob/main/%EA%B0%80%EC%86%8D%EB%8F%84%EC%84%BC%EC%84%9C%20%ED%8F%89%EA%B7%A0%EA%B0%92%20%EA%B2%B0%EA%B3%BC%EC%9D%B4%EB%AF%B8%EC%A7%80.PNG)
  
  Nano RP2040에서 가속도값 샘플링후 평균값 계산후 라즈베리파이4에 전송한 결과 이미지
  
  ![sub 수신정보](https://github.com/controlgit234/projectlab_234/blob/main/sub%20%EC%97%90%EC%84%9C%20%EB%B0%9B%EC%9D%80%20%EA%B0%80%EC%86%8D%EB%8F%84%EC%A0%95%EB%B3%B4.PNG)
  
  sub에서 받은 가속도 정보 이미지
  
  ![라즈베리파이4 gtts](https://github.com/controlgit234/projectlab_234/blob/main/%EA%B0%80%EC%86%8D%EB%8F%84_gtts_%EC%86%8C%EC%8A%A4%EC%BD%94%EB%93%9C.PNG)
  
  라즈베리파이4에서 gtts 실행코드
  
# 작품 실행동영상
[![작품 실행동영상](https://studio.youtube.com/video/WObF141nLoM/edit/0.jpg)](https://studio.youtube.com/video/WObF141nLoM/edit)

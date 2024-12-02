import cv2
import threading
import socket
import time
from ultralytics import YOLO

# YOLOv8 모델 로드
model = YOLO('runs/detect/train3/weights/best3.pt')

# 라즈베리파이4 스트리밍 URL 설정
stream_url = 'http://192.168.168.146:8000/stream.mjpg'
# 비디오 스트림 열기
cap = cv2.VideoCapture(stream_url)
if not cap.isOpened():
    print("오류: 비디오 스트림을 열 수 없습니다.")
    exit()

frame = None  # 전역 변수로 초기화
processed_frame = None  # 처리된 프레임을 저장할 변수
lock = threading.Lock()  # 스레드 간 동기화를 위한 락
# 서보 모터 신호 전송을 위한 소켓 설정
host = '192.168.168.146'  # 라즈베리파이의 IP 주소
port = 8001  # 서보 모터 제어를 위한 포트 번호

# 소켓 생성 (한 번만)
CS = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 마지막 신호 전송 시간 초기화
last_sent_time = 0
send_interval = 3  # 3초
# YOLOv8 객체 인식을 실행하는 함수 (별도 스레드에서 실행)
def detect_objects():
    global frame, processed_frame, last_sent_time
    while True:
        with lock:
            if frame is None:
                continue
            frame_copy = frame.copy()

        results = model(frame_copy)

        for result in results:
            for box in result.boxes:
                conf = box.conf[0]
                class_id = box.cls[0].item()
                class_name = model.names[class_id]
                
                # FL 객체를 감지한 경우
                if class_name == "FL" and conf >= 0.3:
                    current_time = time.time()  # 현재 시간
                    # 3초 이내에 메시지를 보냈는지 확인
                    if current_time - last_sent_time >= send_interval:
                        # 서보 모터에 신호 보내기
                        try:
                            message = 'FL_detected'
                            CS.sendto(message.encode(), (host, port))  # sendto 사용
                            print("Message sent successfully")
                            last_sent_time = current_time  # 마지막 신호 보낸 시간 업데이트
                        except Exception as e:
                            print(f"Error sending data: {e}")
                        

                    # 바운딩 박스 및 라벨 그리기
                    x1, y1, x2, y2 = box.xyxy[0]
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                    cv2.rectangle(frame_copy, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    label = f'{class_name}: {conf:.2f}'
                    cv2.putText(frame_copy, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        with lock:
            processed_frame = frame_copy

def read_frames():
    global frame, processed_frame
    while True:
        ret, new_frame = cap.read()
        if not ret:
            print("프레임을 가져오지 못했습니다.")
            break

        with lock:
            frame = new_frame

        if processed_frame is not None:
            cv2.imshow("YOLOv8 Detection", processed_frame)
        else:
            cv2.imshow("YOLOv8 Detection", new_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# 객체 인식 스레드 시작
detection_thread = threading.Thread(target=detect_objects)
detection_thread.daemon = True
detection_thread.start()

# 비디오 프레임을 읽고 화면에 표시하는 함수 실행
read_frames()

# 비디오 캡처 객체 해제 및 OpenCV 창 닫기
cap.release()
CS.close()  # 소켓 닫기
cv2.destroyAllWindows()
from ultralytics import YOLO
import cv2

# 사용자 정의 모델 best.pt 불러오기
model = YOLO("./runs/detect/train/weights/best.pt")  # 학습된 모델 가중치 파일

# 이미지 예측 및 결과 저장
result = model.predict("./불10.mp4", save=True, conf=0.5)

# 결과 시각화
plots = result[0].plot()
cv2.imshow("plot", plots)
cv2.waitKey(0)
cv2.destroyAllWindows()
from ultralytics import YOLO

if __name__ == '__main__':
    # YOLOv8 모델 불러오기
    model = YOLO('D:/test/runs/detect/train/weights/best.pt')

    # 모델 학습 (기존 모델을 사용하여 새로 학습 시작)
    model.train(
        data='data.yaml',  # 데이터셋 경로
        epochs=10,        # 추가 학습 에포크 수
        imgsz=640,         # 이미지 크기
        workers=6,         # 데이터 로더 워커 수
        lr0=0.01,         # 최초 학습률
        lrf=0.1,           # 최종 학습률
        model='D:/test/runs/detect/train/weights/best.pt',  # 기존 가중치 사용
        batch=32
    )

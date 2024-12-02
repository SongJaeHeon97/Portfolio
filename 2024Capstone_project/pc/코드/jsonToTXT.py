import json
import os

# JSON 파일 경로 및 TXT 파일 저장 경로 설정
json_dir = 'D:/test/dataset/train/labels/'  # JSON 파일이 있는 폴더
txt_output_dir = 'D:/test/dataset/train/labels_txt/'  # 변환된 TXT 파일을 저장할 폴더

os.makedirs(txt_output_dir, exist_ok=True)

# JSON 파일 순회
for json_file in os.listdir(json_dir):
    if json_file.endswith('.json'):
        with open(os.path.join(json_dir, json_file), 'r', encoding='utf-8') as f:
            data = json.load(f)

        # 이미지 크기 가져오기
        image_width = data['image']['width']
        image_height = data['image']['height']

        # category_index를 0부터 시작하는 class_id로 변환
        category_map = {cat['category_index']: cat['category_index'] - 1 for cat in data['categories']}

        # TXT 파일 이름 설정
        txt_file_name = os.path.splitext(json_file)[0] + '.txt'
        with open(os.path.join(txt_output_dir, txt_file_name), 'w', encoding='utf-8') as f:
            # 어노테이션이 없는 경우 빈 파일로 처리
            if not data['annotations']:
                print(f"No annotations found for {json_file}. Creating an empty label file.")
                continue  # 빈 파일 생성 후 다음 파일로 넘어감

            # 어노테이션이 있는 경우 처리
            for annotation in data['annotations']:
                # 클래스 ID 가져오기
                categories_id = annotation['categories_id']
                if categories_id not in category_map:
                    print(f"Warning: categories_id {categories_id} not found in categories for file {json_file}")
                    continue  # 해당 항목 건너뛰기

                class_id = category_map[categories_id]

                # 바운딩 박스 좌표 가져오기 (xmin, ymin, width, height)
                x_min, y_min, bbox_width, bbox_height = annotation['bbox']

                # 바운딩 박스 좌표 검증
                if bbox_width <= 0 or bbox_height <= 0:
                    print(f"Warning: Negative or zero dimension for bbox in file {json_file}")
                    continue  # 잘못된 바운딩 박스 건너뛰기

                # YOLO 형식으로 변환
                x_center = (x_min + (bbox_width / 2)) / image_width
                y_center = (y_min + (bbox_height / 2)) / image_height
                width = bbox_width / image_width
                height = bbox_height / image_height

                # 변환된 데이터를 YOLO 형식으로 파일에 쓰기
                f.write(f'{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n')

print("JSON to YOLO format conversion completed.")

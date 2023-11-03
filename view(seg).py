import cv2
import os
import numpy as np

# 세그멘테이션 데이터와 이미지 경로
seg_path = 'C:/Users/DELL/Desktop/kimjung/wildanimal/train/seg/'
img_path = 'C:/Users/DELL/Desktop/kimjung/wildanimal/train/images/'

# 세그멘테이션 파일을 이미지 파일 이름으로 매핑하기
segmentation_files = [f for f in os.listdir(seg_path) if f.endswith('.txt')]

for seg_file in segmentation_files:
    # 세그멘테이션 데이터 읽기
    with open(os.path.join(seg_path, seg_file), 'r') as file:
        lines = file.readlines()

    # 이미지 파일 이름을 txt 파일 이름에서 추출
    img_filename = seg_file.replace('.txt', '.jpg')  # 확장자가 다를 경우에는 여기를 수정합니다.
    img_full_path = os.path.join(img_path, img_filename)

    # 이미지가 존재하는지 확인하고 읽기
    if not os.path.exists(img_full_path):
        print(f"Image {img_filename} does not exist at path {img_full_path}.")
        continue

    img = cv2.imread(img_full_path)
    print(img_full_path)
    if img is None:
        print(f"Failed to load image {img_filename}.")
        continue

    # 세그멘테이션 데이터를 이용해 폴리곤 그리기
    for line in lines:
        segments = line.strip().split()
        points = np.array([[float(segments[i]), float(segments[i+1])] for i in range(1, len(segments), 2)])
        points = (points * np.array([img.shape[1], img.shape[0]])).astype(np.int32)
        cv2.polylines(img, [points], isClosed=True, color=(0, 255, 0), thickness=2)

    # 이미지 보여주기
    cv2.imshow('Image with segmentation', img)
    cv2.waitKey(0)  # 어떤 키를 누를 때까지 이미지 창을 열어둠

cv2.destroyAllWindows()

import json
import os

def calculate_bbox_from_segmentation(segment):
    if not segment or len(segment) < 1:
        return None
    
    xs = segment[0::2]
    ys = segment[1::2]

    return [[min(xs), min(ys)], [max(xs), max(ys)]]

def convert_to_yolo_format(bbox, img_width, img_height):
    x_start, y_start = bbox[0]
    x_end, y_end = bbox[1]
    
    width = x_end - x_start
    height = y_end - y_start

    x_center = x_start + (width / 2)
    y_center = y_start + (height / 2)
    
    x_center /= img_width
    y_center /= img_height
    width /= img_width
    height /= img_height
    
    class_index = 0
    return f"{class_index} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}"

base_path = '야생동물데이터(한국폴리텍대학강의)/train/labels/'

files = os.listdir(base_path)

for file in files:
    if file.endswith('.json'):
        with open(base_path + file, 'r', encoding='UTF8') as f:
            json_data = json.load(f)
        
        img_width = json_data["images"][0]["width"]
        img_height = json_data["images"][0]["height"]
        
        yolo_data = []
        for ann in json_data["annotations"]:
            if ann["bbox"] is not None:
                bbox = ann["bbox"]
            elif ann["segmentation"] and len(ann["segmentation"]) > 0:
                bbox = calculate_bbox_from_segmentation(ann["segmentation"][0])
            else:
                continue
            
            yolo_data.append(convert_to_yolo_format(bbox, img_width, img_height))
        
        with open(base_path + file.replace('.json', '.txt'), 'w', encoding='UTF8') as f:
            for line in yolo_data:
                f.write(line + "\n")

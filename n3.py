import cv2
import tensorflow as tf
import numpy as np

# بارگذاری مدل پیش‌آموزش دیده SSD
model = tf.saved_model.load('ssd_mobilenet_v2_fpnlite_320x320/saved_model')

# بارگذاری ویدیو
cap = cv2.VideoCapture('video_2024-10-26_21-41-50.mp4')

# تابع برای پردازش هر فریم ویدیو
def process_frame(frame):
    input_tensor = tf.convert_to_tensor(frame)
    input_tensor = input_tensor[tf.newaxis, ...]

    detections = model(input_tensor)

    # استخراج اطلاعات تشخیص
    num_detections = int(detections.pop('num_detections'))
    detections = {key: value[0, :num_detections].numpy() for key, value in detections.items()}
    detection_classes = detections['detection_classes'].astype(np.int64)
    detection_boxes = detections['detection_boxes']
    detection_scores = detections['detection_scores']

    return detection_boxes, detection_classes, detection_scores

# پردازش ویدیو
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # پردازش فریم
    boxes, classes, scores = process_frame(frame)

    # شمارش اشیاء با نمره اعتماد بالاتر از 0.5
    count = sum(score > 0.5 for score in scores)
    print(f'Number of objects detected: {count}')

    # نمایش فریم
    for box in boxes:
        ymin, xmin, ymax, xmax = box
        (startX, startY, endX, endY) = (int(xmin * frame.shape[1]), int(ymin * frame.shape[0]),
                                        int(xmax * frame.shape[1]), int(ymax * frame.shape[0]))
        cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 0), 2)

    cv2.imshow('Frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

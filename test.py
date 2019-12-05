'''
摄像机角度偏移告警
'''
from datetime import time, datetime

import cv2
import do_match
import numpy as np
from PIL import Image, ImageDraw, ImageFont

'''
告警信息
'''


cap = cv2.VideoCapture(0)

if (cap.isOpened() == False):
    print("Error opening video stream or file")

first_frame = True
pre_frame = 0

index = 0

while (cap.isOpened()):
    ret, frame = cap.read()
    cv2.imshow("1",frame)
    if ret == True:
        if first_frame:
            pre_frame = frame
            first_frame = False
            continue

        index += 1
        if index % 24 == 0:
            time1 = datetime.utcnow().microsecond
            result = do_match.match2frames(pre_frame, frame)
            time2 = datetime.now().microsecond
            print(str(time2 - time2))
            print("检测结果===>", texts[result])

            #if result > 1:  # 缓存最近无偏移的帧
                #pre_frame = frame
            if result == 0:
                pre_frame = frame
            size = frame.shape

            if size[1] > 720:  # 缩小显示
                frame = cv2.resize(frame, (int(size[1] * 0.5), int(size[0] * 0.5)), cv2.INTER_LINEAR)

            text_frame = putText(frame, texts[result])

            cv2.imshow('Frame', text_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

cap.release()
cv2.destroyAllWindows()

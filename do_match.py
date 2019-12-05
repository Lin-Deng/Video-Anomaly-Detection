'''
视频帧匹配脚本
'''
import numpy as np
import cv2
from PIL import Image,ImageDraw,ImageFont

# 至少10个点匹配
MIN_MATCH_COUNT = 10
# 完全匹配偏移 d<4
BEST_DISTANCE = 1
# 微量偏移  4<d<10
GOOD_DISTANCE = 10

# 特征点提取方法，内置很多种
algorithms_all = {
    "SIFT": cv2.xfeatures2d.SIFT_create(),
    "SURF": cv2.xfeatures2d.SURF_create(),
    "ORB": cv2.ORB_create()
}
#在图片上添加文字
def putText(frame, text):
    cv2_im = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    pil_im = Image.fromarray(cv2_im)

    draw = ImageDraw.Draw(pil_im)
    font = ImageFont.truetype("C:/Windows/Fonts/simsun.ttc", 30, encoding="utf-8")
    draw.text((50, 50), text,(0, 255, 255),font=font)

    cv2_text_im = cv2.cvtColor(np.array(pil_im), cv2.COLOR_RGB2BGR)

    return cv2_text_im



'''
# 图像匹配
# 0完全不匹配 1场景匹配 2角度轻微偏移 3完全匹配
'''
def match2frames(image1, image2):
    img1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    img2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

    size1 = img1.shape
    size2 = img2.shape

    img1 = cv2.resize(img1, (int(size1[1] * 0.3), int(size1[0] * 0.3)), cv2.INTER_LINEAR)
    img2 = cv2.resize(img2, (int(size2[1] * 0.3), int(size2[0] * 0.3)), cv2.INTER_LINEAR)

    surf = algorithms_all["SIFT"]

    kp1, des1 = surf.detectAndCompute(img1, None)
    kp2, des2 = surf.detectAndCompute(img2, None)

    bf = cv2.BFMatcher()

    matches = bf.knnMatch(des1, des2, k=2)
    # 过滤
    good = []
    for m, n in matches:
        if m.distance < 0.69 * n.distance:
            good.append(m)
    src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
    dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
    M, mask = cv2.findHomography(src_pts, dst_pts,cv2.RANSAC,5.0)
    matchesMask = mask.ravel().tolist()
    good = [good[matchesMask.index(i)] for i in matchesMask if i == 1]
    img3 = cv2.drawMatches(img1, kp1, img2, kp2, good, None)
    good = sorted(good,key=lambda x:x.distance)
    if len(good) < MIN_MATCH_COUNT:
        return img3,0  # 完全不匹配
    else:
        good = good[0:MIN_MATCH_COUNT]
        distance_sum = 0  # 特征点2d物理坐标偏移总和
        for m in good:
            distance_sum += get_distance(kp1[m.queryIdx].pt, kp2[m.trainIdx].pt)
        distance = distance_sum / len(good)  # 单个特征点2D物理位置平均偏移量

        if distance < BEST_DISTANCE:
            return img3,3  # 完全匹配
        elif distance < GOOD_DISTANCE and distance >= BEST_DISTANCE:
            return img3,2  # 部分偏移
        else:
            return img3,1  # 场景匹配

'''
计算2D物理距离
'''


def get_distance(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

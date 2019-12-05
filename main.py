#utf-8
import do_match
import os
from os import path
from datetime import datetime
import cv2
from sys import argv


texts = ["视频遮挡或严重偏移", "严重偏移", "轻微偏移", "无偏移"]

"""
漏判结果保存
"""
def save_fn_result(target, result):
    if len(result) == 0:
        return
    if not path.exists('FNTestResult') :
        os.mkdir('FNTestResult')
    t = str(datetime.now().strftime('%Y-%m-%d %H_%M_%S.%f'))
    pt = os.path.join('FNTestResult', t)
    if path.exists(pt) == False:
        os.mkdir(pt)
    cv2.imwrite(os.path.join(pt,'target.jpg'), target,[int(cv2.IMWRITE_JPEG_QUALITY), 100])
    rpt = os.path.join(pt,'result')
    os.mkdir(rpt)
    for r in 0, len(result) - 1:
        cv2.imwrite(os.path.join(rpt,'%rresult.jpg'%r),result[r][0], [int(cv2.IMWRITE_JPEG_QUALITY), 100])
        cv2.imwrite(os.path.join(rpt,'%rfeatures.jpg'%r),result[r][1], [int(cv2.IMWRITE_JPEG_QUALITY), 100])

"""
误判结果保存
"""
def save_fp_result(target, result):
    if len(result) == 0:
        return
    if not path.exists('FPTestResult'):
        os.mkdir('FPTestResult')
    t = str(datetime.now().strftime('%Y-%m-%d %H_%M_%S.%f'))
    pt = os.path.join('FPTestResult', t)
    if path.exists(pt) == False:
        os.mkdir(pt)
    cv2.imwrite(os.path.join(pt,'target.jpg'), target,[int(cv2.IMWRITE_JPEG_QUALITY), 100])
    rpt = os.path.join(pt,'result')
    os.mkdir(rpt)
    for r in 0, len(result) - 1:
        cv2.imwrite(os.path.join(rpt,'%rresult.jpg'%r),result[r][0], [int(cv2.IMWRITE_JPEG_QUALITY), 100])
        cv2.imwrite(os.path.join(rpt,'%rfeatures.jpg'%r),result[r][1], [int(cv2.IMWRITE_JPEG_QUALITY), 100])

"""
漏判测试
"""
def FN_test(arg, target, source):
    if arg == '-s':
        target = cv2.imread(target)
        source = cv2.imread(source)
        ar = []
        if source is None:
            print("输入的图片路径有误或者无此路径")
            return
        else:
            features, result = do_match.match2frames(target, source)
            print(texts[result])
            if result == 3:
                ar.append([do_match.putText(source, texts[result]),features])
                save_fn_result(target, ar)
    elif arg == '-b':
        ar = []
        target = cv2.imread(target)
        rootdir = source
        for img in os.listdir(rootdir):
            imgpath = os.path.join(rootdir, img)
            if img.startswith('.'):
                continue
            if not os.path.isfile(imgpath) or not os.path.exists(imgpath):
                continue
            source = cv2.imread(imgpath)
            if source is None:
                print("输入的图片路径有误或者无此路径")
                continue
            else:
                features, result = do_match.match2frames(target, source)
                print(texts[result])
                if result == 3:
                    ar.append([do_match.putText(source, texts[result]),features])
        save_fn_result(target, ar)
    else:
        print("参数有误")

"""
全漏判测试
"""
def all_FN_test(source):
    rootdir = source
    for img in os.listdir(rootdir):
        imgpath = os.path.join(rootdir, img)
        if img.startswith('.'):
            continue
        if not os.path.isfile(imgpath) or not os.path.exists(imgpath):
            continue
        target = cv2.imread(imgpath)
        if target is None:
            print("输入的图片路径有误或者无此路径")
            continue
        ar = []
        for img2 in os.listdir(rootdir):
            imgpath2 = os.path.join(rootdir, img2)
            if img2.startswith('.'):
                continue
            if not os.path.isfile(imgpath2) or not os.path.exists(imgpath2) or imgpath == imgpath2:
                continue
            sample = cv2.imread(imgpath2)
            if sample is None:
                print("输入的图片路径有误或者无此路径")
                continue
            else:
                features, result = do_match.match2frames(target, sample)
                print(texts[result])
                if result == 3:
                    ar.append([do_match.putText(sample, texts[result]),features])
        save_fp_result(target, ar)

"""
误判测试
"""
def FP_test(arg, target, source):
    if arg == '-s':
        target = cv2.imread(target)
        source = cv2.imread(source)
        ar = []
        if source is None:
            print("输入的图片路径有误或者无此路径")
            return
        else:
            features, result = do_match.match2frames(target, source)
            print(texts[result])
            if result != 3:
                ar.append([do_match.putText(source, texts[result]),features])
                save_fp_result(target, ar)
    elif arg == '-b':
        ar = []
        target = cv2.imread(target)
        rootdir = source
        for img in os.listdir(rootdir):
            imgpath = os.path.join(rootdir, img)
            if img.startswith('.'):
                continue
            if not os.path.isfile(imgpath) or not os.path.exists(imgpath):
                continue
            source = cv2.imread(imgpath)
            if source is None:
                print("输入的图片路径有误或者无此路径")
                continue
            else:
                features, result = do_match.match2frames(target, source)
                print(texts[result])
                if result != 3:
                    ar.append([do_match.putText(source, texts[result]),features])
        save_fp_result(target, ar)
    else:
        print("参数有误")

def main(cmd):
    args = cmd
    if len(args) == 1:
        print("-help查看帮助")
    elif len(args) == 2:
        if args[1] == "-help":
            print("FNTest: 漏判测试，输入摄像机偏转的图片，如果判断为未偏转，则将图片和特征图像保存在FNTestResult文件夹中")
            print("FPTest: 误判测试，输入摄像机未偏转的图片，如果判断为偏转，则将图片和特征图像保存在FPTestResult文件夹中")
        elif args[1] == "FNTest":
            print("-a [图片资源路径] 路径下的图片相互对比，文件不能以'.'开头，路径不能包含中文")
            print("-s [模板图片路径] [样本图片路径] 1:1 图片对比，文件不能以'.'开头，路径不能包含中文")
            print("-b [模板图片路径] [样本图片目录] 1:N 图片对比，文件不能以'.'开头，路径不能包含中文")
        elif args[1] == "FPTest":
            print("-s [模板图片路径] [样本图片路径] 1:1 图片对比，文件不能以'.'开头，路径不能包含中文")
            print("-b [模板图片路径] [样本图片目录] 1:N 图片对比，文件不能以'.'开头，路径不能包含中文")
        else:
            print("参数错误，-help参看帮助")
    else:
        if args[1] == "FNTest":
            if len(args) == 3 and args[2] == '-help':
                print("-a [图片资源路径] 路径下的图片相互对比，文件不能以'.'开头，路径不能包含中文")
                print("-s [模板图片路径] [样本图片路径] 1:1 图片对比，文件不能以'.'开头，路径不能包含中文")
                print("-b [模板图片路径] [样本图片目录] 1:N 图片对比，文件不能以'.'开头，路径不能包含中文")
            elif len(args) == 4 and args[2] == '-a':
                all_FN_test(args[3])
            elif len(args) == 5:
                FN_test(args[2], args[3], args[4])
            else:
                print("参数错误，-help查看帮助")
        elif args[1] == "FPTest":
            if len(args) == 3 and args[2] == '-help':
                print("-a [模板资源路径] [样本资源路径] 模板中的每一张图片与样本中每一个文件夹中的图片对比，文件不能以'.'开头，路径不能包含中文")
                print("-s [模板图片路径] [样本图片路径] 1:1 图片对比，文件不能以'.'开头，路径不能包含中文")
                print("-b [模板图片路径] [样本图片目录] 1:N 图片对比，文件不能以'.'开头，路径不能包含中文")
            # elif len(args) == 4 and args[2] == '-a':
            #     all_FP_test(args[3])
            elif len(args) == 5:
                FP_test(args[2], args[3], args[4])
            else:
                print("参数错误，-help查看帮助")
        else:
             print("参数错误，-help查看帮助")
main(argv)









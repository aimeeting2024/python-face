#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
人脸识别诊断工具
检查两张图片检测到的人脸，并可视化结果
"""

import sys
import os

# 设置输出编码
if sys.platform.startswith('win'):
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

import cv2
import numpy as np
import face_recognition
from PIL import Image, ImageDraw, ImageFont

def diagnose_image(image_path, output_path):
    """诊断单张图片的人脸检测结果"""
    print("="*80)
    print(f"诊断图片: {image_path}")
    print("="*80)
    
    # 加载图片
    image = cv2.imread(image_path)
    if image is None:
        print(f"[ERROR] 无法加载图片")
        return None
    
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    print(f"图片尺寸: {rgb_image.shape[1]}x{rgb_image.shape[0]}")
    
    # 检测人脸
    print("\n[人脸检测]")
    face_locations = face_recognition.face_locations(rgb_image)
    print(f"检测到 {len(face_locations)} 个人脸")
    
    if len(face_locations) == 0:
        print("[WARN] 未检测到人脸，尝试HOG模型...")
        face_locations = face_recognition.face_locations(rgb_image, model="hog")
        print(f"HOG模型检测到 {len(face_locations)} 个人脸")
    
    if len(face_locations) == 0:
        print("[ERROR] 所有方法都未检测到人脸")
        return None
    
    # 提取特征
    print("\n[特征提取]")
    face_encodings = face_recognition.face_encodings(rgb_image, face_locations)
    print(f"提取到 {len(face_encodings)} 个特征向量")
    
    # 详细信息
    for i, (location, encoding) in enumerate(zip(face_locations, face_encodings)):
        top, right, bottom, left = location
        width = right - left
        height = bottom - top
        area_ratio = (width * height) / (rgb_image.shape[0] * rgb_image.shape[1])
        
        print(f"\n人脸 {i+1}:")
        print(f"  位置: ({left}, {top}) - ({right}, {bottom})")
        print(f"  尺寸: {width}x{height}")
        print(f"  占比: {area_ratio*100:.2f}%")
        print(f"  特征范围: [{encoding.min():.6f}, {encoding.max():.6f}]")
        print(f"  特征均值: {encoding.mean():.6f}")
        print(f"  特征标准差: {encoding.std():.6f}")
        print(f"  前5个值: {encoding[:5].tolist()}")
    
    # 可视化：在图片上画出人脸框
    pil_image = Image.fromarray(rgb_image)
    draw = ImageDraw.Draw(pil_image)
    
    for i, location in enumerate(face_locations):
        top, right, bottom, left = location
        
        # 画矩形框
        draw.rectangle([(left, top), (right, bottom)], outline="red", width=5)
        
        # 标注人脸编号
        draw.text((left, top-30), f"Face {i+1}", fill="red")
    
    # 保存可视化结果
    pil_image.save(output_path)
    print(f"\n[OK] 可视化结果已保存: {output_path}")
    
    return face_encodings[0] if face_encodings else None


def compare_features(encoding1, encoding2):
    """比较两个特征向量"""
    # 计算欧氏距离
    distance = np.linalg.norm(encoding1 - encoding2)
    
    # face_recognition使用0.6作为阈值
    # 距离越小，相似度越高
    is_match = distance < 0.6
    
    # 转换为相似度（0-1）
    similarity = 1.0 - min(distance, 1.0)
    
    print("\n[比对结果]")
    print("="*80)
    print(f"欧氏距离: {distance:.6f}")
    print(f"相似度: {similarity:.6f} ({similarity*100:.2f}%)")
    print(f"标准阈值: 0.6")
    print(f"是否匹配: {is_match}")
    
    if is_match:
        print("\n[结论] 两张照片是同一个人")
    else:
        print("\n[结论] 两张照片是不同的人")
    
    print("="*80)
    
    return distance, similarity, is_match


if __name__ == "__main__":
    print("\n人脸识别诊断工具\n")
    
    # 检查命令行参数
    if len(sys.argv) < 3:
        print("使用方法: python diagnose_face.py <图片1> <图片2>")
        print("示例: python diagnose_face.py admin.jpg admin1.jpg")
        sys.exit(1)
    
    image1_path = sys.argv[1]
    image2_path = sys.argv[2]
    
    # 检查文件是否存在
    if not os.path.exists(image1_path):
        print(f"[ERROR] 文件不存在: {image1_path}")
        sys.exit(1)
    
    if not os.path.exists(image2_path):
        print(f"[ERROR] 文件不存在: {image2_path}")
        sys.exit(1)
    
    # 诊断图片1
    encoding1 = diagnose_image(image1_path, image1_path.replace('.jpg', '_annotated.jpg').replace('.JPG', '_annotated.jpg'))
    if encoding1 is None:
        print("\n[ERROR] 图片1人脸检测失败")
        sys.exit(1)
    
    print("\n")
    
    # 诊断图片2
    encoding2 = diagnose_image(image2_path, image2_path.replace('.jpg', '_annotated.jpg').replace('.JPG', '_annotated.jpg'))
    if encoding2 is None:
        print("\n[ERROR] 图片2人脸检测失败")
        sys.exit(1)
    
    print("\n")
    
    # 比对特征
    compare_features(encoding1, encoding2)


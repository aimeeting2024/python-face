#!/usr/bin/env python3
"""
测试face_recognition特征提取的稳定性
检查同一张图片多次提取是否得到相同的特征向量
"""

import face_recognition
import numpy as np
import cv2
from PIL import Image
import time

def test_feature_stability(image_path, test_count=5):
    """测试特征提取稳定性"""
    print(f"测试图片: {image_path}")
    print(f"测试次数: {test_count}")
    print("=" * 60)
    
    # 读取图片
    try:
        image = face_recognition.load_image_file(image_path)
        print(f"图片尺寸: {image.shape}")
    except Exception as e:
        print(f"❌ 读取图片失败: {e}")
        return
    
    # 多次提取特征
    features = []
    distances = []
    
    for i in range(test_count):
        print(f"\n第 {i+1} 次提取...")
        
        try:
            # 检测人脸位置
            face_locations = face_recognition.face_locations(image)
            if not face_locations:
                print("❌ 未检测到人脸")
                continue
                
            print(f"  检测到 {len(face_locations)} 个人脸")
            
            # 提取特征
            face_encodings = face_recognition.face_encodings(image, face_locations)
            if not face_encodings:
                print("❌ 特征提取失败")
                continue
                
            feature = face_encodings[0]
            features.append(feature)
            
            print(f"  特征维度: {len(feature)}")
            print(f"  前5个值: {feature[:5]}")
            
        except Exception as e:
            print(f"❌ 第 {i+1} 次提取失败: {e}")
            continue
    
    # 分析稳定性
    if len(features) < 2:
        print("\n❌ 提取次数不足，无法分析稳定性")
        return
    
    print(f"\n📊 稳定性分析（共 {len(features)} 次成功提取）:")
    print("-" * 60)
    
    # 计算两两之间的距离
    for i in range(len(features)):
        for j in range(i + 1, len(features)):
            distance = face_recognition.face_distance([features[i]], features[j])[0]
            distances.append(distance)
            print(f"  第{i+1}次 vs 第{j+1}次: 距离 = {distance:.6f}")
    
    # 统计结果
    if distances:
        avg_distance = np.mean(distances)
        max_distance = np.max(distances)
        min_distance = np.min(distances)
        
        print(f"\n📈 统计结果:")
        print(f"  平均距离: {avg_distance:.6f}")
        print(f"  最大距离: {max_distance:.6f}")
        print(f"  最小距离: {min_distance:.6f}")
        
        # 判断稳定性
        print(f"\n🎯 稳定性评估:")
        if avg_distance < 0.001:
            print("  ✅ 非常稳定（平均距离 < 0.001）")
        elif avg_distance < 0.01:
            print("  ✅ 稳定（平均距离 < 0.01）")
        elif avg_distance < 0.1:
            print("  ⚠️ 一般稳定（平均距离 < 0.1）")
        else:
            print("  ❌ 不稳定（平均距离 >= 0.1）")
            print("  可能原因:")
            print("    1. 图片质量差")
            print("    2. 人脸检测位置不稳定")
            print("    3. face_recognition库版本问题")
        
        # face_recognition标准
        print(f"\n📋 face_recognition标准:")
        print(f"  - distance < 0.4: 很可能是同一个人")
        print(f"  - distance < 0.6: 可能是同一个人")
        print(f"  - distance >= 0.6: 很可能是不同人")
        
        if avg_distance < 0.4:
            print(f"  ✅ 特征提取质量很好")
        elif avg_distance < 0.6:
            print(f"  ⚠️ 特征提取质量一般")
        else:
            print(f"  ❌ 特征提取质量差")

def test_different_images():
    """测试不同图片之间的差异"""
    print("\n" + "=" * 60)
    print("测试不同图片之间的特征差异")
    print("=" * 60)
    
    # 这里可以添加多张不同人的照片进行测试
    # 预期：不同人的距离应该 > 0.6
    pass

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("用法: python test_feature_stability.py <image_path> [test_count]")
        print("示例: python test_feature_stability.py test.jpg 5")
        sys.exit(1)
    
    image_path = sys.argv[1]
    test_count = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    
    test_feature_stability(image_path, test_count)

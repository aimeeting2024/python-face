#!/usr/bin/env python3
"""
简单的人脸识别测试程序
测试dlib和OpenCV是否正常工作
"""

import cv2
import dlib
import numpy as np

def test_libraries():
    """测试库是否正常导入"""
    print("正在测试库导入...")
    
    # 测试OpenCV
    print(f"OpenCV版本: {cv2.__version__}")
    
    # 测试dlib
    try:
        detector = dlib.get_frontal_face_detector()
        print("✅ dlib导入成功，人脸检测器创建成功")
        
        # 测试基本的图像处理
        test_image = np.ones((100, 100), dtype=np.uint8) * 128  # 创建灰度图像
        faces = detector(test_image)
        print(f"测试图像检测完成，检测到 {len(faces)} 个人脸")
        
    except Exception as e:
        print(f"❌ dlib测试失败: {e}")
        return False
    
    print("所有库测试通过！")
    return True

if __name__ == "__main__":
    try:
        test_libraries()
        print("✅ 人脸识别环境配置成功！")
    except Exception as e:
        print(f"❌ 测试失败: {e}")
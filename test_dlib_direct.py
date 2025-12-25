#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
直接使用dlib测试人脸检测
绕过face_recognition包装层
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
import dlib

def test_with_dlib(image_path):
    """直接使用dlib进行人脸检测"""
    print("="*80)
    print(f"测试图片: {image_path}")
    print("="*80)
    
    # 1. 加载图片
    print("\n[1] 加载图片...")
    image = cv2.imread(image_path)
    if image is None:
        print(f"[ERROR] 无法加载图片")
        return
    
    # 尝试不同的颜色空间
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    print(f"[OK] RGB图片: shape={rgb_image.shape}, dtype={rgb_image.dtype}")
    print(f"[OK] 灰度图片: shape={gray_image.shape}, dtype={gray_image.dtype}")
    
    # 2. 使用dlib的HOG人脸检测器
    print("\n[2] 使用dlib HOG检测器...")
    try:
        detector = dlib.get_frontal_face_detector()
        
        # 尝试RGB图像
        print("  尝试RGB图像...")
        faces_rgb = detector(rgb_image, 1)
        print(f"  [OK] RGB图像检测到 {len(faces_rgb)} 个人脸")
        
        # 尝试灰度图像
        print("  尝试灰度图像...")
        faces_gray = detector(gray_image, 1)
        print(f"  [OK] 灰度图像检测到 {len(faces_gray)} 个人脸")
        
        if len(faces_gray) > 0:
            print("\n  检测结果（灰度图）:")
            for i, face in enumerate(faces_gray):
                print(f"    人脸 {i+1}: left={face.left()}, top={face.top()}, right={face.right()}, bottom={face.bottom()}")
                
    except Exception as e:
        print(f"  [ERROR] HOG检测失败: {e}")
        import traceback
        traceback.print_exc()
    
    # 3. 如果检测到人脸，尝试提取特征
    if len(faces_gray) > 0:
        print("\n[3] 加载特征提取模型...")
        try:
            import face_recognition_models
            
            # 加载关键点预测器
            predictor_path = face_recognition_models.pose_predictor_model_location()
            print(f"  关键点模型: {predictor_path}")
            predictor = dlib.shape_predictor(predictor_path)
            
            # 加载人脸识别模型
            recognition_model_path = face_recognition_models.face_recognition_model_location()
            print(f"  识别模型: {recognition_model_path}")
            face_encoder = dlib.face_recognition_model_v1(recognition_model_path)
            
            # 提取第一个人脸的特征
            face = faces_gray[0]
            shape = predictor(rgb_image, face)
            face_descriptor = np.array(face_encoder.compute_face_descriptor(rgb_image, shape))
            
            print(f"\n[OK] 特征提取成功!")
            print(f"  维度: {len(face_descriptor)}")
            print(f"  数据类型: {face_descriptor.dtype}")
            print(f"  值范围: [{face_descriptor.min():.6f}, {face_descriptor.max():.6f}]")
            print(f"  前10个值: {face_descriptor[:10]}")
            
            # 检查是否为模拟数据
            mock_pattern = np.array([i * 0.01 for i in range(128)], dtype=np.float64)
            if np.allclose(face_descriptor, mock_pattern, rtol=1e-3):
                print(f"\n  [WARN] 这是模拟测试数据！")
            else:
                print(f"\n  [OK] 这是真实的人脸特征！")
            
            # 保存特征
            output_file = image_path.replace('.jpg', '_dlib_features.npy')
            np.save(output_file, face_descriptor)
            print(f"\n[OK] 特征已保存到: {output_file}")
            
        except Exception as e:
            print(f"[ERROR] 特征提取失败: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "="*80)
    print("[SUCCESS] 测试完成!")
    print("="*80)


if __name__ == "__main__":
    print("\n" + "="*80)
    print("直接使用dlib测试人脸检测")
    print("="*80)
    
    # 检查环境
    print("\n[环境检查]")
    print(f"[OK] dlib 版本: {dlib.__version__}")
    print(f"[OK] OpenCV 版本: {cv2.__version__}")
    print(f"[OK] NumPy 版本: {np.__version__}")
    print(f"[OK] CUDA 支持: {dlib.DLIB_USE_CUDA}")
    
    # 检查模型文件
    print("\n[模型文件检查]")
    try:
        import face_recognition_models
        
        predictor_path = face_recognition_models.pose_predictor_model_location()
        recognition_path = face_recognition_models.face_recognition_model_location()
        
        print(f"[OK] 关键点模型: {os.path.exists(predictor_path)}")
        print(f"     {predictor_path}")
        print(f"[OK] 识别模型: {os.path.exists(recognition_path)}")
        print(f"     {recognition_path}")
    except Exception as e:
        print(f"[ERROR] 模型检查失败: {e}")
    
    print("\n")
    
    # 运行测试
    if len(sys.argv) > 1:
        test_with_dlib(sys.argv[1])
    else:
        # 测试默认图片
        test_dir = "test-pictures"
        if os.path.exists(test_dir):
            images = [f for f in os.listdir(test_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
            if images:
                test_with_dlib(os.path.join(test_dir, images[0]))
            else:
                print("[ERROR] test-pictures目录中没有图片")
        else:
            print("[ERROR] test-pictures目录不存在")


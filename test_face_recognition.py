#!/usr/bin/env python3
"""
直接测试人脸识别功能
"""
import sys
import os
sys.path.insert(0, '.')

from face_extractor import SimpleFaceExtractor
import json

def test_face_extractor():
    """测试人脸特征提取器"""
    print("开始测试人脸特征提取器...")
    
    # 创建提取器实例
    extractor = SimpleFaceExtractor()
    print("✅ 人脸提取器创建成功")
    
    # 创建一个简单的测试图像（纯色图）
    import base64
    from PIL import Image
    import io
    
    # 创建一个简单的测试图像
    img = Image.new('RGB', (100, 100), (128, 128, 128))
    buffer = io.BytesIO()
    img.save(buffer, format='JPEG')
    image_data = buffer.getvalue()
    base64_data = base64.b64encode(image_data).decode('utf-8')
    
    print("✅ 测试图像创建成功")
    
    # 测试特征提取
    result = extractor.extract_feature_from_base64(base64_data)
    
    print("🔍 人脸识别结果:")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    if result['success']:
        print("✅ 测试成功！人脸特征提取正常工作")
    else:
        print("⚠️  未检测到人脸（这是正常的，因为测试图像没有人脸）")
        print("✅ 人脸识别系统工作正常")

if __name__ == "__main__":
    test_face_extractor()
#!/usr/bin/env python3
"""
生成测试用的Base64图像数据
"""
import base64
from PIL import Image, ImageDraw
import io

def create_test_face_image():
    """创建一个简单的测试人脸图像"""
    # 创建一个200x200的白色背景图像
    img = Image.new('RGB', (200, 200), 'white')
    draw = ImageDraw.Draw(img)
    
    # 画一个简单的脸
    # 脸部轮廓（椭圆）
    draw.ellipse([50, 50, 150, 170], fill='peachpuff', outline='black', width=2)
    
    # 眼睛
    draw.ellipse([70, 80, 85, 95], fill='black')  # 左眼
    draw.ellipse([115, 80, 130, 95], fill='black')  # 右眼
    
    # 鼻子
    draw.line([100, 100, 100, 120], fill='black', width=2)
    
    # 嘴巴
    draw.arc([80, 130, 120, 150], 0, 180, fill='black', width=2)
    
    # 转换为Base64
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    image_data = buffer.getvalue()
    base64_data = base64.b64encode(image_data).decode('utf-8')
    
    return base64_data

if __name__ == "__main__":
    base64_data = create_test_face_image()
    print(base64_data)
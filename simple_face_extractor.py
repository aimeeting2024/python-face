#!/usr/bin/env python3
"""
简化的人脸特征提取器 - 直接使用dlib
不依赖face_recognition_models，适用于快速部署
"""

import argparse
import base64
import json
import sys
import time
import platform
from typing import Dict, List, Optional

try:
    import cv2
    import numpy as np
    import dlib
    from PIL import Image
    import io
except ImportError as e:
    print(f"错误: 缺少必要的依赖库: {e}")
    print("请安装: pip install opencv-python pillow dlib")
    sys.exit(1)

__version__ = "1.0.0-simple"
__platform__ = platform.system()

class SimpleFaceExtractor:
    """简化的人脸特征提取器 - 使用dlib内置检测器"""
    
    def __init__(self):
        self.detector = dlib.get_frontal_face_detector()
        self.feature_dim = 128  # 模拟128维特征向量
        
    def extract_feature_from_base64(self, base64_image: str) -> Dict:
        """从Base64图像数据提取特征码"""
        start_time = time.time()
        
        try:
            # 解码Base64图像
            image_data = base64.b64decode(base64_image)
            image = Image.open(io.BytesIO(image_data))
            
            # 转换为RGB格式
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # 转换为numpy数组和灰度图
            image_array = np.array(image)
            gray = cv2.cvtColor(image_array, cv2.COLOR_RGB2GRAY)
            
            # 检测人脸位置
            faces = self.detector(gray)
            
            if len(faces) == 0:
                return {
                    "success": False,
                    "feature_code": "",
                    "quality": 0.0,
                    "process_time": (time.time() - start_time) * 1000,
                    "message": "未检测到人脸"
                }
            
            # 选择最大的人脸
            if len(faces) > 1:
                largest_face = max(faces, key=lambda face: face.area())
                faces = [largest_face]
            
            face = faces[0]
            
            # 提取人脸区域
            face_region = gray[face.top():face.bottom(), face.left():face.right()]
            
            # 生成简化的特征向量（使用HOG特征）
            feature_vector = self._extract_hog_features(face_region)
            
            # 转换为Base64编码
            feature_bytes = feature_vector.tobytes()
            feature_code = base64.b64encode(feature_bytes).decode('utf-8')
            
            # 计算质量评分
            quality = self._calculate_quality(face_region, face.area())
            
            process_time = (time.time() - start_time) * 1000
            
            return {
                "success": True,
                "feature_code": feature_code,
                "quality": quality,
                "process_time": process_time,
                "message": "特征提取成功",
                "face_location": {
                    "left": face.left(),
                    "top": face.top(),
                    "right": face.right(),
                    "bottom": face.bottom()
                }
            }
            
        except Exception as e:
            return {
                "success": False,
                "feature_code": "",
                "quality": 0.0,
                "process_time": (time.time() - start_time) * 1000,
                "message": f"特征提取异常: {str(e)}"
            }
    
    def _extract_hog_features(self, face_image: np.ndarray) -> np.ndarray:
        """提取HOG特征作为人脸特征向量"""
        # 调整人脸图像尺寸
        face_resized = cv2.resize(face_image, (64, 64))
        
        # 计算HOG特征
        hog = cv2.HOGDescriptor((64, 64), (16, 16), (8, 8), (8, 8), 9)
        hog_features = hog.compute(face_resized)
        
        # 调整到固定维度
        if len(hog_features) > self.feature_dim:
            feature_vector = hog_features[:self.feature_dim]
        else:
            feature_vector = np.pad(hog_features, (0, self.feature_dim - len(hog_features)), 'constant')
        
        # L2归一化
        feature_vector = feature_vector.astype(np.float32).flatten()
        norm = np.linalg.norm(feature_vector)
        if norm > 0:
            feature_vector = feature_vector / norm
            
        return feature_vector
    
    def _calculate_quality(self, face_image: np.ndarray, face_area: int) -> float:
        """计算人脸质量评分"""
        try:
            # 计算清晰度（拉普拉斯方差）
            laplacian_var = cv2.Laplacian(face_image, cv2.CV_64F).var()
            clarity_score = min(laplacian_var / 500.0, 1.0)
            
            # 计算尺寸评分
            size_score = min(face_area / 10000.0, 1.0)
            
            # 计算亮度评分
            brightness = np.mean(face_image) / 255.0
            brightness_score = 1.0 - abs(brightness - 0.5) * 2
            
            # 综合评分
            quality = (clarity_score * 0.5 + size_score * 0.3 + brightness_score * 0.2)
            
            return min(max(quality, 0.0), 1.0)
            
        except Exception:
            return 0.5

def main():
    parser = argparse.ArgumentParser(
        description="简化人脸特征提取器",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('--version', action='version', version=f'SimpleFaceExtractor {__version__}')
    
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # extract命令
    extract_parser = subparsers.add_parser('extract', help='提取人脸特征')
    extract_parser.add_argument('--base64', required=True, help='Base64编码的图像数据')
    extract_parser.add_argument('--output', help='输出文件路径（可选）')
    
    if len(sys.argv) == 1:
        parser.print_help()
        return
    
    args = parser.parse_args()
    
    if args.command == 'extract':
        extractor = SimpleFaceExtractor()
        result = extractor.extract_feature_from_base64(args.base64)
        
        output_json = json.dumps(result, indent=2, ensure_ascii=False)
        
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(output_json)
            print(f"结果已保存到: {args.output}")
        else:
            print(output_json)

if __name__ == "__main__":
    main()
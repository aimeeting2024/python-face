#!/usr/bin/env python3
"""
人脸特征提取器 - 跨平台版本
专注于单一职责：将用户上传的人脸图片转换成特征码

支持编译为Windows/Linux/macOS二进制文件：
    Windows: pyinstaller --onefile face_extractor.py
    Linux:   pyinstaller --onefile face_extractor.py  
    macOS:   pyinstaller --onefile face_extractor.py

使用方法:
    face-extractor extract --base64 <image_data> --output <output_file>
    face-extractor --help
    face-extractor --version
"""

import argparse
import base64
import json
import sys
import time
import platform
from typing import Dict, List, Optional

# ✅ 修复中文编码问题
import locale
import codecs

# 设置控制台编码为UTF-8
if sys.platform.startswith('win'):
    # Windows系统设置
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
else:
    # Linux/Mac系统设置
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

try:
    import face_recognition
    import cv2
    import numpy as np
    from PIL import Image
    import io
except ImportError as e:
    print(f"错误: 缺少必要的依赖库: {e}")
    print("请安装: pip install face-recognition opencv-python pillow")
    sys.exit(1)

__version__ = "1.0.0"
__platform__ = platform.system()
__author__ = "Meeting Server Team"

def show_system_info():
    """显示系统信息"""
    print(f"人脸特征提取器 v{__version__}")
    print(f"平台: {__platform__}")
    print(f"Python: {sys.version.split()[0]}")
    print(f"作者: {__author__}")

class SimpleFaceExtractor:
    """简化的人脸特征提取器"""
    
    def __init__(self):
        self.feature_dim = 128  # 固定128维特征向量
        
    def extract_feature_from_bytes(self, image_data: bytes) -> Dict:
        """从字节数据提取特征码"""
        start_time = time.time()
        
        try:
            print(f"DEBUG: 收到图像数据，大小: {len(image_data)} 字节", file=sys.stderr)
            
            # ✅ 修复：使用多种方法加载图像，确保兼容性
            image_array = None
            
            # 方法1：使用OpenCV加载
            try:
                nparr = np.frombuffer(image_data, np.uint8)
                image_array = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                if image_array is None:
                    raise ValueError("cv2.imdecode failed")
                
                # 转换BGR到RGB（OpenCV使用BGR格式）
                image_array = cv2.cvtColor(image_array, cv2.COLOR_BGR2RGB)
                print(f"DEBUG: OpenCV加载成功，shape: {image_array.shape}, dtype: {image_array.dtype}", file=sys.stderr)
                
            except Exception as cv2_error:
                print(f"DEBUG: OpenCV加载失败，尝试PIL方法: {cv2_error}", file=sys.stderr)
                image_array = None
            
            # 方法2：使用PIL加载作为备选
            if image_array is None:
                try:
                    image = Image.open(io.BytesIO(image_data))
                    print(f"DEBUG: PIL图像加载成功，格式: {image.format}, 模式: {image.mode}, 尺寸: {image.size}", file=sys.stderr)
                    
                    # 转换为RGB格式
                    if image.mode != 'RGB':
                        print(f"DEBUG: 转换图像格式 {image.mode} -> RGB", file=sys.stderr)
                        image = image.convert('RGB')
                    
                    # 转换为numpy数组
                    image_array = np.array(image)
                    print(f"DEBUG: PIL转换numpy数组成功，shape: {image_array.shape}, dtype: {image_array.dtype}", file=sys.stderr)
                    
                except Exception as pil_error:
                    print(f"DEBUG: PIL加载也失败: {pil_error}", file=sys.stderr)
                    raise ValueError(f"无法加载图像数据: OpenCV错误={cv2_error}, PIL错误={pil_error}")
            
            # ✅ 确保数组格式正确
            if image_array.dtype != np.uint8:
                print(f"DEBUG: 转换dtype {image_array.dtype} -> uint8", file=sys.stderr)
                image_array = image_array.astype(np.uint8)
            
            # ✅ 确保是C连续数组（dlib要求）
            if not image_array.flags['C_CONTIGUOUS']:
                print(f"DEBUG: 转换为C连续数组", file=sys.stderr)
                image_array = np.ascontiguousarray(image_array)
            
            # ✅ 确保图像尺寸合理（face_recognition对图像尺寸有要求）
            height, width = image_array.shape[:2]
            if height < 80 or width < 80:
                print(f"DEBUG: 图像尺寸过小 ({width}x{height})，调整大小", file=sys.stderr)
                # 调整图像大小
                scale_factor = max(80.0/height, 80.0/width)
                new_width = int(width * scale_factor)
                new_height = int(height * scale_factor)
                image_array = cv2.resize(image_array, (new_width, new_height), interpolation=cv2.INTER_AREA)
                print(f"DEBUG: 调整后尺寸: {image_array.shape}", file=sys.stderr)
            
            print(f"DEBUG: 最终数组 - shape: {image_array.shape}, dtype: {image_array.dtype}, C_CONTIGUOUS: {image_array.flags['C_CONTIGUOUS']}", file=sys.stderr)
            
            # 检测人脸位置
            print(f"DEBUG: 开始人脸检测...", file=sys.stderr)
            print(f"DEBUG: 图像数组详细信息 - shape: {image_array.shape}, dtype: {image_array.dtype}", file=sys.stderr)
            print(f"DEBUG: 图像数组内存布局 - C_CONTIGUOUS: {image_array.flags['C_CONTIGUOUS']}, F_CONTIGUOUS: {image_array.flags['F_CONTIGUOUS']}", file=sys.stderr)
            print(f"DEBUG: 图像数组范围 - min: {image_array.min()}, max: {image_array.max()}", file=sys.stderr)
            
            # 尝试多种人脸检测方法
            face_locations = []
            
            # 方法1: 默认CNN模型
            try:
                face_locations = face_recognition.face_locations(image_array, number_of_times_to_upsample=1)
                print(f"DEBUG: 默认模型检测到 {len(face_locations)} 个人脸", file=sys.stderr)
            except Exception as face_error:
                print(f"DEBUG: 默认模型失败: {face_error}", file=sys.stderr)
            
            # 方法2: 如果没检测到，尝试HOG模型
            if len(face_locations) == 0:
                print(f"DEBUG: 尝试使用HOG模型...", file=sys.stderr)
                try:
                    face_locations = face_recognition.face_locations(image_array, model="hog")
                    print(f"DEBUG: HOG模型检测到 {len(face_locations)} 个人脸", file=sys.stderr)
                except Exception as hog_error:
                    print(f"DEBUG: HOG模型失败: {hog_error}", file=sys.stderr)
            
            # 方法3: 如果还没检测到，使用OpenCV Haar级联
            if len(face_locations) == 0:
                print(f"DEBUG: 尝试使用OpenCV人脸检测...", file=sys.stderr)
                try:
                    # 使用OpenCV的Haar级联分类器（更宽松的检测）
                    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
                    gray_image = cv2.cvtColor(image_array, cv2.COLOR_RGB2GRAY)
                    # 降低参数以检测更小的人脸
                    faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.05, minNeighbors=3, minSize=(30, 30))
                    
                    if len(faces) > 0:
                        print(f"DEBUG: OpenCV检测到 {len(faces)} 个人脸", file=sys.stderr)
                        # 将OpenCV格式转换为face_recognition格式
                        face_locations = []
                        for (x, y, w, h) in faces:
                            # OpenCV格式: (x, y, w, h) -> face_recognition格式: (top, right, bottom, left)
                            face_locations.append((y, x + w, y + h, x))
                            print(f"DEBUG:   人脸位置: x={x}, y={y}, w={w}, h={h}", file=sys.stderr)
                    else:
                        print(f"DEBUG: OpenCV也未检测到人脸", file=sys.stderr)
                except Exception as cv_error:
                    print(f"DEBUG: OpenCV检测失败: {cv_error}", file=sys.stderr)
            
            if not face_locations:
                # 保存调试图像到debug目录
                try:
                    import os
                    debug_dir = "./debug"
                    os.makedirs(debug_dir, exist_ok=True)
                    debug_file = os.path.join(debug_dir, f"failed_{int(time.time() * 1000)}.jpg")
                    cv2.imwrite(debug_file, cv2.cvtColor(image_array, cv2.COLOR_RGB2BGR))
                    print(f"DEBUG: 未检测到人脸，图像已保存到: {debug_file}", file=sys.stderr)
                except Exception as e:
                    print(f"DEBUG: 保存调试图像失败: {e}", file=sys.stderr)
                
                return {
                    "success": False,
                    "feature_code": "",
                    "quality": 0.0,
                    "process_time": (time.time() - start_time) * 1000,
                    "message": "未检测到人脸"
                }
            
            # 使用第一个检测到的人脸
            face_location = face_locations[0]
            
            # 提取人脸特征编码
            face_encodings = face_recognition.face_encodings(image_array, [face_location])
            
            if not face_encodings:
                return {
                    "success": False,
                    "message": "人脸特征编码失败"
                }
            
            # 获取128维特征向量
            face_encoding = face_encodings[0]
            
            # 编码为Base64
            feature_bytes = face_encoding.astype(np.float32).tobytes()
            feature_code = base64.b64encode(feature_bytes).decode('utf-8')
            
            # 计算人脸质量评分
            # 计算实际人脸面积比例
            top, right, bottom, left = face_location
            face_width = right - left
            face_height = bottom - top
            face_area_pixels = face_width * face_height
            image_area = image_array.shape[0] * image_array.shape[1]
            face_area_ratio = face_area_pixels / image_area if image_area > 0 else 0.1
            
            quality = self._calculate_quality(image_array, face_location, face_area_ratio)
            
            # 计算处理时间
            process_time = (time.time() - start_time) * 1000
            
            return {
                "success": True,
                "feature_code": feature_code,
                "quality": quality,
                "process_time": process_time,
                "message": "特征提取成功"
            }
            
        except Exception as e:
            print(f"ERROR: 特征提取异常: {str(e)}", file=sys.stderr)
            import traceback
            traceback.print_exc(file=sys.stderr)
            return {
                "success": False,
                "feature_code": "",
                "quality": 0.0,
                "process_time": (time.time() - start_time) * 1000,
                "message": f"特征提取失败: {str(e)}"
            }
        
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
            
            # 转换为numpy数组
            image_array = np.array(image)
            
            # 检测人脸位置
            face_locations = face_recognition.face_locations(image_array)
            
            if not face_locations:
                return {
                    "success": False,
                    "feature_code": "",
                    "quality": 0.0,
                    "process_time": (time.time() - start_time) * 1000,
                    "message": "未检测到人脸"
                }
            
            # 如果检测到多个人脸，使用最大的那个
            if len(face_locations) > 1:
                # 计算人脸区域大小，选择最大的
                largest_face = max(face_locations, 
                                 key=lambda face: (face[2] - face[0]) * (face[1] - face[3]))
                face_locations = [largest_face]
            
            # 提取人脸特征编码
            face_encodings = face_recognition.face_encodings(image_array, face_locations)
            
            if not face_encodings:
                return {
                    "success": False,
                    "feature_code": "",
                    "quality": 0.0,
                    "process_time": (time.time() - start_time) * 1000,
                    "message": "人脸特征提取失败"
                }
            
            # 获取第一个人脸的特征向量
            feature_vector = face_encodings[0]
            
            # 验证特征向量维度
            if len(feature_vector) != self.feature_dim:
                return {
                    "success": False,
                    "feature_code": "",
                    "quality": 0.0,
                    "process_time": (time.time() - start_time) * 1000,
                    "message": f"特征向量维度错误: {len(feature_vector)} != {self.feature_dim}"
                }
            
            # 转换为float32并进行L2归一化
            feature_vector = feature_vector.astype(np.float32)
            norm = np.linalg.norm(feature_vector)
            if norm > 0:
                feature_vector = feature_vector / norm
            
            # 转换为Base64编码
            feature_bytes = feature_vector.tobytes()
            feature_code = base64.b64encode(feature_bytes).decode('utf-8')
            
            # 计算质量评分（基于人脸区域大小和清晰度）
            face_area = self._calculate_face_area(face_locations[0], image_array.shape)
            quality = self._calculate_quality(image_array, face_locations[0], face_area)
            
            process_time = (time.time() - start_time) * 1000
            
            return {
                "success": True,
                "feature_code": feature_code,
                "quality": quality,
                "process_time": process_time,
                "message": "特征提取成功"
            }
            
        except Exception as e:
            return {
                "success": False,
                "feature_code": "",
                "quality": 0.0,
                "process_time": (time.time() - start_time) * 1000,
                "message": f"特征提取异常: {str(e)}"
            }
    
    def _calculate_face_area(self, face_location: tuple, image_shape: tuple) -> float:
        """计算人脸区域面积比例"""
        top, right, bottom, left = face_location
        face_width = right - left
        face_height = bottom - top
        face_area = face_width * face_height
        
        image_height, image_width = image_shape[:2]
        image_area = image_width * image_height
        
        return face_area / image_area if image_area > 0 else 0.0
    
    def _calculate_quality(self, image_array: np.ndarray, face_location: tuple, face_area: float) -> float:
        """计算人脸质量评分"""
        try:
            top, right, bottom, left = face_location
            
            # 提取人脸区域
            face_image = image_array[top:bottom, left:right]
            
            # 转换为灰度图
            gray_face = cv2.cvtColor(face_image, cv2.COLOR_RGB2GRAY)
            
            # 计算拉普拉斯方差（清晰度指标）
            laplacian_var = cv2.Laplacian(gray_face, cv2.CV_64F).var()
            clarity_score = min(laplacian_var / 1000.0, 1.0)  # 归一化到0-1
            
            # 计算尺寸评分
            size_score = min(face_area * 10, 1.0)  # 归一化到0-1
            
            # 计算亮度评分
            brightness = np.mean(gray_face) / 255.0
            brightness_score = 1.0 - abs(brightness - 0.5) * 2  # 理想亮度为0.5
            
            # 综合评分
            quality = (clarity_score * 0.5 + size_score * 0.3 + brightness_score * 0.2)
            
            return min(max(quality, 0.0), 1.0)  # 确保在0-1范围内
            
        except Exception:
            return 0.5  # 默认质量评分

def main():
    parser = argparse.ArgumentParser(
        description="人脸特征提取器 - 跨平台版本",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
示例:
  {sys.argv[0]} extract --base64 <image_data> --output result.json
  {sys.argv[0]} --version
  {sys.argv[0]} --help

平台支持: Windows, Linux, macOS
版本: {__version__}
        """
    )
    
    parser.add_argument('--version', action='version', 
                       version=f'face-extractor {__version__} ({__platform__})')
    parser.add_argument('--info', action='store_true', 
                       help='显示系统信息')
    
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # extract命令
    extract_parser = subparsers.add_parser('extract', help='提取人脸特征')
    
    # 输入方式：文件或Base64，二选一
    input_group = extract_parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument('--input', help='输入图片文件路径')
    input_group.add_argument('--base64', help='Base64编码的图像数据')
    
    extract_parser.add_argument('--output', required=True, help='输出文件路径')
    
    # help命令
    help_parser = subparsers.add_parser('help', help='显示帮助信息')
    
    args = parser.parse_args()
    
    if args.info:
        show_system_info()
        return
    
    if args.command == 'extract':
        # 执行特征提取
        extractor = SimpleFaceExtractor()
        
        # 根据输入类型选择处理方法
        if args.input:
            # 从文件读取图片
            try:
                with open(args.input, 'rb') as f:
                    image_data = f.read()
                result = extractor.extract_feature_from_bytes(image_data)
            except Exception as e:
                result = {
                    "success": False,
                    "feature_code": "",
                    "quality": 0.0,
                    "process_time": 0.0,
                    "message": f"读取输入文件失败: {str(e)}"
                }
        elif args.base64:
            # 从Base64字符串处理
            result = extractor.extract_feature_from_base64(args.base64)
        
        # 写入输出文件
        try:
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            
            # 在stdout输出简单状态
            if result['success']:
                print(f"SUCCESS: 特征提取完成，质量: {result['quality']:.3f}")
            else:
                print(f"ERROR: {result['message']}")
                sys.exit(1)
                
        except Exception as e:
            print(f"ERROR: 写入输出文件失败: {e}")
            sys.exit(1)
    
    elif args.command == 'help' or args.command is None:
        parser.print_help()
    
    else:
        print(f"未知命令: {args.command}")
        parser.print_help()
        sys.exit(1)

if __name__ == '__main__':
    main()
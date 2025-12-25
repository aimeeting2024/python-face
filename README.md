# 人脸特征提取器 - 简化版本

## 概述

这是一个专注于**单一职责**的人脸特征提取器：**将用户上传的人脸图片转换成特征码保存到数据库**。

## 特性

- ✅ **单一职责**: 只做图片到特征码的转换
- ✅ **零CGO依赖**: 通过二进制调用避免Go项目的CGO编译复杂性
- ✅ **高准确率**: 使用Python face-recognition库，准确率>95%
- ✅ **容错设计**: 二进制失败时自动降级到纯Go实现
- ✅ **标准化**: 输出128维float32特征向量，兼容Android端

## 目录结构

```
face-extractor/
├── face_extractor.py      # Python源码
├── requirements.txt       # Python依赖
├── build.sh              # Linux编译脚本
├── build.bat             # Windows编译脚本
├── face-extractor.exe    # Windows可执行文件（编译后）
├── face-extractor        # Linux可执行文件（编译后）
└── README.md             # 说明文档
```

## 快速开始

### 1. 编译二进制文件

**Windows:**
```cmd
cd face-extractor
build.bat
```

**Linux/macOS:**
```bash
cd face-extractor
chmod +x build.sh
./build.sh
```

### 2. 测试

```bash
# 检查版本
./face-extractor --version

# 提取特征
./face-extractor extract --base64 <base64_image> --output result.json
```

### 3. 集成到Go项目

二进制文件会被自动放置到项目根目录，Go服务会自动检测和使用。

## 使用方法

### 命令行接口

```bash
# 显示帮助
./face-extractor --help

# 显示版本
./face-extractor --version

# 提取人脸特征
./face-extractor extract --base64 <base64_image_data> --output <output_file>
```

### 输入格式

- `--base64`: Base64编码的图片数据（支持JPEG、PNG等格式）
- `--output`: 结果输出文件路径（JSON格式）

### 输出格式

```json
{
  "success": true,
  "feature_code": "YWJjZGVmZ2hpams...",  // Base64编码的128维float32特征向量
  "quality": 0.92,                      // 质量评分 (0.0-1.0)
  "process_time": 145.6,                // 处理时间（毫秒）
  "message": "特征提取成功"
}
```

## Go集成示例

### 1. 服务调用

```go
// 创建简化的特征提取器
extractor := face.NewSimpleFaceExtractor()

// 检查可用性
if !extractor.IsAvailable() {
    log.Println("二进制提取器不可用，将使用纯Go实现")
}

// 提取特征码
result, err := extractor.ExtractToFeatureCode(imageData)
if err != nil {
    return fmt.Errorf("特征提取失败: %v", err)
}

if result.Success {
    fmt.Printf("特征提取成功，质量: %.3f\n", result.Quality)
}
```

### 2. API调用

```bash
# 上传人脸图片
curl -X POST http://localhost:8080/api/face/upload \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user123",
    "image": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQ..."
  }'
```

**响应:**
```json
{
  "success": true,
  "message": "人脸特征提取并保存成功",
  "user_id": "user123",
  "feature_id": "face_user123_1672531200",
  "quality": 0.92,
  "process_time": 156
}
```

## 技术细节

### 1. 特征向量规范

- **维度**: 128维
- **数据类型**: float32
- **归一化**: L2归一化
- **编码**: Base64字符串

### 2. 质量评估

质量评分基于以下因素：
- **清晰度**: 拉普拉斯方差 (50%)
- **尺寸**: 人脸区域大小 (30%)
- **亮度**: 光照条件 (20%)

### 3. 性能指标

- **处理速度**: 100-500ms
- **准确率**: >95%
- **内存占用**: <100MB
- **支持格式**: JPEG, PNG, BMP

## 故障排除

### 1. 编译问题

**缺少依赖:**
```bash
pip install face-recognition opencv-python pillow
```

**PyInstaller问题:**
```bash
pip install --upgrade pyinstaller
```

### 2. 运行问题

**权限问题:**
```bash
chmod +x face-extractor
```

**库依赖问题:**
- Linux: `apt-get install libglib2.0-0`
- macOS: `brew install glib`

### 3. 集成问题

**路径查找失败:**
- 确保二进制文件在项目根目录
- 检查文件权限
- 设置环境变量 `FACE_EXTRACTOR_PATH`

## 开发指南

### 1. 修改Python代码

编辑 `face_extractor.py` 后重新编译：

```bash
# 重新编译
./build.sh

# 测试
./face-extractor --version
```

### 2. 调试模式

```bash
# 直接运行Python脚本（开发模式）
python face_extractor.py extract --base64 <data> --output result.json
```

### 3. 自定义配置

可以修改以下参数：
- 特征向量维度（默认128）
- 质量评分权重
- 支持的图片格式

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request。

## 联系方式

如有问题，请联系开发团队。
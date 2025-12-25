# WSL 路径映射指南

## 📁 WSL 如何访问 Windows 文件

### 路径映射规则

WSL 通过 `/mnt/` 目录挂载 Windows 驱动器：

| Windows 路径 | WSL 路径 |
|-------------|---------|
| `C:\` | `/mnt/c/` |
| `D:\` | `/mnt/d/` |
| `E:\` | `/mnt/e/` |
| `C:\Users\YourName\` | `/mnt/c/Users/YourName/` |

### 你的项目路径

**Windows 路径**：
```
D:\workspace\python-face
```

**WSL 路径**：
```
/mnt/d/workspace/python-face
```

---

## 🔍 查找路径的方法

### 方法1：使用 `pwd` 命令

```bash
# 在 WSL 中，进入项目目录
cd /mnt/d/workspace/python-face

# 查看当前路径
pwd
# 输出：/mnt/d/workspace/python-face
```

### 方法2：从 Windows 路径转换

**规则**：
1. 将 `D:\` 替换为 `/mnt/d/`
2. 将反斜杠 `\` 替换为正斜杠 `/`
3. 去掉末尾的斜杠（如果有）

**示例**：
```
Windows:  D:\workspace\python-face
          ↓
WSL:      /mnt/d/workspace/python-face
```

### 方法3：使用 `wslpath` 命令（在 WSL 中）

```bash
# 将 Windows 路径转换为 WSL 路径
wslpath "D:\workspace\python-face"
# 输出：/mnt/d/workspace/python-face

# 将 WSL 路径转换为 Windows 路径
wslpath -w /mnt/d/workspace/python-face
# 输出：D:\workspace\python-face
```

### 方法4：在 Windows 中查看 WSL 路径

在 Windows PowerShell 中：

```powershell
# 查看当前目录的 WSL 路径
wsl pwd

# 或者直接进入 WSL
wsl
# 然后执行
pwd
```

---

## 🚀 快速导航到项目

### 在 WSL 中

```bash
# 方法1：直接使用完整路径
cd /mnt/d/workspace/python-face

# 方法2：使用相对路径（如果当前在 /mnt/d/）
cd workspace/python-face

# 方法3：创建软链接（方便访问）
ln -s /mnt/d/workspace/python-face ~/python-face
cd ~/python-face
```

### 从 Windows 启动 WSL 并进入项目

在 Windows PowerShell 中：

```powershell
# 直接进入项目目录
wsl -d Ubuntu-22.04 -e bash -c "cd /mnt/d/workspace/python-face && bash"

# 或者
wsl
cd /mnt/d/workspace/python-face
```

---

## 📝 常用路径示例

### 你的项目

```bash
# Python 人脸识别项目
cd /mnt/d/workspace/python-face

# Go 后端项目
cd /mnt/d/workspace/meeting-server

# 前端项目
cd /mnt/d/workspace/meeting-web
```

### 系统路径

```bash
# WSL 用户主目录
cd ~
# 或
cd /home/your_username

# WSL 根目录
cd /

# Windows 用户目录
cd /mnt/c/Users/YourName
```

---

## ⚠️ 注意事项

### 1. 路径大小写

WSL 路径是**大小写敏感**的：
```bash
# ✅ 正确
cd /mnt/d/workspace/python-face

# ❌ 错误（如果实际目录是小写）
cd /mnt/d/Workspace/Python-Face
```

### 2. 空格处理

如果路径包含空格，需要用引号：
```bash
cd "/mnt/d/My Projects/python-face"
```

### 3. 性能考虑

- **Windows 文件系统**（`/mnt/`）：访问较慢，适合读取
- **WSL 文件系统**（`/home/`, `/tmp/` 等）：访问较快，适合编译和构建

**建议**：编译时可以将文件复制到 WSL 文件系统：

```bash
# 复制到 WSL 文件系统（更快）
cp -r /mnt/d/workspace/python-face ~/python-face-build
cd ~/python-face-build
./build_http_service_docker.sh
```

---

## 🔧 验证路径

```bash
# 检查路径是否存在
ls -la /mnt/d/workspace/python-face

# 查看文件列表
ls /mnt/d/workspace/python-face

# 检查当前目录
pwd

# 查看完整路径
realpath .
```

---

## ✅ 快速参考

**你的项目路径**：
```bash
# WSL 路径
/mnt/d/workspace/python-face

# 进入项目
cd /mnt/d/workspace/python-face

# 查看文件
ls -la

# 执行编译脚本
chmod +x build_http_service_docker.sh
./build_http_service_docker.sh
```


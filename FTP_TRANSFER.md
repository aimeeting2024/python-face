# FTP/SFTP 文件传输指南

## 📋 概述

使用 FTP/SFTP 工具将文件从 Windows 上传到 Ubuntu 服务器。

---

## 🚀 方式1：使用宝塔面板（最简单，推荐）

### 步骤

1. **登录宝塔面板**
   - 访问：`http://服务器IP:8888` 或 `https://服务器IP:8888`
   - 输入用户名和密码

2. **进入文件管理**
   - 点击左侧菜单"文件"
   - 导航到 `/opt` 目录

3. **创建项目目录**
   - 点击"新建文件夹"
   - 输入名称：`face-service`
   - 点击"创建"

4. **上传文件**
   - 进入 `/opt/face-service` 目录
   - 点击"上传"按钮
   - 选择文件：
     - `face_service.py`
     - `face_extractor.py`
     - `requirements.txt`
     - `build_http_service.sh`
   - 点击"开始上传"

5. **设置文件权限**
   - 选中 `build_http_service.sh`
   - 点击"权限"
   - 勾选"执行"权限
   - 或使用终端：
     ```bash
     chmod +x /opt/face-service/build_http_service.sh
     ```

---

## 🔧 方式2：使用 FileZilla（FTP/SFTP 客户端）

### 2.1 安装 FileZilla

**Windows**：
- 下载：https://filezilla-project.org/
- 安装 FileZilla Client

### 2.2 连接服务器

1. **打开 FileZilla**
2. **填写连接信息**：
   - **主机**：`sftp://服务器IP` 或 `ftp://服务器IP`
   - **用户名**：服务器用户名（如 `root` 或 `ubuntu`）
   - **密码**：服务器密码
   - **端口**：
     - SFTP：`22`（默认）
     - FTP：`21`（默认）
   - 点击"快速连接"

3. **如果使用 SFTP（推荐，更安全）**：
   - 协议选择：`SFTP - SSH File Transfer Protocol`
   - 端口：`22`

### 2.3 上传文件

1. **左侧窗口**：本地文件（Windows）
   - 导航到：`D:\workspace\python-face`

2. **右侧窗口**：远程服务器
   - 导航到：`/opt/face-service`
   - 如果目录不存在，右键 → "创建目录"

3. **上传文件**：
   - 选中左侧的文件
   - 拖拽到右侧，或右键 → "上传"
   - 上传以下文件：
     - `face_service.py`
     - `face_extractor.py`
     - `requirements.txt`
     - `build_http_service.sh`

4. **设置权限**（在 FileZilla 中）：
   - 右键点击 `build_http_service.sh`
   - 选择"文件权限"
   - 勾选"执行"（Execute）
   - 或使用数字权限：`755`

---

## 🔐 方式3：使用 WinSCP（Windows SCP/SFTP 客户端）

### 3.1 安装 WinSCP

- 下载：https://winscp.net/
- 安装 WinSCP

### 3.2 连接服务器

1. **打开 WinSCP**
2. **新建会话**：
   - **文件协议**：`SFTP`
   - **主机名**：服务器IP
   - **端口号**：`22`
   - **用户名**：服务器用户名
   - **密码**：服务器密码
   - 点击"保存"（可选）
   - 点击"登录"

### 3.3 上传文件

1. **左侧**：本地文件（Windows）
2. **右侧**：远程服务器
3. **导航到目标目录**：`/opt/face-service`
4. **上传文件**：
   - 选中文件，拖拽到右侧
   - 或选中文件，点击"上传"按钮

5. **设置权限**：
   - 右键点击 `build_http_service.sh`
   - 选择"属性" → "权限"
   - 勾选"执行"

---

## 📡 方式4：使用命令行 SCP（如果服务器支持 SSH）

### 在 Windows PowerShell 中

```powershell
# 上传整个目录
scp -r D:\workspace\python-face\* user@server:/opt/face-service/

# 或只上传必需文件
scp face_service.py face_extractor.py requirements.txt build_http_service.sh user@server:/opt/face-service/
```

### 在 Windows CMD 中

```cmd
# 使用 pscp（需要先安装 PuTTY）
pscp -r D:\workspace\python-face\* user@server:/opt/face-service/
```

---

## 🔧 方式5：在服务器上配置 FTP 服务（如果需要）

### 5.1 安装 vsftpd（FTP 服务器）

```bash
# 安装 vsftpd
sudo apt update
sudo apt install -y vsftpd

# 启动服务
sudo systemctl start vsftpd
sudo systemctl enable vsftpd

# 检查状态
sudo systemctl status vsftpd
```

### 5.2 配置 vsftpd

```bash
# 备份原配置
sudo cp /etc/vsftpd.conf /etc/vsftpd.conf.backup

# 编辑配置
sudo nano /etc/vsftpd.conf
```

**关键配置**：
```ini
# 允许本地用户登录
local_enable=YES

# 允许写入
write_enable=YES

# 允许匿名用户（可选，不推荐）
anonymous_enable=NO

# 限制用户在主目录
chroot_local_user=YES

# 允许被动模式
pasv_enable=YES
pasv_min_port=40000
pasv_max_port=50000
```

### 5.3 重启服务

```bash
sudo systemctl restart vsftpd
```

### 5.4 配置防火墙（如果需要）

```bash
# 允许 FTP 端口
sudo ufw allow 21/tcp
sudo ufw allow 40000:50000/tcp
```

---

## ✅ 验证文件上传

上传完成后，在服务器上验证：

```bash
# 进入项目目录
cd /opt/face-service

# 查看文件列表
ls -la

# 应该看到：
# face_service.py
# face_extractor.py
# requirements.txt
# build_http_service.sh

# 检查文件权限
ls -l build_http_service.sh

# 如果权限不对，设置执行权限
chmod +x build_http_service.sh
```

---

## 🎯 推荐方案

### 最简单：宝塔面板

- ✅ 图形界面，操作简单
- ✅ 无需安装客户端
- ✅ 支持拖拽上传
- ✅ 可以直接设置权限

### 最灵活：FileZilla

- ✅ 功能强大
- ✅ 支持 FTP/SFTP
- ✅ 可以保存连接信息
- ✅ 支持断点续传

### 最安全：SFTP（推荐）

- ✅ 加密传输
- ✅ 使用 SSH 端口（22）
- ✅ 不需要额外配置 FTP 服务

---

## 📝 快速参考

### 使用宝塔面板

1. 登录宝塔面板
2. 文件管理 → `/opt` → 新建文件夹 `face-service`
3. 进入 `face-service` → 上传文件
4. 设置 `build_http_service.sh` 的执行权限

### 使用 FileZilla

1. 打开 FileZilla
2. 连接：`sftp://服务器IP`，端口 `22`
3. 左侧：`D:\workspace\python-face`
4. 右侧：`/opt/face-service`
5. 拖拽文件上传
6. 设置权限：右键 → 文件权限 → 755

---

## ⚠️ 注意事项

1. **文件权限**：确保 `build_http_service.sh` 有执行权限
2. **文件完整性**：上传后验证文件大小和内容
3. **路径正确**：确保文件在 `/opt/face-service/` 目录下
4. **编码问题**：如果文件名有中文，注意编码设置

---

完成上传后，继续执行：
```bash
cd /opt/face-service
./build_http_service.sh
```


# 在 WSL Ubuntu 中使用 Docker 编译 Linux 版本

## 📋 前提条件

- Windows 10/11 系统
- 已安装 WSL 2
- WSL 中已安装 Ubuntu

---

## ⚠️ 关于 WSL 代理警告

如果看到以下警告：
```
wsl: 检测到 localhost 代理配置，但未镜像到 WSL。NAT 模式下的 WSL 不支持 localhost 代理。
```

**这是正常的警告，可以忽略**，不影响 Docker 安装和使用。

---

## 🐳 步骤1：在 WSL Ubuntu 中安装 Docker

### 1.1 打开 WSL Ubuntu 并进入项目目录

```powershell
# 在 Windows PowerShell 中
wsl
```

**然后在 WSL 中进入项目目录**：

```bash
# Windows 路径: D:\workspace\python-face
# WSL 路径: /mnt/d/workspace/python-face
cd /mnt/d/workspace/python-face

# 验证路径
pwd
ls -la
```

**路径映射规则**：
- `D:\` → `/mnt/d/`
- `C:\` → `/mnt/c/`
- 反斜杠 `\` → 正斜杠 `/`

### 1.2 更新系统包

```bash
sudo apt update
sudo apt upgrade -y
```

### 1.3 安装 Docker 依赖

```bash
sudo apt install -y \
    ca-certificates \
    curl \
    gnupg \
    lsb-release
```

**⚠️ 如果遇到包找不到的错误，请使用以下命令：**

```bash
# 方法1：分别安装（推荐）
sudo apt install -y ca-certificates
sudo apt install -y curl
sudo apt install -y gnupg2    # 注意：可能是 gnupg2 而不是 gnupg
sudo apt install -y lsb-release  # 注意：必须有连字符，不是 lsbrelease
```

或者：

```bash
# 方法2：一次性安装（修正版）
sudo apt install -y ca-certificates curl gnupg2 lsb-release
```

**常见错误**：
- ❌ `gnupg` → ✅ `gnupg2`
- ❌ `lsbrelease` → ✅ `lsb-release`（必须有连字符）

### 1.4 添加 Docker 官方 GPG 密钥

```bash
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
```

### 1.5 设置 Docker 仓库

```bash
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

**✅ 这是正常的！** 命令使用了 `> /dev/null`，所以没有输出是预期的。

**验证是否成功**：
```bash
# 查看文件内容，确认已写入
cat /etc/apt/sources.list.d/docker.list

# 应该看到类似内容：
# deb [arch=amd64 signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu jammy stable
```

### 1.6 更新 apt 包列表并安装 Docker Engine

**重要**：必须先更新包列表，确保 Docker 仓库已加载。

```bash
# 1. 更新包列表（必须执行）
sudo apt update

# 2. 验证 Docker 仓库是否已添加
cat /etc/apt/sources.list.d/docker.list

# 应该看到类似内容：
# deb [arch=amd64 signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu jammy stable
```

**如果 `apt update` 后仍然找不到包，请检查**：

```bash
# 检查 GPG 密钥是否存在
ls -l /etc/apt/keyrings/docker.gpg

# 检查仓库文件内容
cat /etc/apt/sources.list.d/docker.list

# 如果文件为空或不存在，重新执行步骤 1.4 和 1.5
```

**然后安装 Docker**：

```bash
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

**如果仍然失败，尝试使用 Ubuntu 官方仓库的 Docker（简化版）**：

```bash
# 方法2：使用 Ubuntu 官方仓库的 Docker（更简单）
sudo apt update
sudo apt install -y docker.io docker-compose

# 验证安装
sudo docker --version
```

**版本说明**：
- Ubuntu 22.04 官方仓库的 `docker.io` 通常包含 Docker 20.10+ 或更新的版本
- Docker 28.2.2 是**非常新的版本**（2025年），完全可以使用
- 对于编译 Python 服务，任何 Docker 20.10+ 版本都足够使用

### 1.7 启动 Docker 服务

```bash
sudo service docker start
```

### 1.8 将当前用户添加到 docker 组（可选，避免每次使用 sudo）

```bash
sudo usermod -aG docker $USER
```

**注意**：执行此命令后需要**重新登录 WSL** 才能生效。

**或者设置默认用户为 root（如果经常需要 sudo）：**

在 Windows PowerShell 中：
```powershell
ubuntu2204 config --default-user root
```

然后重新打开 WSL，默认就是 root 用户，不需要 sudo。

**如果忘记了 root 密码，可以重置：**

1. **使用当前用户重置 root 密码**（推荐）：
   ```bash
   # 在 WSL 中，使用当前用户（有 sudo 权限）
   sudo passwd root
   # 输入新的 root 密码
   ```

2. **或者直接使用 sudo，不需要 root 密码**：
   ```bash
   # 如果当前用户在 sudoers 中，可以直接使用 sudo
   sudo docker --version
   sudo service docker start
   # 不需要知道 root 密码
   ```

3. **从 Windows 重置 WSL 默认用户**：
   ```powershell
   # 如果忘记了所有密码，可以重置 WSL 用户
   # 注意：这会重置 WSL，需要重新配置
   wsl --unregister Ubuntu-22.04
   wsl --install -d Ubuntu-22.04
   ```

### 1.9 验证 Docker 安装

```bash
sudo docker --version
sudo docker run hello-world
```

如果看到 "Hello from Docker!" 消息，说明安装成功。

---

## 🚀 步骤2：使用 Docker 编译

### 方式A：使用提供的脚本（推荐）

在 WSL Ubuntu 中：

```bash
# 进入项目目录（Windows 的 D:\workspace\python-face 在 WSL 中是 /mnt/d/workspace/python-face）
cd /mnt/d/workspace/python-face

# 验证路径
pwd
ls -la

# 执行编译脚本
chmod +x build_http_service_docker.sh
./build_http_service_docker.sh
```

**路径说明**：
- Windows: `D:\workspace\python-face`
- WSL: `/mnt/d/workspace/python-face`

### 方式B：手动使用 Docker 编译

```bash
cd /mnt/d/workspace/python-face

# 构建 Docker 镜像
docker build -f Dockerfile.build -t face-service-builder .

# 在容器中编译
docker run --rm \
    -v "$(pwd)/deploy:/app/deploy" \
    face-service-builder

# 编译完成后，文件在 deploy/face_http_service
```

---

## 📝 步骤3：验证编译结果

```bash
# 检查文件是否存在
ls -lh deploy/face_http_service

# 检查文件类型（应该是 Linux 可执行文件）
file deploy/face_http_service

# 应该显示类似：ELF 64-bit LSB executable, x86-64
```

---

## 🔧 常见问题

### Q: Docker 服务启动失败？

```bash
# 检查 Docker 服务状态
sudo service docker status

# 手动启动
sudo service docker start

# 设置开机自启（可选）
sudo systemctl enable docker
```

### Q: 权限被拒绝（Permission denied）？

```bash
# 使用 sudo 运行
sudo docker run ...

# 或者将用户添加到 docker 组（需要重新登录）
sudo usermod -aG docker $USER
# 然后退出并重新登录 WSL
```

### Q: WSL 中 Docker 无法连接到 Docker daemon？

确保 Docker Desktop 没有运行（如果安装了），或者确保 WSL 中的 Docker 服务已启动：

```bash
sudo service docker start
```

### Q: 找不到 docker-ce 等包？

**原因**：Docker 官方仓库未正确添加或 GPG 密钥问题。

**解决方法1：重新添加仓库**

```bash
# 1. 删除旧的配置
sudo rm -f /etc/apt/keyrings/docker.gpg
sudo rm -f /etc/apt/sources.list.d/docker.list

# 2. 重新添加 GPG 密钥
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# 3. 重新添加仓库
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# 4. 更新包列表
sudo apt update

# 5. 再次尝试安装
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

**解决方法2：使用 Ubuntu 官方仓库（更简单）**

```bash
sudo apt update
sudo apt install -y docker.io docker-compose
sudo service docker start
sudo docker --version
```

这种方法安装的 Docker 版本可能较旧，但通常足够使用。

### Q: 编译速度慢？

Docker 首次构建镜像会下载基础镜像，可能需要几分钟。后续编译会快很多。

---

## ✅ 完成

编译完成后，`deploy/face_http_service` 就是 Linux 版本的可执行文件，可以直接上传到 Linux 服务器使用。


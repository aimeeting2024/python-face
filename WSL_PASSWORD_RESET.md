# WSL Ubuntu 密码重置指南

## 🔑 重置 root 密码

### 方法1：使用当前用户重置（推荐）

如果你当前登录的用户有 sudo 权限：

```bash
# 在 WSL Ubuntu 中执行
sudo passwd root
```

然后输入：
1. 当前用户的密码（用于 sudo）
2. 新的 root 密码（两次确认）

### 方法2：直接使用 sudo（最简单）

**不需要知道 root 密码**，直接使用 sudo 即可：

```bash
# 所有需要 root 权限的命令都用 sudo
sudo apt update
sudo service docker start
sudo docker --version
```

### 方法3：设置默认用户为 root（如果已设置但忘记密码）

如果你已经设置了默认用户为 root，但忘记了密码：

1. **从 Windows 重置 WSL 配置**：
   ```powershell
   # 查看当前默认用户
   ubuntu2204 config --default-user
   
   # 改回普通用户（假设用户名是你的 Windows 用户名或 ubuntu）
   ubuntu2204 config --default-user ubuntu
   # 或
   ubuntu2204 config --default-user your_username
   ```

2. **重新打开 WSL**，使用普通用户登录

3. **然后重置 root 密码**：
   ```bash
   sudo passwd root
   ```

4. **如果需要，再改回 root**：
   ```powershell
   ubuntu2204 config --default-user root
   ```

---

## 🚀 推荐方案：直接使用 sudo

**最简单的方式**：不需要设置 root 为默认用户，直接使用 sudo：

```bash
# 安装 Docker
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io

# 启动 Docker
sudo service docker start

# 使用 Docker（每次加 sudo）
sudo docker --version
sudo docker run hello-world
```

**或者将当前用户添加到 docker 组**（避免每次 sudo）：

```bash
# 将当前用户添加到 docker 组
sudo usermod -aG docker $USER

# 退出并重新登录 WSL
exit
# 然后重新打开 WSL
wsl
```

重新登录后，就可以直接使用 `docker` 命令，不需要 sudo。

---

## 🔧 验证

```bash
# 检查当前用户
whoami

# 检查是否有 sudo 权限
sudo -v

# 检查 Docker（如果已安装）
sudo docker --version
```

---

## ⚠️ 注意事项

1. **root 用户风险**：使用 root 作为默认用户有安全风险，建议只在必要时使用
2. **sudo 更安全**：使用 sudo 执行特定命令比直接使用 root 更安全
3. **Docker 组**：将用户添加到 docker 组后，不需要 sudo 也能使用 Docker

---

## ✅ 推荐工作流程

1. **使用普通用户登录 WSL**
2. **使用 sudo 安装 Docker**
3. **将用户添加到 docker 组**（避免每次 sudo）
4. **重新登录后直接使用 docker 命令**

这样既安全又方便！


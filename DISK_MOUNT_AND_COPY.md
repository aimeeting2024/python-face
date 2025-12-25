# Ubuntu 服务器磁盘挂载和文件拷贝指南

## 📋 概述

在 Ubuntu 服务器上挂载磁盘并拷贝文件到指定目录的完整步骤。

---

## 🔍 步骤1：查看磁盘和分区

### 1.1 查看所有磁盘

```bash
# 查看所有磁盘
lsblk

# 或使用 fdisk
sudo fdisk -l

# 查看磁盘使用情况
df -h
```

**输出示例**：
```
NAME   MAJ:MIN RM   SIZE RO TYPE MOUNTPOINT
sda      8:0    0   100G  0 disk
├─sda1   8:1    0   512M  0 part /boot/efi
├─sda2   8:2    0    50G  0 part /
└─sda3   8:3    0   49.5G  0 part          # 未挂载的分区
sdb      8:16   0   500G  0 disk           # 新磁盘
└─sdb1   8:17   0   500G  0 part          # 未挂载的分区
```

### 1.2 查看文件系统类型

```bash
# 查看分区文件系统
sudo blkid

# 或
sudo file -s /dev/sdb1
```

---

## 💾 步骤2：挂载磁盘

### 2.1 创建挂载点

```bash
# 创建挂载目录（例如挂载到 /mnt/data）
sudo mkdir -p /mnt/data

# 或挂载到项目目录
sudo mkdir -p /opt/face-service
```

### 2.2 挂载磁盘

#### 方式1：临时挂载（重启后失效）

```bash
# 挂载到指定目录
sudo mount /dev/sdb1 /mnt/data

# 如果不知道设备名，先查看
lsblk
# 然后挂载，例如：sudo mount /dev/sda3 /mnt/data
```

#### 方式2：指定文件系统类型挂载

```bash
# 如果是 ext4 文件系统
sudo mount -t ext4 /dev/sdb1 /mnt/data

# 如果是 NTFS（Windows 格式）
sudo mount -t ntfs-3g /dev/sdb1 /mnt/data

# 如果是 FAT32
sudo mount -t vfat /dev/sdb1 /mnt/data
```

#### 方式3：挂载 U 盘或移动硬盘

```bash
# 插入 U 盘后，查看设备
lsblk

# 通常 U 盘是 /dev/sdb 或 /dev/sdc
# 挂载（如果是 FAT32 或 NTFS）
sudo mkdir -p /mnt/usb
sudo mount /dev/sdb1 /mnt/usb

# 或自动检测文件系统类型
sudo mount -t auto /dev/sdb1 /mnt/usb
```

### 2.3 验证挂载

```bash
# 查看挂载情况
df -h

# 或
mount | grep /mnt/data

# 查看挂载点内容
ls -la /mnt/data
```

---

## 📁 步骤3：拷贝文件

### 3.1 从挂载的磁盘拷贝到项目目录

```bash
# 假设文件在 /mnt/data/python-face/ 目录下
# 目标目录：/opt/face-service

# 方法1：使用 cp 命令
sudo cp -r /mnt/data/python-face/* /opt/face-service/

# 方法2：只拷贝必需文件
sudo cp /mnt/data/python-face/face_service.py /opt/face-service/
sudo cp /mnt/data/python-face/face_extractor.py /opt/face-service/
sudo cp /mnt/data/python-face/requirements.txt /opt/face-service/
sudo cp /mnt/data/python-face/build_http_service.sh /opt/face-service/

# 方法3：使用 rsync（推荐，显示进度）
sudo rsync -av --progress /mnt/data/python-face/ /opt/face-service/
```

### 3.2 从 Windows 共享拷贝（如果服务器可以访问 Windows 共享）

```bash
# 安装 cifs-utils
sudo apt install -y cifs-utils

# 创建挂载点
sudo mkdir -p /mnt/windows

# 挂载 Windows 共享
sudo mount -t cifs //192.168.1.100/shared /mnt/windows -o username=your_user,password=your_pass

# 拷贝文件
sudo cp -r /mnt/windows/python-face/* /opt/face-service/

# 卸载
sudo umount /mnt/windows
```

### 3.3 从 U 盘拷贝

```bash
# 挂载 U 盘（见步骤2.3）
sudo mount /dev/sdb1 /mnt/usb

# 拷贝文件
sudo cp -r /mnt/usb/python-face/* /opt/face-service/

# 卸载 U 盘
sudo umount /mnt/usb
```

### 3.4 验证文件拷贝

```bash
# 进入目标目录
cd /opt/face-service

# 查看文件列表
ls -la

# 验证必需文件是否存在
ls -la face_service.py face_extractor.py requirements.txt build_http_service.sh
```

---

## 🔧 步骤4：设置开机自动挂载（可选）

### 4.1 获取磁盘 UUID

```bash
# 查看 UUID
sudo blkid /dev/sdb1

# 输出示例：
# /dev/sdb1: UUID="12345678-1234-1234-1234-123456789abc" TYPE="ext4"
```

### 4.2 编辑 /etc/fstab

```bash
# 备份原文件
sudo cp /etc/fstab /etc/fstab.backup

# 编辑 fstab
sudo nano /etc/fstab
```

### 4.3 添加挂载配置

在 `/etc/fstab` 文件末尾添加：

```bash
# 格式：UUID=设备UUID  挂载点  文件系统类型  选项  转储  检查
UUID=12345678-1234-1234-1234-123456789abc  /mnt/data  ext4  defaults  0  2
```

**参数说明**：
- `UUID=...` - 磁盘的 UUID（使用 UUID 比设备名更稳定）
- `/mnt/data` - 挂载点
- `ext4` - 文件系统类型
- `defaults` - 挂载选项
- `0` - 不备份
- `2` - 启动时检查文件系统

### 4.4 测试挂载配置

```bash
# 测试 fstab 配置（不实际挂载）
sudo mount -a

# 如果出错，检查日志
dmesg | tail

# 验证挂载
df -h | grep /mnt/data
```

---

## 📝 完整示例：从 U 盘拷贝文件

### 场景：从 U 盘拷贝 Python 项目到服务器

```bash
# 1. 插入 U 盘，查看设备
lsblk

# 2. 创建挂载点
sudo mkdir -p /mnt/usb

# 3. 挂载 U 盘（假设是 /dev/sdb1）
sudo mount /dev/sdb1 /mnt/usb

# 4. 查看 U 盘内容
ls -la /mnt/usb

# 5. 创建目标目录
sudo mkdir -p /opt/face-service

# 6. 拷贝文件
sudo cp -r /mnt/usb/python-face/* /opt/face-service/

# 7. 设置文件权限
sudo chown -R $USER:$USER /opt/face-service
chmod +x /opt/face-service/build_http_service.sh

# 8. 验证文件
cd /opt/face-service
ls -la

# 9. 卸载 U 盘
sudo umount /mnt/usb
```

---

## 🔍 常用命令参考

### 查看磁盘和分区

```bash
# 查看所有磁盘
lsblk

# 查看磁盘使用情况
df -h

# 查看分区信息
sudo fdisk -l

# 查看文件系统类型
sudo blkid
```

### 挂载和卸载

```bash
# 挂载
sudo mount /dev/sdb1 /mnt/data

# 卸载
sudo umount /mnt/data

# 强制卸载（如果设备忙）
sudo umount -l /mnt/data

# 查看所有挂载点
mount | grep /mnt
```

### 文件拷贝

```bash
# 拷贝目录（递归）
cp -r /source/dir /target/dir

# 拷贝并显示进度
rsync -av --progress /source/ /target/

# 拷贝并保留权限
cp -rp /source/ /target/

# 只拷贝文件（不包括目录）
cp /source/* /target/
```

---

## ⚠️ 注意事项

### 1. 权限问题

```bash
# 如果拷贝后无法访问，修改权限
sudo chown -R $USER:$USER /opt/face-service
chmod +x /opt/face-service/build_http_service.sh
```

### 2. 磁盘空间

```bash
# 拷贝前检查磁盘空间
df -h /opt

# 检查文件大小
du -sh /mnt/data/python-face
```

### 3. 文件系统兼容性

- **ext4** - Linux 原生，推荐
- **NTFS** - Windows 格式，需要安装 `ntfs-3g`
- **FAT32** - 通用格式，但文件大小限制 4GB

### 4. 卸载前确保没有进程使用

```bash
# 查看哪些进程在使用挂载点
lsof /mnt/data

# 或
fuser -m /mnt/data

# 如果有进程，先结束或等待完成，再卸载
```

---

## ✅ 快速参考

### 从 U 盘拷贝到项目目录

```bash
# 1. 查看 U 盘设备
lsblk

# 2. 挂载
sudo mkdir -p /mnt/usb
sudo mount /dev/sdb1 /mnt/usb

# 3. 拷贝
sudo mkdir -p /opt/face-service
sudo cp -r /mnt/usb/python-face/* /opt/face-service/

# 4. 设置权限
sudo chown -R $USER:$USER /opt/face-service

# 5. 卸载
sudo umount /mnt/usb
```

### 从其他分区拷贝

```bash
# 1. 查看分区
lsblk

# 2. 挂载分区
sudo mkdir -p /mnt/data
sudo mount /dev/sda3 /mnt/data

# 3. 拷贝
sudo cp -r /mnt/data/python-face/* /opt/face-service/
```

---

## 🎯 你的场景：拷贝 Python 项目

假设你的文件在某个磁盘或 U 盘上：

```bash
# 1. 查看所有磁盘和分区
lsblk

# 2. 假设文件在 /dev/sdb1，挂载到 /mnt/data
sudo mkdir -p /mnt/data
sudo mount /dev/sdb1 /mnt/data

# 3. 查看文件位置
ls -la /mnt/data/

# 4. 创建项目目录
sudo mkdir -p /opt/face-service

# 5. 拷贝必需文件
sudo cp /mnt/data/python-face/face_service.py /opt/face-service/
sudo cp /mnt/data/python-face/face_extractor.py /opt/face-service/
sudo cp /mnt/data/python-face/requirements.txt /opt/face-service/
sudo cp /mnt/data/python-face/build_http_service.sh /opt/face-service/

# 6. 设置权限
sudo chown -R $USER:$USER /opt/face-service
chmod +x /opt/face-service/build_http_service.sh

# 7. 验证
cd /opt/face-service
ls -la

# 8. 卸载（可选）
sudo umount /mnt/data
```

完成！现在可以继续安装依赖和编译了。


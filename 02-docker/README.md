# Docker

## 学习进度

- [x] Docker 安装
- [x] Image
- [x] Container
- [x] Container Lifecycle
- [x] Volume
- [ ] Bind Mount
- [ ] Network
- [ ] Dockerfile
- [ ] Docker Compose

---

# 1. Image

## 概念

- Image 是只读模板（Read-only Template）
- 用于创建 Container
- 一个 Image 可以创建多个 Container

```
Image
   │
docker run
   ▼
Container
```

## 命令

| 命令 | 作用 |
|------|------|
| `docker images` | 查看镜像 |
| `docker pull ubuntu` | 拉取 Ubuntu 镜像 |

## 实验

```bash
docker pull ubuntu
docker images
```

---

# 2. Container

## 概念

- Container 是 Image 的运行实例
- 可以创建、启动、停止、删除
- 一个 Image 可以对应多个 Container

```
Image
   │
docker run
   ▼
Container
```

## 命令

| 命令 | 作用 |
|------|------|
| `docker run -it ubuntu bash` | 创建并进入容器 |
| `docker exec -it <container> bash` | 进入运行中的容器 |
| `docker ps` | 查看运行中的容器 |
| `docker ps -a` | 查看所有容器 |

## 实验

```bash
docker run -it ubuntu bash
exit

docker ps
docker ps -a
```

---

# 3. Container Lifecycle

## 概念

```
Created
   │
   ▼
Running
   │
   ▼
Exited
   │
   ▼
Removed
```

## 命令

| 命令 | 作用 |
|------|------|
| `docker run` | 创建并启动 |
| `docker stop` | 停止 |
| `docker start` | 启动 |
| `docker rm` | 删除 |

## 实验

```bash
docker run -dit --name myubuntu ubuntu

docker stop myubuntu

docker start myubuntu

docker exec -it myubuntu bash
exit

docker rm -f myubuntu
```

---

# 4. Volume

## 概念

- Volume 用于持久化数据
- 删除 Container 不会删除 Volume

```
Volume
   │
   ├── Container A
   └── Container B
```

## 命令

| 命令 | 作用 |
|------|------|
| `docker volume ls` | 查看 Volume |
| `docker volume create mydata` | 创建 Volume |
| `docker volume inspect mydata` | 查看详情 |

## 实验

```bash
docker volume create mydata

docker run -it \
--name volume-test \
-v mydata:/data \
ubuntu bash

cd /data
echo "Hello Volume" > test.txt
exit

docker rm -f volume-test

docker run -it \
--name volume-test2 \
-v mydata:/data \
ubuntu bash

cd /data
cat test.txt
```

---

# 5. Bind Mount

## 概念

- 将宿主机目录挂载到 Container
- 宿主机和 Container 操作同一份文件
- 常用于代码开发

```
Host Directory
      │
      ▼
Container Directory
```

## 命令

| 命令 | 作用 |
|------|------|
| `docker run -v <host>:<container>` | 挂载宿主机目录 |

## 实验

```bash
mkdir ~/docker-bind
echo "Hello Docker" > ~/docker-bind/test.txt

docker run -it \
-v ~/docker-bind:/app \
ubuntu bash

cat /app/test.txt
```

---

# 6. Network

## 概念

- Network 用于多个 Container 通信
- 同一 Network 中可通过容器名访问

```
Network
│
├── ubuntu1
└── ubuntu2
```

## 命令

| 命令 | 作用 |
|------|------|
| `docker network ls` | 查看 Network |
| `docker network create <name>` | 创建 Network |

## 实验

```bash
docker network create mynetwork

docker run -dit --name ubuntu1 --network mynetwork ubuntu

docker run -dit --name ubuntu2 --network mynetwork ubuntu
```

---

# 7. Dockerfile

## 概念

- Dockerfile 用于构建 Image

```
Dockerfile
      │
docker build
      ▼
Image
      │
docker run
      ▼
Container
```

## 核心指令

| 指令 | 作用 |
|------|------|
| `FROM` | 基础镜像 |
| `RUN` | 构建时执行命令 |
| `COPY` | 复制文件到镜像 |
| `CMD` | 容器启动时执行 |

## 实验

```dockerfile
FROM ubuntu

RUN apt update

COPY hello.txt /hello.txt

CMD ["cat","/hello.txt"]
```

```bash
docker build -t hello-image .
docker run hello-image
```

---

# 8. Docker Compose

## 概念

- 使用一个 YAML 文件管理多个 Container

```
compose.yaml
      │
docker compose up
      ▼
Containers
```

## 常用命令

| 命令 | 作用 |
|------|------|
| `docker compose up -d` | 后台启动 |
| `docker compose down` | 停止并删除 |

## 实验

```yaml
services:
  ubuntu:
    image: ubuntu
    command: sleep infinity
```

```bash
docker compose up -d
docker compose down
```
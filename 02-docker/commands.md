# Docker Commands Cheat Sheet

## Image

| 命令 | 说明 |
|------|------|
| `docker images` | 查看本地镜像 |
| `docker pull <image>` | 拉取镜像 |
| `docker rmi <image>` | 删除镜像 |

---

## Container

| 命令 | 说明 |
|------|------|
| `docker ps` | 查看运行中的容器 |
| `docker ps -a` | 查看所有容器 |
| `docker run <image>` | 创建并启动容器 |
| `docker run -it <image> bash` | 交互式进入容器 |
| `docker exec -it <container> bash` | 进入运行中的容器 |
| `docker stop <container>` | 停止容器 |
| `docker start <container>` | 启动容器 |
| `docker restart <container>` | 重启容器 |
| `docker rm <container>` | 删除容器 |
| `docker rm -f <container>` | 强制删除容器 |

---

## Volume

| 命令 | 说明 |
|------|------|
| `docker volume ls` | 查看 Volume |
| `docker volume create <name>` | 创建 Volume |
| `docker volume inspect <name>` | 查看 Volume 详情 |
| `docker volume rm <name>` | 删除 Volume |

---

## 常用示例

### 创建 Ubuntu 容器

```bash
docker run -it ubuntu bash
```

### 创建后台容器

```bash
docker run -dit --name myubuntu ubuntu
```

### 挂载 Volume

```bash
docker run -it \
--name volume-test \
-v mydata:/data \
ubuntu bash
```

---

## Network

| 命令 | 说明 |
|------|------|
| `docker network ls` | 查看 Network |
| `docker network create <name>` | 创建 Network |
| `docker network inspect <name>` | 查看 Network |
| `docker network rm <name>` | 删除 Network |

---

## Dockerfile

| 命令 | 说明 |
|------|------|
| `docker build -t <image> .` | 构建镜像 |

---

## Docker Compose

| 命令 | 说明 |
|------|------|
| `docker compose up -d` | 后台启动 |
| `docker compose down` | 停止并删除 |
| `docker compose ps` | 查看服务 |
| `docker compose logs` | 查看日志 |
| `docker compose restart` | 重启服务 |
# Git

## 学习进度

- [x] Git 安装
- [x] Git 配置
- [x] git init
- [x] git status
- [x] git diff
- [x] git add
- [x] git commit
- [x] git log
- [x] .gitignore
- [x] GitHub Remote
- [x] git push

---

# 1. Git 基本概念

## 概念

- Git 用于管理文件版本
- 每次 commit 都是一次版本保存
- GitHub 用于保存远程仓库

```
Working Directory
        │
        │ git add
        ▼
Staging Area
        │
        │ git commit
        ▼
Local Repository
        │
        │ git push
        ▼
GitHub Repository
```

---

# 2. 本地仓库

## 概念

- 本地仓库保存在当前项目目录
- `git init` 后，项目目录变成 Git 仓库

## 命令

| 命令 | 作用 |
|------|------|
| `git init` | 初始化仓库 |
| `git status` | 查看状态 |
| `git diff` | 查看修改内容 |
| `git add .` | 添加修改到暂存区 |
| `git commit -m "message"` | 提交版本 |
| `git log --oneline` | 查看提交历史 |
| `git config --global user.name "xxx"` | 配置git用户名 |
| `git config --global user.email "xxx"` | 配置git邮箱 |
| `git config user.name` | 查看git用户名 |
| `git config user.email` | 查看git邮箱 |

## 实验

```bash
git init
git status
git add .
git commit -m "Add notes"
git log --oneline
```

---

# 3. .gitignore

## 概念

- `.gitignore` 用于排除不需要提交的文件
- 常见排除：缓存、日志、虚拟环境、敏感配置、数据文件

## 示例

```gitignore
__pycache__/
*.pyc
.venv/
venv/

*.log
logs/

.env

.vscode/

.DS_Store
Thumbs.db

*.csv
*.parquet
*.json
```

---

# 4. GitHub Remote

## 概念

- Remote Repository 是 GitHub 上的远程仓库
- `origin` 是远程仓库的默认名称
- `git push` 将本地提交推送到 GitHub

```
Local Repository
        │
        │ git push
        ▼
GitHub Repository
```

## 命令

| 命令 | 作用 |
|------|------|
| `git remote add origin <url>` | 连接远程仓库 |
| `git remote -v` | 查看远程仓库 |
| `git branch -M main` | 设置主分支为 main |
| `git push -u origin main` | 第一次推送 |
| `git push` | 后续推送 |

## 实验

```bash
git remote add origin https://github.com/<username>/<repo>.git

git branch -M main

git push -u origin main
```

---

# 5. 日常工作流

```bash
git status
git diff
git add .
git commit -m "Update notes"
git push
```

---

# 6. 注意事项

- 不要提交密码、Token、Access Key
- 不要提交大数据文件
- 不要提交 `.env`
- 空文件夹不会被 Git 提交，可用 `.gitkeep` 占位
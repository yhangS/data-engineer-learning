# Git Commands Cheat Sheet

## Basic

| 命令 | 说明 |
|------|------|
| `git --version` | 查看 Git 版本 |
| `git init` | 初始化仓库 |
| `git status` | 查看状态 |
| `git diff` | 查看修改 |
| `git add .` | 添加所有修改 |
| `git commit -m "message"` | 提交版本 |
| `git log --oneline` | 查看提交历史 |

---

## Remote

| 命令 | 说明 |
|------|------|
| `git remote add origin <url>` | 添加远程仓库 |
| `git remote -v` | 查看远程仓库 |
| `git branch -M main` | 修改主分支名 |
| `git push -u origin main` | 第一次推送 |
| `git push` | 推送到 GitHub |

---

## 常用流程

```bash
git status
git diff
git add .
git commit -m "Update notes"
git push
```

---

## Empty Folder

Git 不会提交空文件夹。

```bash
touch .gitkeep
```
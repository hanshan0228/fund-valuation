# GitHub 操作指南

## 📦 仓库信息

- **仓库地址**: https://github.com/Cabbage-xz/fund-valuation
- **用户名**: Cabbage-xz
- **分支**: main

## 🚀 常用Git命令

### 提交代码

```bash
# 1. 查看修改状态
git status

# 2. 添加所有修改的文件
git add .

# 或添加特定文件
git add backend/app/main.py

# 3. 提交修改
git commit -m "你的提交说明"

# 4. 推送到GitHub
git push
```

### 拉取最新代码

```bash
# 从GitHub拉取最新代码
git pull
```

### 查看提交历史

```bash
# 查看提交记录
git log

# 简化显示
git log --oneline

# 图形化显示
git log --graph --oneline --all
```

### 分支操作

```bash
# 查看所有分支
git branch -a

# 创建新分支
git branch feature/new-feature

# 切换分支
git checkout feature/new-feature

# 或创建并切换（推荐）
git checkout -b feature/new-feature

# 合并分支到main
git checkout main
git merge feature/new-feature

# 删除分支
git branch -d feature/new-feature
```

### 撤销修改

```bash
# 撤销工作区修改（未add）
git checkout -- filename

# 撤销暂存区修改（已add，未commit）
git reset HEAD filename

# 撤销最后一次提交（保留修改）
git reset --soft HEAD^

# 撤销最后一次提交（丢弃修改）⚠️
git reset --hard HEAD^
```

## 🌐 GitHub CLI 常用命令

### 仓库操作

```bash
# 查看仓库信息
gh repo view

# 在浏览器中打开仓库
gh repo view --web

# 克隆仓库
gh repo clone Cabbage-xz/fund-valuation

# 创建新仓库
gh repo create my-new-repo --public
```

### Issue管理

```bash
# 查看所有issues
gh issue list

# 创建issue
gh issue create --title "Bug: xxx" --body "描述"

# 查看issue详情
gh issue view 1

# 关闭issue
gh issue close 1
```

### Pull Request

```bash
# 创建PR
gh pr create --title "Feature: xxx" --body "说明"

# 查看PR列表
gh pr list

# 查看PR详情
gh pr view 1

# 合并PR
gh pr merge 1
```

### 查看状态

```bash
# 查看认证状态
gh auth status

# 查看当前用户
gh auth status | grep "Logged in"
```

## 📝 实用工作流

### 日常开发流程

```bash
# 1. 拉取最新代码
git pull

# 2. 创建功能分支
git checkout -b feature/add-export

# 3. 进行开发...
# 4. 添加修改
git add .

# 5. 提交修改
git commit -m "feat: 添加数据导出功能"

# 6. 推送到GitHub
git push -u origin feature/add-export

# 7. 在GitHub上创建PR
gh pr create --title "添加数据导出功能"

# 8. PR合并后，切换回main并更新
git checkout main
git pull
```

### 修复Bug流程

```bash
# 1. 创建bug修复分支
git checkout -b fix/ocr-recognition

# 2. 修复bug...
# 3. 提交
git add .
git commit -m "fix: 修复OCR识别准确率问题"

# 4. 推送并创建PR
git push -u origin fix/ocr-recognition
gh pr create --title "修复OCR识别问题"
```

### 快速提交推送

```bash
# 一行命令完成 add + commit + push
git add . && git commit -m "update: 更新README" && git push
```

## 🔧 配置优化

### 设置Git用户信息

```bash
# 全局设置
git config --global user.name "Cabbage-xz"
git config --global user.email "your-email@example.com"

# 查看配置
git config --list
```

### Git别名（快捷命令）

```bash
# 设置常用别名
git config --global alias.st status
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.cm commit
git config --global alias.ps push
git config --global alias.pl pull

# 使用别名
git st  # 等同于 git status
git co main  # 等同于 git checkout main
```

### 忽略文件权限变化

```bash
git config core.fileMode false
```

## 🔒 安全最佳实践

### .gitignore 配置

确保敏感文件不被上传：

```gitignore
# 环境变量
.env
.env.local
.env.*.local

# 数据库
*.db
*.sqlite

# 密钥
*.key
*.pem
secrets.json

# 依赖
node_modules/
venv/
```

### 检查提交内容

```bash
# 提交前查看将要提交的内容
git diff --staged
```

## 📊 GitHub仓库管理

### 在浏览器中管理

```bash
# 打开仓库主页
gh repo view --web

# 打开Issues页面
gh issue list --web

# 打开PR页面
gh pr list --web
```

### 仓库设置

访问: https://github.com/Cabbage-xz/fund-valuation/settings

可以设置：
- 仓库描述和主题
- 功能开关（Issues, Discussions等）
- 分支保护规则
- Secrets（用于GitHub Actions）
- Webhooks

## 🎯 协作开发

### Fork工作流

```bash
# 如果有其他贡献者Fork了你的仓库

# 1. 他们fork仓库并克隆
# 2. 创建分支开发
# 3. 推送到他们的fork
# 4. 创建PR到你的仓库

# 你可以：
# 查看PR
gh pr list

# 审查PR
gh pr review 1 --approve

# 合并PR
gh pr merge 1
```

## 📱 移动端访问

下载GitHub官方App:
- iOS: App Store搜索"GitHub"
- Android: Google Play搜索"GitHub"

可以在手机上：
- 查看代码
- 审查PR
- 回复Issue
- 查看提交历史

## 🆘 常见问题

### Q: 推送失败：rejected

```bash
# 原因：远程仓库有新提交
# 解决：先拉取再推送
git pull --rebase
git push
```

### Q: 合并冲突

```bash
# 1. 拉取时出现冲突
git pull

# 2. 手动解决冲突文件
# 3. 添加解决后的文件
git add .

# 4. 完成合并
git commit

# 5. 推送
git push
```

### Q: 误提交敏感信息

```bash
# ⚠️ 如果已经推送到GitHub，需要：
# 1. 立即修改密码/密钥
# 2. 从历史中删除（复杂，建议重新创建仓库）

# 如果还未推送：
git reset --soft HEAD^
# 删除敏感文件
git add .
git commit -m "fix: 移除敏感信息"
```

### Q: 克隆速度慢

```bash
# 使用GitHub CLI
gh repo clone Cabbage-xz/fund-valuation

# 或浅克隆（只获取最近的提交）
git clone --depth 1 https://github.com/Cabbage-xz/fund-valuation.git
```

## 📚 学习资源

- Git官方文档: https://git-scm.com/doc
- GitHub文档: https://docs.github.com
- GitHub CLI文档: https://cli.github.com/manual
- 交互式学习: https://learngitbranching.js.org

## 🎓 Pro Tips

1. **提交信息规范**：
   - `feat:` 新功能
   - `fix:` 修复bug
   - `docs:` 文档更新
   - `style:` 代码格式
   - `refactor:` 重构
   - `test:` 测试
   - `chore:` 构建/工具

2. **使用.gitattributes**：
   统一行尾符，避免跨平台问题

3. **定期同步**：
   每天开始工作前 `git pull`

4. **小步提交**：
   频繁提交，每次提交一个完整功能

5. **有意义的分支名**：
   - `feature/user-auth`
   - `fix/login-bug`
   - `refactor/api-service`

---

💡 **快速参考**：
- 提交推送: `git add . && git commit -m "message" && git push`
- 查看状态: `git status`
- 查看仓库: `gh repo view --web`

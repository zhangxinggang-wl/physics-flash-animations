# 部署到 GitHub Pages

把这份 Flash 动画库发布到网上，任何人打开链接就能在线播放（无需安装任何东西）。

---

## 一、准备工作：确认本地仓库已就绪

本地 git 仓库已经建好，**无需再做任何配置**。

当前位置：`桌面\系列讲座\高中物理动画\_按章节归档\`

| 项目 | 状态 |
|---|---|
| git 仓库 | ✅ 已初始化（分支 `main`） |
| 提交记录 | ✅ 3 次提交，1395 个文件 |
| 上传体积 | **129.3 MB**（SWF 100.9 MB + Ruffle 28.3 MB） |
| `.exe` 文件 | ✅ 已排除（113 个 / 295 MB，浏览器跑不了） |
| 单文件最大 | 13.67 MB（**远低于 GitHub 100 MB 硬限制**） |

> 为什么排除 exe：它们占总体积的 74.5%，而浏览器根本无法运行 exe。
> 排除后上传量从 396 MB 降到 129 MB。本地使用不受影响，exe 原件仍在磁盘上。

---

## 二、第一步：在 GitHub 上建一个空仓库

打开 → **https://github.com/new**

填写：

| 字段 | 填什么 |
|---|---|
| Repository name | `physics-flash-animations`（或任意名字） |
| Description | 高中物理 Flash 教学动画库（可留空） |
| Visibility | **Public** —— 免费版 GitHub Pages 只支持公开仓库 |
| Initialize this repository with | **三个勾全部不勾**（不加 README、不加 .gitignore、不加 license） |

点 **Create repository**。

建完后页面会显示一个地址，形如：

```
https://github.com/zhangxinggang-wl/physics-flash-animations.git
```

**把这个地址复制下来**，下一步要用。

> ⚠️ 如果建仓库时勾了 README，仓库就不是空的，推送会被拒。
> 遇到这种情况：删掉仓库重建，或者先执行 `git pull --rebase origin main` 再推。

---

## 三、第二步：一键推送

双击归档目录里的 **`PushToGitHub.bat`**。

脚本会：
1. 提示你粘贴仓库地址
2. 自动设置 remote
3. 执行 `git push -u origin main`
4. 完成后打印 GitHub Pages 的开启步骤

**上传 129 MB，需要几分钟，请耐心等待。**

### 关于密码（最容易卡住的地方）

推送时 Git 会问用户名和密码。注意：

- **用户名** = 你的 GitHub 用户名
- **密码** ≠ 你的账号登录密码，而是 **Personal Access Token**

生成 Token：

1. 打开 **https://github.com/settings/tokens**
2. 点 **Generate new token** → **Generate new token (classic)**
3. Note 随便填，比如 `push-physics-anim`
4. Expiration 选 90 days 或 No expiration
5. **勾选 `repo`**（必须，否则无法推送）
6. 拉到最下面点 **Generate token**
7. **立刻复制**那串 `ghp_...` 开头的字符（离开页面就再也看不到了）
8. 推送时把它粘贴到密码位置

> Token 只需生成一次。Windows 的凭据管理器会记住它，之后推送不用再输。

---

## 四、第三步：开启 GitHub Pages

推送成功后，打开你的仓库页面：

**Settings** → 左侧找到 **Pages**

| 字段 | 选什么 |
|---|---|
| Source | Deploy from a branch |
| Branch | `main` |
| Folder | `/ (root)` |

点 **Save**，等约 1 分钟。

刷新页面，顶部会出现你的网址：

```
https://zhangxinggang-wl.github.io/physics-flash-animations/
```

**打开它 → 就是导航页 → 点任意卡片 → Ruffle 直接在线播放。**

---

## 五、在线播放的原理

浏览器 2020 年就彻底移除了 Flash 支持，所以 `.swf` 直接放是放不了的。

本方案用 **Ruffle**（用 Rust 写的 Flash 模拟器，编译成 WebAssembly）在浏览器里"重演"Flash 运行时。

文件都在仓库的 `ruffle/` 目录里（**自托管**，不依赖外部 CDN）：

| 文件 | 大小 | 作用 |
|---|---|---|
| `ruffle.js` | 465 KB | 入口脚本 |
| `core.ruffle.c80159b526e567babaf5.js` | 106 KB | 核心分包 |
| `core.ruffle.f000070ea72f8ae4fe3a.js` | 112 KB | 核心分包 |
| `826bb0938097485a2c9d.wasm` | 13.6 MB | 主运行时 |
| `72a20ef1c0b8ceb37720.wasm` | 13.6 MB | 第二运行时 |

播放流程：

```
点卡片
  → player.html?f=00-初中物理/密度.swf
  → ruffle.js 加载 wasm 运行时
  → Ruffle 从同目录拉取该 .swf
  → 在 <canvas> 里渲染播放
```

**实测已验证**（用 Chromium 无头浏览器跑了三组测试）：

| 请求 | 结果 |
|---|---|
| `ruffle.js` | 200 ✅ |
| 两个 js 分包 | 200 ✅ |
| `826bb093...wasm` | 200 ✅ |
| `00-初中物理/密度.swf` | 200 ✅ |

截图确认：Ruffle 完整渲染出了 Flash 画面（山水背景 + 红色「密度」标题 + 播放按钮）。

> 注意：首次打开播放页要下载约 14 MB 的 wasm，慢几秒属正常。
> 之后浏览器会缓存，再打开就很快了。

---

## 六、本地使用（不联网也能用）

在线版只包含 SWF。要在本地用，有三种方式，任选：

### 方式 1：GUI 启动器（推荐）

双击 **`PlayFlash.bat`** → 弹出图形界面：

- 左侧章节树（18 章 + 全部，带计数）
- 顶部实时搜索
- 右侧列表**双击即播**
- 底部：播放选中 / 打开所在文件夹 / 打开播放器

### 方式 2：直接双击 SWF

`.swf` 文件关联是完好的，双击任意 `.swf` 就会用播放器打开。这是最省事的。

### 方式 3：拖进播放器

把 `.swf` 拖到 `flashplayer（动画播放器）.exe` 窗口里。

---

## 七、后续更新

改了页面或补了新动画，在归档目录执行：

```bash
git add -A
git commit -m "更新说明"
git push
```

`PushToGitHub.bat` 也可以重复运行（它会先移除旧的 remote 再重新添加，不会报错）。

---

## 八、已知限制

| 限制 | 说明 |
|---|---|
| exe 不在线上 | 113 个 exe（295 MB）被排除，浏览器无法运行 |
| 首次加载慢 | 需下载 14 MB wasm，之后走缓存 |
| 部分动画兼容性 | Ruffle 对 ActionScript 3.0 支持已很成熟，但个别老动画（尤其涉及复杂视频/3D）可能表现不完全一致 |
| 仓库体积 | 129 MB，在 GitHub 1 GB 限制内，但已不适合继续大量堆文件 |
| 免费流量 | GitHub Pages 每月约 100 GB 软限制，个人教学使用远远够 |

---

## 九、如果推送失败

先看脚本打印的错误提示。高频原因：

| 现象 | 原因 | 解决 |
|---|---|---|
| `Authentication failed` | 密码填了账号密码 | 改成 Personal Access Token（见第三节） |
| `remote: Repository not found` | 仓库名或用户名写错 / 仓库不存在 | 检查 URL |
| `! [rejected] main -> main (fetch first)` | 建仓库时勾了 README，仓库非空 | 删掉仓库重建，或先 `git pull --rebase origin main` |
| `Failed to connect to github.com` | 网络/代理问题 | 稍后重试；公司网络可能需配置代理 |
| 卡在 `Writing objects` 很久 | 129 MB 上传慢 | 正常，耐心等，别关窗口 |

修好原因后，**直接再双击一次脚本**即可，git 会从断点继续。

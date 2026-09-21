# Flash 物理教学动画资源库

> 人教版高中物理 · **1381 个 Flash 教学动画** · 按章节归档 · **浏览器直接在线播放**

张兴刚工作室（河北省沧州市第一中学）

---

## 这是什么

一个把散落在本地硬盘的 Flash 物理教学动画，整理成**按人教版章节归档**、并且**能在浏览器里直接播放**的资源站。

所有动画原本都是 `.swf` 格式。Adobe 已于 2020 年底彻底停止 Flash 支持，Chrome / Edge / Firefox 全部移除了 Flash 运行能力，所以这些动画在过去几年里基本处于"没法在网页上看"的状态。

本站使用 **[Ruffle](https://ruffle.rs/)**（用 Rust + WebAssembly 重写的开源 Flash 模拟器）在浏览器中还原播放能力，**不需要安装任何插件，也不需要 Flash Player**。

---

## 在线访问

部署到 GitHub Pages 后，访问地址形如：

```
https://<你的用户名>.github.io/<仓库名>/
```

**使用方式**：在目录页搜索或浏览 → 点击任意卡片 → 在新标签页中播放。

播放页支持：

| 操作 | 说明 |
|---|---|
| 返回目录 | 顶部按钮，或按 `Backspace` |
| 全屏 | 顶部按钮，或按 `F` |
| 重新加载 | 顶部按钮，或按 `R` |

---

## 章节分布

| 章节 | 动画数 | 章节 | 动画数 |
|---|---:|---|---:|
| 初中物理 | 69 | 机械振动与波 | 93 |
| 直线运动 | 44 | 光学 | 109 |
| 相互作用与力 | 44 | 热学与分子动理论 | 48 |
| 牛顿运动定律 | 55 | 原子物理与核物理 | 32 |
| 曲线运动与抛体 | 63 | 实验仪器与测量 | 62 |
| 万有引力与航天 | 22 | 电路与电学基础 | 50 |
| 机械能与功 | 36 | 待识别 | 474 |
| 电场与磁场 | 76 | | |
| 电磁感应 | 47 | **合计** | **1381** |
| 交变电流与电磁波 | 30 | | |
| 动量守恒 | 27 | | |

### 关于「待识别」的 474 个文件

约 34% 的动画文件名是纯编号（`001.swf` ~ `096.swf`）、P 系列编码（如 `PX3005.swf`）或无意义短名（`（二）.swf`、`钟.swf`），无法从文件名判断所属章节。

SWF 内部文字采用 Flash 位压缩编码，无法直接提取中文标题。为避免误归档，这批文件统一放入 `99-待识别/`，未做任何猜测性重命名。

---

## 目录结构

```
.
├── index.html                  # 目录页：搜索 + 章节导航 + 1381 张卡片
├── player.html                 # 播放页：加载 Ruffle 并播放指定动画
├── ruffle/                     # Ruffle 播放引擎（自托管，共 27.9 MB）
│   ├── ruffle.js
│   ├── core.ruffle.f000070ea72f8ae4fe3a.js
│   ├── core.ruffle.c80159b526e567babaf5.js
│   ├── 72a20ef1c0b8ceb37720.wasm
│   └── 826bb0938097485a2c9d.wasm
├── 00-初中物理/                # 各章节动画（.swf）
├── 01-直线运动/
│   ├── ...
├── 91-电路与电学基础/
├── 99-待识别/
│
├── PlayFlash.bat               # 【离线方案】本地启动器（Windows）
├── FlashAnimationPlayer.pyw    # 【离线方案】本地 GUI 播放器
└── 使用说明.md                  # 详细使用文档
```

---

## 技术说明

### 为什么需要 Ruffle

`.swf` 是 Adobe Flash 的专有格式。Flash Player 已于 2020 年 12 月 31 日停止支持，所有主流浏览器都移除了播放能力。

Ruffle 用 Rust 重新实现了 Flash 运行时，编译为 WebAssembly 在浏览器中执行，因而可以在不安装插件的前提下播放绝大多数 Flash 内容（对 ActionScript 2 支持最好，ActionScript 3 覆盖度持续提升）。

### 播放链路

```
index.html  ──点击卡片──▶  player.html?f=<章节/动画.swf>
                                    │
                                    ├─ 加载 ruffle/ruffle.js
                                    ├─ Ruffle 按需拉取 wasm 与 chunk
                                    └─ 请求并渲染该 .swf
```

### 关于 wasm 的 MIME 类型

Ruffle 依赖 `.wasm` 文件以 `application/wasm` 类型返回。本地调试若使用简易静态服务器可能遇到 `Incorrect response MIME type` 报错，GitHub Pages 会自动返回正确类型，无需额外配置。

---

## 本地离线使用

如果不想走网络，可以在本地直接播放：

**方式一（推荐）**：双击 `PlayFlash.bat`

会打开一个图形启动器：左侧按章节筛选、顶部关键词搜索、**双击列表项直接播放**。

**方式二**：在文件资源管理器中进入任意章节文件夹，双击 `.swf` 文件（需已配置文件关联）。

> 注意：直接用 `file://` 双击打开 `index.html` 时，浏览器会因跨域限制无法加载 Ruffle 的 wasm，**在线播放功能在 `file://` 下不可用**。本地请用上面两种方式。

---

## 部署到 GitHub Pages

> **本地 git 仓库已经建好了**（分支 `main`，4 次提交，跟踪 1395 个文件）。
> 你只需要：建远程仓库 → 推送 → 开 Pages。详细步骤见 **[部署到GitHub.md](部署到GitHub.md)**。

### 三步走

**第一步：在 GitHub 上建一个空仓库**

打开 https://github.com/new，填写仓库名（如 `physics-flash-animations`），
可见性选 **Public**（免费版 Pages 只支持公开仓库），
**三个初始化选项全部不勾**（不要加 README / .gitignore / license）。

建好后复制仓库地址，形如 `https://github.com/<用户名>/<仓库名>.git`。

**第二步：双击 `PushToGitHub.bat` 推送**

脚本会提示你粘贴仓库地址，然后自动完成 `git remote add` 与 `git push -u origin main`。

上传约 129 MB，需要几分钟。

> 推送时会要求输入密码 —— 必须填 **Personal Access Token**，不是账号密码。
> 在 https://github.com/settings/tokens 生成（classic 类型，勾选 `repo`）。

**第三步：开启 GitHub Pages**

仓库页面 → **Settings** → **Pages** →
Source 选 `Deploy from a branch`，Branch 选 `main`，目录选 `/ (root)` → **Save**。

等约 1 分钟，访问：

```
https://<用户名>.github.io/<仓库名>/
```

### 手动命令行方式（等价）

```bash
cd _按章节归档
git remote add origin https://github.com/<用户名>/<仓库名>.git
git push -u origin main
```

### 注意事项

- 仓库体积约 **129 MB**（1381 个 SWF 共 101 MB + Ruffle 28 MB），首次推送视网速可能需要几分钟
- 单文件最大 13.67 MB，远小于 GitHub 的 100 MB 上限，不需要 Git LFS
- `.exe` 已在 `.gitignore` 中排除（113 个 / 295 MB），不会被推送
- `.nojekyll` 已包含在仓库中 —— 缺了它 GitHub Pages 的 Jekyll 处理可能失败
- `github.io` 在中国大陆访问可能较慢或不稳定，必要时需代理

---

## 版权与使用

本站动画来自公开网络的教学资源，仅供物理教学与学习参考使用。Ruffle 采用 MIT / Apache-2.0 双协议开源。

如涉及版权问题，请联系删除。

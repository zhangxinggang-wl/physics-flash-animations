# -*- coding: utf-8 -*-
"""
Flash 物理动画启动器（GUI 版）
- 双击本文件（.pyw 无黑窗）即可运行
- 左侧章节树 / 右侧动画列表 / 顶部搜索
- 单击选中，双击用内置播放器打开
"""
import os
import sys
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox

BASE = os.path.dirname(os.path.abspath(__file__))
PLAYER_CANDIDATES = [
    os.path.join(BASE, "flashplayer（动画播放器）.exe"),
    os.path.join(BASE, "..", "flashplayer（动画播放器）.exe"),
]

def find_player():
    for p in PLAYER_CANDIDATES:
        if os.path.isfile(p):
            return os.path.normpath(p)
    return None

PLAYER = find_player()

# 章节中文名
CH_NAMES = {
    "00-初中物理": "初中物理",
    "01-直线运动": "直线运动",
    "02-相互作用与力": "相互作用与力",
    "03-牛顿运动定律": "牛顿运动定律",
    "04-曲线运动与抛体": "曲线运动与抛体",
    "05-万有引力与航天": "万有引力与航天",
    "06-机械能与功": "机械能与功",
    "07-电场与磁场": "电场与磁场",
    "08-电磁感应": "电磁感应",
    "09-交变电流与电磁波": "交变电流与电磁波",
    "10-动量守恒": "动量守恒",
    "11-机械振动与波": "机械振动与波",
    "12-光学": "光学",
    "13-热学与分子动理论": "热学与分子动理论",
    "14-原子物理与核物理": "原子物理与核物理",
    "90-实验仪器与测量": "实验仪器与测量",
    "91-电路与电学基础": "电路与电学基础",
    "99-待识别": "待识别",
}

class App:
    def __init__(self, root):
        self.root = root
        self.all_items = []      # [(章节目录, 文件名, 完整路径)]
        self.filtered = []

        root.title("Flash 物理教学动画启动器 · 张兴刚工作室")
        root.geometry("1080x680")
        root.minsize(820, 520)

        # 深色顶栏
        top = tk.Frame(root, bg="#1e293b", height=56)
        top.pack(fill="x")
        top.pack_propagate(False)
        tk.Label(top, text="Flash 物理教学动画启动器", bg="#1e293b", fg="#ffffff",
                 font=("Microsoft YaHei", 13, "bold")).pack(side="left", padx=18)
        self.stat = tk.Label(top, text="", bg="#1e293b", fg="#94a3b8",
                             font=("Microsoft YaHei", 9))
        self.stat.pack(side="right", padx=18)

        # 搜索栏
        bar = tk.Frame(root, bg="#f0f2f5")
        bar.pack(fill="x", padx=14, pady=(10, 4))
        tk.Label(bar, text="搜索：", bg="#f0f2f5",
                 font=("Microsoft YaHei", 10)).pack(side="left")
        self.q = tk.StringVar()
        ent = tk.Entry(bar, textvariable=self.q, font=("Microsoft YaHei", 10),
                       relief="solid", bd=1)
        ent.pack(side="left", fill="x", expand=True, padx=(0, 8), ipady=3)
        ent.bind("<KeyRelease>", lambda e: self.refresh_list())
        tk.Button(bar, text="清空", font=("Microsoft YaHei", 9),
                  relief="solid", bd=1, command=self.clear_q).pack(side="left")

        # 主体
        body = tk.Frame(root, bg="#f0f2f5")
        body.pack(fill="both", expand=True, padx=14, pady=(4, 12))

        # 左：章节
        left = tk.Frame(body, bg="#ffffff", highlightbackground="#e2e8f0",
                        highlightthickness=1, width=190)
        left.pack(side="left", fill="y")
        left.pack_propagate(False)
        tk.Label(left, text="章节", bg="#ffffff", fg="#1e293b",
                 font=("Microsoft YaHei", 10, "bold")).pack(anchor="w", padx=12, pady=(10, 6))
        self.ch_list = tk.Listbox(left, font=("Microsoft YaHei", 10), relief="flat",
                                  selectbackground="#2563eb", selectforeground="#ffffff",
                                  activestyle="none", highlightthickness=0)
        self.ch_list.pack(fill="both", expand=True, padx=6, pady=(0, 8))
        self.ch_list.bind("<<ListboxSelect>>", lambda e: self.refresh_list())

        # 右：文件列表
        right = tk.Frame(body, bg="#ffffff", highlightbackground="#e2e8f0",
                         highlightthickness=1)
        right.pack(side="left", fill="both", expand=True, padx=(10, 0))

        cols = ("name", "ch")
        self.tree = ttk.Treeview(right, columns=cols, show="headings",
                                 selectmode="extended")
        self.tree.heading("name", text="动画名称")
        self.tree.heading("ch", text="章节")
        self.tree.column("name", width=620, anchor="w")
        self.tree.column("ch", width=150, anchor="center")
        vsb = ttk.Scrollbar(right, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        self.tree.pack(side="left", fill="both", expand=True, padx=(6, 0), pady=6)
        vsb.pack(side="right", fill="y", pady=6, padx=(0, 6))
        self.tree.bind("<Double-1>", self.open_selected)

        # 底部
        bot = tk.Frame(root, bg="#f0f2f5")
        bot.pack(fill="x", padx=14, pady=(0, 10))
        tk.Button(bot, text="▶ 播放选中", font=("Microsoft YaHei", 10, "bold"),
                  bg="#2563eb", fg="#ffffff", relief="flat", padx=18, pady=6,
                  cursor="hand2", command=self.open_selected).pack(side="left")
        tk.Button(bot, text="打开所在文件夹", font=("Microsoft YaHei", 10),
                  relief="solid", bd=1, padx=14, pady=6,
                  command=self.open_folder).pack(side="left", padx=8)
        tk.Button(bot, text="打开播放器", font=("Microsoft YaHei", 10),
                  relief="solid", bd=1, padx=14, pady=6,
                  command=self.open_player).pack(side="left")

        self.hint = tk.Label(bot, text="", bg="#f0f2f5", fg="#64748b",
                             font=("Microsoft YaHei", 9))
        self.hint.pack(side="right")

        self.scan()
        self.build_chapters()
        self.refresh_list()

        if not PLAYER:
            self.hint.config(text="⚠ 未找到播放器，将用系统默认程序打开", fg="#b45309")

    def scan(self):
        if not os.path.isdir(BASE):
            return
        for d in sorted(os.listdir(BASE)):
            full = os.path.join(BASE, d)
            if not os.path.isdir(full):
                continue
            if d not in CH_NAMES:
                continue
            for f in sorted(os.listdir(full)):
                if f.lower().endswith((".swf", ".exe")):
                    self.all_items.append((d, f, os.path.join(full, f)))

    def build_chapters(self):
        self.ch_list.insert("end", "全部章节")
        counts = {}
        for ch, _, _ in self.all_items:
            counts[ch] = counts.get(ch, 0) + 1
        for ch in sorted(CH_NAMES.keys()):
            if ch in counts:
                self.ch_list.insert("end", CH_NAMES[ch] + "  (" + str(counts[ch]) + ")")
        self.ch_list.selection_set(0)
        self.stat.config(text="共 " + str(len(self.all_items)) + " 个动画")

    def cur_chapter(self):
        sel = self.ch_list.curselection()
        if not sel or sel[0] == 0:
            return None
        label = self.ch_list.get(sel[0])
        for k, v in CH_NAMES.items():
            if label.startswith(v):
                return k
        return None

    def clear_q(self):
        self.q.set("")
        self.refresh_list()

    def refresh_list(self):
        kw = self.q.get().strip().lower()
        ch = self.cur_chapter()
        self.tree.delete(*self.tree.get_children())
        self.filtered = []
        for d, f, full in self.all_items:
            if ch and d != ch:
                continue
            if kw and kw not in f.lower():
                continue
            self.filtered.append(full)
            self.tree.insert("", "end", values=(os.path.splitext(f)[0], CH_NAMES.get(d, d)))
        self.stat.config(text="显示 " + str(len(self.filtered)) + " / " + str(len(self.all_items)) + " 个")

    def selected_paths(self):
        out = []
        for iid in self.tree.selection():
            idx = self.tree.index(iid)
            if 0 <= idx < len(self.filtered):
                out.append(self.filtered[idx])
        return out

    def open_selected(self, event=None):
        paths = self.selected_paths()
        if not paths:
            messagebox.showinfo("提示", "请先选中一个动画")
            return
        for p in paths:
            self.launch(p)

    def launch(self, path):
        try:
            if PLAYER:
                subprocess.Popen([PLAYER, path])
            else:
                os.startfile(path)
        except Exception as e:
            messagebox.showerror("打开失败", str(e))

    def open_folder(self):
        paths = self.selected_paths()
        if not paths:
            messagebox.showinfo("提示", "请先选中一个动画")
            return
        try:
            subprocess.Popen(["explorer", "/select,", os.path.normpath(paths[0])])
        except Exception as e:
            messagebox.showerror("打开失败", str(e))

    def open_player(self):
        if not PLAYER:
            messagebox.showwarning("提示", "未找到 flashplayer（动画播放器）.exe")
            return
        try:
            subprocess.Popen([PLAYER])
        except Exception as e:
            messagebox.showerror("打开失败", str(e))


def main():
    root = tk.Tk()
    App(root)
    root.mainloop()


if __name__ == "__main__":
    main()

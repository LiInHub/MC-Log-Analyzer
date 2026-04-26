import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json
import os
import requests
from requests.exceptions import Timeout

#配置文件路径（存储API密钥）
CONFIG_PATH = "mc_log_analyzer_config.json"

class MCLogAnalyzer:
    def __init__(self, root):
        self.root = root
        self.root.title("我的世界 日志分析工具 - deepseek API")
        self.root.geometry("850x950")
        self.root.resizable(False, False)

        #初始化变量
        self.api_keys = []
        self.selected_files = []
        self.load_api_keys()

        #API管理区域 
        api_frame = ttk.LabelFrame(root, text="deepseek API 管理")
        api_frame.place(x=20, y=10, width=800, height=120)

        ttk.Label(api_frame, text="选择API密钥：").place(x=10, y=10)
        self.api_var = tk.StringVar()
        self.api_combobox = ttk.Combobox(api_frame, textvariable=self.api_var, state="readonly", width=45)
        self.api_combobox.place(x=110, y=10)
        self.api_combobox.bind("<<ComboboxSelected>>", self.on_api_select)
        self.update_api_combobox()

        ttk.Label(api_frame, text="输入新API：").place(x=10, y=45)
        self.api_input = ttk.Entry(api_frame, width=48)
        self.api_input.place(x=110, y=45)

        ttk.Button(api_frame, text="保存API", command=self.save_api_key).place(x=450, y=10, width=100)
        ttk.Button(api_frame, text="删除选中API", command=self.delete_api_key).place(x=560, y=10, width=110)
        ttk.Button(api_frame, text="清空输入框", command=lambda: self.api_input.delete(0, tk.END)).place(x=680, y=10, width=100)

        #文件上传区域 
        file_frame = ttk.LabelFrame(root, text="日志文件上传。实例目录→ logs/latest.log 或 crash-reports")
        file_frame.place(x=20, y=140, width=800, height=100)

        self.file_label = ttk.Label(file_frame, text="未选择任何文件")
        self.file_label.place(x=10, y=10)
        ttk.Button(file_frame, text="选择日志文件", command=self.select_files).place(x=10, y=45, width=120)
        ttk.Button(file_frame, text="清空已选文件", command=self.clear_files).place(x=140, y=45, width=120)

        #分析按钮 
        self.analyze_btn = ttk.Button(root, text="开始分析日志", command=self.start_analyze)
        self.analyze_btn.place(x=350, y=255, width=150, height=40)

        #分析结果区域【拉长到底部】 
        result_frame = ttk.LabelFrame(root, text="分析结果")
        result_frame.place(x=20, y=310, width=800, height=625)

        self.result_text = tk.Text(result_frame, wrap=tk.WORD, font=("微软雅黑", 10), state=tk.DISABLED)
        self.result_text.place(x=10, y=10, width=780, height=595)
        scrollbar = ttk.Scrollbar(self.result_text, command=self.result_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.result_text.config(yscrollcommand=scrollbar.set)

    #Markdown转纯文本
    def clean_markdown(self, text):
        #一键清除所有markdown格式符号
        text = text.replace("#", "").replace("#", "")
        text = text.replace("**", "").replace("*", "")
        text = text.replace("`", "").replace("```", "")
        text = text.replace("> ", "")
        text = text.replace("---", "")
        text = text.replace("###", "").replace("##", "").replace("- ", "")
        return text.strip()

    #API管理
    def load_api_keys(self):
        if os.path.exists(CONFIG_PATH):
            try:
                with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                    self.api_keys = json.load(f)
            except:
                self.api_keys = []

    def save_api_keys(self):
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(self.api_keys, f, ensure_ascii=False, indent=2)

    def update_api_combobox(self):
        self.api_combobox["values"] = self.api_keys
        if self.api_keys:
            self.api_combobox.current(0)

    def on_api_select(self, event):
        self.api_input.delete(0, tk.END)
        self.api_input.insert(0, self.api_var.get())

    def save_api_key(self):
        api = self.api_input.get().strip()
        if not api:
            messagebox.showwarning("提示", "请输入有效的API密钥！")
            return
        if api in self.api_keys:
            messagebox.showinfo("提示", "该API已存在！")
            return
        self.api_keys.append(api)
        self.save_api_keys()
        self.update_api_combobox()
        messagebox.showinfo("成功", "API密钥保存成功！")

    def delete_api_key(self):
        current_api = self.api_var.get()
        if not current_api:
            messagebox.showwarning("提示", "请先选择要删除的API！")
            return
        self.api_keys.remove(current_api)
        self.save_api_keys()
        self.update_api_combobox()
        self.api_input.delete(0, tk.END)
        messagebox.showinfo("成功", "API密钥删除成功！")

    #文件选择
    def select_files(self):
        files = filedialog.askopenfilenames(
            title="选择我的世界日志文件",
            filetypes=[("日志文件", "*.log *.txt"), ("所有文件", "*.*")]
        )
        if files:
            self.selected_files = list(files)
            self.file_label.config(text=f"已选择 {len(self.selected_files)} 个文件")

    def clear_files(self):
        self.selected_files = []
        self.file_label.config(text="未选择任何文件")

    #日志分析
    def start_analyze(self):
        current_api = self.api_var.get()
        if not current_api:
            messagebox.showwarning("错误", "请先选择或添加API密钥！")
            return
        if not self.selected_files:
            messagebox.showwarning("错误", "请先选择日志文件！")
            return

        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, "正在分析日志，请稍候...\n\n")
        self.result_text.config(state=tk.DISABLED)
        self.root.update()

        for idx, file_path in enumerate(self.selected_files, 1):
            try:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    log_content = f.read()

                log_content = log_content[-8000:]
                filename = os.path.basename(file_path)

                self.result_text.config(state=tk.NORMAL)
                self.result_text.insert(tk.END, f"===== 第{idx}个文件：{filename} =====\n")
                self.result_text.config(state=tk.DISABLED)
                self.root.update()

                url = "https://api.deepseek.com/chat/completions"
                headers = {
                    "Authorization": f"Bearer {current_api}",
                    "Content-Type": "application/json"
                }
                data = {
                    "model": "deepseek-chat",
                    "messages": [
                        {"role": "user", "content": """
                         请你分析Minecraft日志，解析提供的游戏日志，输出精准、实用的分析结果。
                         要求如下：
                         语言简洁直白，避免冗余，不添加任何无关内容；
                         优先定位崩溃核心原因、模组冲突/不兼容问题、参数配置错误；
                         修复方案需具体可落地，明确告知操作步骤（如删除某模组、修改某配置）；
                         全程使用简洁通俗的语言，杜绝专业术语堆砌，确保普通玩家能快速理解并操作。\n""" + log_content}
                    ],
                    "temperature": 0.1,
                    "stream": False
                }

                try:
                    response = requests.post(url, headers=headers, json=data, timeout=90)
                    response.raise_for_status()
                    result = response.json()["choices"][0]["message"]["content"]
                    
                    #自动转为纯文本
                    result = self.clean_markdown(result)

                    self.result_text.config(state=tk.NORMAL)
                    self.result_text.insert(tk.END, result + "\n\n" + "-"*80 + "\n\n")
                    self.result_text.config(state=tk.DISABLED)
                    self.root.update()

                except Timeout:
                    self.result_text.config(state=tk.NORMAL)
                    self.result_text.insert(tk.END, "❌ 请求超时！AI服务器响应超过90秒，请重试或检查网络。\n\n")
                    self.result_text.config(state=tk.DISABLED)
                    messagebox.showerror("超时", "请求超时！\nAI 响应时间超过 90 秒\n\n建议：\n1. 重试一次\n2. 检查网络\n3. 日志内容过大")
                    self.root.update()
                    continue

                except Exception as e:
                    self.result_text.config(state=tk.NORMAL)
                    self.result_text.insert(tk.END, f"❌ 分析失败：{str(e)}\n\n")
                    self.result_text.config(state=tk.DISABLED)
                    self.root.update()

            except Exception as e:
                self.result_text.config(state=tk.NORMAL)
                self.result_text.insert(tk.END, f"❌ 文件读取失败：{str(e)}\n\n")
                self.result_text.config(state=tk.DISABLED)
                self.root.update()

        self.result_text.config(state=tk.NORMAL)
        self.result_text.insert(tk.END, "✅ 所有文件分析完成！")
        self.result_text.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = MCLogAnalyzer(root)
    root.mainloop()

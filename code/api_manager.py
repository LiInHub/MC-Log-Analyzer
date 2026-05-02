import json
import os
from tkinter import messagebox
from config import CONFIG_PATH

class APIManager:
    def __init__(self):
        self.api_keys = []
        # 确保Data文件夹存在
        self._ensure_data_dir()
        self.load_api_keys()

    def _ensure_data_dir(self):
        """创建Data文件夹（如果不存在）"""
        data_dir = os.path.dirname(CONFIG_PATH)
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)

    def load_api_keys(self):
        # 从文件加载API
        if os.path.exists(CONFIG_PATH):
            try:
                with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                    self.api_keys = json.load(f)
            except Exception as e:
                messagebox.showerror("加载失败", f"配置文件读取错误：{str(e)}")
                self.api_keys = []
        else:
            self.api_keys = []

    def save_api_keys(self):
        # 保存API（自动确保文件夹存在）
        self._ensure_data_dir()
        try:
            with open(CONFIG_PATH, "w", encoding="utf-8") as f:
                json.dump(self.api_keys, f, ensure_ascii=False, indent=2)
        except Exception as e:
            messagebox.showerror("保存失败", f"配置文件写入错误：{str(e)}")

    def add_api_key(self, api):
        # 添加API
        api = api.strip()
        if not api:
            messagebox.showwarning("提示", "请输入有效的API密钥！")
            return False
        if api in self.api_keys:
            messagebox.showinfo("提示", "该API已存在！")
            return False
        self.api_keys.append(api)
        self.save_api_keys()
        return True

    def remove_api_key(self, api):
        # 删除API
        if not api:
            messagebox.showwarning("提示", "请先选择要删除的API！")
            return False
        if api not in self.api_keys:
            messagebox.showwarning("提示", "该API不存在！")
            return False
        self.api_keys.remove(api)
        self.save_api_keys()
        return True
from tkinter import *
from tkinter.ttk import *
from typing import Dict
import ctypes
import os
import subprocess
from tkinter import messagebox
import configparser

# 创建 ConfigParser 对象
config = configparser.ConfigParser()
# 读取配置文件
with open('config.ini', 'r', encoding='utf-8') as file:
    config.read_file(file)
directory_path = ""
java_home = ""
maven_setting = ""
bat_file = ""
# 在路径周围添加引号


# 设置应用程序窗口的 DPI
ctypes.windll.shcore.SetProcessDpiAwareness(1)
profile_files = ""

class WinGUI(Tk):
    widget_dic: Dict[str, Widget] = {}

    def __init__(self):
        super().__init__()
        self.__init_config()
        self.__win()
        self.widget_dic["tk_list_box_directory"] = self.__tk_list_box_directory(self)
        self.widget_dic["tk_button_start"] = self.__tk_button_start(self)
        self.widget_dic["tk_list_box_selected"] = self.__tk_list_box_selected(self)
        self.widget_dic["tk_button_reset"] = self.__tk_button_reset(self)
        self.widget_dic["tk_label_lleur49b"] = self.__tk_label_lleur49b(self)
        self.widget_dic["tk_label_lleurirs"] = self.__tk_label_lleurirs(self)
        self.__init_config()
    def __init_config(self):
        global directory_path
        directory_path = config.get('variable', 'project_root')
        global java_home
        java_home = config.get('variable', 'java_home')
        global maven_setting
        maven_setting = config.get('variable', 'maven_setting')
        global bat_file
        bat_file = r'update.bat'
    def __win(self):
        self.title("代码更新助手")
        # 设置窗口大小、居中
        width = 600
        height = 500
        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()
        geometry = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.geometry(geometry)
        self.resizable(width=False, height=False)
        # 自动隐藏滚动条

    def scrollbar_autohide(self, bar, widget):
        self.__scrollbar_hide(bar, widget)
        widget.bind("<Enter>", lambda e: self.__scrollbar_show(bar, widget))
        bar.bind("<Enter>", lambda e: self.__scrollbar_show(bar, widget))
        widget.bind("<Leave>", lambda e: self.__scrollbar_hide(bar, widget))
        bar.bind("<Leave>", lambda e: self.__scrollbar_hide(bar, widget))

    def __scrollbar_show(self, bar, widget):
        bar.lift(widget)

    def __scrollbar_hide(self, bar, widget):
        bar.lower(widget)

    def vbar(self, ele, x, y, w, h, parent):
        sw = 15  # Scrollbar 宽度
        x = x + w - sw
        vbar = Scrollbar(parent)
        ele.configure(yscrollcommand=vbar.set)
        vbar.config(command=ele.yview)
        vbar.place(x=x, y=y, width=sw, height=h)
        self.scrollbar_autohide(vbar, ele)

    def __tk_list_box_directory(self, parent):
        lb = Listbox(parent)

        # 遍历目录
        for item in os.listdir(directory_path):
            item_path = os.path.join(directory_path, item)
            if os.path.isdir(item_path):
                # 将文件夹名称添加到Listbox
                lb.insert(END, item)
        lb.place(x=0, y=40, width=278, height=400)
        return lb

    def __tk_button_start(self, parent):
        btn = Button(parent, text="开始", takefocus=False,)
        btn.place(x=320, y=450, width=58, height=40)
        return btn

    def __tk_list_box_selected(self, parent):
        lb = Listbox(parent)

        lb.place(x=320, y=40, width=278, height=400)
        return lb

    def __tk_button_reset(self, parent):
        btn = Button(parent, text="重置", takefocus=False, )
        btn.place(x=220, y=450, width=58, height=40)
        return btn

    def __tk_label_lleur49b(self, parent):
        label = Label(parent, text="目录", anchor="center", )
        label.place(x=110, y=10, width=50, height=30)
        return label

    def __tk_label_lleurirs(self, parent):
        label = Label(parent, text="选中", anchor="center", )
        label.place(x=430, y=10, width=50, height=30)
        return label

class Win(WinGUI):
    def __init__(self):
        super().__init__()
        self.__event_bind()
        global directory_path
        directory_path = config.get('variable', 'project_root')

    # 双击选中目录
    def hanle_selected(self, evt):
        widget = evt.widget
        selected_indices = widget.curselection()
        selected_values = [widget.get(idx) for idx in selected_indices]
        selected_listbox = self.widget_dic["tk_list_box_selected"]
        for value in selected_values:
            if value not in selected_listbox.get(0, END):
                selected_listbox.insert(END, value)
    def hanle_cancel(self, evt):
        selected_listbox = self.widget_dic["tk_list_box_selected"]
        selected_index = selected_listbox.curselection()
        if selected_index:
            selected_listbox.delete(selected_index)

    # 重置
    def fnReset(self, evt):
        selected_listbox = self.widget_dic["tk_list_box_selected"]
        if selected_listbox.size() == 0:
            return
        selected_listbox.delete(0, END)

    # 开始
    def fnStart(self, evt):
        selected_listbox = self.widget_dic["tk_list_box_selected"]
        if selected_listbox.size() == 0:
            messagebox.showinfo("提示", "至少选择一个项目进行更新！")
            return
        selected_listbox = self.widget_dic["tk_list_box_selected"]
        items = selected_listbox.get(0, END)
        result = ','.join(items)
        global profile_files
        profile_files = result
        command = f'cmd /c start "" "{bat_file}" {profile_files}'
        subprocess.Popen(command, shell=True)

    def __event_bind(self):
        self.widget_dic["tk_list_box_directory"].bind('<Double-Button-1>', self.hanle_selected)
        self.widget_dic["tk_list_box_selected"].bind('<Double-Button-1>', self.hanle_cancel)
        self.widget_dic["tk_button_start"].bind('<Button-1>', self.fnStart)
        self.widget_dic["tk_button_reset"].bind('<Button-1>', self.fnReset)
        pass

if __name__ == "__main__":
    win = Win()
    win.mainloop()
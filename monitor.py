import requests
import sched
import time
import json
import tkinter as tk
import threading
from datetime import datetime

# 初始化sched模块的scheduler类
# 第一个参数是一个可以返回时间戳的函数，第二个参数可以在定时未到达之前阻塞。
schedule = sched.scheduler(time.time, time.sleep)


def get_kline(text_widget, headers, code, name):
    resultText = requests.get(
        f"https://stock.xueqiu.com/v5/stock/realtime/quotec.json?symbol={code}",
        headers=headers,
    )
    # print(resultText.text)
    data = json.loads(resultText.text)["data"][0]

    # 为每个信息集创建独特的标签
    name_tag = f"{name}_name_tag"
    value_tag = f"{name}_value_tag"

    text_widget.tag_configure(name_tag, foreground="blue")
    if data['percent'] < -0.6:
        text_widget.tag_configure(value_tag, foreground="green")
    elif data['percent'] >= 0.6:
        text_widget.tag_configure(value_tag, foreground="red")
    else:
        text_widget.tag_configure(value_tag, foreground="black")

    text_widget.insert("insert", f"{name}：", name_tag)
    text_widget.insert("insert", f"\n当前价格：{data['current']}", value_tag)
    text_widget.insert("insert", f"\n幅度：{data['percent']}%", value_tag)
    text_widget.insert("insert", f"\n增长值：{data['chg']}", value_tag)
    text_widget.insert("insert", "\n---------\n")


def getData():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
    }

    text.delete(1.0, "end")
    print(datetime.now())
    get_kline(text, headers=headers, code="SH000001", name="上证指数")
    get_kline(text, headers=headers, code="SH600418", name="江淮汽车")


def task(inc):
    getData()
    schedule.enter(inc, 0, task, (inc,))


def func(inc=2):
    # enter四个参数分别为：
    # 间隔事件、优先级（用于同时间到达的两个事件同时执行时定序）、被调用触发的函数、给该触发函数的参数（tuple形式）
    schedule.enter(0, 0, task, (inc,))
    schedule.run()


# def insert_point():
#     code = entry.get()
#     text.delete(1.0, "end")
#     # text.insert('insert', var)
#     func()


if __name__ == "__main__":
    ## 可视化
    root_window = tk.Tk()
    root_window.title("  实时  ")
    root_window.resizable(False, False)
    root_window.geometry("180x130")
    root_window["background"] = "#C9C9C9"
    ## 显示区域
    text = tk.Text(root_window, height=9)
    text.pack()
    ## 置顶
    root_window.attributes("-topmost", 1)
    root_window.attributes("-alpha", 0.8)
    # root_window.attributes("-toolwindow", 2)
    ## 拿数据
    t1 = threading.Thread(target=func)
    t1.start()
    # 进入主循环，显示主窗口
    root_window.mainloop()

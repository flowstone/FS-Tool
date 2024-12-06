import sys
import time
from PyQt5.QtWidgets import QApplication
from progress_tool import ProgressTool,ProgressSignalEmitter

def task1_progress_update(value):
    print(f"任务1进度更新: {value}%")


def task2_progress_update(value):
    print(f"任务2进度更新: {value}%")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # 场景一：模拟任务1的进度更新
    progress_tool1 = ProgressTool()
    progress_tool1.show()
    progress_signal_emitter1 = ProgressSignalEmitter()
    progress_signal_emitter1.progress_signal.connect(progress_tool1.set_value)
    for i in range(101):
        time.sleep(0.1)
        progress_signal_emitter1.update_progress(i)

    # 场景二：模拟任务2的进度更新，同时设置不同的进度条格式
    # progress_tool2 = ProgressTool()
    # progress_tool2.show()
    # progress_tool2.set_format("任务2进度: %v/%m")
    # progress_signal_emitter2 = ProgressSignalEmitter()
    # progress_signal_emitter2.progress_signal.connect(progress_tool2.set_value)
    # for i in range(101):
    #     time.sleep(0.2)
    #     progress_signal_emitter2.update_progress(i)
    #     progress_tool2.connect_update_function(task2_progress_update)

    sys.exit(app.exec_())
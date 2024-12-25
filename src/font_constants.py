from PyQt5.QtGui import QColor, QFont

class FontConstants:
    """字体常量类"""
    # 模拟H1标题字体
    H1 = QFont()
    H1.setPointSize(32)
    H1.setBold(True)
    H1.setWeight(75)

    # 模拟H2标题字体
    H2 = QFont()
    H2.setPointSize(28)
    H2.setBold(True)
    H2.setWeight(70)

    # 模拟H3标题字体
    H3 = QFont()
    H3.setPointSize(24)
    H3.setBold(True)
    H3.setWeight(65)

    # 普通正文大字体
    BODY_LARGE = QFont()
    BODY_LARGE.setPointSize(18)

    # 普通正文字体
    BODY_NORMAL = QFont()
    BODY_NORMAL.setPointSize(16)

    # 普通正文小字体
    BODY_SMALL = QFont()
    BODY_SMALL.setPointSize(14)



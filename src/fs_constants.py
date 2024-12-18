class FsConstants:
    """
    ---------------------
    宽度为0 高度为0,则表示窗口【宽高】由组件们决定
    ---------------------
    """
    # 主窗口相关常量
    APP_WINDOW_WIDTH = 300
    APP_WINDOW_HEIGHT = 300
    APP_WINDOW_TITLE = "流体石头的工具箱"

    # 悬浮球相关常量
    APP_MINI_WINDOW_WIDTH = 90
    APP_MINI_WINDOW_HEIGHT = 90
    APP_MINI_WINDOW_TITLE = ""

    # 工具栏相关常量
    TOOLBAR_HELP_TITLE = "帮助"
    TOOLBAR_README_TITLE = "说明"
    TOOLBAR_AUTHOR_TITLE = "作者"
    ## 主窗口
    APP_TOOLBAR_README_TEXT = '<!DOCTYPE html><html><head><meta charset="utf-8"><title>HTML Editor-LDDGO.NET</title><link rel="stylesheet"href="https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@11.5.1/build/styles/default.min.css"type="text/css"></head><body><h2 style="text-align: center;">说明</h2><p>作者开发的小工具，目前只有Win端，如果有问题，可以去项目中提Issues，有时间会修复小问题。</p><h3><strong>功能</strong></h3><p><span style="color: #e03e2d;"><strong>【透明时间】</strong></span></p><p>主要为直播开发的小应用，在桌面左上角生成一个时间控件</p><p><strong><span style="color: #e03e2d;">【</span>图转大师<span style="color: #e03e2d;">】</span></strong></p><p>图片的格式转换，目前有很大问题，暂未修复</p><p><strong><span style="color: #e03e2d;">【</span>文件夹创建师<span style="color: #e03e2d;">】</span></strong></p><p>选择文件夹，找出相同部分的文件名，以它进行切割，如abc_123，以_分割的话，会创建abc文件夹，把abc相关的文件全部移动到文件夹中，不支持递归</p><p><span style="color: #3598db;"><strong><span style="color: #e03e2d;">【</span>重命名使者<span style="color: #e03e2d;">】</span></strong></span></p><p>选择文件夹，批量修改文件名，包括后缀，前缀，替换指定字符，不支持递归</p><p>&nbsp;</p><h3>项目地址</h3><p><span style="color: #e03e2d;">【</span><a href="https://github.com/flowstone/FS-Tool"target="_blank"rel="noopener">FS-Tool</a><span style="color: #e03e2d;">】</span><span>https://github.com/flowstone/FS-Tool</span></p><script src="https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@11.5.1/build/highlight.min.js"type="text/javascript"></script><script type="text/javascript">hljs.highlightAll();</script></body></html>'
    APP_TOOLBAR_AUTHOR_TEXT = '<!DOCTYPE html><html><head><meta charset="utf-8"><title>HTML Editor-LDDGO.NET</title><link rel="stylesheet"href="https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@11.5.1/build/styles/default.min.css"type="text/css"></head><body><h2 style="text-align: center;">作者</h2><p>没有特长的吗喽，哈哈哈</p><h3><strong>地址</strong></h3><p><span style="color: #e03e2d;"><strong>【<a href="https://github.com/flowstone">Github</a>】<span style="color: #000000;">https://github.com/flowstone/FS-Tool</span></strong></span></p><p><strong><span style="color: #e03e2d;">【</span><a href="http://blog.xueyao.tech/"><span style="color: #e03e2d;">博客</span></a><span style="color: #e03e2d;">】<span style="color: #000000;"></span></span></strong>文章基本不更新，但是域名注册了10年，到2034年结束</p><p><strong><span style="color: #e03e2d;">【</span>邮箱<span style="color: #e03e2d;">】<span style="color: #000000;"></span></span></strong>略，太多了不知道写哪个</p><p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</p><h4><span style="color: #3598db;"><strong>欢迎你的关注!</strong></span></h4><p><span style="color: #e03e2d;"><strong>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;于202411.14&nbsp;&nbsp;23:45</strong></span></p><p>&nbsp;</p><script src="https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@11.5.1/build/highlight.min.js"type="text/javascript"></script><script type="text/javascript">hljs.highlightAll();</script></body></html>'

    ## 自动答题
    AUTO_ANSWER_TOOLBAR_README_TEXT = '<!DOCTYPE html><html><head><meta charset="utf-8"><title>HTML Editor-LDDGO.NET</title><link rel="stylesheet"href="https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@11.5.1/build/styles/default.min.css"type="text/css"></head><body><p>&nbsp;</p><h2 style="text-align: center;">说明</h2><h3><em><span style="color: #e03e2d;"><strong>私人使用</strong></span></em></h3><p>自动答题的工具，必须的条件，加上次数即可模仿用户点击答题</p><p>防止恶意操作，添加密码访问，密码是手机号</p><p>如果网站改版，功能将失效，可使用JS脚本代替</p><p><span style="background-color: #f1c40f;"><strong>【Chrome指定版本：131.0.6778.69】</strong></span></p><p><strong>Chrome</strong>下载：<a href="https://pan.quark.cn/s/e3e92f0b8882">https://pan.quark.cn/s/e3e92f0b8882</a><h3><strong>特殊说明</strong></h3><ol><li>当页面下拉框加载失败后，将重复刷新页面(最多10次，间隔2秒)</li><li>有异常出现，只有本次答题失败，继续执行下一次</li><li>存在程序闪崩情况</li></ol><h3><strong>试题地址</strong></h3><p>https://www.jscdc.cn<h3><strong>其它版本</strong></h3><p>【<a href="https://github.com/flowstone/Auto-Answers">Github</a>】：Java、JS脚本</p><p>&nbsp;</p><p><strong><span style="color: #e03e2d; font-size: 8pt; font-family: "courier new", courier, monospace;"><em>注：此版本，没有调用接口获得正确答案，所以分数大概不及格，</em></span></strong><br/><strong><span style="color: #e03e2d; font-size: 8pt; font-family: "courier new", courier, monospace;"><em>如果希望高分，可以使用JS脚本(青龙面板)</em></span></strong></p><p>&nbsp;</p><script src="https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@11.5.1/build/highlight.min.js"type="text/javascript"></script><script type="text/javascript">hljs.highlightAll();</script></body></html>'
    DESKTOP_CLOCK_WINDOW_TITLE = "透明时间"
    CREATE_FOLDER_WINDOW_TITLE = "文件夹老师"
    FILE_RENAMER_WINDOW_TITLE = "重命名使者"
    HEIC_JPG_BUTTON_TITLE = "HEIC作家"
    PIC_CONVERSION_WINDOW_TITLE = "图转大师"
    AUTO_ANSWERS_WINDOW_TITLE = "自动答题"
    STICK_NOTE_WINDOW_TITLE = "快捷便签"
    PASSWORD_GENERATOR_TITLE = "密码生成器"
    FILE_GENERATOR_WINDOW_TITLE = "文件生成"
    FILE_COMPARATOR_WINDOW_TITLE = "文件比较"
    FILE_ENCRYPTOR_WINDOW_TITLE = "文件加密"
    RSA_KEY_GENERATOR_WINDOW_TITLE = "RSA生成器"
    HASH_CALCULATOR_WINDOW_TITLE = "hash校验"

    # 桌面时钟相关常量
    DESKTOP_CLOCK_WINDOW_WIDTH = 0
    DESKTOP_CLOCK_WINDOW_HEIGHT = 0

    # 批量创建文件夹相关常量
    CREATE_FOLDER_WINDOW_WIDTH = 0
    CREATE_FOLDER_WINDOW_HEIGHT = 0

    # 批量修改文件名相关常量
    FILE_RENAMER_WINDOW_WIDTH = 0
    FILE_RENAMER_WINDOW_HEIGHT = 0
    FILE_RENAMER_TYPE_FILE = "文件"
    FILE_RENAMER_TYPE_FOLDER = "文件夹"

    # 批量HEIC转JPG
    HEIC_JPG_WINDOW_WIDTH = 0
    HEIC_JPG_WINDOW_HEIGHT = 0
    HEIC_JPG_WINDOW_TITLE = "批量HEIC转JPG(递归)"

    # 图片转换相关常量
    PIC_CONVERSION_WINDOW_WIDTH = 500
    PIC_CONVERSION_WINDOW_HEIGHT = 400

    # 自动答题相关常量
    AUTO_ANSWERS_WINDOW_WIDTH = 0
    AUTO_ANSWERS_WINDOW_HEIGHT = 0
    AUTO_ANSWERS_TITLE_IMAGE = "resources/auto_answers_title.png"
    AUTO_ANSWERS_PASSWORD_MD5 = "adf0558822da93b55f6fc48790ff3137"
    AUTO_ANSWERS_DRIVER_PATH = "resources/driver"
    AUTO_ANSWERS_WIN_DRIVER_NAME = "chromedriver.exe"
    AUTO_ANSWERS_OTHER_DRIVER_NAME = "chromedriver"

    #快捷便签相关常量
    STICK_NOTE_WINDOW_WIDTH = 400
    STICK_NOTE_WINDOW_HEIGHT = 300
    STICK_NOTE_WINDOW_MIN_WIDTH = 300
    STICK_NOTE_WINDOW_MIN_HEIGHT = 200

    #密码生成器

    # 颜色相关常量
    BACKGROUND_COLOR = "#f0f0f0"
    BUTTON_COLOR_NORMAL = "#3498db"
    BUTTON_COLOR_HOVER = "#2980b9"
    BUTTON_COLOR_PRESS = "#1f618d"

    # 字体相关常量
    DEFAULT_FONT_FAMILY = "Arial"
    DEFAULT_FONT_SIZE = 12

    # 共用的常量，应用图标
    APP_ICON_PATH = "resources/app.ico"
    APP_MINI_ICON_PATH = "resources/app_mini.ico"
    LOADING_PATH = "resources/loading.gif"
    AUTHOR_MAIL = "xueyao.me@gmail.com"
    AUTHOR_BLOG = "https://blog.xueyao.tech"
    AUTHOR_GITHUB = "https://github.com/flowstone"
    PROJECT_ADDRESS = "https://github.com/flowstone/FS-Tool"
    BASE_QSS_PATH = "resources/stylesheets/styles.qss"
    BASE_COLOR_MAP = "resources/img_colormap.gif"

    BUTTON_ICON_PATH = "resources/icon/"
    BUTTON_TIME_ICON = "time-icon.svg"
    BUTTON_PIC_ICON = "img_conv-icon.svg"
    BUTTON_FOLDER_ICON = "folder-icon.svg"
    BUTTON_FILE_ICON = "move-icon.svg"
    BUTTON_HEIC_ICON = "heic_jpg-icon.svg"
    BUTTON_ANSWERS_ICON = "auto_answers-icon.svg"
    BUTTON_PASSWORD_ICON = "unlock-icon.svg"
    BUTTON_STICK_NOTE_ICON = "business-icon.svg"
    BUTTON_FILE_GENERATOR_ICON = "file_generator-icon.svg"
    BUTTON_FILE_COMPARATOR_ICON = "file_comparator-icon.svg"
    BUTTON_FILE_ENCRYPTOR_ICON = "file_encryptor-icon.svg"
    BUTTON_RSA_KEY_GENERATOR_ICON = "rsa-icon.svg"
    BUTTON_HASH_CALCULATOR_ICON = "MD5-icon.svg"


    BUTTON_IMAGE_LOCK_OPEN = "resources/btn/lock-open-solid.svg"
    BUTTON_IMAGE_LOCK_CLOSE = "resources/btn/lock-solid.svg"

    # 保存文件路径
    SAVE_FILE_PATH_WIN = "C:\\"
    SAVE_FILE_PATH_MAC = "~"
    DATABASE_FILE = "database.db"
    AUTO_ANSWERS_TABLE_NAME = "auto_answers_log"

    APP_CONFIG_FILE = "config.json"
    HELP_PDF_FILE_PATH = "resources/pdf/help.pdf"
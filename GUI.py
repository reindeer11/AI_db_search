import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QLineEdit, QPushButton,
    QLabel, QScrollArea
)
from PyQt5.QtCore import Qt
from config_AI import post_AI

from  db_config import cursor

class DatabaseQueryGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # 设置窗口标题和大小
        self.setWindowTitle("AI查询数据库界面-reindeer制作version=1.0")
        self.setGeometry(100, 100, 800, 600)

        # 主布局：垂直布局
        main_layout = QVBoxLayout()

        # 第一部分：用户输入框和查询按钮（水平布局）
        input_layout = QHBoxLayout()

        self.input_box = QLineEdit()
        self.input_box.setPlaceholderText("请输入查询内容...")
        input_layout.addWidget(self.input_box)

        self.query_button = QPushButton("查询")
        self.query_button.clicked.connect(self.on_query_button_clicked)
        input_layout.addWidget(self.query_button)

        main_layout.addLayout(input_layout)

        # 第二部分：聊天框（AI 回复 + 用户输入）和数据库查询结果（水平布局）
        result_layout = QHBoxLayout()

        # 聊天框区域
        chat_area_layout = QVBoxLayout()

        # 滚动区域
        self.chat_scroll_area = QScrollArea()
        self.chat_scroll_area.setWidgetResizable(True)

        # 聊天内容容器
        self.chat_container = QWidget()
        self.chat_layout = QVBoxLayout(self.chat_container)
        self.chat_layout.setAlignment(Qt.AlignTop)  # 内容从顶部开始排列
        self.chat_scroll_area.setWidget(self.chat_container)

        chat_area_layout.addWidget(self.chat_scroll_area)

        result_layout.addLayout(chat_area_layout, stretch=3)

        # 数据库查询结果窗口
        self.db_result = QTextEdit()
        self.db_result.setReadOnly(True)  # 只读模式
        self.db_result.setPlaceholderText("数据库查询结果将显示在这里...")

        result_layout.addWidget(self.db_result, stretch=1)  # 占 1/4 的宽度 #显示数据库查询的结果

        main_layout.addLayout(result_layout)

        # 设置主布局
        self.setLayout(main_layout)

    def on_query_button_clicked(self):
        """
        查询按钮的槽函数，您可以在这里调用您的 AI 查询函数。
        假设您的 AI 查询函数返回两个结果：AI 回复和数据库查询结果。
        """
        user_input = self.input_box.text()  # 获取用户输入
        if not user_input.strip():
            return

        # 清空输入框
        self.input_box.clear()

        # 显示用户输入的内容（右侧对齐）
        self.add_chat_message(user_input, is_user=True)

        # 调用 AI 查询函数
        ai_reply, ai_model,sentence = post_AI(user_input)

        # 显示 AI 回复的内容（左侧对齐），并显示模型名称
        self.add_chat_message(ai_reply, ai_model=ai_model, is_user=False)
        self.db_search(sentence)
    def add_chat_message(self, message, ai_model=None, is_user=False):
        """
        添加一条聊天消息到聊天框中。
        :param message: 消息内容
        :param ai_model: AI 模型名称（仅用于 AI 回复）
        :param is_user: 是否为用户发送的消息
        """
        # 创建一个标签来显示消息内容
        if is_user:
            label_text = f"<b><span style='font-family: \"Berlin Sans FB\"; font-weight: normal ;'>User:</span></b><br>{message}"
        else:
            label_text = f"<b><span style='font-family: \"Berlin Sans FB\"; font-weight: normal ;'>{ai_model}:</span></b><br>{message}"

        label = QLabel(label_text)
        label.setWordWrap(True)  # 自动换行
        label.setTextFormat(Qt.RichText)  # 启用富文本支持

        # 设置消息背景样式
        label.setStyleSheet("""
            background-color: #DCF8C6; /* AI 回复背景色 */
            padding: 10px;
            border-radius: 10px;
            max-width: 70%; /* 控制消息的最大宽度 */
        """ if not is_user else """
            background-color: #ECECEC; /* 用户消息背景色 */
            padding: 10px;
            border-radius: 10px;
            max-width: 70%; /* 控制消息的最大宽度 */
        """)

        # 对齐方式
        label.setAlignment(Qt.AlignRight if is_user else Qt.AlignLeft)

        # 确保消息宽度填满滚动区域
        label.setFixedWidth(self.chat_scroll_area.width() - 40)  # 减去一些 padding

        # 将标签添加到聊天框
        self.chat_layout.addWidget(label)

        #数据库查询
    def db_search(self, sentence):
        try:
            cursor.execute(sentence)
            results = cursor.fetchall()
            field_names = [desc[0] for desc in cursor.description]
            result_str = ""
            for row in results:
                for field_name, data in zip(field_names, row):
                    print(f"{field_name}:{data}")
                    result_str += f"{field_name}:{data}\n"
                result_str+="-"*20+'\n'
            self.db_result.setText(result_str)


        except Exception as e:
            print(f"数据库查询失败！错误信息: {str(e)}")

if __name__ == "__main__":
    print("""
============================================================================================================
                                   editor: reindeer
                             ~ AIdatabasequeryGUI : v1.0 ~
The project is a PyQt5 database query interface that implements chat function and database query function.
              project_address：https://github.com/reindeer11/demo/tree/master 
    """)
    app = QApplication(sys.argv)
    window = DatabaseQueryGUI()
    window.show()
    sys.exit(app.exec_())

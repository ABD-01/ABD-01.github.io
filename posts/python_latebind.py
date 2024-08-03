import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget

# from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        layout = QVBoxLayout()
        self.setupBtns(layout)
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        ## TODO: 4. (a) Use lambda to create a new scope
        # def create_click_handler(btn):
        #     return lambda: print("BTN_CLICKED:", btn.text())

        self.buttons = self.findChildren(QPushButton)
        for btn in self.buttons:
            print(btn.text())
            ## TODO: 1. Comment the below code
            btn.clicked.connect(lambda: print("BTN_CLICKED:", btn.text()))
            ## TODO: 3. Early binding the `btn` variable to the lambda function
            # btn.clicked.connect(lambda i, btn=btn: print("BTN_CLICKED:", btn.text()))
            ## TODO: 4. (b) Using function to create new scope
            # btn.clicked.connect(create_click_handler(btn))
            ## TODO: 5. Using lambda to create new scope
            # btn.clicked.connect((lambda btn: lambda: print("BTN_CLICKED:", btn.text()))(btn))
            
        ## TODO: 6. This is horrible. Do not do this
        # list(map(lambda btn: btn.clicked.connect((lambda btn: lambda: print("BTN_CLICKED:", btn.text()))(btn)), self.buttons))

        ## TODO: 2. Uncomment the below code and run again
        # btn = QPushButton(self, text="EXIT")
        # layout.addWidget(btn)

        self.show()

    def setupBtns(self, layout):
        btnAskName = QPushButton(self, text="Name")
        btnAskDate = QPushButton(self, text="Date")
        btnAskAge = QPushButton(self, text="Age")
        btnAskMajor = QPushButton(self, text="Major")
        btnAskGPA = QPushButton(self, text="GPA")
        # ... I had around 12 buttons on that page

        layout.addWidget(btnAskName)
        layout.addWidget(btnAskDate)
        layout.addWidget(btnAskAge)
        layout.addWidget(btnAskMajor)
        layout.addWidget(btnAskGPA)


app = QApplication(sys.argv)
window = MainWindow()
app.exec_()  # exec() in case of PySide6

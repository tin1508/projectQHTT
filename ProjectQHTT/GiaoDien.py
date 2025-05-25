import sys
import os
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QSplashScreen, QScrollArea
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPixmap
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import ChuanTac_ChinhTac
import HinhHoc_ToaDo
import DonHinh_Bland

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")

        self.titleLabel = QtWidgets.QLabel(parent=self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.titleLabel.setFont(font)
        self.titleLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.titleLabel.setObjectName("titleLabel")
        self.verticalLayout.addWidget(self.titleLabel)

        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalLayout.setStretch(0, 3)  # Ưu tiên không gian cho inputGroupBox
        self.horizontalLayout.setStretch(1, 7)  # Ưu tiên không gian cho outputGroupBox

        # Input Group Box
        self.inputGroupBox = QtWidgets.QGroupBox(parent=self.centralwidget)
        self.inputGroupBox.setObjectName("inputGroupBox")
        self.inputGroupBox.setMinimumWidth(300)  # Chiều rộng tối thiểu
        self.inputLayout = QtWidgets.QVBoxLayout(self.inputGroupBox)
        self.inputLayout.setObjectName("inputLayout")

        self.objectiveLabel = QtWidgets.QLabel(parent=self.inputGroupBox)
        self.objectiveLabel.setObjectName("objectiveLabel")
        self.inputLayout.addWidget(self.objectiveLabel)

        self.objectiveLineEdit = QtWidgets.QLineEdit(parent=self.inputGroupBox)
        self.objectiveLineEdit.setObjectName("objectiveLineEdit")
        self.inputLayout.addWidget(self.objectiveLineEdit)

        self.constraintsLabel = QtWidgets.QLabel(parent=self.inputGroupBox)
        self.constraintsLabel.setObjectName("constraintsLabel")
        self.inputLayout.addWidget(self.constraintsLabel)

        self.constraintsPlainTextEdit = QtWidgets.QPlainTextEdit(parent=self.inputGroupBox)
        self.constraintsPlainTextEdit.setObjectName("constraintsPlainTextEdit")
        self.constraintsPlainTextEdit.setMinimumHeight(150)  # Chiều cao tối thiểu
        self.inputLayout.addWidget(self.constraintsPlainTextEdit)

        self.methodLabel = QtWidgets.QLabel(parent=self.inputGroupBox)
        self.methodLabel.setObjectName("methodLabel")
        self.inputLayout.addWidget(self.methodLabel)

        self.standardizeButton = QtWidgets.QPushButton(parent=self.inputGroupBox)
        self.standardizeButton.setObjectName("standardizeButton")
        self.inputLayout.addWidget(self.standardizeButton)

        self.canonicalizeButton = QtWidgets.QPushButton(parent=self.inputGroupBox)
        self.canonicalizeButton.setObjectName("canonicalizeButton")
        self.inputLayout.addWidget(self.canonicalizeButton)

        self.methodComboBox = QtWidgets.QComboBox(parent=self.inputGroupBox)
        self.methodComboBox.setObjectName("methodComboBox")
        self.methodComboBox.addItems([
            "Chọn phương pháp",
            "Phương pháp Hình học (cho 2 biến, dùng tọa độ)",
            "Phương pháp Hình học (cho 2 biến, dùng trượt)",
            "Phương pháp Đơn hình",
            "Phương pháp Bland",
            "Phương pháp Hai pha"
        ])
        self.inputLayout.addWidget(self.methodComboBox)

        self.solveButton = QtWidgets.QPushButton(parent=self.inputGroupBox)
        self.solveButton.setObjectName("solveButton")
        self.inputLayout.addWidget(self.solveButton)

        self.horizontalLayout.addWidget(self.inputGroupBox, 3)

        # Output Group Box
        self.outputGroupBox = QtWidgets.QGroupBox(parent=self.centralwidget)
        self.outputGroupBox.setObjectName("outputGroupBox")
        self.outputGroupBox.setMinimumWidth(600)  # Tăng chiều rộng tối thiểu
        self.outputLayout = QtWidgets.QVBoxLayout(self.outputGroupBox)
        self.outputLayout.setObjectName("outputLayout")

        self.scrollArea = QScrollArea(parent=self.outputGroupBox)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setMinimumHeight(500)  # Tăng chiều cao tối thiểu cho khu vực cuộn
        self.scrollContent = QtWidgets.QWidget()
        self.scrollLayout = QtWidgets.QVBoxLayout(self.scrollContent)
        self.scrollLayout.setObjectName("scrollLayout")

        self.resultTextEdit = QtWidgets.QTextEdit(parent=self.scrollContent)
        self.resultTextEdit.setReadOnly(True)
        self.resultTextEdit.setObjectName("resultTextEdit")
        self.resultTextEdit.setMinimumHeight(200)  # Chiều cao tối thiểu
        self.scrollLayout.addWidget(self.resultTextEdit, 1)

        self.figure = Figure(figsize=(7, 5))  # Tăng kích thước đồ thị
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setMinimumHeight(400)  # Tăng chiều cao tối thiểu cho đồ thị
        self.scrollLayout.addWidget(self.canvas, 1)

        self.scrollArea.setWidget(self.scrollContent)
        self.outputLayout.addWidget(self.scrollArea)

        self.horizontalLayout.addWidget(self.outputGroupBox, 7)
        self.verticalLayout.addLayout(self.horizontalLayout)

        # # Biểu đồ
        # self.figure = Figure(figsize=(7, 5))
        # self.canvas = FigureCanvas(self.figure)
        # self.canvas.setMinimumHeight(400)
        # self.outputSplitter.addWidget(self.canvas)

        # # Thêm splitter vào layout
        # self.outputLayout.addWidget(self.outputSplitter)

        # self.horizontalLayout.addWidget(self.outputGroupBox, 7)

        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.standardizeButton.clicked.connect(self.converToStandardForm)
        self.canonicalizeButton.clicked.connect(self.convertToAugmentedForm)
        self.solveButton.clicked.connect(self.solveProblemBySolutions)

        self._setup_empty_plot()

    def _setup_empty_plot(self):
        ax = self.figure.add_subplot(111)
        ax.clear()
        ax.set_xlim(-10, 10)
        ax.set_ylim(-10, 10)
        ax.set_xlabel("x1", fontsize=12, labelpad=15)  # Tăng khoảng cách nhãn
        ax.set_ylabel("x2", fontsize=12, labelpad=15)  # Tăng khoảng cách nhãn
        ax.grid(True)
        self.figure.tight_layout(pad=2.0)  # Tự động điều chỉnh khoảng cách
        self.canvas.draw()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Công cụ giải bài toán Quy hoạch Tuyến tính"))
        self.titleLabel.setText(_translate("MainWindow", "CÔNG CỤ GIẢI BÀI TOÁN QUY HOẠCH TUYẾN TÍNH"))
        self.inputGroupBox.setTitle(_translate("MainWindow", "Nhập dữ liệu bài toán"))
        self.objectiveLabel.setText(_translate("MainWindow", "Hàm mục tiêu:"))
        self.objectiveLineEdit.setPlaceholderText(_translate("MainWindow", "Ví dụ: max or min 2x1 + 3x2"))
        self.constraintsLabel.setText(_translate("MainWindow", "Các ràng buộc:"))
        self.constraintsPlainTextEdit.setPlaceholderText(_translate("MainWindow", "Nhập mỗi ràng buộc trên một dòng.\nVí dụ:\nx1 + x2 <= 10\n2x1 + x2 >= 5\nx1 >= 0\nx2 >= 0"))
        self.methodLabel.setText(_translate("MainWindow", "Chọn phương pháp:"))
        self.standardizeButton.setText(_translate("MainWindow", "Chuyển sang dạng chuẩn tắc"))
        self.canonicalizeButton.setText(_translate("MainWindow", "Chuyển sang dạng chính tắc"))
        self.solveButton.setText(_translate("MainWindow", "Giải"))
        self.outputGroupBox.setTitle(_translate("MainWindow", "Kết quả"))

    #nhận chuỗi đầu vào từ người nhập
    def receiveInputFromUser(self):
        aimText = self.objectiveLineEdit.text();
        constraintText = self.constraintsPlainTextEdit.toPlainText();
        return aimText + '\n' + constraintText;

    #chức năng
    #chuyển bài toán sang dạng chuẩn tắc 
    def converToStandardForm(self):
        s = self.receiveInputFromUser();
        #xử lý chuỗi đầu vào
        ChuanTac_ChinhTac.inputStringProcessing(s);
        result = ChuanTac_ChinhTac.changeIntoStandardForm();
        self.resultTextEdit.setText("Dạng chuẩn tắc: " + '\n' + result);
    #chuyển bài toán sang dạng chính tắc
    def convertToAugmentedForm(self):
        s = self.receiveInputFromUser();
        #xử lý chuỗi đầu vào
        ChuanTac_ChinhTac.inputStringProcessing(s);
        result = ChuanTac_ChinhTac.changeIntoAugmentedForm();
        self.resultTextEdit.setText("Dạng chính tắc: " + '\n' + result);
    #giải bài toán bằng phương pháp hình học

    def solveProblemBySolutions(self):
        self.resultTextEdit.clear()
        method = self.methodComboBox.currentText()
        #Phương pháp hình học tọa độ
        if method == "Phương pháp Hình học (cho 2 biến, dùng tọa độ)":
            self.solveByGeometrySolution()
        elif method ==  "Phương pháp Hình học (cho 2 biến, dùng trượt)":
            return;
        #Phương pháp đơn hình
        elif method == "Phương pháp Đơn hình" or method == "Phương pháp Bland":
            s = self.receiveInputFromUser()
            ChuanTac_ChinhTac.inputStringProcessing(s)
            equation = ChuanTac_ChinhTac.returnFormToSolveSimplexAndBland()
            condition = "min"
            if method == "Phương pháp Đơn hình":
                DonHinh_Bland.solveSymplex(equation, condition, outputCall= self.outputCall)
            else:
                DonHinh_Bland.solveBland(equation, condition, outputCall = self.outputCall)
        elif method == "Phương pháp Hai pha":
            return;
    #hàm này dùng để in kết quả đơn hình, bland, 2 pha ra result text
    #cách sử dụng giống print() nhưng print chỉ in được trên console, còn outputCall này là 1 hàm mình tự định nghĩa để giúp in ra trên màn hình app
    def outputCall(self, text):
        self.resultTextEdit.append(text)

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, size=None):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.resize(1200, 800)  # Tăng kích thước cửa sổ chính

def showProgram():
    app = QtWidgets.QApplication(sys.argv)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(script_dir, "photo.png")

    if not os.path.exists(image_path):
        print(f"Error: Image file not found at {image_path}")
        sys.exit(1)

    splash_pix = QPixmap(image_path)
    splash_size = splash_pix.size()

    splash = QSplashScreen(splash_pix, Qt.WindowType.WindowStaysOnTopHint)
    splash.setWindowFlag(Qt.WindowType.FramelessWindowHint)
    splash.setFixedSize(splash_size)
    splash.move(
        QtWidgets.QApplication.primaryScreen().geometry().center() - splash.rect().center()
    )
    splash.show()

    def start_app():
        splash.close()
        global main_window
        main_window = MainWindow()
        main_window.show()

    QTimer.singleShot(1000, start_app)
    sys.exit(app.exec())

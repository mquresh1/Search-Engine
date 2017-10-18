from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import queryLinks

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Smoogle")
        Form.resize(1080, 720)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lineEdit = QtWidgets.QLineEdit(Form)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.buttonClicked)
        self.horizontalLayout.addWidget(self.pushButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.label_1 = QtWidgets.QLabel(Form)
        self.label_1.setText("")
        self.label_1.setObjectName("label")
        self.label_1.setWordWrap(True)
        self.verticalLayout.addWidget(self.label_1)
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setText("")
        self.label_2.setObjectName("label_2")
        self.label_2.setWordWrap(True)
        self.verticalLayout.addWidget(self.label_2)
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setText("")
        self.label_3.setObjectName("label_3")
        self.label_3.setWordWrap(True)
        self.verticalLayout.addWidget(self.label_3)
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setText("")
        self.label_4.setObjectName("label_4")
        self.label_4.setWordWrap(True)
        self.verticalLayout.addWidget(self.label_4)
        self.label_5 = QtWidgets.QLabel(Form)
        self.label_5.setText("")
        self.label_5.setObjectName("label_5")
        self.label_5.setWordWrap(True)
        self.verticalLayout.addWidget(self.label_5)

        self.bookkeeping, self.inverted, self.special, self.pageranks = queryLinks.importIndex()

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Smoogle"))
        self.pushButton.setText(_translate("Form", "Search"))
        
    def buttonClicked(self):
        links = queryLinks.query(self.lineEdit.text(), self.bookkeeping, self.inverted, self.special, self.pageranks)
        titles, urls, previews = queryLinks.getPreview(links, self.bookkeeping)
        for i in range(1,len(titles)+1):
            try:
                eval("self.label_"+ str(i)).setText("<span style='font-size:14pt; font-weight:600; color:#0000CC;'>" + titles[i-1] + "<br></span>"+
                                    "<span style='font-size:11pt; font-weight:600; color:#00aa00;'>"+ urls[i-1] +"<br></span>" +
                                    "<span style='font-size:11pt; font-weight:600; color:#000000;'>" + str(previews[i-1]) + "<br></span>")
            except:
                pass
        
        
    def closeEvent(self, event):
        print("event")
        event.accept()


if __name__ == "__main__":
    app = 0
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())


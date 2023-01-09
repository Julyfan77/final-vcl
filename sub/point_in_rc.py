# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'point_in.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_point_Form(object):
    def setupUi(self, point_Form):
        point_Form.setObjectName("point_Form")
        point_Form.resize(180, 101)
        self.gridLayout = QtWidgets.QGridLayout(point_Form)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(point_Form)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.label_2 = QtWidgets.QLabel(point_Form)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_4 = QtWidgets.QLabel(point_Form)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_3.addWidget(self.label_4)
        self.label_5 = QtWidgets.QLabel(point_Form)
        self.label_5.setObjectName("label_5")
        self.verticalLayout_3.addWidget(self.label_5)
        self.horizontalLayout.addLayout(self.verticalLayout_3)
        self.horizontalLayout_3.addLayout(self.horizontalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.x = QtWidgets.QLineEdit(point_Form)
        self.x.setObjectName("x")
        self.verticalLayout_2.addWidget(self.x)
        self.y = QtWidgets.QLineEdit(point_Form)
        self.y.setObjectName("y")
        self.verticalLayout_2.addWidget(self.y)
        self.horizontalLayout_3.addLayout(self.verticalLayout_2)
        self.verticalLayout_4.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.ok_btn = QtWidgets.QPushButton(point_Form)
        self.ok_btn.setObjectName("ok_btn")
        self.horizontalLayout_2.addWidget(self.ok_btn)
        self.re_btn = QtWidgets.QPushButton(point_Form)
        self.re_btn.setObjectName("re_btn")
        self.horizontalLayout_2.addWidget(self.re_btn)
        self.verticalLayout_4.addLayout(self.horizontalLayout_2)
        self.gridLayout.addLayout(self.verticalLayout_4, 0, 0, 1, 1)

        self.retranslateUi(point_Form)
        self.re_btn.clicked.connect(self.x.clear)
        self.re_btn.clicked.connect(self.y.clear)
        QtCore.QMetaObject.connectSlotsByName(point_Form)

    def retranslateUi(self, point_Form):
        _translate = QtCore.QCoreApplication.translate
        point_Form.setWindowTitle(_translate("point_Form", "参数输入"))
        self.label.setText(_translate("point_Form", "<html><head/><body><p><span style=\" font-size:10pt; font-weight:600;\">X</span><span style=\" font-size:10pt; font-weight:600; vertical-align:sub;\">图形内某点</span></p></body></html>"))
        self.label_2.setText(_translate("point_Form", "<html><head/><body><p><span style=\" font-size:10pt; font-weight:600;\">Y</span><span style=\" font-size:10pt; font-weight:600; vertical-align:sub;\">图形内某点</span></p></body></html>"))
        self.label_4.setText(_translate("point_Form", "<html><head/><body><p><span style=\" font-size:10pt; font-weight:600;\">：</span></p></body></html>"))
        self.label_5.setText(_translate("point_Form", "<html><head/><body><p><span style=\" font-size:10pt; font-weight:600;\">：</span></p></body></html>"))
        self.ok_btn.setText(_translate("point_Form", "确定"))
        self.re_btn.setText(_translate("point_Form", "重置"))


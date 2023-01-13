from typing import Any

from PyQt5.QtCore import QModelIndex, Qt, pyqtSignal
from PyQt5.QtGui import QIcon, QStandardItem, QStandardItemModel




class DrawingModel(QStandardItemModel):
    ID, TYPE = range(2)
    changed = pyqtSignal()

    def __init__(self, parent) -> None:
        super().__init__(0, 1, parent)
        self.setHeaderData(DrawingModel.ID, Qt.Horizontal, "Id")
        self.setHeaderData(DrawingModel.TYPE, Qt.Horizontal, "Type")
        self.obj = None

    

    def data(self, index: QModelIndex, role: int) -> Any:
        if index.column() == self.ID:
            drawing = self.getUserData(index)
            if role == Qt.DisplayRole or role == Qt.EditRole:
                if drawing == self.obj:  # Root
                    return "Document"
                else:
                    return drawing.id
            elif role == Qt.DecorationRole:
                return self._getIcon(drawing)
        return super().data(index, role)

    def setData(self, index: QModelIndex, value: Any, role: int) -> bool:
        if role == Qt.EditRole:
            if index.column() == self.ID:
                drawing = self.getUserData(index)
                try:
                    parent = drawing.parent()
                    if parent is not None:
                        parent.setItemId(drawing.id, str(value))
                    else:
                        drawing.id = str(value)
                except Exception:
                    return False
                self.dataChanged.emit(index, index, [role])
                self.changed.emit()
                return True
        return super().setData(index, value, role)

    

    def _addChildren(self, root: QStandardItem, value: DrawingGroup) -> None:
        for drawing in value.children:
            type = drawing.__class__.__name__
            item = QStandardItem(drawing.id)
            self._setUserData(item, drawing)
            root.appendRow(item)
            index = self.indexFromItem(item).row()

            typeItem = QStandardItem(type)
            typeItem.setEditable(False)
            root.setChild(index, self.TYPE, typeItem)

            if isinstance(drawing, DrawingGroup):
                self._addChildren(item, drawing)

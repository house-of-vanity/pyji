import random
import sys
from PySide6.QtWidgets import (
    QTableWidget,
    QTableWidgetItem,
    QCheckBox,
    QHeaderView,
    QApplication,
    QLabel,
    QVBoxLayout,
    QWidget,
    QPushButton,
    QHBoxLayout,
    QDialog,
    QSpinBox,
    QFormLayout,
    QDialogButtonBox,
    QSlider,
    QColorDialog,
    QProgressBar,
    QInputDialog,
    QFileDialog,
    QMessageBox,
)
from PySide6.QtCore import QTimer, QTime, Qt, QPoint
from PySide6.QtGui import QIcon, QMouseEvent, QPixmap, QColor, QFontMetrics

# Locals
import config as conf
import deck


class DeckSelectionDialog(QDialog):
    def __init__(self, collection, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Select Items")
        self.collection = collection
        self.setFixedSize(400, 500)  # Set fixed size for the dialog

        self.layout = QVBoxLayout(self)

        # Create the table widget
        self.table = QTableWidget(self)
        self.table.setColumnCount(2)  # Two columns: one for checkbox and one for item name
        self.table.setHorizontalHeaderLabels(["Select", "Deck Name"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Add example items to the table
        config = conf.read_config(conf.get_config_path())
        selected_decks = config.get('UI', 'selected_decks', fallback='').split(',')

        self.populate_table(selected_decks)

        self.layout.addWidget(self.table)

        # Button to add file from the file system
        self.add_file_button = QPushButton("Add File", self)
        self.add_file_button.clicked.connect(self.add_file)

        # Button to add URL
        self.add_url_button = QPushButton("Add URL", self)
        self.add_url_button.clicked.connect(self.add_url)

        # Layout for add buttons
        add_button_layout = QHBoxLayout()
        add_button_layout.addWidget(self.add_file_button)
        add_button_layout.addWidget(self.add_url_button)

        self.layout.addLayout(add_button_layout)

        # OK and Cancel buttons
        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        self.layout.addWidget(self.button_box)

    def populate_table(self, selected_decks):
        deck_names = self.collection.get_decks()
        self.table.setRowCount(len(deck_names))
        for row, deck_name in enumerate(deck_names):
            checkbox = QCheckBox()
            if deck_name in selected_decks:
                checkbox.setChecked(True)
            self.table.setCellWidget(row, 0, checkbox)
            self.table.setItem(row, 1, QTableWidgetItem(deck_name))


    def get_selected_items(self):
        selected_items = []
        for row in range(self.table.rowCount()):
            checkbox = self.table.cellWidget(row, 0)
            if checkbox.isChecked():
                item_name = self.table.item(row, 1).text()
                selected_items.append(item_name)
        return selected_items

    def add_file(self):
        file_dialog = QFileDialog(self)
        file_path, _ = file_dialog.getOpenFileName(self, "Select File")
        if file_path:
            self.add_item(file_path)

    def add_url(self):
        url, ok = QInputDialog.getText(self, "Add URL", "Enter URL:")
        if ok and url:
            self.add_item(url)

    def add_item(self, item):
        row_count = self.table.rowCount()
        self.table.insertRow(row_count)

        checkbox = QCheckBox()
        self.table.setCellWidget(row_count, 0, checkbox)
        self.table.setItem(row_count, 1, QTableWidgetItem(item))

    def show_error_message(self, message):
        QMessageBox.critical(self, "Error", message)


class SettingsDialog(QDialog):
    def __init__(self, current_interval, current_opacity, collection, parent=None):
        super().__init__(parent)
        self.collection = collection
        self.setWindowTitle("Settings")

        self.main_bg_color = parent.bg_color
        self.main_text_color = parent.text_color

        self.layout = QFormLayout(self)

        # Create spinbox for selecting interval
        self.interval_spinbox = QSpinBox(self)
        self.interval_spinbox.setMinimum(1)
        self.interval_spinbox.setMaximum(60)
        self.interval_spinbox.setValue(current_interval)
        self.layout.addRow("Update interval (seconds):", self.interval_spinbox)

        # Create slider for selecting opacity
        self.opacity_slider = QSlider(Qt.Horizontal, self)
        self.opacity_slider.setMinimum(10)
        self.opacity_slider.setMaximum(100)
        self.opacity_slider.setValue(int(current_opacity * 100))
        self.layout.addRow("Window opacity (%):", self.opacity_slider)

        # Button for selecting background color
        self.bg_color_button = QPushButton("Select Background Color", self)
        self.bg_color_button.clicked.connect(self.select_bg_color)
        self.layout.addRow(self.bg_color_button)

        # Button for selecting text color
        self.text_color_button = QPushButton("Select Text Color", self)
        self.text_color_button.clicked.connect(self.select_text_color)
        self.layout.addRow(self.text_color_button)

        # Select decks button
        self.item_selection_button = QPushButton("Deck manager", self)
        self.item_selection_button.clicked.connect(self.open_item_selection)
        self.layout.addRow(self.item_selection_button)

        # OK and Cancel buttons
        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        self.layout.addWidget(self.button_box)

    def open_item_selection(self):
        dialog = DeckSelectionDialog(self.collection, self)
        if dialog.exec():
            selected_items = dialog.get_selected_items()
            print("Selected items:", selected_items)
            self.save_selected_decks(selected_items)

    def save_selected_decks(self, selected_decks):
        self.parent().selected_decks = selected_decks
        self.parent().config['UI']['selected_decks'] = ','.join(selected_decks)
        conf.write_config(self.parent().config)

    def select_bg_color(self):
        color = QColorDialog.getColor(self.main_bg_color, self, "Select Background Color")
        if color.isValid():
            self.main_bg_color = color

    def select_text_color(self):
        color = QColorDialog.getColor(self.main_text_color, self, "Select Text Color")
        if color.isValid():
            self.main_text_color = color

    def get_settings(self):
        return (
            self.interval_spinbox.value(),
            self.opacity_slider.value() / 100.0,
            self.main_bg_color,
            self.main_text_color,
        )


class MainWindow(QWidget):
    def __init__(self, config):
        super().__init__()
        self.collection = deck.Collection(directory_path=f"{conf.get_config_path(config=False)}/decks/")
        self.current_card = None
        self.config = config
        self.update_interval = config.getint("UI", "update_interval", fallback=10)
        self.window_opacity = config.getfloat("UI", "window_opacity", fallback=1.0)
        self.bg_color = QColor(config.get("UI", "bg_color", fallback="darkCyan"))
        self.text_color = QColor(config.get("UI", "text_color", fallback="black"))
        selected_decks = self.config.get('UI', 'selected_decks', fallback='')
        if selected_decks:
            self.selected_decks = selected_decks.split(',')
        else:
            self.selected_decks = self.collection.get_decks()

        self.oldPos = self.pos()  # For moving the window
        self.resizing = False  # For resizing the window
        self.always_on_top = False  # Track the always on top state
        self.timer_running = True  # Track timer state
        self.initUI()

    def initUI(self):
        self.resize(200, 200)
        self.setWindowTitle("PyJi")

        # Remove window frame
        self.setWindowFlags(Qt.FramelessWindowHint)

        # Set window opacity
        self.setWindowOpacity(self.window_opacity)

        # Apply styles specific to MainWindow only
        self.setStyleSheet(
            f"""
            MainWindow {{
                background-color: {self.bg_color.name()};
            }}
            QLabel#MainText {{
                color: {self.text_color.name()};
            }}
            """
        )

        # Create QLabel for displaying text
        self.label = QLabel("^_,,_^", self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setWordWrap(True)
        self.label.setObjectName("MainText")
        self.update_font_size()

        # Settings button
        self.settings_button = QPushButton(self)
        self.settings_button.setIcon(QIcon("icons/settings.png"))
        self.settings_button.setFixedSize(16, 16)
        self.settings_button.clicked.connect(self.open_settings)
        self.settings_button.setStyleSheet("QPushButton { border: none; }")
        self.settings_button.setCursor(Qt.CursorShape.PointingHandCursor)

        # Close button
        self.close_button = QPushButton(self)
        self.close_button.setIcon(QIcon("icons/close.png"))
        self.close_button.setFixedSize(12, 12)
        self.close_button.clicked.connect(self.close)
        self.close_button.setStyleSheet("QPushButton { border: none; }")
        self.close_button.setCursor(Qt.CursorShape.PointingHandCursor)

        # Always on top button
        self.always_on_top_button = QPushButton(self)
        # Set pin state
        if self.config.getboolean("UI", "pin", fallback=False):
            self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
            self.always_on_top_button.setIcon(QIcon("icons/pin.png"))
            self.always_on_top = not self.always_on_top
        else:
            self.always_on_top_button.setIcon(QIcon("icons/unpin.png"))
        self.always_on_top_button.setFixedSize(20, 20)
        self.always_on_top_button.clicked.connect(self.toggle_always_on_top)
        self.always_on_top_button.setStyleSheet("QPushButton { border: none; }")
        self.always_on_top_button.setCursor(Qt.CursorShape.PointingHandCursor)

        # Resize icon
        self.resize_icon = QLabel(self)
        self.resize_icon.setPixmap(
            QPixmap("icons/resize.png").scaled(14, 14, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        )
        self.resize_icon.setCursor(Qt.SizeFDiagCursor)

        # Timer icon
        self.timer_icon = QLabel(self)
        self.update_timer_icon()
        # self.timer_icon.setFixedSize(20, 20)

        # Layout for settings, always on top, and close buttons
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.settings_button)
        button_layout.addStretch()
        button_layout.addWidget(self.always_on_top_button)
        button_layout.addWidget(self.close_button)

        # Center layout for the label
        center_layout = QVBoxLayout()
        center_layout.addStretch()
        center_layout.addWidget(self.label)
        center_layout.addStretch()
        center_layout.setAlignment(Qt.AlignCenter)

        # Layout for bottom buttons
        bottom_layout = QHBoxLayout()
        bottom_layout.addWidget(self.timer_icon, alignment=Qt.AlignLeft | Qt.AlignBottom)
        bottom_layout.addStretch()
        bottom_layout.addWidget(self.resize_icon, alignment=Qt.AlignRight | Qt.AlignBottom)

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.addLayout(button_layout)
        main_layout.addLayout(center_layout)
        main_layout.addLayout(bottom_layout)
        main_layout.setStretch(1, 1)  # Make center_layout take all available space
        self.setLayout(main_layout)

        # Create timer for updating text every second
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_text)
        self.timer.start(self.update_interval * 1000)  # Interval in milliseconds

    def update_text(self):
        if self.selected_decks:
            deck_name = random.choice(self.selected_decks)
            try:
                card = self.collection.get_random_card(deck_name)
                self.current_card = card  # Сохраняем текущую карточку
                self.label.setText(card[0])  # Отображаем первую сторону карточки (вопрос)
                self.update_font_size(is_question=True)  # Устанавливаем большой шрифт для вопроса
                self.label.adjustSize()
            except ValueError as e:
                self.label.setText(str(e))
        else:
            self.label.setText("No decks selected")

    def update_timer_icon(self):
        if self.timer_running:
            self.timer_icon.setPixmap(
                QPixmap("icons/play.png").scaled(14, 14, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            )
        else:
            self.timer_icon.setPixmap(
                QPixmap("icons/pause.png").scaled(14, 14, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            )

    def open_settings(self):
        dialog = SettingsDialog(self.update_interval, self.window_opacity, self.collection, self)
        if dialog.exec():
            self.update_interval, self.window_opacity, self.bg_color, self.text_color = dialog.get_settings()
            self.timer.setInterval(self.update_interval * 1000)  # Update timer interval
            self.setWindowOpacity(self.window_opacity)  # Update window opacity
            # Apply styles specific to MainWindow only
            self.config["UI"]["update_interval"] = str(self.update_interval)
            self.config["UI"]["window_opacity"] = str(self.window_opacity)
            self.config["UI"]["bg_color"] = self.bg_color.name()
            self.config["UI"]["text_color"] = self.text_color.name()
            conf.write_config(self.config)

    def update_font_size(self, is_question=True):
        # Рассчитываем базовый размер шрифта в зависимости от размера окна
        base_font_size = min(self.width(), self.height()) // 5
        font = self.label.font()
        if is_question:
            font.setPointSize(base_font_size)  # Большой шрифт для вопроса
        else:
            font.setPointSize(base_font_size * 0.5)  # Меньший шрифт для ответа (70% от базового)
        self.label.setFont(font)

    def resizeEvent(self, event):
        # Проверяем, какая сторона карточки отображается
        if self.current_card and self.label.text() == self.current_card[0]:
            # Если отображается вопрос
            self.update_font_size(is_question=True)
        else:
            # Если отображается ответ или другой текст
            self.update_font_size(is_question=False)
        super().resizeEvent(event)

    def toggle_always_on_top(self):
        if self.always_on_top:
            self.setWindowFlags(self.windowFlags() & ~Qt.WindowStaysOnTopHint)
            self.config["UI"]["pin"] = "False"
            self.always_on_top_button.setIcon(QIcon("icons/unpin.png"))
        else:
            self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
            self.always_on_top_button.setIcon(QIcon("icons/pin.png"))
            self.config["UI"]["pin"] = "True"
        self.always_on_top = not self.always_on_top
        conf.write_config(self.config)
        self.show()

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.oldPos = event.globalPos()
            if self.is_in_resize_zone(event.pos()):
                self.resizing = True
            else:
                self.resizing = False

    def mouseMoveEvent(self, event: QMouseEvent):
        if event.buttons() == Qt.LeftButton:
            if self.resizing:
                self.resize_window(event.globalPos())
            else:
                delta = QPoint(event.globalPos() - self.oldPos)
                self.move(self.x() + delta.x(), self.y() + delta.y())
                self.oldPos = event.globalPos()

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            if not self.resizing:
                if self.label.geometry().contains(event.pos()):
                    if not self.timer_running:
                        self.timer.start(self.update_interval * 1000)
                        self.timer_running = True
                        self.update_timer_icon()
                        self.update_text()
                    else:
                        self.timer.stop()
                        self.timer_running = False
                        self.update_timer_icon()
        elif event.button() == Qt.RightButton:
            if self.current_card:
                # Останавливаем таймер, если он запущен
                if self.timer_running:
                    self.timer.stop()
                    self.timer_running = False
                    self.update_timer_icon()
                current_text = self.label.text()
                # Проверяем, отображается ли первая сторона
                if current_text == self.current_card[0]:
                    # Объединяем обратную сторону и комментарий
                    combined_text = self.current_card[1]
                    if len(self.current_card) > 2:
                        combined_text += '\n\n' + self.current_card[2]
                    self.label.setText(combined_text)
                    self.update_font_size(is_question=False)  # Устанавливаем меньший шрифт для ответа
                else:
                    # Возвращаемся к первой стороне
                    self.label.setText(self.current_card[0])
                    self.update_font_size(is_question=True)  # Устанавливаем большой шрифт для вопроса
                self.label.adjustSize()

        self.resizing = False

    def is_in_resize_zone(self, pos):
        return pos.x() > self.width() - 30 and pos.y() > self.height() - 30

    def resize_window(self, globalPos):
        delta = globalPos - self.oldPos
        new_width = max(self.minimumWidth(), self.width() + delta.x())
        new_height = max(self.minimumHeight(), self.height() + delta.y())
        self.resize(new_width, new_height)
        self.oldPos = globalPos

    def update_text_right_click(self):
        # Function to update text on right click
        self.label.setText("Right-click content updated")
        self.label.adjustSize()

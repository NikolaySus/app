"""
Модуль с реализацией граничного класса EvaluationUI.
"""
from PyQt6.QtWidgets import (
    QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QSlider,
    QLineEdit, QTextEdit, QMessageBox, QListWidget, QComboBox, QApplication
)
from PyQt6.QtCore import QObject, QEvent, QTimer, Qt

from control.create_evaluation import CreateEvaluation
from control.select_evaluation import SelectEvaluation
from control.run_evaluation import RunEvaluation
from control.delete_evaluation import DeleteEvaluation
from util.translation_manager import TranslationManager


class EvaluationUI(QWidget):
    """
    Граничный класс.
    """
    def __init__(self):
        super().__init__()
        # Левая сторона: поиск + список
        self.search_input = QLineEdit()

        self.eval_list = QListWidget()

        left_layout = QVBoxLayout()
        left_layout.addWidget(self.search_input)
        left_layout.addWidget(self.eval_list)

        # Правая сторона: детали / действия
        self.name_input = QLineEdit()
        self.name_input.setDisabled(False)
        self.result_box = QTextEdit()
        self.result_box.setDisabled(True)

        self.current_eval = None
        self.state_label = QLabel()
        self.state_label.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignCenter)
        self.state_label.setMaximumWidth(54)
        self.polling_enabled = True

        self.create_btn = QPushButton()
        self.run_btn = QPushButton()
        self.stop_btn = QPushButton()
        self.delete_btn = QPushButton()

        right_layout = QVBoxLayout()
        name_layout = QHBoxLayout()
        name_layout.addWidget(self.name_input, stretch=4)
        name_layout.addWidget(self.state_label, stretch=1)

        right_layout.addLayout(name_layout)
        right_layout.addWidget(self.result_box)
        right_layout.addWidget(self.create_btn)
        right_layout.addWidget(self.run_btn)
        right_layout.addWidget(self.stop_btn)
        right_layout.addWidget(self.delete_btn)

        # Основной макет
        main_layout = QHBoxLayout()
        main_layout.addLayout(left_layout, stretch=1)
        main_layout.addLayout(right_layout, stretch=4)

        # Итоговый основной макет
        final_main_layout = QVBoxLayout()
        final_main_layout.addLayout(main_layout)
        ui_settings_layout = QHBoxLayout()
        self.lang_box = QComboBox()
        self.lang_box.addItems(["English", "Русский"])
        self.ui_scaler = QSlider(Qt.Orientation.Horizontal, self)

        # Создание меток для каждого значения деления
        max_val = 275
        tick_interval = 25
        self.min_val = tick_interval
        self.init_val = (max_val + self.min_val) // 2
        self.ui_scaler.setMinimum(self.min_val)
        self.ui_scaler.setMaximum(max_val)
        self.ui_scaler.setTickInterval(tick_interval)
        self.ui_scaler.setTickPosition(QSlider.TickPosition.TicksBothSides)
        self.ui_scaler.setValue(self.init_val)
        self.ui_scaler.setSingleStep(tick_interval)
        self.ui_scaler.setPageStep(tick_interval)
        self.ui_scaler.valueChanged.connect(self.set_scale)

        # Create a container for slider and labels
        slider_container = QWidget()
        slider_container_layout = QVBoxLayout()
        slider_container_layout.setContentsMargins(0, 0, 0, 0)
        slider_container_layout.setSpacing(2)

        # Добавление ползунка
        slider_container_layout.addWidget(self.ui_scaler)

        # Создание меток для делений
        self.tick_labels = {}
        tick_labels_layout = QHBoxLayout()
        tick_labels_layout.setContentsMargins(0, 0, 0, 0)
        tick_labels_layout.setSpacing(0)  # No spacing between items

        # Create labels for each tick value
        tick_values = list(range(self.min_val, max_val + 1, tick_interval))

        for i, value in enumerate(tick_values):
            label = QLabel(f"{value}%")
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setMinimumWidth(20)
            # Store reference to label for highlighting
            self.tick_labels[value] = label

            # Add the label
            tick_labels_layout.addWidget(label)

        # Добавление растяжения между метками (кроме последней)
            if i < len(tick_values) - 1:
                # Add stretch to create even spacing between labels
                # Use stretch factor 2 for more even distribution
                tick_labels_layout.addStretch(1)

        # Добавление небольшого растяжения для учета отступа ползунка
        tick_labels_layout.addStretch(0)

        self.ui_settings_label = QLabel()
        slider_container_layout.addLayout(tick_labels_layout)
        slider_container.setLayout(slider_container_layout)
        ui_settings_layout.addWidget(self.ui_settings_label, stretch=1)
        ui_settings_layout.addWidget(slider_container, stretch=7)
        ui_settings_layout.addWidget(self.lang_box, stretch=2)
        final_main_layout.addLayout(ui_settings_layout)
        self.setLayout(final_main_layout)

        # Connect valueChanged signal to update label highlighting
        self.ui_scaler.valueChanged.connect(self._update_tick_label_highlight)
        # Initialize highlighting for initial value
        self._update_tick_label_highlight(self.init_val)

        # Signals
        self.search_input.textChanged.connect(self.update_eval_list)
        self.search_input.installEventFilter(self)
        self.eval_list.itemClicked.connect(self.select_eval)
        self.eval_list.viewport().mousePressEvent = self.on_list_clicked
        self.eval_list.viewport().installEventFilter(self)

        self.create_btn.clicked.connect(self.create_eval)
        self.run_btn.clicked.connect(self.run_eval)
        self.stop_btn.clicked.connect(self.stop_eval)
        self.delete_btn.clicked.connect(self.delete_eval)

        self.update_eval_list()
        self.scale_factor = 1.0
        self.set_scale(self.init_val)

        # Poll for selected evaluation updates
        self.poll_timer = QTimer()
        self.poll_timer.timeout.connect(self.select_eval)
        self.poll_timer.start(1000)  # poll every 1 second

        # Connect language change to update UI texts
        self.lang_box.currentTextChanged.connect(self._update_ui_texts)
        self._update_ui_texts()

    def eventFilter(self, obj: QObject, event: QEvent) -> bool:
        """
        Утилита.
        Снимает выделение с элемента в self.eval_list, если пользователь
        кликнул на пустую область или на поле поиска.
        """
        if (obj == self.eval_list.viewport() and
            event.type() == QEvent.Type.MouseButtonPress):
            pos = event.position().toPoint()
            item = self.eval_list.itemAt(pos)
            if item is None:
                # Clicked empty area → deselect
                self.eval_list.clearSelection()
                self.clear_current_evaluation()
            # Let the normal event processing continue
            return False
        elif (obj == self.search_input and
              event.type() == QEvent.Type.MouseButtonPress):
            # Clicked on search input → deselect
            self.eval_list.clearSelection()
            self.clear_current_evaluation()
            # Let the normal event processing (so the search input gets focus)
            return False
        return super().eventFilter(obj, event)

    def create_eval(self):
        """
        Создание оценки.
        """
        name = self.name_input.text()
        controller = CreateEvaluation()

        try:
            self.current_eval = controller.create_eval(name)
            self.name_input.setDisabled(True)  # lock after creation
            self.update_eval_list()

            # Select the newly created evaluation in the list
            self._select_eval_in_list(self.current_eval.eval_id)
        except ValueError as e:
            QMessageBox.warning(self, "Invalid name", str(e))

    def run_eval(self):
        """
        Запуск оценки.
        """
        if not self.current_eval:
            return
        self.polling_enabled = False  # Приостановка опроса во время операции
        try:
            RunEvaluation.run_eval(self.current_eval)
        except AssertionError:
            self.polling_enabled = True  # Возобновление опроса
            return
        state_info = self.current_eval.get_state_timestamps()
        self.state_label.setText(f"{state_info['state']}")
        self.polling_enabled = True  # Resume polling

    def stop_eval(self):
        """
        Остановка оценки.
        """
        if not self.current_eval:
            return
        try:
            RunEvaluation.stop_eval(self.current_eval.get_eval_id())
        except KeyError:
            QMessageBox.warning(
                self, "Not running",
                f"{self.current_eval.get_eval_name()} not running")
        state_info = self.current_eval.get_state_timestamps()
        self.state_label.setText(f"{state_info['state']}")

    def delete_eval(self):
        """
        Удаление оценки.
        """
        if not self.current_eval:
            return

        self.polling_enabled = False  # Приостановка опроса во время удаления
        controller = DeleteEvaluation()
        controller.delete_eval(self.current_eval.eval_id)

        self.current_eval = None
        self.name_input.clear()
        self.name_input.setDisabled(False)  # Enable for new creation
        self.result_box.clear()
        self.state_label.setText("-")
        self.eval_list.clear()

        self.update_eval_list()
        self.polling_enabled = True  # Возобновление опроса

    def update_eval_list(self):
        """
        Утилита.
        """
        prefix = self.search_input.text()
        controller = SelectEvaluation()
        evals = controller.select_eval_by_name(prefix)

        self.eval_list.clear()
        for evaluation in evals:
            self.eval_list.addItem(
                f"{evaluation.eval_id}: {evaluation.eval_name}"
            )

    def select_eval(self, item=None):
        """
        Выбор оценки.
        """
        if not self.polling_enabled and item is None:
            return  # Пропустить опрос во время выполнения операций

        if item is None and not self.current_eval:
            return

        if item is not None:
            eval_id = int(item.text().split(":")[0])
        else:
            eval_id = self.current_eval.eval_id

        controller = SelectEvaluation()
        self.current_eval = controller.select_eval_by_id(eval_id)

        self.name_input.setText(self.current_eval.eval_name)
        self.name_input.setDisabled(True)   # Disable renaming

        self.result_box.setText(self.current_eval.eval_results or "")

        state_info = self.current_eval.get_state_timestamps()
        self.state_label.setText(f"{state_info['state']}")

    def on_list_clicked(self, event):
        """
        Утилита.
        """
        item = self.eval_list.itemAt(event.pos())

        if item is None:
            # Clicked empty area → deselect
            self.eval_list.clearSelection()
            self.clear_current_evaluation()
        else:
            # Let normal selection handling continue
            QListWidget.viewport(self.eval_list).mousePressEvent(event)

    def clear_current_evaluation(self):
        """
        Утилита.
        """
        self.current_eval = None
        self.name_input.clear()
        self.name_input.setDisabled(False)
        self.result_box.clear()
        self.state_label.setText(TranslationManager.tr("state_label"))

    def _update_ui_texts(self):
        """Обновление всех текстов интерфейса при смене языка."""
        TranslationManager.switch_language(self.lang_box.currentText())
        self.setWindowTitle(TranslationManager.tr("window_title"))
        self.search_input.setPlaceholderText(
            TranslationManager.tr("search_placeholder"))
        self.name_input.setPlaceholderText(
            TranslationManager.tr("name_placeholder"))
        self.create_btn.setText(TranslationManager.tr("create_btn"))
        self.run_btn.setText(TranslationManager.tr("run_btn"))
        self.stop_btn.setText(TranslationManager.tr("stop_btn"))
        self.delete_btn.setText(TranslationManager.tr("delete_btn"))
        self.ui_settings_label.setText(
            TranslationManager.tr("ui_settings_label"))
        self.state_label.setText(
            TranslationManager.tr("state_label"))

    def _select_eval_in_list(self, eval_id: int):
        """
        Утилита.
        Выбор оценки в виджете списка по её идентификатору.
        """
        for i in range(self.eval_list.count()):
            item = self.eval_list.item(i)
            if item and item.text().startswith(f"{eval_id}:"):
                self.eval_list.setCurrentItem(item)
                # Trigger the selection handler to update UI
                self.select_eval(item)
                break

    def _update_tick_label_highlight(self, value: int):
        """
        Обновление подсветки меток делений в зависимости от текущего значения ползунка.
        Подсвечивает метку, соответствующую текущему или ближайшему значению деления.
        """
        # Сброс всех меток к стилю по умолчанию
        for _, label in self.tick_labels.items():
            label.setStyleSheet("")  # Reset to default
        # Сброс жирности шрифта при необходимости
            font = label.font()
            font.setBold(False)
            label.setFont(font)

        # Find the nearest tick value
        self.min_val = self.ui_scaler.minimum()
        tick_interval = self.ui_scaler.tickInterval()
        if tick_interval <= 0:
            return

        # Вычисление ближайшего значения деления
        remainder = (value - self.min_val) % tick_interval
        if remainder <= tick_interval // 2:
            nearest_tick = value - remainder
        else:
            nearest_tick = value + (tick_interval - remainder)

        # Ensure nearest tick is within bounds
        nearest_tick = max(self.min_val,
                           min(nearest_tick, self.ui_scaler.maximum()))

        # Подсветка метки для ближайшего деления
        if nearest_tick in self.tick_labels:
            label = self.tick_labels[nearest_tick]
            # Apply highlight style
            label.setStyleSheet("font-weight: bold; color: #0066cc;")
            # Also set font weight for consistency
            font = label.font()
            font.setBold(True)
            label.setFont(font)

    def _snap_to_tick(self):
        """
        Привязка ползунка к ближайшему делению при отпускании.
        Это заставляет ползунок фиксироваться на делениях.
        """
        value = self.ui_scaler.value()
        tick_interval = self.ui_scaler.tickInterval()
        if tick_interval <= 0:
            return

        # Вычисление ближайшего значения деления
        self.min_val = self.ui_scaler.minimum()
        remainder = (value - self.min_val) % tick_interval
        if remainder <= tick_interval // 2:
            snapped_value = value - remainder
        else:
            snapped_value = value + (tick_interval - remainder)

        # Ensure snapped value is within bounds
        snapped_value = max(self.min_val,
                            min(snapped_value, self.ui_scaler.maximum()))

        # Set the snapped value
        self.ui_scaler.setValue(snapped_value)
        # Update label highlighting after snapping
        self._update_tick_label_highlight(snapped_value)
        return snapped_value

    def set_scale(self, value: int):
        """
        Установка масштаба интерфейса на основе значения ползунка.
        Значение в процентах (25-325).
        """
        value = self._snap_to_tick()
        # Convert slider value to scale factor (1.0 = 100%)
        wtf = self.scale_factor
        self.scale_factor = value / 100.0
        wtf = self.scale_factor / wtf

        # Получение шрифта приложения
        app = QApplication.instance()
        if app:
            font = app.font()
        # Масштабирование размера шрифта
            base_font_size = 9  # Base font size in points
            scaled_font_size = int(base_font_size * self.scale_factor)
            font.setPointSize(scaled_font_size)

        # Применение шрифта ко всем виджетам
            app.setFont(font)

            # Also adjust some widget minimum sizes based on scale
            self._adjust_widget_sizes(wtf)

    def _adjust_widget_sizes(self, wtf):
        """
        Корректировка минимальных размеров виджетов на основе коэффициента масштаба.
        """
        # Корректировка минимальной высоты для кнопок и полей ввода
        min_height = int(25 * self.scale_factor)

        widgets_to_adjust = [
            self.search_input,
            self.name_input,
            self.create_btn,
            self.run_btn,
            self.stop_btn,
            self.delete_btn,
            self.state_label
        ]

        for widget in widgets_to_adjust:
            widget.setMinimumHeight(min_height)
            if widget.maximumWidth():
                widget.setMaximumWidth(int(widget.maximumWidth() * wtf))

        # Adjust list widget minimum sizes
        list_min_height = int(200 * self.scale_factor)
        self.eval_list.setMinimumHeight(list_min_height)

        # Adjust text box minimum sizes
        text_min_height = int(150 * self.scale_factor)
        self.result_box.setMinimumHeight(text_min_height)

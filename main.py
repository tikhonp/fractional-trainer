import sys
import random
from fractions import Fraction
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout
)
from PyQt6.QtCore import Qt, QTimer

# Эти числа можно поменять, чтобы генерировались другие дроби
MIN_DENOMINATOR = 2
MAX_DENOMINATOR = 10
MIN_NUMERATOR = 1
MAX_NUMERATOR = 10


def generate_fraction() -> Fraction:
    """Генерирует случайную дробь для примера"""

    denominator = random.randint(MIN_DENOMINATOR, MAX_DENOMINATOR)  # Знаменатель от 2 до 10
    numerator = random.randint(MIN_NUMERATOR, MAX_NUMERATOR)
    return Fraction(numerator, denominator)  # Создание объекта дроби


class FractionApp(QWidget):
    """Основной класс приложения"""

    def __init__(self):
        # Инициализация родительского класса
        # (от которого этот унаследован `QWidget`)
        super().__init__()

        self.initUI()
        self.generate_new_problem()

    def initUI(self):

        # Основные настройки окна
        self.setWindowTitle('Примеры с дробями')  # Заголовок окна
        self.setGeometry(100, 100, 400, 200)  # Позиция и размер окна (x, y, width, height)

        # Создание виджетов
        self.start_btn = QPushButton('Начать', self)  # Кнопка старта
        self.problem_label = QLabel(self)  # Метка для отображения примера
        self.result_label = QLabel(self)  # Метка для отображения результата проверки

        # Поля для ввода числителя и знаменателя
        self.numerator_input = QLineEdit(self)  # Поле ввода числителя
        self.denominator_input = QLineEdit(self)  # Поле ввода знаменателя
        self.check_btn = QPushButton('Проверить', self)  # Кнопка проверки

        self.frac_label = QLabel('/')

        # Начальные настройки видимости элементов
        self.problem_label.hide()  # Скрыть метку с примером
        self.result_label.hide()  # Скрыть метку с результатом
        self.numerator_input.hide()  # Скрыть поле числителя
        self.denominator_input.hide()  # Скрыть поле знаменателя
        self.check_btn.hide()  # Скрыть кнопку проверки
        self.frac_label.hide()

        # Настройка макетов
        input_layout = QHBoxLayout()  # Горизонтальный макет для полей ввода
        input_layout.addWidget(self.numerator_input)  # Добавить поле числителя
        input_layout.addWidget(self.frac_label)  # Добавить метку с дробью
        input_layout.addWidget(self.denominator_input)  # Добавить поле знаменателя

        main_layout = QVBoxLayout()  # Вертикальный основной макет
        main_layout.addWidget(self.start_btn, alignment=Qt.AlignmentFlag.AlignCenter)  # Центрировать кнопку старта
        main_layout.addWidget(self.problem_label, alignment=Qt.AlignmentFlag.AlignCenter)  # Центрировать пример
        main_layout.addLayout(input_layout)  # Добавить макет с полями ввода
        main_layout.addWidget(self.check_btn, alignment=Qt.AlignmentFlag.AlignCenter)  # Центрировать кнопку проверки
        main_layout.addWidget(self.result_label, alignment=Qt.AlignmentFlag.AlignCenter)  # Центрировать результат

        self.setLayout(main_layout)  # Установить основной макет для окна

        # Подключение обработчиков событий
        self.start_btn.clicked.connect(self.start_exercise)  # Клик по кнопке "Начать"
        self.check_btn.clicked.connect(self.check_answer)  # Клик по кнопке "Проверить"

    def start_exercise(self):
        """Начинает упражнение, показывает необходимые элементы"""

        self.start_btn.hide()  # Скрыть кнопку старта
        self.problem_label.show()  # Показать пример
        self.numerator_input.show()  # Показать поле числителя
        self.denominator_input.show()  # Показать поле знаменателя
        self.check_btn.show()  # Показать кнопку проверки
        self.result_label.show()  # Показать метку результата
        self.frac_label.show()

    def generate_new_problem(self):
        """Генерирует новую математическую задачу с дробями"""

        operators = ['+', '-', '*', '/']          # Допустимые операторы
        self.operator = random.choice(operators)  # Случайный выбор оператора

        # Генерация двух дробей
        self.f1 = generate_fraction()  # Первая дробь
        self.f2 = generate_fraction()  # Вторая дробь

        # Защита от деления на ноль
        while self.operator == '/' and self.f2 == 0:
            self.f2 = generate_fraction()

        # Вычисление правильного ответа
        if self.operator == '+':
            self.correct_answer = self.f1 + self.f2
        elif self.operator == '-':
            self.correct_answer = self.f1 - self.f2
        elif self.operator == '*':
            self.correct_answer = self.f1 * self.f2
        else:
            self.correct_answer = self.f1 / self.f2

        # Обновление текста задачи
        self.problem_label.setText(
            f"{self.f1.numerator}/{self.f1.denominator} "
            f"{self.operator} "
            f"{self.f2.numerator}/{self.f2.denominator} = ?"
        )

        # Сброс полей ввода и метки результата
        self.numerator_input.clear()
        self.denominator_input.clear()
        self.result_label.clear()

    def check_answer(self):
        """Проверяет введенный пользователем ответ"""

        try:
            # Попытка преобразовать ввод в целые числа
            numerator = int(self.numerator_input.text())
            denominator = int(self.denominator_input.text())

            if denominator == 0:  # Проверка на нулевой знаменатель
                self.result_label.setText("Ошибка ввода! В знаменателе не может быть ноль.")
                return

            user_answer = Fraction(numerator, denominator)  # Создание дроби из ввода
        except Exception:
            self.result_label.setText("Ошибка ввода! Введите целые числа.")
            return

        # Сравнение с правильным ответом
        if user_answer == self.correct_answer:
            self.result_label.setText("Правильно! Генерирую новый пример...")

            # ждем 2 секунды (2000 миллисекунд) показываем что результат правильный
            QTimer.singleShot(2000, self.generate_new_problem)

        else:
            self.result_label.setText("Неправильно. Попробуйте ещё раз.")


# Точка входа в приложение
if __name__ == '__main__':
    app = QApplication(sys.argv)  # Создание QApplication
    ex = FractionApp()  # Создание экземпляра приложения
    ex.show()  # Показать окно
    sys.exit(app.exec())  # Запуск основного цикла обработки событий

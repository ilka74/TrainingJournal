"""
Проект "Дневник тренировок".
Реализованы ввод информации о тренировках и запись этой информации в файл формата JSON.
Также доступны чтение информации, фильтрация записей, импорт в файлы формата CSV, построение графиков.

В проекте используется библиотеки:
- tkinter для графического интерфейса;
- datetime для работы с датами;
- matplotlib для построения графиков.

=========================================
Описание импортов:
* import os: стандартная библиотека в Python, которая позволяет работать с операционной системой,
включая файловую систему, процессы и переменные окружения.
Модуль os обеспечивает платформонезависимый доступ к различным функциям, что делает код более переносимым;

* import tkinter as tk: импорт основной библиотеки для создания графического пользовательского интерфейса

* from tkinter import ttk, Toplevel, messagebox, filedialog:
1. модуль ttk предоставляет расширенные виджеты для Tkinter, такие, как стилизованные кнопки, метки и комбобоксы.
2. класс Toplevel используется для создания новых окон, независимых от основного окна приложения.
3. модуль messagebox позволяет отображать всплывающие окна с сообщениями, такими как предупреждения или ошибки.
4. модуль filedialog предоставляет функции для открытия и сохранения файлов через диалоговые окна.

* from PIL import Image, ImageTk:
1. PIL (Pillow): библиотека для работы с изображениями, которая позволяет открывать, изменять и сохранять
различные форматы изображений.
2. класс Image предоставляет методы для создания, открытия и манипуляции изображениями.
С его помощью можно выполнять такие операции, как изменение размера, поворот, обрезка, фильтрация и многое другое.
3. модуль ImageTk обеспечивает связь между библиотекой PIL и tkinter, позволяя использовать изображения
в графических интерфейсах.

* import json: позволяет преобразовывать в строку (и преобразовывать из строки) данные в формате JSON

* модуль csv: предоставляет инструменты для чтения и записи данных в формате CSV.
Он поддерживает различные конфигурации, включая разные разделители, кавычки и кодировки.

* from datetime import datetime, time:
1. класс datetime предоставляет методы для работы с датами и временем. Это позволяет выполнять такие операции,
как получение текущей даты и времени, форматирование и арифметику дат.
2. класс time представляет собой объект времени (час, минуты, секунды, микросекунды) без привязки к конкретной дате.
Он позволяет создавать, сравнивать и выполнять операции с временными значениями.

* from tkcalendar import DateEntry:
1. библиотека tkcalendar расширяет возможности стандартной библиотеки tkinter, добавляя функциональность для работы
с календарями и выбора дат. Она позволяет интегрировать календарные виджеты в графические интерфейсы.
2. класс DateEntry представляет собой виджет, который позволяет пользователю выбирать дату из выпадающего календаря
или вручную вводить дату в текстовое поле. Это удобно для форм, где требуется вводить даты.

* from matplotlib.figure import Figure:
1. библиотека matplotlib используется для построения графиков и визуализации данных в Python. Она позволяет
создавать статические, анимационные и интерактивные графики.
2. класс Figure представляет собой основное окно для построения графиков. Он управляет размещением этих окон,
их размерами и другими параметрами.

* from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg:
1. модуль matplotlib.backends.backend_tkagg используется для интеграции графиков Matplotlib в приложения на tkinter;
2. класс FigureCanvasTkAgg связывает объект Figure (график Matplotlib) с виджетами tkinter.
Он позволяет отображать графики в tkinter приложениях.
=========================================

Структура программы:
** В директории "icons" содержатся файлы с иконками, соответствующие основным действиям пользователя
(добавление, просмотр, фильтрация записей и др.)

** Переменная data_file хранит имя файла по умолчанию, в который будут сохраняться данные о тренировках в формате JSON

** Основные функции программы:
- resize_image: для изменения размера изображения иконок. Новые размеры для каждой иконки указываются
в соответствующем методе класса TrainingLogApp;
- load_data: загрузка из JSON файла данных о тренировках. Применены обработки исключений для обработки возможных ошибок;
- save_data: принимает данные о тренировках в виде списка словарей и сохраняет их в файл в формате JSON.
Данные форматируются с отступом для лучшей читаемости.

** Класс TrainingLogApp:
- конструктор класса __init__: принимает объект root, который является главным окном приложения, и вызывает метод
create_widgets для создания виджетов интерфейса;
- метод create_widgets: создает виджеты для ввода данных, кнопки для добавления записи о тренировке, просмотра
и фильтрации сохраненных записей. Также реализованы кнопки экспорта записей в файлы CSV формата и импорта записей
из них, кнопки формирования статистической информации и построения графиков;
- метод update_exercise_filter: обновляет список доступных упражнений для фильтрации;
- метод add_entry: считывает данные из полей ввода, проверяет их наличие, создает словарь с информацией о тренировке,
добавляет его в список с данными и сохраняет изменения в файл;
- метод view_records: загружает сохраненные данные и отображает их в новом окне с помощью виджета Treeview.
Для каждой записи создается строка в таблице;
- метод filter_records: метод фильтрации записей по диапазону дат и упражнению;
- метод export_to_csv: применяется для экспорта данных в формат CSV. Пользователь задает имя файла в диалоговом окне,
а файл сохраняется в папке files внутри проекта;
- метод import_from_csv: используется для импорта данных из CSV файла. Пользователь выбирает файл, и данные из него
добавляются в журнал;
- метод edit_record: необходим для редактирования выбранной записи;
- метод delete_record используется для удаления выбранной записи;
- метод show_statistics: отображение статистики по выполненным упражнениям;
- метод show_charts: для визуализации прогресса по упражнениям. Применяется для построения графиков изменения веса
и количества повторов упражнений. Графики также сохраняются в формате "png" в директории "images".

** Функция main:
- Создает экземпляр Tk, который является главным окном приложения.
- Создает экземпляр приложения TrainingLogApp, передавая ему главное окно.
- Запускает главный цикл обработки событий Tkinter, чтобы окно приложения отображалось и реагировало
на действия пользователя.
"""

import os
import tkinter as tk
from tkinter import ttk, Toplevel, messagebox, filedialog
from PIL import Image, ImageTk
import json
import csv
from datetime import datetime, time
from tkcalendar import DateEntry
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Файлы с иконками
add_icon_path = 'icons/add.png'
view_icon_path = 'icons/eye.png'
filter_icon_path = 'icons/filter.png'
export_icon_path = 'icons/export.png'
import_icon_path = 'icons/import.png'
stats_icon_path = 'icons/stats.png'
chart_icon_path = 'icons/chart.png'

# Файл (по умолчанию) для сохранения данных
data_file = 'training_log.json'

# Создание папки для файлов обмена данными, если она не существует
os.makedirs('files', exist_ok=True)

def resize_image(image_path, new_width, new_height):
    """
    Функция для изменения размера изображения иконок
    """
    image = Image.open(image_path)
    resized_image = image.resize((new_width, new_height))
    return ImageTk.PhotoImage(resized_image)

def load_data():
    """
    Загрузка данных о тренировках из JSON файла. Применены обработки исключений для обработки возможных ошибок.
    """
    try:
        with open(data_file, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        # Создание пустого файла, если он не существует
        with open(data_file, 'w') as file:
            json.dump([], file)  # создаем пустой список
        messagebox.showerror("Внимание!", "Файл журнала тренировок не найден. Создан новый файл")
        return []
    except json.JSONDecodeError:
        messagebox.showerror("Внимание!", "Ошибка при разборе данных из файла или журнал пустой.")
        return []
    except Exception as e:
        messagebox.showerror("Ошибка!", f"Произошла ошибка: {e}")
        return []

def save_data(data):
    """
    Принимает данные о тренировках в виде списка словарей и сохраняет их в файл в формате JSON.
    Данные форматируются с отступом для лучшей читаемости
    """
    messagebox.showinfo("Сохранение файла", "Выберите, куда сохранить ваш журнал тренировок "
                                            "или нажмите отмену для сохранения в файл по умолчанию")
    file_path = filedialog.asksaveasfilename(
        defaultextension=".json",
        filetypes=[("JSON files", ".json"), ("ALL files", '*.*')],
        title="Сохранить файл как"
    )
    if not file_path:  # Если пользователь отменил действие, используем файл по умолчанию
        file_path = data_file

    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)


class DateTimePicker(ttk.Frame):
    """
    Класс для построения виджетов выбора даты и времени
    """
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        # Виджет даты (число/месяц/год)
        self.date_entry = DateEntry(self, width=10, background='darkblue', foreground='white',
                                    borderwidth=2, date_pattern='dd/mm/yyyy')
        self.date_entry.pack(side=tk.LEFT, padx=(0, 5))

        # Валидация для часов
        self.hour_validate = self.register(self.validate_hour)
        self.hour_spin = ttk.Spinbox(self, from_=0, to=23, width=3, format="%02.0f", validate='key',
                                     validatecommand=(self.hour_validate, '%P'))
        self.hour_spin.pack(side=tk.LEFT)

        # Валидация для минут
        self.minute_validate = self.register(self.validate_minute)
        self.minute_spin = ttk.Spinbox(self, from_=0, to=59, width=3, format="%02.0f", validate='key',
                                       validatecommand=(self.minute_validate, '%P'))
        self.minute_spin.pack(side=tk.LEFT)

    def validate_hour(self, hour):
        """
        Метод валидации для часов: только целые числа от 00 до 23.
        """
        if hour == "" or hour.isdigit() and 0 <= int(hour) <= 23:
            return True
        return False

    def validate_minute(self, minute):
        if minute == "" or minute.isdigit() and 0 <= int(minute) <= 59:
            return True
        return False

    def get(self):
        date_str = self.date_entry.get()
        time_str = f"{int(self.hour_spin.get()):02}:{int(self.minute_spin.get()):02}"  # Форматирование с нулями
        return f"{date_str} {time_str}"


class TrainingLogApp:
    """
    Основной класс проекта.
    """
    def __init__(self, root):
        self.root = root
        root.geometry("500x400")
        root.title("Дневник тренировок")
        self.exercises = []  # Список для хранения уникальных упражнений
        self.chart_counter = 1  # Инициализация счетчика графиков
        self.create_widgets()
        self.update_exercise_filter()  # Обновляем список упражнений

    def create_widgets(self):
        """
        Этот метод создает виджеты для ввода данных, кнопки для добавления записи о тренировке, просмотра и фильтрации
        сохраненных записей. Также реализованы кнопки экспорта записей в файлы CSV формата и импорта записей из них;
        кнопки формирования статистической информации и построения графиков
        """

        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)

        # Виджеты ввода информации
        self.datetime_picker = DateTimePicker(self.main_frame)
        self.datetime_picker.grid(column=0, row=0, columnspan=2, sticky=tk.EW)

        self.exercise_label = ttk.Label(self.main_frame, text="Упражнение:")
        self.exercise_label.grid(column=0, row=1, sticky=tk.W)
        self.exercise_entry = ttk.Entry(self.main_frame)
        self.exercise_entry.grid(column=1, row=1, sticky=tk.EW)

        self.weight_label = ttk.Label(self.main_frame, text="Вес, кг:")
        self.weight_label.grid(column=0, row=2, sticky=tk.W)
        self.weight_entry = ttk.Entry(self.main_frame)
        self.weight_entry.grid(column=1, row=2, sticky=tk.EW)

        self.repetitions_label = ttk.Label(self.main_frame, text="Повторения:")
        self.repetitions_label.grid(column=0, row=3, sticky=tk.W)
        self.repetitions_entry = ttk.Entry(self.main_frame)
        self.repetitions_entry.grid(column=1, row=3, sticky=tk.EW)

        self.add_icon = resize_image(add_icon_path, 30, 20)
        self.add_button = ttk.Button(
            self.main_frame,
            text="Добавить запись",
            image=self.add_icon,
            compound="left",
            command=self.add_entry
        )
        self.add_button.grid(column=0, row=4, columnspan=2, pady=5)

        self.view_icon = resize_image(view_icon_path, 30, 30)
        self.view_button = ttk.Button(
            self.main_frame,
            text="Просмотреть записи",
            image=self.view_icon,
            compound="left",
            command=self.view_records
        )
        self.view_button.grid(column=0, row=5, columnspan=2, pady=5)

        # Поля для фильтрации
        self.start_date_label = ttk.Label(self.main_frame, text="Дата начала")
        self.start_date_label.grid(column=0, row=6, sticky=tk.W)
        self.start_date_entry = DateEntry(self.main_frame, date_pattern='dd/mm/yyyy')
        self.start_date_entry.grid(column=1, row=6, sticky=tk.EW)

        self.end_date_label = ttk.Label(self.main_frame, text="Дата окончания:")
        self.end_date_label.grid(column=0, row=7, sticky=tk.W)
        self.end_date_entry = DateEntry(self.main_frame, date_pattern='dd/mm/yyyy')
        self.end_date_entry.grid(column=1, row=7, sticky=tk.EW)

        # Поле для фильтрации по упражнению (используем Combobox)
        self.exercise_filter_label = ttk.Label(self.main_frame, text="Фильтр по упражнению:")
        self.exercise_filter_label.grid(column=0, row=8, sticky=tk.W)
        self.exercise_filter_entry = ttk.Combobox(self.main_frame)
        self.exercise_filter_entry.grid(column=1, row=8, sticky=tk.EW)

        # Формируем кнопку фильтра записей по дате и упражнению
        self.filter_icon = resize_image(filter_icon_path, 20, 20)
        self.filter_button = ttk.Button(
            self.main_frame,
            text="Отфильтровать записи",
            image=self.filter_icon,
            compound="left",
            command=self.filter_records
        )
        self.filter_button.grid(column=0, row=9, columnspan=2, pady=5)

        # Контейнер для кнопок экспорта и импорта
        self.csv_frame = ttk.Frame(self.main_frame)
        self.csv_frame.grid(column=0, row=10, columnspan=2, pady=5, sticky=tk.EW)
        self.csv_frame.columnconfigure(0, weight=1)
        self.csv_frame.columnconfigure(1, weight=1)

        # Кнопка экспорта в файл формата CSV
        self.export_icon = resize_image(export_icon_path, 20, 20)
        self.export_button = ttk.Button(
            self.csv_frame,
            text="Экспорт в CSV",
            image=self.export_icon,
            compound="left",
            command=self.export_to_csv
        )
        self.export_button.grid(column=0, row=0, padx=(0, 10), sticky=tk.E)

        # Кнопка импорта из файла формата CSV
        self.import_icon = resize_image(import_icon_path, 20, 20)
        self.import_button = ttk.Button(
            self.csv_frame,
            text="Импорт из CSV",
            image=self.import_icon,
            compound="left",
            command=self.import_from_csv
        )
        self.import_button.grid(column=1, row=0, padx=(10, 0), sticky=tk.W)

        # Контейнер для кнопок статистики и визуализации
        self.stats_charts_frame = ttk.Frame(self.main_frame)
        self.stats_charts_frame.grid(column=0, row=11, columnspan=2, pady=5, sticky=tk.EW)
        self.stats_charts_frame.columnconfigure(0, weight=1)
        self.stats_charts_frame.columnconfigure(1, weight=1)

        # Кнопка формирования статистики
        self.stats_icon = resize_image(stats_icon_path, 20, 30)
        self.stats_button = ttk.Button(
            self.stats_charts_frame,
            text="Статистика",
            image=self.stats_icon,
            compound="left",
            command=self.show_statistics
        )
        self.stats_button.grid(column=0, row=0, padx=5, sticky=tk.E)

        # Кнопка визуализации (построения графиков)
        self.chart_icon = resize_image(chart_icon_path, 40, 30)
        self.chart_button = ttk.Button(
            self.stats_charts_frame,
            text="Визуализация",
            image=self.chart_icon,
            compound="left",
            command=self.show_charts
        )
        self.chart_button.grid(column=1, row=0, padx=5, sticky=tk.W)

        # Настройки колонок в основном фрейме при изменении размера окна
        self.main_frame.columnconfigure(1, weight=1)

    def update_exercise_filter(self):
        """
        Обновляет список доступных упражнений для фильтрации.
        """
        data = load_data()
        self.exercises = sorted(set(entry['exercise'] for entry in data))  # Получаем уникальные упражнения
        self.exercise_filter_entry['values'] = self.exercises  # Устанавливаем значения в Combobox

    def add_entry(self):
        """
        Этот метод считывает данные из полей ввода, проверяет их наличие, создает словарь с информацией о тренировке,
        добавляет его в список с данными и сохраняет изменения в файл.
        """
        datetime_str = self.datetime_picker.get()
        exercise = self.exercise_entry.get()
        weight = self.weight_entry.get()
        repetitions = self.repetitions_entry.get()

        if not (exercise and weight and repetitions):
            messagebox.showerror("Ошибка!", "Все поля должны быть заполнены!")
            return

        # Проверка на корректность указанного веса
        try:
            weight_value = float(weight)  # Пробуем преобразовать вес в число с плавающей запятой
            if weight_value <= 0 or weight_value > 200:
                messagebox.showerror("Ошибка!", "Вес должен быть положительным числом до 200 кг.")
                return
        except ValueError:
            messagebox.showerror("Ошибка!", "Вес должен быть числом")
            return

        # Проверка на корректность указанных повторений
        if not repetitions.isdigit() or int(repetitions) <= 0:
            messagebox.showerror("Ошибка!", "Количество повторений должно быть целым положительным числом")
            return

        entry = {
            'datetime': datetime_str,
            'exercise': exercise,
            'weight': weight,
            'repetitions': repetitions
        }

        data = load_data()
        data.append(entry)
        save_data(data)

        self.update_exercise_filter()

        # Очистка полей ввода после добавления
        self.exercise_entry.delete(0, tk.END)
        self.weight_entry.delete(0, tk.END)
        self.repetitions_entry.delete(0, tk.END)
        messagebox.showinfo("Успешно!", "Запись успешно добавлена!")

    def view_records(self, records=None):
        """
        Загружает сохраненные данные и отображает их в новом окне с помощью виджета Treeview.
        Для каждой записи создается строка в таблице.
        """
        if records is None:
            records = load_data()

        # Создаем новое окно для отображения записей
        records_window = Toplevel(self.root)
        records_window.title("Записи тренировок")

        # Создаем Treeview и сохраняем его в атрибут класса
        self.tree = ttk.Treeview(records_window, columns=("Дата", "Упражнение", "Вес", "Повторения"), show="headings")
        self.tree.heading('Дата', text="Дата")
        self.tree.heading('Упражнение', text="Упражнение")
        self.tree.heading('Вес', text="Вес")
        self.tree.heading('Повторения', text="Повторения")

        # Добавляем строки в Treeview
        for entry in records:
            self.tree.insert('', tk.END, values=(
            entry.get('datetime', 'Неизвестно'),
            entry.get('exercise', ''),
            entry.get('weight', ''),
            entry.get('repetitions', '')
            ))

        # Отображаем Treeview
        self.tree.pack(expand=True, fill=tk.BOTH)

        # Кнопки для редактирования и удаления
        ttk.Button(records_window, text="Редактировать", command=self.edit_record).pack(side=tk.LEFT, padx=5, pady=5)
        ttk.Button(records_window, text="Удалить", command=self.delete_record).pack(side=tk.LEFT, padx=5, pady=5)

    def filter_records(self):
        """
        Метод фильтрации записей по диапазону дат и упражнению
        """
        # Получаем даты из виджетов DateEntry
        start_date = self.start_date_entry.get_date()
        end_date = self.end_date_entry.get_date()
        exercise_filter = self.exercise_filter_entry.get().strip()

        # Преобразуем даты в объекты datetime, добавляя время начала и конца дня
        start_datetime = datetime.combine(start_date, time.min)  # 00:00
        end_datetime = datetime.combine(end_date, time.max)  # 23:59:59

        if start_datetime > end_datetime:
            messagebox.showerror("Ошибка!", "Дата начала не может быть позже даты окончания.")
            return

        # Загружаем данные и фильтруем
        data = load_data()
        filtered_records = [
            entry for entry in data
            if start_datetime <= datetime.strptime(entry['datetime'], '%d/%m/%Y %H:%M') <= end_datetime
               and (exercise_filter.lower() in entry['exercise'].lower() if exercise_filter else True)
        ]

        # Отображаем отфильтрованные записи
        self.view_records(filtered_records)

    def export_to_csv(self):
        """
        Метод для экспорта данных в формат CSV. Пользователь задает имя файла в диалоговом окне,
        а файл сохраняется в папке files внутри проекта.
        """
        data = load_data()
        if not data:
            messagebox.showerror("Ошибка!", "Нет данных для экспорта")
            return

        file_name = filedialog.asksaveasfilename(
            initialdir="files",
            title="Сохранить как",
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )

        if not file_name:
            return

        try:
            with open(file_name, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(["Дата", "Упражнение", "Вес", "Повторения"])
                for entry in data:
                    writer.writerow([entry['datetime'], entry['exercise'], entry['weight'], entry['repetitions']])

            messagebox.showinfo("Успешно", f"Данные успешно экспортированы в файл: {file_name}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка экспорта данных: {e}")

    def import_from_csv(self):
        """
        Метод для импорта данных из CSV файла. Пользователь выбирает файл, и данные из него добавляются в журнал.
        """
        file_name = filedialog.askopenfilename(
            initialdir="files",
            title="Выбрать файл",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )

        if not file_name:
            return

        try:
            with open(file_name, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                imported_data = []
                for row in reader:
                    # Проверяем наличие всех необходимых полей в строке
                    if "Дата" in row and "Упражнение" in row and "Вес" in row and "Повторения" in row:
                        try:
                            # Проверяем правильность формата даты
                            datetime.strptime(row["Дата"], '%d/%m/%Y %H:%M')

                            # Проверяем корректность значения "Вес"
                            weight = float(row["Вес"])
                            if weight <= 0 or weight > 200:
                                messagebox.showerror("Ошибка!",
                                                     f"Некорректное значение веса: {row['Вес']}. Вес должен быть положительным числом не более 200.")
                                return

                            # Проверяем корректность значения "Повторения"
                            repetitions = int(row["Повторения"])
                            if repetitions <= 0:
                                messagebox.showerror("Ошибка!",
                                                     f"Некорректное значение повторений: {row['Повторения']}. Повторения должны быть целым положительным числом.")
                                return

                            # Если все проверки пройдены, добавляем запись
                            imported_data.append({
                                "datetime": row["Дата"],
                                "exercise": row["Упражнение"],
                                "weight": row["Вес"],
                                "repetitions": row["Повторения"]
                            })
                        except ValueError as e:
                            messagebox.showerror("Ошибка!", f"Ошибка в строке: {row}. Проверьте формат данных. {e}")
                            return
                    else:
                        messagebox.showerror("Ошибка!", "Некорректный формат данных в файле. Убедитесь, что файл "
                                                        "содержит столбцы 'Дата', 'Упражнение', 'Вес', 'Повторения'.")
                        return
            if imported_data:
                # Загружаем текущие данные, добавляем новые и сохраняем
                data = load_data()
                data.extend(imported_data)
                save_data(data)
                self.update_exercise_filter()
                messagebox.showinfo("Успешно!", f"Данные успешно импортированы из файла: {file_name}")
            else:
                messagebox.showerror("Ошибка", "Файл не содержит данных для импорта.")

        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка импорта данных: {e}")

    def edit_record(self):
        """
        Метод для редактирования выбранной записи.
        """
        # Окно с записями должно быть открыто
        try:
            selected_item = self.tree.selection()[0]  # Получаем выбранную строку
            values = self.tree.item(selected_item, "values")  # Считываем данные строки
        except IndexError:
            messagebox.showerror("Ошибка!", "Выберите запись для редактирования")
            return

        # Открываем окно для редактирования
        edit_window = Toplevel(self.root)
        edit_window.title("Редактирование записи")
        edit_window.geometry("350x300")

        ttk.Label(edit_window, text="Дата и время").pack(pady=5)
        datetime_entry = ttk.Entry(edit_window)
        datetime_entry.insert(0, values[0])  # Заполняем текущими значениями
        datetime_entry.pack(pady=5)

        ttk.Label(edit_window, text="Упражнение:").pack(pady=5)
        exercise_entry = ttk.Entry(edit_window)
        exercise_entry.insert(0, values[1])
        exercise_entry.pack(pady=5)

        ttk.Label(edit_window, text="Вес, кг:").pack(pady=5)
        weight_entry = ttk.Entry(edit_window)
        weight_entry.insert(0, values[2])
        weight_entry.pack(pady=5)

        ttk.Label(edit_window, text="Повторения:").pack(pady=5)
        repetitions_entry = ttk.Entry(edit_window)
        repetitions_entry.insert(0, values[3])
        repetitions_entry.pack(pady=5)

        def save_changes():
            """
            Сохраняем изменения в файл.
            """
            new_datetime = datetime_entry.get().strip()
            new_exercise = exercise_entry.get().strip()
            new_weight = weight_entry.get().strip()
            new_repetitions = repetitions_entry.get().strip()

            # Проверяем корректность данных
            try:
                datetime.strptime(new_datetime, '%d/%m/%Y %H:%M')  # Проверяем формат даты
            except ValueError:
                messagebox.showerror("Ошибка!", "Некорректный формат даты. Формат: ДД/ММ/ГГГГ ЧЧ:ММ")
                return

            try:
                new_weight = float(new_weight)
                if new_weight <= 0 or new_weight > 200:
                    messagebox.showerror("Ошибка!", "Вес должен быть положительным числом не более 200 кг.")
                    return
            except ValueError:
                messagebox.showerror("Ошибка!", "Вес должен быть числом.")
                return

            if not new_repetitions.isdigit() or int(new_repetitions) <= 0:
                messagebox.showerror("Ошибка!", "Повторения должны быть целым положительным числом.")
                return

            # Загружаем текущие данные
            data = load_data()
            for entry in data:
                if entry["datetime"] == values[0] and entry["exercise"] == values[1]:
                    # Обновляем запись
                    entry["datetime"] = new_datetime
                    entry["exercise"] = new_exercise
                    entry["weight"] = str(new_weight)
                    entry["repetitions"] = new_repetitions
                    break

            # Сохраняем изменения
            save_data(data)
            messagebox.showinfo("Успешно!", "Запись успешно обновлена.")
            edit_window.destroy()
            self.view_records()  # Обновляем отображение записей

        ttk.Button(edit_window, text="Сохранить", command=save_changes).pack(pady=10)

    def delete_record(self):
        """
        Метод для удаления выбранной записи.
        """
        try:
            selected_item = self.tree.selection()[0]  # Получаем выбранную строку
            values = self.tree.item(selected_item, "values")  # Считываем данные строки
        except IndexError:
            messagebox.showerror("Ошибка!", "Выберите запись для удаления.")
            return

        # Подтверждение удаления
        confirm = messagebox.askyesno("Подтверждение", "Вы уверены, что хотите удалить эту запись?")
        if not confirm:
            return

        # Удаляем запись из данных
        data = load_data()
        data = [entry for entry in data if not (
                entry["datetime"] == values[0] and
                entry["exercise"] == values[1] and
                entry["weight"] == values[2] and
                entry["repetitions"] == values[3]
        )]

        # Сохраняем изменения
        save_data(data)
        messagebox.showinfo("Успешно!", "Запись успешно удалена.")
        self.view_records()  # Обновляем отображение записей

    def show_statistics(self):
        """
        Метод для отображения статистики по выполненным упражнениям.
        """
        # Получаем диапазон дат
        start_date = self.start_date_entry.get_date()
        end_date = self.end_date_entry.get_date()
        exercise_filter = self.exercise_filter_entry.get().strip()

        # Преобразуем даты в объекты datetime
        start_datetime = datetime.combine(start_date, time.min)
        end_datetime = datetime.combine(end_date, time.max)

        if start_datetime > end_datetime:
            messagebox.showerror("Ошибка!", "Дата начала не может быть позже даты окончания.")
            return

        # Загружаем данные и фильтруем по датам и упражнению
        data = load_data()
        filtered_records = [
            entry for entry in data
            if start_datetime <= datetime.strptime(entry['datetime'], '%d/%m/%Y %H:%M') <= end_datetime
               and (exercise_filter.lower() in entry['exercise'].lower() if exercise_filter else True)
        ]

        # Вычисляем статистику
        total_weight = 0
        total_repetitions = 0
        exercises_stats = {}

        for entry in filtered_records:
            weight = float(entry['weight'])
            repetitions = int(entry['repetitions'])
            total_weight += weight * repetitions
            total_repetitions += repetitions

            exercise = entry['exercise']
            if exercise not in exercises_stats:
                exercises_stats[exercise] = {'weight': 0, 'repetitions': 0}
            exercises_stats[exercise]['weight'] += weight * repetitions
            exercises_stats[exercise]['repetitions'] += repetitions

        # Создаем окно для отображения статистики
        stats_window = Toplevel(self.root)
        stats_window.title("Статистика тренировок")
        stats_window.geometry("400x300")

        # Общая статистика
        ttk.Label(stats_window, text=f"Суммарный вес: {total_weight:.2f} кг").pack(pady=5)
        ttk.Label(stats_window, text=f"Суммарное количество повторений: {total_repetitions}").pack(pady=5)

        # Статистика по упражнениям
        ttk.Label(stats_window, text="Упражнения:").pack(pady=5)
        for exercise, stats in exercises_stats.items():
            ttk.Label(
                stats_window,
                text=f"{exercise}: {stats['weight']:.2f} кг, {stats['repetitions']} повторений").pack(pady=2)

    def show_charts(self):
        """
        Метод для визуализации прогресса по упражнениям.
        """
        # Получаем диапазон дат
        start_date = self.start_date_entry.get_date()
        end_date = self.end_date_entry.get_date()
        exercise_filter = self.exercise_filter_entry.get().strip()

        start_datetime = datetime.combine(start_date, time.min)
        end_datetime = datetime.combine(end_date, time.max)

        if start_datetime > end_datetime:
            messagebox.showerror("Ошибка!", "Дата начала не может быть позже даты окончания.")
            return

        # Фильтрация данных
        data = load_data()
        filtered_records = [
            entry for entry in data
            if start_datetime <= datetime.strptime(entry['datetime'], '%d/%m/%Y %H:%M') <= end_datetime
               and (exercise_filter.lower() in entry['exercise'].lower() if exercise_filter else True)
        ]

        if not filtered_records:
            messagebox.showinfo("Нет данных", "Нет данных для отображения графиков.")
            return

        # Данные для графиков
        dates = [datetime.strptime(entry['datetime'], '%d/%m/%Y %H:%M') for entry in filtered_records]
        weights = [float(entry['weight']) for entry in filtered_records]
        repetitions = [int(entry['repetitions']) for entry in filtered_records]

        # Уникальный идентификатор для файлов с графиками
        file_id = self.chart_counter  # Используем счетчик
        self.chart_counter += 1  # Увеличиваем счетчик для следующего графика

        # График веса
        fig1 = Figure(figsize=(8, 6), dpi=100)
        weight_ax = fig1.add_subplot(111)
        weight_ax.plot(dates, weights, marker='o', label='Вес (кг)', color='blue')
        weight_ax.set_title("Изменение веса")
        weight_ax.set_ylabel("Вес (кг)")
        weight_ax.grid()
        weight_path = os.path.join('images', f'weight_chart_{file_id}.png')
        fig1.savefig(weight_path)

        # Открытие окна для графика веса
        weight_window = Toplevel(self.root)
        weight_window.title("График веса")
        weight_window.geometry("800x600")
        canvas1 = FigureCanvasTkAgg(fig1, master=weight_window)
        canvas1.draw()
        canvas1.get_tk_widget().pack(expand=True, fill=tk.BOTH)

        # График повторений
        fig2 = Figure(figsize=(8, 6), dpi=100)
        repetition_ax = fig2.add_subplot(111)
        repetition_ax.plot(dates, repetitions, marker='o', label='Повторения', color='green')
        repetition_ax.set_title("Изменение повторений")
        repetition_ax.set_ylabel("Повторения")
        repetition_ax.grid()
        repetition_path = os.path.join('images', f'repetitions_chart_{file_id}.png')
        fig2.savefig(repetition_path)

        # Открытие окна для графика повторений
        repetition_window = Toplevel(self.root)
        repetition_window.title("График повторений")
        repetition_window.geometry("800x600")
        canvas2 = FigureCanvasTkAgg(fig2, master=repetition_window)
        canvas2.draw()
        canvas2.get_tk_widget().pack(expand=True, fill=tk.BOTH)

        # Уведомление о сохранении
        messagebox.showinfo("Графики сохранены", f"Графики сохранены:\n{weight_path}\n{repetition_path}")

def main():
    root = tk.Tk()
    app = TrainingLogApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()

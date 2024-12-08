"""
Проект "Журнал тренировок". Реализованы ввод информации о тренировках и запись этой информации в файл формата JSON.
В проекте используется библиотека tkinter для графического интерфейса

Функции загрузки и сохранения данных:
- load_data: пытается открыть файл с именем, указанным в переменной data_file, и загрузить из него данные в формате JSON. Если файл не существует или происходит ошибка при разборе данных, возвращается пустой список;
- save_data: принимает данные о тренировках в виде списка словарей и сохраняет их в файл в формате JSON. Данные форматируются с отступом для лучшей читаемости

Класс TrainingLogApp:
- Конструктор класса __init__: принимает объект root, который является главным окном приложения, и вызывает метод create_widgets для создания виджетов интерфейса.
- Метод create_widgets: создает виджеты для ввода данных о тренировке (название упражнения, вес, количество повторений), кнопки для добавления записи о тренировке и просмотра сохраненных записей.
- Метод add_entry: считывает данные из полей ввода, проверяет их наличие, создает словарь с информацией о тренировке, добавляет его в список с данными и сохраняет изменения в файл. После добавления записи поля ввода очищаются, и пользователю показывается сообщение об успехе.
- Метод view_records: загружает сохраненные данные и отображает их в новом окне с помощью виджета Treeview. Для каждой записи создается строка в таблице.

Функция main:
- Создает экземпляр Tk, который является главным окном приложения.
- Создает экземпляр приложения TrainingLogApp, передавая ему главное окно.
- Запускает главный цикл обработки событий Tkinter, чтобы окно приложения отображалось и реагировало на действия пользователя.

Описание импортов:
- import tkinter as tk: импорт основной библиотеки для создания графического пользовательского интерфейса
- from tkinter import ttk, Toplevel, messagebox:
1. модуль ttk предоставляет расширенные виджеты для Tkinter, такие, как стилизованные кнопки, метки и комбобоксы.
2. класс Toplevel используется для создания новых окон, независимых от основного окна приложения.
3. модуль messagebox позволяет отображать всплывающие окна с сообщениями, такими как предупреждения или ошибки;
- import json: модуль json позволяет преобразовывать в строку (и преобразовывать из строки) данные в формате JSON
- from datetime import datetime: класс datetime из модуля datetime предоставляет методы для работы с датами и временем.
Это позволяет выполнять операции, такие как получение текущей даты и времени, форматирование и арифметику дат.
"""
import os
import tkinter as tk
from os import write
from tkinter import ttk, Toplevel, messagebox, filedialog
from PIL import Image, ImageTk
import json
import csv
from datetime import datetime, time
from tkcalendar import DateEntry
from PIL.ImageOps import expand

# Файлы с иконками
add_icon_path = 'images/add.png'
view_icon_path = 'images/eye.png'
export_icon_path = 'images/export.png'
import_icon_path = 'images/import.png'

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
    Загрузка данных о тренировках из файла. Применены обработки исключений для обработки возможных ошибок.
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
    Сохранение данных о тренировках в файл
    """
    messagebox.showinfo("Сохранение файла", "Выберите, куда сохранить ваш журнал тренировок или нажмите отмену для сохранения в файл по умолчанию")
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
        root.title("Дневник тренировок")
        self.exercises = []  # Список для хранения уникальных упражнений
        self.create_widgets()
        self.update_exercise_filter()  # Обновляем список упражнений

    def create_widgets(self):
        """
        Этот метод создает виджеты для ввода данных, кнопки для добавления записи о тренировке, просмотра и фильтрации
        сохраненных записей. Также реализованы кнопки экспорта записей в файлы CSV формата и импорта записей из них.
        """

        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)

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

        self.add_icon = resize_image(add_icon_path, 20, 20)
        self.add_button = ttk.Button(
            self.main_frame,
            text="Добавить запись",
            image=self.add_icon,
            compound="left",
            command=self.add_entry
        )
        self.add_button.grid(column=0, row=4, columnspan=2, pady=5)

        self.view_icon = resize_image(view_icon_path, 20, 20)
        self.view_button = ttk.Button(
            self.main_frame,
            text="Просмотреть записи",
            image=self.view_icon,
            compound="left",
            command=self.view_records
        )
        self.view_button.grid(column=0, row=5, columnspan=2, pady=5)

        # Поля для выбора даты
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
        self.filter_button = ttk.Button(self.main_frame, text="Отфильтровать записи", command=self.filter_records)
        self.filter_button.grid(column=0, row=9, columnspan=2, pady=5)

        # Кнопка экспорта в файл формата CSV
        self.export_icon = resize_image(export_icon_path, 20, 20)
        self.export_button = ttk.Button(
            self.main_frame,
            text="Экспорт в CSV",
            image=self.export_icon,
            compound="left",
            command=self.export_to_csv
        )
        self.export_button.grid(column=0, row=10, columnspan=2, pady=5)

        # Кнопка импорта из файла формата CSV
        self.import_icon = resize_image(import_icon_path, 20, 20)
        self.import_button = ttk.Button(
            self.main_frame,
            text="Импорт из CSV",
            image=self.import_icon,
            compound="left",
            command=self.import_from_csv
        )
        self.import_button.grid(column=0, row=11, columnspan=2, pady=5)


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
        records_window = Toplevel(self.root)
        records_window.title("Записи тренировок")

        tree = ttk.Treeview(records_window, columns=("Дата", "Упражнение", "Вес", "Повторения"), show="headings")
        tree.heading('Дата', text="Дата")
        tree.heading('Упражнение', text="Упражнение")
        tree.heading('Вес', text="Вес")
        tree.heading('Повторения', text="Повторения")

        for entry in records:
            tree.insert('', tk.END, values=(
            entry.get('datetime', 'Неизвестно'),
            entry.get('exercise', ''),
            entry.get('weight', ''),
            entry.get('repetitions', '')))
        tree.pack(expand=True, fill=tk.BOTH)

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


def main():
    root = tk.Tk()
    app = TrainingLogApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()

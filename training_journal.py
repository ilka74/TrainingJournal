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
1. модуль ttk предоставляет расширенные виджеты для Tkinter, такие как стилизованные кнопки, метки и комбобоксы.
2. класс Toplevel используется для создания новых окон, независимых от основного окна приложения.
3. модуль messagebox позволяет отображать всплывающие окна с сообщениями, такими как предупреждения или ошибки;
- import json: модуль json позволяет преобразовывать в строку (и преобразовывать из строки) данные в формате JSON
- from datetime import datetime: класс datetime из модуля datetime предоставляет методы для работы с датами и временем.
Это позволяет выполнять операции, такие как получение текущей даты и времени, форматирование и арифметику дат.
"""
import tkinter as tk
from tkinter import ttk, Toplevel, messagebox
import json
from datetime import datetime

# Файл для сохранения данных
data_file = 'training_log.json'

def load_data():
    """Загрузка данных о тренировках из файла."""
    try:
        with open(data_file, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_data(data):
    """Сохранение данных о тренировках в файл."""
    with open(data_file, 'w') as file:
        json.dump(data, file, indent=4)

class TrainingLogApp:
    def __init__(self, root):
        self.root = root
        root.title("Дневник тренировок")
        self.create_widgets()

    def create_widgets(self):
        # Создает виджеты для ввода данных, кнопки для добавления записи о тренировке и просмотра сохраненных записей
        self.exercise_label = ttk.Label(self.root, text="Упражнение:")
        self.exercise_label.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)

        self.exercise_entry = ttk.Entry(self.root)
        self.exercise_entry.grid(column=1, row=0, sticky=tk.EW, padx=5, pady=5)

        self.weight_label = ttk.Label(self.root, text="Вес:")
        self.weight_label.grid(column=0, row=1, sticky=tk.W, padx=5, pady=5)

        self.weight_entry = ttk.Entry(self.root)
        self.weight_entry.grid(column=1, row=1, sticky=tk.EW, padx=5, pady=5)

        self.repetitions_label = ttk.Label(self.root, text="Повторения:")
        self.repetitions_label.grid(column=0, row=2, sticky=tk.W, padx=5, pady=5)

        self.repetitions_entry = ttk.Entry(self.root)
        self.repetitions_entry.grid(column=1, row=2, sticky=tk.EW, padx=5, pady=5)

        self.add_button = ttk.Button(self.root, text="Добавить запись", command=self.add_entry)
        self.add_button.grid(column=0, row=3, columnspan=2, pady=10)

        self.view_button = ttk.Button(self.root, text="Просмотреть записи", command=self.view_records)
        self.view_button.grid(column=0, row=4, columnspan=2, pady=10)

    def add_entry(self):
        """
        Этот метод считывает данные из полей ввода, проверяет их наличие, создает словарь с информацией о тренировке,
        добавляет его в список с данными и сохраняет изменения в файл.
        """
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        exercise = self.exercise_entry.get()
        weight = self.weight_entry.get()
        repetitions = self.repetitions_entry.get()

        if not (exercise and weight and repetitions):
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены!")
            return

        entry = {
            'date': date,
            'exercise': exercise,
            'weight': weight,
            'repetitions': repetitions
        }

        data = load_data()
        data.append(entry)
        save_data(data)

        # Очистка полей ввода после добавления
        self.exercise_entry.delete(0, tk.END)
        self.weight_entry.delete(0, tk.END)
        self.repetitions_entry.delete(0, tk.END)
        messagebox.showinfo("Успешно", "Запись успешно добавлена!")

    def view_records(self):
        """
        Загружает сохраненные данные и отображает их в новом окне с помощью виджета Treeview.
        Для каждой записи создается строка в таблице.
        """
        data = load_data()
        records_window = Toplevel(self.root)
        records_window.title("Записи тренировок")

        tree = ttk.Treeview(records_window, columns=("Дата", "Упражнение", "Вес", "Повторения"), show="headings")
        tree.heading('Дата', text="Дата")
        tree.heading('Упражнение', text="Упражнение")
        tree.heading('Вес', text="Вес")
        tree.heading('Повторения', text="Повторения")

        for entry in data:
            tree.insert('', tk.END, values=(entry['date'], entry['exercise'], entry['weight'], entry['repetitions']))

        tree.pack(expand=True, fill=tk.BOTH)

def main():
    root = tk.Tk()
    app = TrainingLogApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()

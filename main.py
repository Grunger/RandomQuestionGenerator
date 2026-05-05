import json
import os
import tkinter as tk
from datetime import datetime

# Глобальные переменные
data_file = "quotes.json"
records = []
current_filter_author = ""
current_filter_theme = None

def load_data():
    """Загрузка данных из JSON файла"""
    global records
    try:
        if os.path.exists(data_file):
            with open(data_file, 'r', encoding='utf-8') as f:
                records = json.load(f)
        else:
            records = []
    except Exception as e:
        print(f"Ошибка загрузки: {e}")
        records = []

def save_data():
    """Сохранение данных в JSON файл"""
    try:
        with open(data_file, 'w', encoding='utf-8') as f:
            json.dump(records, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Ошибка сохранения: {e}")

def validate_date(date_str):
    """Проверка корректности даты в формате ГГГГ-ММ-ДД"""
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def clear_table(table_frame):
    """Очистка таблицы"""
    for widget in table_frame.winfo_children():
        widget.destroy()

def display_records(table_frame, record_list):
    """Отображение записей в таблице"""
    clear_table(table_frame)
    
    # Заголовки
    headers = ["Автор", "Тема", "Текст"]
    for col, header in enumerate(headers):
        label = tk.Label(table_frame, text=header, font=("Arial", 10, "bold"), 
                        borderwidth=1, relief="solid", padx=10, pady=5, bg="lightgray")
        label.grid(row=0, column=col, sticky="nsew")
    
    # Данные
    for row, rec in enumerate(record_list, start=1):
        tk.Label(table_frame, text=rec["author"], borderwidth=1, relief="solid", padx=10, pady=5).grid(row=row, column=0, sticky="nsew")
        tk.Label(table_frame, text=str(rec["theme"]), borderwidth=1, relief="solid", padx=10, pady=5).grid(row=row, column=1, sticky="nsew")
        tk.Label(table_frame, text=rec["text"], borderwidth=1, relief="solid", padx=10, pady=5).grid(row=row, column=2, sticky="nsew")
    
    # Настройка веса столбцов
    for col in range(3):
        table_frame.columnconfigure(col, weight=1)

def refresh_table(table_frame):
    """Обновление таблицы с учетом фильтрации"""
    filtered = filter_records()
    display_records(table_frame, filtered)

def filter_records():
    """Фильтрация записей по автору и теме"""
    global current_filter_author, current_filter_theme
    
    filtered = records.copy()
    
    # Фильтр по автору
    if current_filter_author:
        filtered = [r for r in filtered if r["author"] == current_filter_author]
    
    # Фильтр по температуре (выше заданного порога)
    if current_filter_theme is not None:
        filtered = [r for r in filtered if r["theme"] == current_filter_theme]
    
    return filtered

def add_record(author_entry, theme_entry, desc_entry, table_frame):
    """Добавление новой записи о погоде"""
    author = author_entry.get().strip()
    theme = theme_entry.get().strip()
    text = desc_entry.get().strip()
    # Проверка полей
    if not author:
        status_label.config(text="Ошибка: поле Автор не может быть пустым", fg="red")
        return
    if not theme:
        status_label.config(text="Ошибка: поле Тема не может быть пустым", fg="red")
        return
    if not text:
        status_label.config(text="Ошибка: поле Текст не может быть пустым", fg="red")
        return
    
    # Добавление записи
    record = {
        "author": author,
        "theme": theme,
        "text": text,
    }
    records.append(record)
    save_data()
    
    # Очистка полей
    author_entry.delete(0, tk.END)
    theme_entry.delete(0, tk.END)
    desc_entry.delete(0, tk.END)
    
    status_label.config(text=f"Запись за добавлена!", fg="green")
    refresh_table(table_frame)

def filter_by_author(filter_author_entry, table_frame):
    """Фильтрация по автору"""
    global current_filter_author
    date_str = filter_author_entry.get().strip()
    if not date_str:
        status_label.config(text="Ошибка: Неверный формат для фильтра!", fg="red")
        return
    current_filter_author = date_str
    refresh_table(table_frame)
    
    if current_filter_author:
        status_label.config(text=f"Фильтр по автору: {current_filter_author}", fg="blue")
    else:
        status_label.config(text="Фильтр по автору сброшен", fg="blue")

def filter_by_theme(filter_theme_entry, table_frame):
    """Фильтрация по теме"""
    global current_filter_theme
    temp_str = filter_theme_entry.get().strip()
    if not temp_str:
        status_label.config(text="Ошибка: Поле пустое!", fg="red")
        return
        
    else:
        current_filter_theme = temp_str
    
    refresh_table(table_frame)
    
    if current_filter_theme is not None:
        status_label.config(text=f"Фильтр: тема {current_filter_theme}", fg="blue")
    else:
        status_label.config(text="Фильтр по теме сброшен", fg="blue")

def reset_filters(filter_author_entry, filter_theme_entry, table_frame):
    """Сброс всех фильтров"""
    global current_filter_author, current_filter_theme
    current_filter_author = ""
    current_filter_theme = None
    filter_author_entry.delete(0, tk.END)
    filter_theme_entry.delete(0, tk.END)
    refresh_table(table_frame)
    status_label.config(text="Фильтры сброшены", fg="blue")

def delete_record(table_frame):
    """Удаление выбранной записи"""
    selection_window = tk.Toplevel()
    selection_window.title("Удаление записи")
    selection_window.geometry("500x350")
    
    tk.Label(selection_window, text="Выберите запись для удаления:", font=("Arial", 10, "bold")).pack(pady=10)
    
    listbox = tk.Listbox(selection_window, width=60)
    listbox.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
    
    # Заполнение списка
    for i, rec in enumerate(records):
        listbox.insert(tk.END, f"{i+1}. {rec['author']} | {rec['theme']} | {rec['text']}")
    
    def delete_selected():
        selected = listbox.curselection()
        if selected:
            index = selected[0]
            deleted_rec = records.pop(index)
            save_data()
            refresh_table(table_frame)
            selection_window.destroy()
            status_label.config(text=f"Запись удалена!", fg="red")
        else:
            status_label.config(text="Ошибка: Выберите запись для удаления!", fg="red")
    
    tk.Button(selection_window, text="Удалить", command=delete_selected, bg="red", fg="white").pack(pady=10)

def main():
    global status_label
    
    root = tk.Tk()
    root.title("Random Quote Generator (Генератор случайных цитат)")
    root.geometry("900x600")
    root.configure(bg="#f0f0f0")
    
    # Загрузка данных
    load_data()
    
    # Фрейм для ввода данных
    input_frame = tk.Frame(root, bg="#f0f0f0", bd=2, relief="groove")
    input_frame.pack(fill="x", padx=10, pady=10)
    
    tk.Label(input_frame, text="ДОБАВЛЕНИЕ ЗАПИСИ", font=("Arial", 12, "bold"), bg="#f0f0f0").grid(row=0, column=0, columnspan=4, pady=5)
    
    tk.Label(input_frame, text="Автор:", bg="#f0f0f0").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    author_entry = tk.Entry(input_frame, width=15)
    author_entry.grid(row=1, column=1, padx=5, pady=5)
    
    tk.Label(input_frame, text="Тема:", bg="#f0f0f0").grid(row=1, column=2, padx=5, pady=5, sticky="e")
    theme_entry = tk.Entry(input_frame, width=10)
    theme_entry.grid(row=1, column=3, padx=5, pady=5)
    
    tk.Label(input_frame, text="Текст:", bg="#f0f0f0").grid(row=2, column=0, padx=5, pady=5, sticky="e")
    desc_entry = tk.Entry(input_frame, width=40)
    desc_entry.grid(row=2, column=1, columnspan=2, padx=5, pady=5, sticky="w")
    
    # Кнопки добавления и удаления
    button_frame = tk.Frame(root, bg="#f0f0f0")
    button_frame.pack(fill="x", padx=10, pady=5)
    
    add_button = tk.Button(button_frame, text="ДОБАВИТЬ ЗАПИСЬ", bg="green", fg="white", font=("Arial", 10, "bold"),
                          command=lambda: add_record(author_entry, theme_entry, desc_entry, button_frame))
    add_button.pack(side="left", padx=5)
    
    delete_button = tk.Button(button_frame, text="УДАЛИТЬ ЗАПИСЬ", bg="red", fg="white", font=("Arial", 10, "bold"),
                            command=lambda: delete_record(button_frame))
    delete_button.pack(side="left", padx=5)
    
    # Фрейм для фильтрации
    filter_frame = tk.Frame(root, bg="#f0f0f0", bd=2, relief="groove")
    filter_frame.pack(fill="x", padx=10, pady=10)
    
    tk.Label(filter_frame, text="ФИЛЬТРАЦИЯ", font=("Arial", 10, "bold"), bg="#f0f0f0").grid(row=0, column=0, columnspan=4, pady=5)
    
    tk.Label(filter_frame, text="По автору:", bg="#f0f0f0").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    filter_author_entry = tk.Entry(filter_frame, width=15)
    filter_author_entry.grid(row=1, column=1, padx=5, pady=5)
    tk.Button(filter_frame, text="Применить", command=lambda: filter_by_author(filter_author_entry, table_frame)).grid(row=1, column=2, padx=5)
    
    tk.Label(filter_frame, text="По теме:", bg="#f0f0f0").grid(row=2, column=0, padx=5, pady=5, sticky="e")
    filter_theme_entry = tk.Entry(filter_frame, width=10)
    filter_theme_entry.grid(row=2, column=1, padx=5, pady=5)
    tk.Button(filter_frame, text="Применить", command=lambda: filter_by_theme(filter_theme_entry, table_frame)).grid(row=2, column=2, padx=5)
    
    tk.Button(filter_frame, text="СБРОСИТЬ ФИЛЬТРЫ", bg="orange", 
              command=lambda: reset_filters(filter_author_entry, filter_theme_entry, table_frame)).grid(row=1, column=3, rowspan=2, padx=20)
    
    # Статус бар
    status_label = tk.Label(root, text="Готов к работе", relief="sunken", anchor="w", bg="#ffffcc")
    status_label.pack(fill="x", side="bottom", padx=10, pady=5)
    
    # Фрейм для таблицы
    table_frame = tk.Frame(root, bg="white")
    table_frame.pack(fill="both", expand=True, padx=10, pady=10)
    
    # Отображение записей
    display_records(table_frame, records)
    
    root.mainloop()

if __name__ == "__main__":
    main()

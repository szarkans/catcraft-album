import os
import subprocess

# Укажи здесь путь к папке, где лежат изображения
INPUT_FOLDER = "7season"

# Путь к утилитам (если нужно, настрой вручную)
OXIPNG_CMD = "oxipng"    # Обычно просто oxipng, если установлен через pip install oxipng
JPEGTRAN_CMD = "jpegtran" # Нужно установить jpegtran (обычно часть пакета libjpeg или mozjpeg)

# Проход по всем файлам в папке
for root, dirs, files in os.walk(INPUT_FOLDER):
    for file in files:
        file_path = os.path.join(root, file)
        
        # Оптимизация PNG
        if file.lower().endswith(".png"):
            print(f"Оптимизация PNG: {file_path}")
            subprocess.run([OXIPNG_CMD, "--opt", "max", "--strip", "all", "--out", file_path, file_path])

        # Оптимизация JPEG
        elif file.lower().endswith((".jpg", ".jpeg")):
            print(f"Оптимизация JPEG: {file_path}")
            output_path = file_path + ".opt"
            subprocess.run([
                JPEGTRAN_CMD, 
                "-copy", "none",    # Удалить метаданные EXIF
                "-optimize",        # Оптимизировать скан
                "-progressive",     # Сделать JPEG прогрессивным
                "-outfile", output_path, 
                file_path
            ])
            os.replace(output_path, file_path)  # Перезаписываем оригинальный файл

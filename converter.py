import os
from PIL import Image


def optimize_and_replace_to_webp(source_dir, quality=80):
    if not os.path.exists(source_dir):
        print(f"Папка {source_dir} не найдена. Проверь правильность пути.")
        return

    total_saved_bytes = 0

    for root, dirs, files in os.walk(source_dir):
        for file in files:
            if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                file_path = os.path.join(root, file)
                base_name = os.path.splitext(file)[0]
                new_file_path = os.path.join(root, f"{base_name}.webp")

                try:
                    # Запоминаем размер до конвертации
                    old_size = os.path.getsize(file_path)

                    with Image.open(file_path) as img:
                        if img.mode in ("RGBA", "P"):
                            img = img.convert("RGBA")
                        else:
                            img = img.convert("RGB")

                        img.save(new_file_path, 'webp', optimize=True, quality=quality)

                    # Получаем размер после конвертации
                    new_size = os.path.getsize(new_file_path)

                    # Вычисляем процент сжатия
                    if old_size > 0:
                        saved_percent = ((old_size - new_size) / old_size) * 100
                    else:
                        saved_percent = 0

                    total_saved_bytes += (old_size - new_size)

                    # Удаляем оригинал
                    os.remove(file_path)

                    # Вывод результата в запрошенном формате
                    print(f"{file} -> {base_name}.webp ({saved_percent:.1f}% сжато)")

                except Exception as e:
                    print(f"Ошибка при обработке {file_path}: {e}")

    # Переводим байты в мегабайты для итоговой статистики
    total_saved_mb = total_saved_bytes / (1024 * 1024)
    print(f"\nГотово! Всего сэкономлено места: {total_saved_mb:.2f} МБ")


if __name__ == "__main__":
    target_directory = "."
    optimize_and_replace_to_webp(target_directory, quality=80)
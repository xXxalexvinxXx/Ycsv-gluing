import argparse
import csv
import glob
import os


def merge_csv_files(input_dir, output_file, check_headers=False):
    # Получаем список CSV-файлов в директории
    csv_files = glob.glob(os.path.join(input_dir, '*.csv'))
    if not csv_files:
        print("Ошибка: в указанной директории нет CSV-файлов.")
        return

    # Сортируем файлы по имени
    csv_files.sort()

    # Проверяем заголовки (если требуется)
    if check_headers:
        try:
            with open(csv_files[0], 'r', newline='', encoding='utf-8') as f:
                reader = csv.reader(f)
                first_headers = next(reader)

            for file in csv_files[1:]:
                with open(file, 'r', newline='', encoding='utf-8') as f:
                    reader = csv.reader(f)
                    headers = next(reader)
                    if headers != first_headers:
                        print(f"Ошибка: заголовки в файле {file} не совпадают с первым файлом.")
                        return
        except StopIteration:
            print("Ошибка: один из файлов пустой или имеет неправильный формат.")
            return

    # Объединяем файлы
    try:
        with open(output_file, 'w', newline='', encoding='utf-8') as outfile:
            writer = csv.writer(outfile)

            # Обрабатываем первый файл
            with open(csv_files[0], 'r', newline='', encoding='utf-8') as infile:
                reader = csv.reader(infile)
                headers = next(reader)
                writer.writerow(headers)
                for row in reader:
                    writer.writerow(row)

            # Обрабатываем остальные файлы
            for file in csv_files[1:]:
                with open(file, 'r', newline='', encoding='utf-8') as infile:
                    reader = csv.reader(infile)
                    next(reader)  # Пропускаем заголовок
                    for row in reader:
                        writer.writerow(row)
        print(f"Файлы успешно объединены в {output_file}")

    except Exception as e:
        print(f"Ошибка при объединении файлов: {str(e)}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Объединение CSV-файлов из указанной директории')
    parser.add_argument('-i', '--input_dir', default='.',
                        help='Путь к директории с CSV-файлами (по умолчанию текущая)')
    parser.add_argument('-o', '--output', default='combined.csv',
                        help='Имя выходного файла (по умолчанию combined.csv)')
    parser.add_argument('--check_headers', action='store_true',
                        help='Проверять совпадение заголовков во всех файлах')

    args = parser.parse_args()

    merge_csv_files(args.input_dir, args.output, args.check_headers)
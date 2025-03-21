import argparse
import csv
import glob
import os


def merge_csv_files(input_dir, output_file, check_headers=False):
    csv_files = glob.glob(os.path.join(input_dir, '*.csv'))
    if not csv_files:
        print("Ошибка: в указанной директории нет CSV-файлов.")
        return

    csv_files.sort()
    delimiter = ';'  # Фиксированный разделитель

    if check_headers:
        try:
            with open(csv_files[0], 'r', newline='', encoding='utf-8') as f:
                reader = csv.reader(f, delimiter=delimiter)
                first_headers = next(reader)

            for file in csv_files[1:]:
                with open(file, 'r', newline='', encoding='utf-8') as f:
                    reader = csv.reader(f, delimiter=delimiter)
                    headers = next(reader)
                    if headers != first_headers:
                        print(f"Ошибка: заголовки в файле {file} не совпадают с первым файлом.")
                        return
        except StopIteration:
            print("Ошибка: один из файлов пустой или имеет неправильный формат.")
            return

    try:
        with open(output_file, 'w', newline='', encoding='utf-8') as outfile:
            writer = csv.writer(outfile, delimiter=delimiter)

            # Обрабатываем первый файл
            with open(csv_files[0], 'r', newline='', encoding='utf-8') as infile:
                reader = csv.reader(infile, delimiter=delimiter)
                headers = next(reader)

                # Добавляем новую колонку в заголовки
                new_headers = [headers[0], "Link"] + headers[1:]
                writer.writerow(new_headers)

                # Обрабатываем строки данных
                for row in reader:
                    if row:
                        new_row = [row[0], f"link/{row[0]}"] + row[1:]
                        writer.writerow(new_row)

            # Обрабатываем остальные файлы
            for file in csv_files[1:]:
                with open(file, 'r', newline='', encoding='utf-8') as infile:
                    reader = csv.reader(infile, delimiter=delimiter)
                    next(reader)  # Пропускаем заголовок

                    for row in reader:
                        if row:
                            new_row = [row[0], f"link/{row[0]}"] + row[1:]
                            writer.writerow(new_row)

            print(f"Файлы успешно объединены в {output_file}")

    except Exception as e:
        print(f"Ошибка при объединении файлов: {str(e)}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Объединение CSV-файлов с разделителем ";" и добавлением колонки ссылок')
    parser.add_argument('-i', '--input_dir', default='.',
                        help='Путь к директории с CSV-файлами')
    parser.add_argument('-o', '--output', default='combined.csv',
                        help='Имя выходного файла')
    parser.add_argument('--check_headers', action='store_true',
                        help='Проверять совпадение заголовков')

    args = parser.parse_args()
    merge_csv_files(args.input_dir, args.output, args.check_headers)
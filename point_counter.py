import codecs

grades = {
    (0, 449): 'F',
    (450, 474): 'E',
    (475, 499): 'D',
    (500, 549): 'C',
    (550, 599): 'B',
    (600, 2000): 'A'
}

BONUS_POINTS = 50


def calculate_grade(pts):
    for (l, r), grade in grades.items():
        if l <= pts <= r:
            return grade

    return 'F'


if __name__ == '__main__':
    f = codecs.open('solved.md', 'r', "utf_8_sig")

    points_sum = 0
    problems_cnt = 0

    for line in f:
        if line.count('|') != 4:
            break

        _, name, solved, points, *_ = line.split('|')

        name = name.strip()

        if name == 'vm':
            points_sum += float(solved)
            problems_cnt += 1
            continue

        if solved.strip() not in ['', 'x']:
            continue

        solved = True if solved.strip() == 'x' else False
        points = float(points.strip())

        if solved:
            points_sum += points
            problems_cnt += 1

    f.close()

    print(f'Всего задач: {problems_cnt}')
    print(f'Всего баллов за задачи: {points_sum}')
    print(f'Бонусные баллы: {BONUS_POINTS}')
    print(f'Итого баллов: {points_sum + BONUS_POINTS}')
    print(f'Оценка: {calculate_grade(points_sum + BONUS_POINTS)}')

    f = codecs.open('solved.md', 'r', "utf_8_sig")
    text_before_output = f.read()

    output_pos = text_before_output.find('<!--- Script Output Start --->')

    if output_pos != -1:
        text_before_output = text_before_output[:output_pos]

    f.close()

    f = codecs.open('solved.md', 'w', "utf_8_sig")

    f.write(text_before_output)
    f.write('<!--- Script Output Start --->\n')
    f.write(f'```\nРешено задач: {problems_cnt}\n')
    f.write(f'Баллов за задачи: {points_sum}\n')
    f.write(f'Бонусные баллы: {BONUS_POINTS}\n')
    f.write(f'Итого баллов: {points_sum + BONUS_POINTS}\n')
    f.write(f'Оценка: {calculate_grade(points_sum)}\n```\n')

    f.close()

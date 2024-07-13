from flask import Flask, render_template, request

app = Flask(__name__)

win_point = []
result = []

def print_infor():
    info = "="*30 + "\n"
    info += " " * 10

    for i in range(1, 11):
        info += str(i) + "  "
    info += "\n"

    info += "승리 점수:"
    for point in win_point:
        info += str(point) + ' '
    info += "\n"

    info += "패배 점수:"
    for point in win_point:
        info += str(100 - point) + ' '
    info += "\n"

    info += "승리 패배:"
    for point in result:
        info += str(point) + '  '
    info += "\n"

    info += "="*30
    return info

@app.route('/', methods=['GET', 'POST'])
def index():
    global win_point, result

    if request.method == 'POST':
        try:
            x_n = int(request.form['win_point'])
            y_n = int(request.form['result'])
            win_point.append(x_n)
            result.append(y_n)
        except ValueError:
            pass

        if 'progress' in request.form and request.form['progress'] == '0':
            First = False

    info = print_infor()
    return render_template('index.html', info=info)

@app.route('/result')
def show_result():
    x = len(result)
    win_num = 0

    for point in result:
        if point == 1:
            win_num += 1

    if x == 0:
        C = 0
    else:
        C = 0.6 * win_num + 0.4 * (x - win_num)
    
    if C == 0:
        c1, c2 = 0, 0
    else:
        c1 = 0.6 / C
        c2 = 0.4 / C

    total = 0
    for point1, point2 in zip(win_point, result):
        if point2 == 1:
            total += point1 * c1
        else:
            total += point1 * c2

    return f"총 점수: {total}"

if __name__ == '__main__':
    app.run(debug=True)
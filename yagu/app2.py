from flask import Flask, render_template, request, jsonify, redirect, url_for

app = Flask(__name__)

win_num = 0
win_point = []
result = []
i = 1

def calculate_c(win_num, total_games):
    if total_games == 0:
        return 0, 0
    
    C = 0.6 * win_num + 0.4 * (total_games - win_num)
    c1 = 0.6 / C
    c2 = 0.4 / C
    return c1, c2

@app.route('/', methods=['GET', 'POST'])
def index():
    global i, win_num, win_point, result
    
    if request.method == 'POST':
        x_n = int(request.form['win_point'])
        y_n = int(request.form['result'])
        
        win_point.append(x_n)
        result.append(y_n)
        
        if y_n == 1:
            win_num += 1
        
        i += 1
        return redirect(url_for('index'))
    
    return render_template('index.html', win_point=win_point, result=result, i=i)

@app.route('/calculate', methods=['POST'])
def calculate():
    global win_num, result, win_point
    sum_value = 0

    c1, c2 = calculate_c(win_num, len(result))

    for idx, y_n in enumerate(result):
        x_n = win_point[idx]
        
        if y_n == 1:
            sum_value += x_n * c1
        else:
            sum_value += (100 - x_n) * c2
    
    return jsonify({'sum': sum_value})

@app.route('/reset', methods=['POST'])
def reset():
    global i, win_num, win_point, result
    i = 1
    win_num = 0
    win_point.clear()
    result.clear()

    return jsonify({'message': '데이터가 초기화되었습니다.'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port= 8080, debug=True)

#python yagu/app2.py
#http://127.0.0.1:8080
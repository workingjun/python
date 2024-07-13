const express = require('express');
const bodyParser = require('body-parser');

const app = express();

let win_num = 0;
let win_point = [];
let result = [];
let i = 1;

function calculateC(win_num, total_games) {
    if (total_games === 0) {
        return [0, 0];
    }
    
    const C = 0.6 * win_num + 0.4 * (total_games - win_num);
    const c1 = 0.6 / C;
    const c2 = 0.4 / C;
    return [c1, c2];
}

app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());

// EJS 뷰 엔진 설정
app.set('view engine', 'ejs'); // EJS를 사용

app.get('/', (req, res) => {
    res.render('index', { win_point, result, i });
});

app.post('/', (req, res) => {
    const { win_point: x_n, result: y_n } = req.body;

    win_point.push(parseInt(x_n));
    result.push(parseInt(y_n));

    if (parseInt(y_n) === 1) {
        win_num += 1;
    }
    
    i += 1;
    res.redirect('/');
});

app.post('/calculate', (req, res) => {
    let sum_value = 0;

    const [c1, c2] = calculateC(win_num, result.length);

    for (let idx = 0; idx < result.length; idx++) {
        const x_n = win_point[idx];
        const y_n = result[idx];

        if (parseInt(y_n) === 1) {
            sum_value += x_n * c1;
        } else {
            sum_value += (100 - x_n) * c2;
        }
    }

    res.json({ sum: sum_value });
});

app.post('/reset', (req, res) => {
    i = 1;
    win_num = 0;
    win_point = [];
    result = [];

    res.json({ message: '데이터가 초기화되었습니다.' });
});

// 공인 IP 주소를 사용하여 서버 바인딩
const ipAddress = '172.29.34.16';
const port = 80;
app.listen(port, ipAddress, () => {
    console.log(`서버가 http://${ipAddress}:${port} 에서 실행 중입니다.`);
});
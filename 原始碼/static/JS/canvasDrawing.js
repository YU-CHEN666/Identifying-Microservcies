//計算出滾軸width，並在root建立變數
document.documentElement.style.setProperty(
    '--scrollbar-width', 
    `${window.innerWidth - document.documentElement.clientWidth}px`
);
    
const canvas = document.getElementById('writeArea');
const ctx = canvas.getContext('2d');
function DrawingConfig() {
// 設定畫筆基本樣式
    ctx.strokeStyle = '#FF0000'; // 筆跡顏色，不可使用黑色，轉換成Base64會出問題
    ctx.lineWidth = 18;           // 筆跡粗細
    ctx.lineCap = 'round';       // 讓筆劃邊緣平滑
    ctx.lineJoin = 'round';
}

function ResizeCanvas() {
    //Canvas內部解析度即時更新
    canvas.width = canvas.clientWidth;
    canvas.height = canvas.clientHeight;
    DrawingConfig();
}

window.addEventListener('resize',ResizeCanvas);
ResizeCanvas();

// 計算Canvas相對座標
let isDrawing = false;
let lastX = 0;
let lastY = 0;
function getCoordinates(e) {
const rect = canvas.getBoundingClientRect();
    return {
        x: e.clientX - rect.left,
        y: e.clientY - rect.top
    }
};

//Canvas作畫
canvas.addEventListener('pointerdown', (e) => {
    isDrawing = true;
    const { x, y } = getCoordinates(e);
    lastX = x;
    lastY = y;
});

canvas.addEventListener('pointermove', (e) => {
    if (!isDrawing) return;
    const { x, y } = getCoordinates(e);
    ctx.beginPath();
    ctx.moveTo(lastX, lastY);
    ctx.lineTo(x, y);
    ctx.stroke();
    lastX = x;
    lastY = y;
})

function StopDrawing(e) {
    if (isDrawing) {
        isDrawing = false;
    }
};

canvas.addEventListener('pointerup', StopDrawing);
canvas.addEventListener('pointerleave', StopDrawing);

//清除Canvas畫布
const clnButton = document.getElementById('cleanButton');
clnButton.addEventListener('click', function (e) {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
});

export function GetBase64() {
    return canvas.toDataURL('image/png');
}

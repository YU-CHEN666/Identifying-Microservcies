/*訊息頁面邏輯*/
const messagePagebackground = document.getElementById('messagePagebackground');
const circleRotation = document.getElementById('circleRotation');
const messagePageImage = document.getElementById('messagePageImage');
const messageShow = document.getElementById('message');
const messagePageButton = document.getElementById('messagePageButton');

messagePageButton.addEventListener('click', function (e) {
         messagePagebackground.style.display = 'none';
});

export function MessagePageShow() {
    circleRotation.style.display = 'block';
    messageShow.textContent = '處理中...';
    messageShow.style.display = 'block';
    messagePageImage.style.display = 'none';
    messagePageButton.style.display = 'none';
    messagePagebackground.style.display = 'block';
}

export function MessageDisplay(imageMode, message) {
    messagePageImage.src = imageMode ? '/static/IconImg/Success.png' : '/static/IconImg/Error.png';
    circleRotation.style.display = 'none';
    messagePageImage.style.display = 'inline-block';
    messageShow.textContent = message;
    messageShow.style.display = 'block';
    messagePageButton.style.display = 'inline-block';
    messagePagebackground.style.display = 'block';
}

function MessageDisplayInformation(message) {
    messagePageImage.src = '/static/IconImg/Information.png';
    circleRotation.style.display = 'none';
    messagePageImage.style.display = 'inline-block';
    messageShow.textContent = message;
    messageShow.style.display = 'block';
    messagePageButton.style.display = 'inline-block';
    messagePagebackground.style.display = 'block';
}
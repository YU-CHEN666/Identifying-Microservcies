import { GetBase64 } from './canvasDrawing.js';
import { MessagePageShow,MessageDisplay } from './MessagePage.js';

const resultSpan = document.getElementById('result');
const sentButton = document.getElementById('sentButton');
sentButton.addEventListener('click',async function(e) {
    try{
        MessagePageShow();
        const token = document.getElementById('token').value;
        const response = await fetch('/idntify',{
            method: 'POST',
            headers: {
                'Content-Type': 'text/plain',
                'Token': token
            },
            body:GetBase64()
        });
        const responseData = await response.json();
        if(!response.ok)
        {
            if(response.status == '400') MessageDisplay(responseData.sucess,responseData.message);  
            else MessageDisplay(false,`發生未預期的錯誤，HTTP狀態碼:${response.status}`);  
            resultSpan.textContent = ''; 
            return;
        }
        MessageDisplay(responseData.sucess,responseData.message);
        resultSpan.textContent = responseData.result;
    }
    catch(error){ 
        resultSpan.textContent = '';
        MessageDisplay(false,'發生未預期的錯誤');
        console.error(`發生錯誤:${error}`);
    }
});
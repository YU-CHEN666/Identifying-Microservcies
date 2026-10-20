#後端邏輯檔案
from fastapi import FastAPI,Request,Body,Header,Cookie,Depends
from fastapi.responses import HTMLResponse,JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import Annotated
from pydantic import BaseModel
import secrets
from Detect import Detect
from pathlib import Path


app = FastAPI(docs_url=None, redoc_url=None,openapi_url=None)
cwdPath = Path(__file__).resolve().parent
app.mount("/static", StaticFiles(directory=cwdPath/"static"), name="static")
templates = Jinja2Templates(directory=cwdPath/"static"/"templates")
detect = Detect()


#網站首頁
@app.get("/",response_class=HTMLResponse)
async def root(request: Request):
    csrfToken = secrets.token_hex(16)  
    response = templates.TemplateResponse(request=request, name="FrontEnd.html",
                                      context={"token":csrfToken})
    response.set_cookie(key="sessionToken",value=csrfToken,httponly=True,secure=True,     
        samesite="lax",)  
    return response


class IdntifyResult(BaseModel):
    #當辨識失敗，sucess = false，reslut = ""，並且在message說明原因
    sucess: bool
    result: str | None = ""
    message: str


class CSRFErrorException(Exception):
    def __init__(self):
        super().__init__()


#CSRFError例外處理器
@app.exception_handler(CSRFErrorException)
async def CSRFErroe_Exception_Handler(request: Request, exc: CSRFErrorException):
    return JSONResponse(
        status_code=400,
        content={"sucess": False,"message":"你目前看到的頁面是假冒的，所以拒絕你的請求，請立即關閉此頁面"},)


#驗證Token函式，作為依賴項
async def verifyToken(Token:Annotated[str,Header()],
                      sessionToken:Annotated[str,Cookie()]=None):
    if Token != sessionToken:
        raise CSRFErrorException()


#辨識API
@app.post("/idntify",response_model=IdntifyResult,dependencies=[Depends(verifyToken)])
async def Idntify(img:Annotated[str,Body()]) -> IdntifyResult:
    detect.StartDetect(img)
    return {"sucess":detect.sucess,"result":detect.result,"message":detect.message}


#錯誤範例網頁
@app.get("/ErrorExample",response_class=HTMLResponse)
async def ErrorExample(request: Request): 
    response = templates.TemplateResponse(request=request, name="ErrorExample.html")
    return response


#前端請求測試，測試後端發送的JSON結構
@app.post("/idntify/{sucess}",response_model=IdntifyResult,dependencies=[Depends(verifyToken)])
async def IdntifyAPITest(sucess:bool,img:Annotated[str,Body()]) -> IdntifyResult:
    if sucess:
        return {"sucess":True,"result":"10","message":"辨識成功"}
    return {"sucess":False,"message":"無法辨識"}
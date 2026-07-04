import json
from fastapi import FastAPI,UploadFile,File
from fastapi.staticfiles import StaticFiles
import uvicorn
from pathlib import Path
from fastapi.responses import FileResponse

path="baza.json"

app=FastAPI()

@app.get('/')
def serve_frontend():
    return FileResponse("index.html")


@app.get('/status')
def status():
    
    return {"status":"Live"}












@app.post('/register')
def register(data:dict):
    login=data.get("login")
    password=data.get("password")
    
    if not login or not password:
        return {"status":"must have login and password"}
    if not Path(path).exists():
        
        with open("baza.json","w",encoding="UTF-8") as f:
            json.dump({"users":[]},f)
            
        
    
    
    with open("baza.json","r",encoding="UTF-8") as f:
        dannie=json.load(f)
        for user in dannie["users"]:
            if login==user["login"]:
                return {"status":"busy"}
    with open("baza.json","w",encoding="UTF-8") as f:

        new_user={"login":login,"password":password}
        dannie["users"].append(new_user)
        json.dump(dannie,f)        
        return {"status":"ok"}       









@app.post('/login')
def login(data:dict):
    login=data.get("login")
    password=data.get("password")
    with open("baza.json","r",encoding="UTF-8") as f:
    
        dannie=json.load(f)

        for user in dannie["users"]:
            if user["login"]==login and user["password"]==password:
                return {"status":"ok"}
            

        return {"status":"wrong password or login"}
    








@app.post('/upload')
async def upload(file:UploadFile=File(...)):
    data= await file.read()
    if not Path("uploads").exists():
        Path("uploads").mkdir()
    with open(f"uploads/{file.filename}","wb") as f:
        f.write(data)
    return {"status":"ok","filename":file.filename}


@app.get('/files')
def get():
    files=[]

    for file in Path("uploads").iterdir():
        size=file.stat().st_size/(1024**2)
        files.append({"name":file.name,"size":round(size,2)})
    return {"files":files}






@app.get('/download/{filename}')
def download(filename:str):
    file_path=Path("uploads")/filename
    if not file_path.exists():
        return {"status":"no file onserver"}
    return FileResponse(
        path=file_path,
        filename=filename,
        media_type="application/octet-stream"
    )


@app.delete('/delete/{filename}')

def delete(filename:str):
    file_path=Path("uploads")/filename
    if not file_path.exists():
        return {"status":"file not found"}
    file_path.unlink()
    return {"status":f"file {filename} was deleted"}














if __name__=='__main__':
    uvicorn.run(app)
    





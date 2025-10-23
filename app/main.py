from fastapi import FastAPI, HTTPException, Request
from app.config import OPENAI_API_KEY
import openai
import uvicorn

openai.api_key = OPENAI_API_KEY
app = FastAPI(title="Chatbot AI API")

@app.get("/")
def root():
    return {"message": "Chatbot API is running!"}

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_message = data.get("message")
    
    if not user_message:
        raise HTTPException(status_code=400, detail="Message field is required.")
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_message}]
        )
        reply = response.choices[0].message["content"]
        return {"reply": reply}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

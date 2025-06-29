from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from main import generate_response
from fastapi.middleware.cors import CORSMiddleware

# Create a FastAPI app
app = FastAPI(
    title="AI Mentor API",
    description="API for AI Mentor",
    version="1.0.0"
)

# CORS Middleware
origins = [
    "*",  # Allow all origins
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health Check Endpoint
@app.get("/health")
def health_check():
    return {"status": "healthy"}

# Define a Pydantic model for the request body
class ChatRequest(BaseModel):
    question: str
    
# Define a Pydantic model for the response body
class ChatResponse(BaseModel):
    response: str

# Define a route for the chat endpoint
@app.post("/chat",response_model=ChatResponse)
def chat(input:ChatRequest):
    response = generate_response(input.question)
    return ChatResponse(response=response)

# Run the app
if __name__ == "__main__":
    uvicorn.run(app,host="0.0.0.0",port=8000)

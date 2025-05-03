from fastapi import FastAPI

app = FastAPI(
    title="Globant Data Migration API",
    description="API for handling employee data migration",
    version="1.0.0"
)

@app.get("/")
async def root():
    return {"message": "Welcome to Globant Data Migration API"}

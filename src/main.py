from fastapi import FastAPI


app = FastAPI(
    title="Simple task manager API",
    version="0.1.0",
    root_path="/api",
)

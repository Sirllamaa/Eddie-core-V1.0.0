import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "api_module.api_app:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
        workers=2  # Or however many you want
    )

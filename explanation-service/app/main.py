from fastapi import FastAPI

app = FastAPI(
    title="JusExplica - Explanation Service",
    description="Serviço responsável pela futura interpretação de movimentações judiciais.",
    version="0.1.0",
)


@app.get("/")
def home():
    return {
        "success": True,
        "message": "Serviço Python do JusExplica está funcionando.",
    }


@app.get("/health")
def health_check():
    return {
        "success": True,
        "service": "explanation-service",
        "status": "online",
    }
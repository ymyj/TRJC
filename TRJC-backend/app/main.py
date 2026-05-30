from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.api import personnel, plots, tasks, survey, samples, datasets, auth, task_plots, analysis
from app.database import engine, Base
from app.middleware.auth import AuthMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="耕地质量监测管理系统后端API"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

app.add_middleware(AuthMiddleware)

# 所有API路由添加/trjcai前缀
app.include_router(auth.router, prefix="/trjcai")
app.include_router(personnel.router, prefix="/trjcai")
app.include_router(plots.router, prefix="/trjcai")
app.include_router(tasks.router, prefix="/trjcai")
app.include_router(task_plots.router, prefix="/trjcai")
app.include_router(survey.router, prefix="/trjcai")
app.include_router(samples.router, prefix="/trjcai")
app.include_router(analysis.router, prefix="/trjcai")
app.include_router(datasets.router, prefix="/trjcai")


@app.get("/")
def read_root():
    return {"message": "TRJC Backend API is running", "version": settings.APP_VERSION}


@app.get("/health")
def health_check():
    return {"status": "healthy"}

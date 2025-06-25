from fastapi import FastAPI
from routers.calc_router import router as calc_router
from routers.case_router import router as case_router
from routers.currency_router import router as currency_router
from routers.user_router import router as user_router


app = FastAPI(
    title="API Gateway",
    description="Centralized API Gateway with docs",
    version="1.0.0"
)

app.include_router(calc_router, prefix="/calc", tags=["Calculator Service"])
app.include_router(case_router, prefix="/case", tags=["Cases Service"])
app.include_router(currency_router, prefix="/currency", tags=["Currency Service"])
app.include_router(user_router, prefix="/user", tags=["Users Service"])

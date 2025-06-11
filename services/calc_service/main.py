from fastapi import FastAPI
from prometheus_client import Counter, Summary
from prometheus_fastapi_instrumentator import Instrumentator

from schemas import CalcRequest, CalcResponse, PriceRow
from price_table_data import household_price_table, other_price_table

app = FastAPI()
Instrumentator().instrument(app).expose(app, endpoint="/metrics")\

# Общее количество расчётов
calc_requests_total = Counter(
    "calc_requests_total", "Количество обращений к калькулятору"
)

# Количество по типу груза
calc_requests_by_type = Counter(
    "calc_requests_by_type", "Обращения к калькулятору по типу груза", ["cargo_type"]
)

# Дополнительно — средняя плотность и цена
calc_density_summary = Summary("calc_density", "Плотность груза")
calc_total_price_summary = Summary("calc_total_price", "Общая стоимость расчёта")

@app.get("/calc/price_table", response_model=dict)
def get_price_table():
    return {
        "household": household_price_table,
        "other": other_price_table,
    }

@app.post("/calculate")
def calculate_price(data: CalcRequest):
    density = data.weight / data.volume if data.volume else 0
    table = household_price_table if data.cargo_type.lower() == "household" else other_price_table

    for row in table:
        if row["min"] <= density <= row["max"]:
            price_per_kgm3 = row["price"]
            break
    else:
        price_per_kgm3 = 0

    total_price = round(price_per_kgm3 * density, 2)

    calc_requests_total.inc()
    calc_requests_by_type.labels(cargo_type=data.cargo_type.lower()).inc()
    calc_density_summary.observe(density)
    calc_total_price_summary.observe(total_price)
    return price_per_kgm3
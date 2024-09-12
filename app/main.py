from fastapi import FastAPI

app = FastAPI()


@app.get("/ping")
def pong():
    return {"ping": "pong!"}


def convert(from_symbol, to_symbol, amount, rates):
    rate = (rates.get(to_symbol) or {}).get(from_symbol, None)

    if rate is None:
        rate = (rates.get(from_symbol) or {}).get(to_symbol, None)
        rate = 1 / rate if rate else None

    if rate is None:
        return None

    return amount * rate

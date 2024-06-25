from fastapi import FastAPI

app = FastAPI()
@app.get("/health")
async def get_status():
    return {"message": "API is working"}

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

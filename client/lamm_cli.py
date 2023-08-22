import requests

with open("./client/test_file.json", "rb") as file:
    r = requests.post("http://localhost:80/sbs/create", files={"test_file.json": file})

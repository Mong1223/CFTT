from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
from datetime import datetime, timedelta
import jwt
from data import employees  # Простейшая имитация базы данных с данными о сотрудниках

app = FastAPI()
SECRET_KEY = 'secret_key'   # Секретный ключ для подписи JWT-токена
TOKEN_EXP = 3600  # Время действия токена (в секундах)


# Модель для данных авторизации (JSON)
class LoginData(BaseModel):
    username: str
    password: str


# Модель для данных о зарплате (JSON)
class SalaryData(BaseModel):
    token: str


# Генерация токена по логину и паролю
def generate_token(username: str, password: str) -> str | None:
    if username in employees and employees[username]['password'] == password:
        payload = {
            'username': username,
            'exp': datetime.utcnow() + timedelta(seconds=TOKEN_EXP)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        return token
    else:
        return None


# Проверка валидности токена
def verify_token(token: str) -> str:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload['username']
    except jwt.ExpiredSignatureError:
        return 'Token expired. Please, log in again.'
    except jwt.InvalidTokenError:
        return 'Invalid token. PLease, log in again.'


# Маршрут для авторизации и получения токена
@app.post('/login')
async def login(login_data: LoginData):
    token = generate_token(login_data.username, login_data.password)
    if token:
        return {'token': token}
    else:
        raise HTTPException(status_code=401, detail='Invalid username or password')


# Маршрут для получения данных о зарплате и дате следующего повышения
@app.get('/salary')
async def get_salary(authorization: str = Header(...)):
    if authorization:
        token = authorization.split(' ')[1]
        username = verify_token(token)
        if username:
            return {
                'username': username,
                'salary': employees[username]['salary'],
                'promotion_date': employees[username]['promotion_date']
            }
        else:
            return {'error': 'Invalid or expired token'}
    else:
        return {'error': 'Token is missing'}

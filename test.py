import requests
import json

url = 'http://127.0.0.1:8000/login'
print("Введите имя: ")
name = input()
print("Введите пароль: ")
password = input()

data = {'username': name, 'password': password}
headers = {'Content-Type': 'application/json'}

response = requests.post(url, data=json.dumps(data), headers=headers)
# print(response.json())

# Извлечение токена из объекта
token = response.json().get('token')

url = 'http://127.0.0.1:8000/salary'

headers = {'Authorization': 'Bearer ' + token}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    print("Данные о зарплате:\n","username:", response.json()['username'],"\n","Salary: ",
          response.json()['salary'],"\n", "promotion_date: ",response.json()['promotion_date']
          )
else:
    print("Ошибка при получении данных о зарплате:", response.text)





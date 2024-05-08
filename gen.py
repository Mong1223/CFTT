import random
import string
import pandas as pd


def generate_random_password(length=8):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


def generate_random_date(start_date, end_date):
    start_timestamp = pd.to_datetime(start_date).timestamp()
    end_timestamp = pd.to_datetime(end_date).timestamp()
    random_timestamp = random.uniform(start_timestamp, end_timestamp)
    return pd.to_datetime(random_timestamp, unit='s').strftime('%Y-%m-%d')


def generate_random_salary(min_salary=30000, max_salary=100000):
    return random.randint(min_salary, max_salary)


def generate_employees(num_employees):
    employees = {}
    for i in range(num_employees):
        name = 'employee{}'.format(i+1)
        password = generate_random_password()
        salary = generate_random_salary()
        promotion_date = generate_random_date('2023-01-01', '2024-12-31')
        employees[name] = {'password': password, 'salary': salary, 'promotion_date': promotion_date}
    return employees


num_employees = 100
employees = generate_employees(num_employees)
print(employees)


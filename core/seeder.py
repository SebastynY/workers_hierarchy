from django_seed import Seed
from core.models import Worker
from faker import Faker
from dateutil import parser as date_parser
from django.conf import settings
from django_seed.seeder import Seeder

fake = Faker()


def add(seeder: Seeder, position: int, amount: int = 1, superior: Worker = None):
    seeder.add_entity(Worker, amount, {
        'first_name': lambda _: fake.first_name(),
        'last_name': lambda _: fake.last_name(),
        'date_hired': lambda _: date_parser.parse(fake.date()).date(),
        'salary': lambda _: fake.pydecimal(left_digits=6, right_digits=2, positive=True),
        'position': lambda _: position,
        'superior': lambda _: superior
    })


def add_ceo():
    # Создаём seeder (Пустой)
    seeder = Seed.seeder()
    # Заполняем seeder одной записью
    add(seeder, Worker.Position.CEO)
    # Записываем данные из seeder в базу данных, при этом сам seeder удаляется
    seeder.execute()
    # Создаём seeder (Пустой) и возварщаем
    return Seed.seeder()


def add_presidents(seeder):
    ceo = Worker.objects.get(position=Worker.Position.CEO)
    add(seeder, Worker.Position.PRESIDENT, settings.PRESIDENTS_AMOUNT, ceo)
    seeder.execute()
    return Seed.seeder()


def add_directors(seeder):
    presidents = Worker.objects.filter(position=Worker.Position.PRESIDENT)
    for president in presidents:
        add(seeder, Worker.Position.DIRECTOR, settings.DIRECTORS_AMOUNT, president)
    seeder.execute()
    return Seed.seeder()


def add_managers(seeder):
    directors = Worker.objects.filter(position=Worker.Position.DIRECTOR)
    for director in directors:
        add(seeder, Worker.Position.MANAGER, settings.MANAGERS_AMOUNT, director)
    seeder.execute()
    return Seed.seeder()


def add_employees(seeder):
    managers = Worker.objects.filter(position=Worker.Position.MANAGER)
    for manager in managers:
        add(seeder, Worker.Position.EMPLOYEE, settings.EMPLOYEES_AMOUNT, manager)
    seeder.execute()


def execute():
    seeder = add_ceo()
    seeder = add_presidents(seeder)
    seeder = add_directors(seeder)
    seeder = add_managers(seeder)
    add_employees(seeder)

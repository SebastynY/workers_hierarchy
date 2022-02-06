from django.db import models


class Worker(models.Model):
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    date_hired = models.DateField()
    salary = models.DecimalField(decimal_places=2, max_digits=15)
    superior = models.ForeignKey('self', blank=True, null=True,
                                 on_delete=models.SET_NULL, related_name='subordinates')

    class Position(models.IntegerChoices):
        CEO = 0
        PRESIDENT = 1
        DIRECTOR = 2
        MANAGER = 3
        EMPLOYEE = 4

    position = models.IntegerField(choices=Position.choices)

    def __str__(self):
        if self.superior:
            superior_position = self.superior.position
            superior_first_name = self.superior.first_name
            superior_last_name = self.superior.last_name
        else:
            superior_first_name = '-'
            superior_last_name = '-'
            superior_position = 0
        return f'{self.first_name} {self.last_name}, ' \
               f'{self.Position.choices[self.position][1]} -> ' \
               f'{self.Position.choices[superior_position][1]} ' \
               f'({superior_first_name} {superior_last_name})'



from dataclasses import dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        message = (f'Тип тренировки: {self.training_type}; '
                   f'Длительность: {self.duration:.3f} ч.; '
                   f'Дистанция: {self.distance:.3f} км; '
                   f'Ср. скорость: {self.speed:.3f} км/ч; '
                   f'Потрачено ккал: {self.calories:.3f}.')
        return message.format(self.training_type,
                              self.duration,
                              self.distance,
                              self.speed, self.calories)


@dataclass
class Training:
    """Базовый класс тренировки."""

    LEN_STEP = 0.65
    V_V_MIN = 60
    M_IN_KM = 1000

    action: int
    duration: float
    weight: float

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError(
            'Определите get_spent_caloires в %s' % (type(self).__name__))

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(type(self).__name__, self.duration,
                           self.get_distance(), self.get_mean_speed(),
                           self.get_spent_calories())


@dataclass
class Running(Training):
    """Тренировка: бег."""

    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def get_spent_calories(self) -> float:
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed()
                + self.CALORIES_MEAN_SPEED_SHIFT)
                * (self.weight / self.M_IN_KM)
                * (self.duration * self.V_V_MIN))


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    K_1 = 0.035
    K_2 = 0.029
    SR_SKOROST_V_MS = 0.278
    R_V_SM = 100

    height: int

    def get_spent_calories(self) -> float:
        return ((self.K_1 * self.weight
                + (((self.get_mean_speed() * self.SR_SKOROST_V_MS)**2)
                   / (self.height / self.R_V_SM)) * self.K_2 * self.weight)
                * self.duration * self.V_V_MIN)


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP = 1.38
    K_3 = 1.1
    K_4 = 2

    length_pool: float
    count_pool: float

    def get_mean_speed(self) -> float:
        return (self.length_pool * self.count_pool / self.M_IN_KM
                / self.duration)

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed() + self.K_3) * self.K_4
                * self.weight * self.duration)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_means = {'SWM': Swimming,
                      'RUN': Running,
                      'WLK': SportsWalking}
    if workout_type in training_means:
        return training_means[workout_type](*data)
    raise KeyError(f'В {training_means[workout_type]}'
                   f'не верно получены данные')


def main(training: Training) -> None:
    """Главная функция."""
    print(training.show_training_info().get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)

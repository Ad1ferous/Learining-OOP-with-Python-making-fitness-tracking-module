from typing import NoReturn, List, Dict, Type, Tuple
from dataclasses import asdict, dataclass


@dataclass
class InfoMessage:
    """Information about training."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    MESSAGE: str = ('Type of training: {training_type}; '
                    'Duration: {duration:.3f} h.; '
                    'Distance: {distance:.3f} km; '
                    'Average speed: {speed:.3f} km/h; '
                    'Calories spent: {calories:.3f}.')

    def get_message(self) -> str:
        return self.MESSAGE.format(**asdict(self))


class Training:
    """Base traing class."""
    LEN_STEP: float = 0.65
    M_IN_KM: float = 1000
    M_IN_H: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> NoReturn:
        self.action_qty: int = action
        self.duration_h: float = duration
        self.weight_kg: float = weight

    def get_distance(self) -> float:
        """Get distance in km."""
        return self.action_qty * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Get average speed."""
        return self.get_distance() / self.duration_h

    def get_spent_calories(self) -> float:
        """Get amount of spent calories."""

        pass

    def show_training_info(self) -> InfoMessage:
        """Reurn message about performed training."""
        return InfoMessage(type(self).__name__,
                           self.duration_h,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Training: running."""
    COEFF_MULPIPLIER: float = 18
    COEFF_MEAN_SPEED_SUBTRACTOR: float = 20

    def get_spent_calories(self) -> float:
        return ((self.COEFF_MULPIPLIER * self.get_mean_speed()
                - self.COEFF_MEAN_SPEED_SUBTRACTOR) * self.weight_kg
                / self.M_IN_KM * self.duration_h * self.M_IN_H)


class SportsWalking(Training):
    """Training: sports walking."""
    COEFF_MULPIPLIER_1: float = 0.035
    COEFF_MULPIPLIER_2: float = 0.029

    def __init__(self, action: int, duration: float,
                 weight: float, height: float,) -> NoReturn:
        super().__init__(action, duration, weight)
        self.height: float = height
        self.duration: float = duration

    def get_spent_calories(self) -> float:
        return ((self.COEFF_MULPIPLIER_1 * self.weight_kg
                + (self.get_mean_speed() ** 2
                 // self.height) * self.COEFF_MULPIPLIER_2 * self.weight_kg)
                * self.duration * self.M_IN_H)


class Swimming(Training):
    """Training: swimming."""
    LEN_STEP: float = 1.38
    COEFF_MULPIPLIER_1: float = 1.1
    COEFF_MULPIPLIER_2: float = 2

    def __init__(self, action: int, duration: float, weight: float,
                 length_pool: int, count_pool: int, ) -> NoReturn:
        super().__init__(action, duration, weight)
        self.length_pool_m: int = length_pool
        self.count_pool_qty: int = count_pool

    def get_mean_speed(self) -> float:
        return (self.length_pool_m * self.count_pool_qty
                / self.M_IN_KM / self.duration_h)

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed() + self.COEFF_MULPIPLIER_1)
                * self.COEFF_MULPIPLIER_2 * self.weight_kg)


def read_package(workout_type: str, data: list) -> Training:
    """Read data from sensors."""
    try:
        training_type: Dict[str, Type[Training]] = {'RUN': Running,
                                                    'SWM': Swimming,
                                                    'WLK': SportsWalking}
        return training_type[workout_type](*data)
    except KeyError:
        print(f'Data of unknown training was read. '
              f'Expected: {list(training_type.keys())}')


def main(training: Training) -> NoReturn:
    """Main function."""
    info: InfoMessage = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages: List[Tuple[str, List[int]]] = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training: Training = read_package(workout_type, data)
        main(training)

from typing import Any, Optional
from unit import BaseUnit


class BaseSingleton(type):
    _instances: dict[Any, Any] = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Arena(metaclass=BaseSingleton):
    STAMINA_PER_ROUND: str= 1
    player: BaseUnit= None
    enemy: BaseUnit = None
    game_is_running: bool = False

    def start_game(self, player: BaseUnit, enemy: BaseUnit) -> None:
        # TODO НАЧАЛО ИГРЫ -> None
        # TODO присваиваем экземпляру класса аттрибуты "игрок" и "противник"
        # TODO а также выставляем True для свойства "началась ли игра"
        self.player = player
        self.enemy = enemy
        self.game_is_running = True

    def _check_players_hp(self):
        # TODO ПРОВЕРКА ЗДОРОВЬЯ ИГРОКА И ВРАГА
        # TODO проверка здоровья игрока и врага и возвращение результата строкой:
        # TODO может быть три результата:
        # TODO Игрок проиграл битву, Игрок выиграл битву, Ничья и сохраняем его в аттрибуте (self.battle_result)
        # TODO если Здоровья игроков в порядке то ничего не происходит
        if self.player.hp > 0 and self.enemy.hp > 0:
            self.battle_result = 'Ничья'
            return None
        if self.player.hp <= 0:
            self.battle_result = 'Игрок проиграл битву'
            self.player.hp = 0
        elif self.enemy.hp <= 0:
            self.battle_result = 'Игрок выиграл битву'
            self.enemy.hp = 0
        return self._end_game()



    def _stamina_regeneration(self) -> None:
        # TODO регенерация здоровья и стамины для игрока и врага за ход
        # TODO в этом методе к количеству стамины игрока и врага прибавляется константное значение.
        # TODO главное чтобы оно не привысило максимальные значения (используйте if)
        if self.player.unit_class.max_stamina > self.player.stamina:
            self.player.stamina += self.STAMINA_PER_ROUND * self.player.unit_class.stamina
            if self.player.unit_class.max_stamina < self.player.stamina:
                self.player.stamina = self.player.unit_class.max_stamina
        if self.enemy.unit_class.max_stamina > self.enemy.stamina:
            self.enemy.stamina += self.STAMINA_PER_ROUND * self.enemy.unit_class.stamina
            if self.enemy.unit_class.max_stamina < self.enemy.stamina:
                self.enemy.stamina = self.enemy.unit_class.max_stamina




    def next_turn(self):
        # TODO СЛЕДУЮЩИЙ ХОД -> return result | return self.enemy.hit(self.player)
        # TODO срабатывает когда игроп пропускает ход или когда игрок наносит удар.
        # TODO создаем поле result и проверяем что вернется в результате функции self._check_players_hp
        # TODO если result -> возвращаем его
        # TODO если же результата пока нет и после завершения хода игра продолжается,
        # TODO тогда запускаем процесс регенирации стамины и здоровья для игроков (self._stamina_regeneration)
        # TODO и вызываем функцию self.enemy.hit(self.player) - ответный удар врага
        result = self._check_players_hp()
        if result is not None:
            return result

        self._stamina_regeneration()
        res = self.enemy.hit(self.player)
        result = self._check_players_hp()
        if result is not None:
            return result
        return res


    def _end_game(self)-> str:
        # TODO КНОПКА ЗАВЕРШЕНИЕ ИГРЫ - > return result: str
        # TODO очищаем синглтон - self._instances = {}
        # TODO останавливаем игру (game_is_running)
        # TODO возвращаем результат
        self._instances = {}
        self.game_is_running = False
        return self.battle_result

    def player_hit(self)-> str:
        # TODO КНОПКА УДАР ИГРОКА -> return result: str
        # TODO получаем результат от функции self.player.hit
        # TODO запускаем следующий ход
        # TODO возвращаем результат удара строкой
        result = self.player.hit(self.enemy)
        enemy_turn = self.next_turn()
        return f'{result}\n {enemy_turn}'

    def player_use_skill(self)-> str:
        # TODO КНОПКА ИГРОК ИСПОЛЬЗУЕТ УМЕНИЕ
        # TODO получаем результат от функции self.use_skill
        # TODO включаем следующий ход
        # TODO возвращаем результат удара строкой
        result = self.player.use_skill(self.enemy)
        enemy_turn = self.next_turn()
        return f'{result}\n {enemy_turn}'

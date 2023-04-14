from __future__ import annotations
from abc import ABC, abstractmethod


from equipment import Equipment, Weapon, Armor
from classes import UnitClass
from random import randint
from typing import Optional


class BaseUnit(ABC):
    """
    Базовый класс юнита
    """
    def __init__(self, name: str, unit_class: UnitClass):
        """
        При инициализации класса Unit используем свойства класса UnitClass
        """
        self.name: str = name
        self.unit_class: UnitClass = unit_class
        self.hp: float = unit_class.max_health
        self.stamina: float = unit_class.max_stamina
        self.weapon: Weapon | None = None
        self.armor: Armor | None = None
        self._is_skill_used: bool = False


    @property
    def skill_used(self) -> bool:
        return self._is_skill_used

    @property
    def health_points(self):
        return round(self.hp, 1)

    @property
    def stamina_points(self):
        return  round(self.stamina, 1)

    def equip_weapon(self, weapon: str)-> str:
        equipment = Equipment()
        self.weapon = equipment.get_weapon(weapon)
        return f"{self.name} экипирован оружием {self.weapon.name}"

    def equip_armor(self, armor: str)-> str:
        equipment = Equipment()
        self.armor = equipment.get_armor(armor)
        return f"{self.name} экипирован броней {self.armor.name}"

    def _count_damage(self, target: BaseUnit) -> Optional[float]:
        # TODO Эта функция должна содержать:
        #  логику расчета урона игрока
        #  логику расчета брони цели
        #  здесь же происходит уменьшение выносливости атакующего при ударе
        #  и уменьшение выносливости защищающегося при использовании брони
        #  если у защищающегося нехватает выносливости - его броня игнорируется
        #  после всех расчетов цель получает урон - target.get_damage(damage)
        #  и возвращаем предполагаемый урон для последующего вывода пользователю в текстовом виде

        if not  self._checking_stamina_unit():
            return False

        if self._checking_stamina_target(target):
            self._stamina_changes_target(target)

            damage = round(self._get_unit_damage_with_weapons() - self._get_target_protection_with_armor(target), 1)
        else:
            damage = round(self._get_unit_damage_with_weapons(), 1)
        self._stamina_changes_unit()
        target.get_damage(damage)
        return damage

    def _checking_stamina_unit(self) -> bool:
        """
        проверяет достаточно ли выносливасти у атакующего
        :return: bool
        """
        return self.stamina > self.weapon.stamina_per_hit



    def _get_unit_damage_with_weapons(self) -> float:
        """
        получает урон атакующего
        :return: float
        """
        return self.weapon.damage * self.unit_class.attack

    def _stamina_changes_unit(self) -> None:
        """
        меняет показатель стамины атакующего
        :return:None
        """
        self.stamina -= self.weapon.stamina_per_hit
        if self.stamina < 0:
            self.stamina =0

    def _checking_stamina_target(self, target: BaseUnit) -> bool:
        """
        проверяет достаточно ли выносливасти у обороняющегося
        :param target: экземпляр класа обороняющегося
        :return: bool
        """
        return target.stamina > target.armor.stamina_per_turn

    def _get_target_protection_with_armor(self, target: BaseUnit) -> float:
        """
        получает показатель защиты защищающегося
        :param target: BaseUnit
        :return: float
        """
        return target.armor.defence * target.unit_class.armor

    def _stamina_changes_target(self, target: BaseUnit) -> None:
        """
        меняет показатель стамины защищающегося
        :param target:BaseUnit
        :return: None
        """
        target.stamina -= target.armor.stamina_per_turn

    def get_damage(self, damage: int) -> Optional[float]:
        # TODO получение урона целью
        #      присваиваем новое значение для аттрибута self.hp
        if not damage:
            return False
        if damage > 0:
            self.hp -= damage
            return damage
        return damage


    @abstractmethod
    def hit(self, target: BaseUnit) -> str:
        """
        этот метод будет переопределен ниже
        """
        pass

    def use_skill(self, target: BaseUnit) -> str:
        """
        метод использования умения.
        если умение уже использовано возвращаем строку
        Навык использован
        Если же умение не использовано тогда выполняем функцию
        self.unit_class.skill.use(user=self, target=target)
        и уже эта функция вернем нам строку которая характеризует выполнение умения
        """
        if self.skill_used:
            return 'Навык использован'

        self._is_skill_used = True
        return self.unit_class.skill.use(user=self, target=target)



class PlayerUnit(BaseUnit):
    def hit(self, target: BaseUnit) -> str:
        """
        функция удар игрока:
        здесь происходит проверка достаточно ли выносливости для нанесения удара.
        вызывается функция self._count_damage(target)
        а также возвращается результат в виде строки
        """
        damage = self._count_damage(target)

        if not damage:
            return f"{self.name} попытался использовать {self.weapon.name}, но у него не хватило выносливости."

        if damage > 0:
            return f"{self.name} используя {self.weapon.name} пробивает {target.armor.name}" \
                   f" соперника и наносит {damage} урона."

        return f"{self.name} используя {self.weapon.name} наносит удар, но {target.armor.name} " \
               f"cоперника его останавливает."


class EnemyUnit(BaseUnit):

    def hit(self, target: BaseUnit) -> str:
        """
        функция удар соперника
        должна содержать логику применения соперником умения
        (он должен делать это автоматически и только 1 раз за бой).
        Например, для этих целей можно использовать функцию randint из библиотеки random.
        Если умение не применено, противник наносит простой удар, где также используется
        функция _count_damage(target
        """
        if not self._is_skill_used and randint(0, 1):
                return self.use_skill(target=target)

        damage = self._count_damage(target)
        if not damage:
            return f"{self.name} попытался использовать {self.weapon.name}, но у него не хватило выносливости."

        if damage > 0:
            return f"{self.name} используя {self.weapon.name} пробивает {target.armor.name} и наносит Вам {damage} урона."

        return f"{self.name} используя {self.weapon.name} наносит удар, но Ваш(а) {target.armor.name} его останавливает."



from flask import Flask, render_template, request, redirect, url_for

from classes import unit_classes
from equipment import Equipment
from unit import BaseUnit, PlayerUnit, EnemyUnit
from base import Arena


app = Flask(__name__)



heroes: dict[BaseUnit] = {}

arena = Arena() # TODO инициализируем класс арены


@app.route("/")
def menu_page():
    # TODO рендерим главное меню (шаблон index.html)
    return render_template("index.html")


@app.route("/fight/")
def start_fight():
    # TODO выполняем функцию start_game экземпляра класса арена и передаем ему необходимые аргументы
    # TODO рендерим экран боя (шаблон fight.html)
    arena.start_game(heroes["player"], heroes["enemy"])
    return render_template("fight.html", heroes=heroes)

@app.route("/fight/hit")
def hit():
    # TODO кнопка нанесения удара
    # TODO обновляем экран боя (нанесение удара) (шаблон fight.html)
    # TODO если игра идет - вызываем метод player.hit() экземпляра класса арены
    # TODO если игра не идет - пропускаем срабатывание метода (простот рендерим шаблон с текущими данными)
    if arena.game_is_running:
        result = arena.player_hit()
    else:
        result = arena.battle_result
    return render_template("fight.html", heroes=heroes, result=result)


@app.route("/fight/use-skill")
def use_skill():
    # TODO кнопка использования скилла
    # TODO логика пркатикчески идентична предыдущему эндпоинту
    if arena.game_is_running:
        result = arena.player_use_skill()
    else:
        result = arena.battle_result
    return render_template("fight.html", heroes=heroes, result=result)


@app.route("/fight/pass-turn")
def pass_turn():
    # TODO кнопка пропус хода
    # TODO логика пркатикчески идентична предыдущему эндпоинту
    # TODO однако вызываем здесь функцию следующий ход (arena.next_turn())
    if arena.game_is_running:
        result = arena.next_turn()
    else:
        result = arena.battle_result
    return render_template("fight.html", heroes=heroes, result=result)


@app.route("/fight/end-fight")
def end_fight():
    # TODO кнопка завершить игру - переход в главное меню
    return render_template("index.html", heroes=heroes)


@app.route("/choose-hero/", methods=['post', 'get'])
def choose_hero():
    # TODO кнопка выбор героя. 2 метода GET и POST
    # TODO на GET отрисовываем форму.
    # TODO на POST отправляем форму и делаем редирект на эндпоинт choose enemy
    if request.method == 'GET':
        equipment = Equipment()
        result = {
            "header": 'Выбери героя',  # для названия страниц
            "classes": unit_classes,  # для названия классов
            "weapons": equipment.get_weapons_names(),  # для названия оружия
            "armors": equipment.get_armors_names()  # для названия брони
        }
        return render_template("hero_choosing.html", result=result)
    if request.method == "POST":
        name = request.form['name']
        classes = request.form['unit_class']
        weapon = request.form['weapon']
        armor = request.form['armor']

        player = PlayerUnit(name=name, unit_class=unit_classes[classes])
        player.equip_weapon(weapon)
        player.equip_armor(armor)
        heroes["player"] = player
        return redirect(url_for("choose_enemy"))
    return ""



@app.route("/choose-enemy/", methods=['post', 'get'])
def choose_enemy():
    # TODO кнопка выбор соперников. 2 метода GET и POST
    # TODO также на GET отрисовываем форму.
    # TODO а на POST отправляем форму и делаем редирект на начало битвы
    if request.method == 'GET':
        equipment = Equipment()
        result = {
            "header": 'Выбери героя',  # для названия страниц
            "classes": unit_classes,  # для названия классов
            "weapons": equipment.get_weapons_names(),  # для названия оружия
            "armors": equipment.get_armors_names()  # для названия брони
        }
        return render_template("hero_choosing.html", result=result)
    if request.method == "POST":
        name = request.form['name']
        classes = request.form['unit_class']
        weapon = request.form['weapon']
        armor = request.form['armor']

        enemy = EnemyUnit(name=name, unit_class=unit_classes[classes])
        enemy.equip_weapon(weapon)
        enemy.equip_armor(armor)
        heroes["enemy"] = enemy
        return redirect(url_for("start_fight"))
    return ""


if __name__ == "__main__":
    app.run()

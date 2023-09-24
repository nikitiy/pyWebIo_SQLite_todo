from functools import partial

from pywebio import start_server
from pywebio.input import *
from pywebio.output import *

from database import *


def rendering_tasks():
    tasks = execute_select_query(connection)
    clear("tasks_box")
    with use_scope('tasks_box'):
        for task_id, task_text in tasks:
            put_row([
                put_text(task_text),
                None,
                put_buttons(['Изменить', 'Удалить'], onclick=partial(edit_task, task_id))
            ], size='1fr 1% auto')


def edit_task(task_id, mode):
    if mode == 'Изменить':
        task = input_group("Редактирование задачи", [
            input(placeholder="Задача", name="task"),
            actions(name="cmd", buttons=["Сохранить"])
        ])
        execute_query(connection, update_query(task['task'], task_id))
    elif mode == 'Удалить':
        execute_query(connection, delete_query(task_id))

    rendering_tasks()


def create_task_input():
    task = input_group("Новая задача", [
        input(placeholder="Задача", name="task"),
        actions(name="cmd", buttons=["Создать"])
    ], validate=lambda t: ('task', 'Введите задачу!') if t['cmd'] == "Создать" and not t['task'] else None)

    execute_query(connection, insert_query(task['task']))


def main():
    put_markdown("## Добро пожаловать в наш TODO!")
    tasks_box = put_scope(name="tasks_box")
    put_scrollable(tasks_box, height=300, keep_bottom=True)
    rendering_tasks()

    while True:
        create_task_input()
        rendering_tasks()


if __name__ == "__main__":
    connection = create_connection()
    start_server(main, debug=True, port=8080, cdn=False)

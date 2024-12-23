from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import psycopg2
from db import get_connection

tasks_bp = Blueprint('tasks', __name__)

# Ruta para ver todas las tareas
@tasks_bp.route('/tasks')
def tasks():
    user_id = session.get('user_id')  # Obtén el ID del usuario de la sesión
    if not user_id:
        flash('Debes iniciar sesión primero')
        return redirect(url_for('auth.login'))

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM tasks WHERE user_id = %s;", (user_id,))
    tasks = cursor.fetchall()

    cursor.close()
    connection.close()
    return render_template('tasks/tasks.html', tasks=tasks)

# Ruta para crear una nueva tarea
@tasks_bp.route('/tasks/create', methods=['GET', 'POST'])
def create_task():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        user_id = session.get('user_id')  # Obtén el ID del usuario de la sesión

        if not title:
            flash('El título de la tarea es obligatorio')
            return redirect(url_for('tasks.create_task'))

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO tasks (title, description, user_id) 
            VALUES (%s, %s, %s);
        """, (title, description, user_id))

        connection.commit()
        cursor.close()
        connection.close()
        flash('Tarea creada exitosamente')
        return redirect(url_for('tasks.tasks'))

    return render_template('tasks/create_task.html')

# Ruta para editar una tarea existente
@tasks_bp.route('/tasks/edit/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM tasks WHERE id = %s;", (task_id,))
    task = cursor.fetchone()

    if not task:
        flash('Tarea no encontrada')
        return redirect(url_for('tasks.tasks'))

    if task[3] != session.get('user_id'):  # Suponiendo que task[3] es el user_id
        flash('No tienes permiso para editar esta tarea')
        return redirect(url_for('tasks.tasks'))

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        cursor.execute("""
            UPDATE tasks SET title = %s, description = %s, updated_at = CURRENT_TIMESTAMP 
            WHERE id = %s;
        """, (title, description, task_id))
        connection.commit()
        cursor.close()
        connection.close()
        flash('Tarea actualizada exitosamente')
        return redirect(url_for('tasks.tasks'))

    cursor.close()
    connection.close()
    return render_template('tasks/edit_task.html', task=task)


# Ruta para eliminar una tarea
@tasks_bp.route('/tasks/delete/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    user_id = session.get('user_id')
    if not user_id:
        flash('Debes iniciar sesión primero')
        return redirect(url_for('auth.login'))

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT user_id FROM tasks WHERE id = %s;", (task_id,))
    task = cursor.fetchone()

    if not task:
        flash('Tarea no encontrada')
        return redirect(url_for('tasks.tasks'))

    # Verificar si el usuario que realiza la solicitud es el mismo que creó la tarea
    if task[0] != user_id:  # Asumiendo que el user_id está en la primera columna
        flash('No tienes permiso para eliminar esta tarea')
        return redirect(url_for('tasks.tasks'))

    cursor.execute("DELETE FROM tasks WHERE id = %s;", (task_id,))
    connection.commit()

    cursor.close()
    connection.close()
    flash('Tarea eliminada exitosamente')
    return redirect(url_for('tasks.tasks'))


from flask import Flask, render_template, request, redirect, url_for
import psycopg2

app = Flask('My Todolist webapp')
app.secret_key = 'abcdefgh1029384756'


# multiple route goes to the same page
@app.route('/')
@app.route('/home')
def home():
    # templates/home.html
    return render_template('home.html')


@app.route('/add_project')
def add_pr():
    # templates/home.html
    return render_template('add_project.html', )


@app.route('/add_project_db', methods=["GET", "POST"])
def add_project_db():
    project_db = "Test_project"
    task_db = "Test_task"
    status_db = "Not_started"
    if request.method == "POST":
        # getting project id from HTML form
        pid_db = request.form.get("id")
        # getting project name from HTML form
        project_db = request.form.get("project")
        # getting task name from HTML form
        task_db = request.form.get("task")
        # getting task status from HTML form
        status_db = request.form.get("status")
        print(pid_db, project_db, task_db, status_db)
        val = (pid_db, project_db, task_db, status_db)
        try:
            conn = psycopg2.connect(user="postgres",
                                    password="2323",
                                    host="localhost",
                                    port="1412",
                                    database="todolist")
            cursor = conn.cursor()

            select_Query = """select * from todolist"""
            cursor.execute(select_Query)
            projects = cursor.fetchall()
            found = False
            for row in projects:
                if row[0] == pid_db:
                    found = True
            if found == False:
                insert_Query = """insert into todolist(id,project,task,status) values(%s,%s,%s,%s)"""
                cursor.execute(insert_Query, val)
                print("Inseram in tabela todolist folosind insert")
                conn.commit()
                return 'Succesfully added project!' \
                       '<a href="/projects"> Projects list</a>'
            else:
                return render_template('eroare.html',
                                       mesaj=" Project already exists in table!",
                                       )


        except (Exception, psycopg2.Error) as error:
            print("Error while inserting data to PostgreSQL", error)

        finally:
            # closing database connection.
            if conn:
                cursor.close()
                conn.close()
                print("PostgreSQL connection is closed")

    return render_template('home.html')


@app.route('/projects')
def show_projects():
    try:
        conn = psycopg2.connect(user="postgres",
                                password="2323",
                                host="localhost",
                                port="1412",
                                database="todolist")
        cursor = conn.cursor()
        select_Query = """select * from todolist"""
        cursor.execute(select_Query)
        projects_db = cursor.fetchall()
        print(projects_db)
        for row in projects_db:
            print(row[0] + ':' + row[1] + ':' + row[2])

        return render_template(
            'projects.html',
            title='Our great projects',
            projects=projects_db)

    except (Exception, psycopg2.Error) as error:
        print("Error while selecting data to PostgreSQL", error)

    finally:
        # closing database connection.
        if conn:
            cursor.close()
            conn.close()
            print("PostgreSQL connection is closed")


@app.route('/update_status')
def update_status():
    try:
        conn = psycopg2.connect(user="postgres",
                                password="2323",
                                host="localhost",
                                port="1412",
                                database="todolist")
        cursor = conn.cursor()
        select_Query = """select * from todolist"""
        cursor.execute(select_Query)
        projects_db = cursor.fetchall()
        print(projects_db)
        for row in projects_db:
            print(row[0] + ':' + row[1] + ':' + row[2] + ':' + row[3])

        return render_template(
            'update_status.html',
            title='Our great projects',
            projects=projects_db)

    except (Exception, psycopg2.Error) as error:
        print("Error while selecting data to PostgreSQL", error)

    finally:
        # closing database connection.
        if conn:
            cursor.close()
            conn.close()
            print("PostgreSQL connection is closed")


@app.route('/update_db/<string:pid_db>', methods=["GET", "POST"])
def update_db(pid_db):
    try:
        conn = psycopg2.connect(user="postgres",
                                password="2323",
                                host="localhost",
                                port="1412",
                                database="todolist")
        cursor = conn.cursor()
        select_Query = """select * from todolist"""
        cursor.execute(select_Query)
        projects_db = cursor.fetchall()
        for row in projects_db:
            if row[0] == pid_db:
                project_db = row[1]
                task_db = row[2]
                status_db = row[3]
        print(pid_db, status_db)
        return render_template(
            'update_db.html',
            pid=pid_db,
            project=project_db,
            task=task_db,
            status=status_db
        )

    except (Exception, psycopg2.Error) as error:
        print("Error while selecting data to PostgreSQL", error)

    finally:
        # closing database connection.
        if conn:
            cursor.close()
            conn.close()
            print("PostgreSQL connection is closed")
    return render_template('projects.html')


@app.route('/update_task_db/<string:pid_db>', methods=["GET", "POST"])
def update_task_db(pid_db):
    print(pid_db)
    if request.method == "POST":
        # getting task status from HTML form
        status_db = request.form.get("status")
        print(pid_db, status_db)
        val = (pid_db, status_db)
        try:
            conn = psycopg2.connect(user="postgres",
                                    password="2323",
                                    host="localhost",
                                    port="1412",
                                    database="todolist")
            cursor = conn.cursor()
            val = (status_db, pid_db)
            update_Query = """Update todolist set status = %s where id = %s"""
            cursor.execute(update_Query, val)
            conn.commit()
            select_Query = """select * from todolist"""
            cursor.execute(select_Query)
            projects_db = cursor.fetchall()
            return redirect('/projects')

        except (Exception, psycopg2.Error) as error:
            print("Error while inserting data to PostgreSQL", error)

        finally:
            # closing database connection.
            if conn:
                cursor.close()
                conn.close()
                print("PostgreSQL connection is closed")

    return render_template('home.html')


@app.route('/delete_task')
def delete_task():
    try:
        conn = psycopg2.connect(user="postgres",
                                password="2323",
                                host="localhost",
                                port="1412",
                                database="todolist")
        cursor = conn.cursor()
        select_Query = """select * from todolist"""
        cursor.execute(select_Query)
        projects_db = cursor.fetchall()
        print(projects_db)
        for row in projects_db:
            print(row[0] + ':' + row[1] + ':' + row[2] + ':' + row[3])

        return render_template(
            'delete_task.html',
            title='ToDoList',
            projects=projects_db)

    except (Exception, psycopg2.Error) as error:
        print("Error while selecting data to PostgreSQL", error)

    finally:
        # closing database connection.
        if conn:
            cursor.close()
            conn.close()
            print("PostgreSQL connection is closed")


@app.route('/delete_task_db/<string:pid_db>')
def delete_task_db(pid_db):
    try:
        conn = psycopg2.connect(user="postgres",
                                password="2323",
                                host="localhost",
                                port="1412",
                                database="todolist")
        cursor = conn.cursor()
        delete_Query = """delete from todolist where id='{0}'""".format(pid_db)
        # val=(pid_db)
        print(delete_Query)
        cursor.execute("""delete from todolist where id='{0}'""".format(pid_db))
        conn.commit()
        select_Query = """select * from todolist"""
        cursor.execute(select_Query)
        projects_db = cursor.fetchall()
        for row in projects_db:
            print(row[0] + ':' + row[1] + ':' + row[2] + ':' + row[3])

        return render_template(
            'projects.html',
            title='Our great projects',
            projects=projects_db)

    except (Exception, psycopg2.Error) as error:
        print("Error while deleting data from PostgreSQL", error)

    finally:
        # closing database connection.
        if conn:
            cursor.close()
            conn.close()
            print("PostgreSQL connection is closed")

    return redirect(url_for('show_projects'))


if __name__ == '__main__':
    # run in debug mode; no need to restart on changes
    app.run(debug=True)

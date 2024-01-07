from flask import Flask, request, session, redirect, url_for, send_file, render_template, g
import secrets
import re
import uuid
import sqlite3


app = Flask(__name__)
app.secret_key = secrets.token_hex(16)


def db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect("/tmp/db.sqlite3")
        db.row_factory = sqlite3.Row
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()


@app.before_first_request
def db_init():
    db = sqlite3.connect("/tmp/db.sqlite3")
    cursor = db.cursor()
    cursor.executescript(
        """
    CREATE TABLE IF NOT EXISTS copypasta_template (
        id TEXT,
        title,
        template TEXT,
        PRIMARY KEY (id)
    );
    """
    )
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS copypasta (
        id TEXT,
        orig_id TEXT,
        PRIMARY KEY (id)
    );
    """
    )
    
    cursor.execute( 
        "INSERT OR IGNORE INTO copypasta_template (id, title, template) VALUES (?,?,?), (?,?,?), (?,?,?)",
        ("1", "求求你們不要再貼疑似...", "求求你們不要再貼疑似{field[event]}的{field[media]}\n我從{field[when]}的時候就開始{field[action]}\n每當我被生活壓得喘不過氣來的時候\n只要聽到{field[hope]}\n就能找回活下去的希望\n昨天看到了那段{field[media]}\n雖然我知道{field[media]}是{field[who]}的可能性很少 畢竟有那麽多{field[similar]}\n難免會有相似的存在\n但是那個{field[thing]}真的太像了 我一看到就能反應過來\n感覺世界開始逐漸崩塌\n求求你們不要再討論這件事了\n再這樣下去我連唯一支持自己活下去的理由都沒有了",
         "2", "宿儺太強了...", "{field[character]}太強了\n而且{field[character]}還沒有使出全力的樣子\n對方就算沒有{field[object]}也會贏\n我甚至覺得有點對不起他\n我沒能在這場戰鬥讓{field[character]}展現他的全部給我\n殺死我的不是{field[thing1]}或{field[thing2]}\n而是比我更強的傢伙，真是太好了",
         "3", "FLAG???", "The flag is: {field[flag]}")
    )

    # add flag
    flag_uuid = str(uuid.uuid4())
    cursor.execute(
        "INSERT OR IGNORE INTO copypasta (id, orig_id) VALUES (?,?)",
        (flag_uuid, "3")
    )
    open(f'posts/{flag_uuid}', 'w').write(
        "The flag is: " + open('/flag').read()
    )

    db.commit()
    db.close()


@app.route("/")
def index():
    if session.get('posts') is None:
        session['posts'] = []
    templates = db().cursor().execute(
        "SELECT * FROM copypasta_template"
    ).fetchall()
    return render_template("index.html", templates=templates)


@app.get("/use")
def create():
    id = request.args.get("id")
    tmpl = db().cursor().execute(
        f"SELECT * FROM copypasta_template WHERE id = {id}"
    ).fetchone()
    content = tmpl["template"]
    fields = dict.fromkeys(re.findall(r"{field\[([^}]+)\]}", content))
    content = re.sub(r"{field\[([^}]+)\]}", r"{\1}", tmpl["template"])

    return render_template("create.html", content=content, fields=fields, id=id)


@app.post("/use")
def create_post():
    id = request.args.get("id")
    tmpl = db().cursor().execute(
        f"SELECT * FROM copypasta_template WHERE id = {id}"
    ).fetchone()
    content = tmpl["template"]

    res = content.format(field=request.form)
    id = str(uuid.uuid4())
    db().cursor().execute(
        "INSERT INTO copypasta (id, orig_id) VALUES (?, ?)",
        (id, tmpl["id"])
    )
    db().commit()

    with open(f"posts/{id}", "w") as f:
        f.write(res)

    session['posts'] = [id] + session['posts']

    return redirect(url_for("view", id=id))


@app.get("/view/<id>")
def view(id):
    if id in session.get('posts', []):
        content = open(f"posts/{id}").read()
    else:
        content = "(permission denied)"
    return render_template("view.html", content=content)

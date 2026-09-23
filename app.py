from flask import Flask, render_template, request, redirect, url_for, session, make_response
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'tem742'

usuarios = {'esther':'esther1234'}

cursos = [
    {'nombre':'desarrollo web', 'docente':'Ing. Lopez'},
    {'nombre':'Base de Datos', 'docente':'Ing. Garcia'},
    {'nombre':'Emergentes II', 'docente':'Ing. Mamani'}
]

@app.route('/')
def index():
    msg = request.args.get('msg')
    usuario_pref = request.cookies.get('usuario_preferido')
    if usuario_pref:
        bienvenida = f"Bienvenido nuevamente, {usuario_pref}."
    else:
        bienvenida = "Bienvenido al Portal Académico."
    return render_template('index.html', bienvenida=bienvenida, usuario_pref=usuario_pref, msg=msg)

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        u = request.form['username']
        p = request.form['password']
        if u in usuarios and usuarios[u] == p:
            session['usuario'] = u
            resp = make_response(redirect(url_for('perfil')))
            resp.set_cookie('usuario_preferido', u, max_age=60*60*24*30) # 30 dias
            return resp
        else:
            return render_template('login.html', error="Usuario o contraseña incorrectos")
    return render_template('login.html')

@app.route('/cursos')
def ver_cursos():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    return render_template('cursos.html', cursos=cursos)

@app.route('/perfil')
def perfil():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    return render_template('perfil.html', usuario=session['usuario'])

# PUNTO 6 - CIERRE DE SESION
@app.route('/logout')
def logout():
    session.clear() # 1. Elimina sesion
    resp = make_response(redirect(url_for('index', msg="La sesión fue cerrada correctamente."))) # 2. Redirige a principal
    return resp # 3. El mensaje se muestra en index con?msg=

# PUNTO 5 - ELIMINAR COOKIE
@app.route('/eliminar_cookie')
def eliminar_cookie():
    resp = make_response(redirect(url_for('index', msg="Cookie eliminada.")))
    resp.delete_cookie('usuario_preferido')
    return resp

if __name__ == '__main__':
    app.run(debug=True)
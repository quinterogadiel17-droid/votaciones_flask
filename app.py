from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

from database.conexion import obtener_conexion

app = Flask(__name__)


def obtener_puestos():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT id, lugar_votacion FROM puestos_votacion ORDER BY lugar_votacion")
    puestos = cursor.fetchall()
    cursor.close()
    conexion.close()
    return puestos


@app.route("/")
def inicio():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    error = None

    try:
        puestos = obtener_puestos()
    except mysql.connector.Error as exc:
        puestos = []
        error = f"No se pudieron cargar los puestos de votacion: {exc.msg}"

    if request.method == "POST":
        identificacion = request.form.get("identificacion", "").strip()
        nombre = request.form.get("nombre", "").strip()
        puesto_id = request.form.get("puesto_id", "").strip()

        if not identificacion or not nombre or not puesto_id:
            return render_template(
                "registro.html",
                puestos=puestos,
                error="Todos los campos son obligatorios.",
            )

        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(
                """
                INSERT INTO ciudadanos (numero_identificacion, nombre, puesto_id)
                VALUES (%s, %s, %s)
                """,
                (identificacion, nombre, puesto_id),
            )
            conexion.commit()
            cursor.close()
            conexion.close()
            return redirect(url_for("inicio"))
        except mysql.connector.IntegrityError:
            error = "La identificacion ya existe o el puesto no es valido."
        except mysql.connector.Error as exc:
            error = f"No se pudo registrar el ciudadano: {exc.msg}"

    return render_template("registro.html", puestos=puestos, error=error)


@app.route("/consult", methods=["GET", "POST"])
def consult():
    if request.method == "POST":
        identificacion = request.form.get("identificacion", "").strip()

        if not identificacion:
            return render_template(
                "resultado.html",
                ciudadano=None,
                error="Debes ingresar una identificacion.",
            )

        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor(dictionary=True)
            cursor.execute(
                """
                SELECT
                    c.numero_identificacion,
                    c.nombre,
                    p.lugar_votacion,
                    p.direccion,
                    p.mesa,
                    p.zona
                FROM ciudadanos c
                JOIN puestos_votacion p ON c.puesto_id = p.id
                WHERE c.numero_identificacion = %s
                """,
                (identificacion,),
            )
            ciudadano = cursor.fetchone()
            cursor.close()
            conexion.close()
        except mysql.connector.Error as exc:
            return render_template(
                "resultado.html",
                ciudadano=None,
                error=f"Error consultando la base de datos: {exc.msg}",
            )

        if ciudadano is None:
            return render_template(
                "resultado.html",
                ciudadano=None,
                error="No existe un ciudadano registrado con esa identificacion.",
            )

        return render_template("resultado.html", ciudadano=ciudadano, error=None)

    return render_template("consulta.html")


if __name__ == "__main__":
    app.run(debug=True)

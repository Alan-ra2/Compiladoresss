from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Función de análisis léxico
def analizador_lexico(codigo):
    lineas = codigo.splitlines()
    analisis_lexico = []
    
    num_linea = 1
    for linea in lineas:
        tokens = linea.split()  # Dividir la línea en tokens (por espacios)
        resultado_linea = f"Línea {num_linea}:\n"
        simbolos = []

        for token in tokens:
            if token in ["int", "float"]:
                resultado_linea += f"<Tipo de dato> {token}\n"
                simbolos.append(token)
            elif token == "main":
                resultado_linea += f"<Reservada main> {token}\n"
                simbolos.append(token)
            elif token == "(":
                resultado_linea += f"<Paréntesis de apertura> {token}\n"
                simbolos.append(token)
            elif token == ")":
                resultado_linea += f"<Paréntesis de cierre> {token}\n"
                simbolos.append(token)
            elif token == "{":
                resultado_linea += f"<Llave de apertura> {token}\n"
                simbolos.append(token)
            elif token == "}":
                resultado_linea += f"<Llave de cierre> {token}\n"
                simbolos.append(token)
            elif token == ";":
                resultado_linea += f"<Punto y coma> {token}\n"
                simbolos.append(token)
            else:
                resultado_linea += f"<Identificador> {token}\n"
                simbolos.append(token)
        
        analisis_lexico.append((resultado_linea, simbolos))
        num_linea += 1
    
    return analisis_lexico

# Función de análisis sintáctico
def analizador_sintactico(codigo):
    lineas = codigo.splitlines()
    analisis_sintactico = []
    
    for linea in lineas:
        tokens = linea.split()
        if not tokens:
            continue

        # Comprobar una declaración de función: int main() { }
        if len(tokens) >= 5 and tokens[0] in ["int", "float"] and tokens[1] == "main" and tokens[2] == "(" and tokens[3] == ")" and tokens[4] == "{":
            analisis_sintactico.append("<Sintácticamente correcto: declaración de función>\n")
        # Comprobar una declaración de variable: int x;
        elif len(tokens) == 3 and tokens[0] in ["int", "float"] and tokens[2] == ";":
            analisis_sintactico.append("<Sintácticamente correcto: declaración de variable>\n")
        # Comprobar una llave de cierre
        elif len(tokens) == 1 and tokens[0] == "}":
            analisis_sintactico.append("<Sintácticamente correcto: cierre de bloque>\n")
        else:
            analisis_sintactico.append("<Error sintáctico>\n")
    
    return analisis_sintactico

@app.route("/", methods=["GET", "POST"])
def index():
    resultado_lexico = []
    resultado_sintactico = []
    
    if request.method == "POST":
        if "codigo" in request.form:
            codigo = request.form["codigo"]
            
            # Ejecutar análisis léxico
            resultado_lexico = analizador_lexico(codigo)
            
            # Ejecutar análisis sintáctico
            resultado_sintactico = analizador_sintactico(codigo)
        elif "borrar" in request.form:
            # Si se presiona el botón de borrar, simplemente redirigimos para resetear el formulario
            return redirect(url_for("index"))
    
    return render_template("index3.html", resultado_lexico=resultado_lexico, resultado_sintactico=resultado_sintactico)

if __name__ == "__main__":
    app.run(debug=True)


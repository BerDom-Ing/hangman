## Ejecución del servidor Flask

Para evitar problemas de imports, ejecuta el servidor Flask desde la raíz del proyecto usando el módulo y la variable de entorno FLASK_APP:

En PowerShell (Windows):

$env:FLASK_APP="app.web"
flask run

En Linux/Mac:

export FLASK_APP=app.web
flask run

No uses `python app/web.py` para ejecutar la app, ya que eso puede causar errores de importación.

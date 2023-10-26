# Seguimiento de Gastos

## Instalacion

### Inicializando el venv

Creamos el ambiente virtual, parado en la carpeta backend correr:

```
python -m venv venv
```

Habilitamos la ejecucion de scripts en Windows. En la terminal:
```
Set-ExecutionPolicy Unrestricted -Scope Process
```
Ahora si podemos continuar con la incializacion del ambiente virtual, corremos:

```
.\venv\Scripts\activate
```
Por ultimo, instalamos los requirements (las librerias que va a usar el proyecto). Esto lo logramos ejecutando:

```
python -m pip install -r requirements.txt
```

### Termianndo el venv

Cuando ya no necesitamos mas el proyecto, procedemos a desactivar el ambiente virtual. Esto se hace con el comando:

```
deactivate
```

## Corriendo la app

Una vez inicializado el ambiente virtual debemos setear algunas variables de ambiente para lograr que Flask reconozca el archivo de la aplicacion. Esto lo hacemos con el comando:

```
$env:FLASK_APP="__init__.py"
```

Para inicializar la app ejecutamos el comando:

```
flask run
```

Ya se puede acceder a la app mediante la url:
```
 http://127.0.0.1:5000
```

Por ahora tiene las opciones:

* /signup
* /login
* /logout
* /profile


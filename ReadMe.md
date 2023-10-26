# Seguimiento de Gastos

## Instalacion

### Inicializando el venv

Primero hay que habilitar la ejecucion de scripts en Windows. EN la terminal, parado en la carpeta backend correr:
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
sdhgkghkdfjshjgf
## :snake: Python o como mejorar la vida de un administrador de sistemas
[![][license-svg]][license-url]

Código base que ilustró la charla [_Python o como mejorar la vida de un administrador de sistemas_](http://2016.es.pycon.org/es/schedule/python-o-como-mejorar-la-vida-de-un-administrador/) impartida en la [PyConES Almería 2016](http://2016.es.pycon.org/).

### ¿Sobre qué se habló?

Comparamos dos aplicaciones *gemelas* escritas en `Bash` y `Python` cuyo código está contenido en este mismo `repo`.

Las funcionalidades de estas utilidades *demo* son:

- [x] Consultar el espacio disponible en un `FS` (local o remoto)
- [x] Consultar es las tablas mas *pesadas* de un servidor `mysql` (local o remoto)
- [x] Reporting `HTML`.

Con atención especial a los siguientes puntos:

#### Toma de argumentos

- `getops` vs `arparse`
- Parámetros posicionales.
- Chequeo de valores permitidos.
- Acumulativos (listas/arrays)
- Mensajes HELP.
- Funciones de validación.

#### Logging

- *do it yourself* vs `import`
- Configuración del `logger`.
- Calls.
- Bash caveats.

#### Captura de excepciones

- `return/$?` vs `try/except`

#### Llamadas externas

- Gestión del interfaces.
- raw ssh vs paramiko
- Flexibilidad (raise).

#### Connexion contra BBDD

- `HERE-DOCS` vs Python `driver`

#### Y otros trucos ...

- Gestión de archivos de configuración.
- `Docstrings` + `Sphinx`
- Reusabilidad (`__name__ == “__main__"`).
- Distribución y packaging (`setup.py`).
- Webapp (`Flask` + `Jinja2` *templates*)

#### Vídeo de la charla

[![Python o como mejorar la vida de un administrador de sistemas](https://raw.githubusercontent.com/klashxx/PyConES/master/python-sysadmin-small.png)](https://youtu.be/gFa0gGXPQG4)

### Contacta conmigo

Mis perfiles online están [**aquí**](https://klashxx.github.io/about), no te cortes ... :godmode:

<h6 align="center">
<a href="http://2016.es.pycon.org/es/schedule/python-o-como-mejorar-la-vida-de-un-administrador/">
  <img src="https://github.com/klashxx/PyConES/blob/master/rspace/rspace/docs/images/pycones.jpg">
</a></h6>
<br>
<h6 align="center">
Made with :heart: in <a href="https://www.google.com/search?q=almeria&espv=2&biw=1217&bih=585&sa=X#tbm=isch&q=almeria+movies">Almería</a>, Spain.</h6>


[license-svg]: https://img.shields.io/badge/license-MIT-blue.svg
[license-url]: https://opensource.org/licenses/MIT

## :snake: Python o como mejorar la vida de un administrador de sistemas
[![][license-svg]][license-url]

Código base que ilustrará la charla [_Python o como mejorar la vida de un administrador de sistemas_](http://2016.es.pycon.org/es/schedule/python-o-como-mejorar-la-vida-de-un-administrador/) en la [PyConES Almería 2016](http://2016.es.pycon.org/).

### ¿Sobre que hablaremos?

Compararemos dos aplicaciones *gemelas* escritas en `Bash` y `Python` cuyo código está contenido en este mismo `repo`.

Las funcionalidades de estas utilidades *demo* son:

- [x] Consultar el espacio disponible en un `FS` (local o remoto)
- [x] Consultar es las tablas mas *pesadas* de un servidor `mysql` (local o remoto)
- [ ] Enviar un informe vía mail.

Prestaremos atención especial a los siguientes puntos:

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

- Gestion del interfaces.
- raw ssh vs paramiko
- Flexibilidad (raise).

#### Connexion contra BBDD

- `HERE-DOCS` vs Python `driver`

Y si aún tenemos más ganas (y tiempo :stuck_out_tongue_winking_eye:), comentaremos alguno de los :snake: *superpowers*, gracias a sus extraordinarias *Batteries included*:

- Gestión de archivos de configuración.
- `Docstrings` + `Sphinx`
- Reusabilidad (`__name__ == “__main__"`).
- Distribución y packaging (`setup.py`).
- Webapp (`Flask`)

### Contacta conmigo

Mis perfiles online están [**aquí**](https://klashxx.github.io/about), no te cortes ... :godmode:

<center><h6 align="center">
[![][pycones-img]][pycones-url]
<br>*Made with* :heart: *in* [*Almería*](https://www.google.com/search?q=almeria&espv=2&biw=1217&bih=585&sa=X#tbm=isch&q=almeria+movies)*, Spain.*
</h6></center>


[license-svg]: https://img.shields.io/badge/license-MIT-blue.svg
[license-url]: https://opensource.org/licenses/MIT

[pycones-img]: https://github.com/klashxx/PyConES/blob/master/rspace/rspace/docs/images/pycones.jpg
[pycones-url]: http://2016.es.pycon.org/es/schedule/python-o-como-mejorar-la-vida-de-un-administrador/

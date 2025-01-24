# Set up
## Python version: 3.10.9

### Setup Virtual Environment
python -m venv env
### Activate the venv before running
source env/bin/activate

### Install requirements
pip install -r requirements.txt

#### Uninstall
pip uninstall -r requirements.txt -y

### Static Files not found fix
http://127.0.0.1:8080/_nicegui/2.10.1/static/nicegui.css not found
http://127.0.0.1:8080/_nicegui/2.10.1/static/fonts.css not found
http://127.0.0.1:8080/_nicegui/2.10.1/static/socket.io.min.js not found
http://127.0.0.1:8080/_nicegui/2.10.1/static/tailwindcss.min.js not found
http://127.0.0.1:8080/_nicegui/2.10.1/static/quasar.prod.css not found
http://127.0.0.1:8080/_nicegui/2.10.1/static/es-module-shims.js not found
http://127.0.0.1:8080/_nicegui/2.10.1/static/vue.global.prod.js not found
http://127.0.0.1:8080/_nicegui/2.10.1/static/quasar.umd.prod.js not found
http://127.0.0.1:8080/_nicegui/2.10.1/static/nicegui.js not found
http://127.0.0.1:8080/_nicegui/2.10.1/static/lang/en-US.umd.prod.js not found
http://127.0.0.1:8080/_nicegui/2.10.1/static/socket.io.min.js not found
http://127.0.0.1:8080/_nicegui/2.10.1/static/tailwindcss.min.js not found
http://127.0.0.1:8080/_nicegui/2.10.1/static/vue.global.prod.js not found
http://127.0.0.1:8080/_nicegui/2.10.1/static/quasar.umd.prod.js not found
http://127.0.0.1:8080/_nicegui/2.10.1/static/nicegui.js not found
http://127.0.0.1:8080/_nicegui/2.10.1/static/lang/en-US.umd.prod.js not found
http://127.0.0.1:8080/_nicegui/2.10.1/static/favicon.ico not found

env/lib/python3.13/site-packages/nicegui/nicegui.py

#### Replace
static_files = CacheControlledStaticFiles(
    directory=(Path(__file__).parent / 'static').resolve(),
    follow_symlink=False,
)

follow_symlink=True
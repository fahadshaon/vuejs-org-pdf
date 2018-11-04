import os

import click
import dotenv

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
cli = click.Group(name='vuejs-doc-pdf', help="Build pdf of vue.js guides", context_settings=CONTEXT_SETTINGS)


def project_relative_path(*args):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), *args)


base = project_relative_path()
os.environ['PROJECT_PATH'] = base

dotenv.load_dotenv(project_relative_path('.env'))
vue_js_path = os.environ.get('VUEJS_ORG_PATH')

if not vue_js_path or not os.path.exists(vue_js_path):
    raise ValueError('VUEJS_ORG_PATH not found')

html_path = os.path.join(vue_js_path, 'public', 'v2', 'guide')
md_path = os.path.join(vue_js_path, 'src', 'v2', 'guide')

dist_path = project_relative_path('build', 'dist')


# Bash placeholders for help generation

@cli.command(
    name='init',
    help='Initialize the project'
)
def cmd_init():
    pass


@cli.command(
    name='install_wkhtmltopdf',
    help='Install wkhtmltopdf with qt patch'
)
def cmd_install_wkhtmltopdf():
    pass

import uuid
import click
from prom_finagle_exporter.handler import falcon_app
from prom_finagle_exporter.discovery import register_consul


@click.group(help='')
def cli():
    pass


@click.command()
@click.option('-s', '--service', help='service name', required=True, type=str)
@click.option('-u', '--url', help='url to collect from', required=True, type=str)
@click.option('-p', '--port', help='', default=9191, type=int)
@click.option('-c', '--consul-host', help='', type=str)
@click.option('-e', '--exclude', help='exclude metrics named', multiple=True)
def start(service, url, port, consul_host, exclude):
    service_id = 'finagle-exporter-'.format(uuid.uuid4().hex)
    if consul_host:
        register_consul(consul_host, port, service_id=service_id)

    falcon_app(url, service, port=port, exclude=list(exclude))


cli.add_command(start)


if __name__ == '__main__':
    cli()

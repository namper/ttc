# -*- coding: UTF-8 -*-
import click
from independent import show_times, live_bus
from independent import closest_stop_runner


@click.group(chain=True)
@click.pass_context
def cli(ctx, **kwargs):
    return True


@cli.command(name='time')
@click.option('--stop_id', '-s', help='გაჩერების საიდენტიპიკაციო კოდი')
def show_times_cli(stop_id: int) -> None:
    show_times(stop_id=stop_id)


@cli.command(name='live')
@click.option('--bus_id', '-b', help='ავტობუსის ნომერი')
def live_bus_cli(bus_id: int) -> None:
    live_bus(bus_id=bus_id)


@cli.command(name='main')
@click.option('--bus_id', '-b', help='ავტობუსის ნომერი')
def main_func(bus_id: int) -> None:
    live_bus(bus_id=bus_id)
    closest_stop_runner(bus_id=bus_id)


if __name__ == '__main__':
    cli(obj={})

#!/usr/bin/env python3
from __future__ import annotations

import logging
from pathlib import Path

import click

from myhelpers.dummy import longest_common_prefix
from myhelpers.primitives.logging import setup_logging

root_dir = Path(__file__).resolve().parents[1]
logger = logging.getLogger("main")


@click.group()
def program():
    pass


@program.command()
@click.argument('fst', metavar='STRING')
@click.argument('snd', metavar='STRING')
def lcp(fst, snd):
    """
    Computes the longest common prefix of both STRING's.
    """
    result = longest_common_prefix(fst, snd)
    print(result)


@program.command()
@click.option('--log-config', type=click.Path(exists=True, dir_okay=False))
def daemon(log_config):
    """
    Computes the longest common prefix of both STRING's.
    """
    setup_logging(config_file=log_config)
    logger.info("Start daemon...")
    logger.info("Stop daemon...")


program()

#  Copyright (c) 2015-2018 Cisco Systems, Inc.
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to
#  deal in the Software without restriction, including without limitation the
#  rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
#  sell copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#  FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#  DEALINGS IN THE SOFTWARE.
"""Test Command Module."""

import logging
import os

import click

from molecule import util
from molecule.api import drivers
from molecule.command import base
from molecule.config import DEFAULT_DRIVER

LOG = logging.getLogger(__name__)
MOLECULE_PARALLEL = os.environ.get("MOLECULE_PARALLEL", False)
MOLECULE_PLATFORM_NAME = os.environ.get("MOLECULE_PLATFORM_NAME", None)


class Test(base.Base):
    """
    Test Command Class.

    .. program:: molecule test

    .. option:: molecule test

        Target the default scenario.

    .. program:: molecule test --scenario-name foo

    .. option:: molecule test --scenario-name foo

        Targeting a specific scenario.

    .. program:: molecule test --all

    .. option:: molecule test --all

        Target all scenarios.

    .. option:: molecule test -- -vvv --tags foo,bar

        Providing additional command line arguments to the `ansible-playbook`
        command.  Use this option with care, as there is no sanitation or
        validation of input.  Options passed on the CLI are combined with options
        provided in provisioner's `options` section of `molecule.yml`.

    .. program:: molecule test --destroy=always

    .. option:: molecule test --destroy=always

        Always destroy instances at the conclusion of a Molecule run.

    .. option:: molecule test --destroy=never

        Never destroy instances at the conclusion of a Molecule run.

    .. program:: molecule --debug test

    .. option:: molecule --debug test

        Executing with `debug`.

    .. program:: molecule --base-config base.yml test

    .. option:: molecule --base-config base.yml test

        Executing with a `base-config`.

    .. program:: molecule --env-file foo.yml test

    .. option:: molecule --env-file foo.yml test

        Load an env file to read variables from when rendering
        molecule.yml.

    .. program:: molecule test --parallel

    .. option:: molecule test --parallel

       Run in parallelizable mode.
    """

    def execute(self, action_args=None):
        """
        Execute the actions necessary to perform a `molecule test` and \
        returns None.

        :return: None
        """


@base.click_command_ex()
@click.pass_context
@click.option(
    "--scenario-name",
    "-s",
    default=base.MOLECULE_DEFAULT_SCENARIO_NAME,
    help=f"Name of the scenario to target. ({base.MOLECULE_DEFAULT_SCENARIO_NAME})",
)
@click.option(
    "--platform-name",
    "-p",
    default=MOLECULE_PLATFORM_NAME,
    help="Name of the platform to target only. Default is None",
)
@click.option(
    "--driver-name",
    "-d",
    type=click.Choice([str(s) for s in drivers()]),
    help=f"Name of driver to use. ({DEFAULT_DRIVER})",
)
@click.option(
    "--all/--no-all",
    "__all",
    default=False,
    help="Test all scenarios. Default is False.",
)
@click.option(
    "--destroy",
    type=click.Choice(["always", "never"]),
    default="always",
    help=("The destroy strategy used at the conclusion of a " "Molecule run (always)."),
)
@click.option(
    "--parallel/--no-parallel",
    default=MOLECULE_PARALLEL,
    help="Enable or disable parallel mode. Default is disabled.",
)
@click.argument("ansible_args", nargs=-1, type=click.UNPROCESSED)
def test(
    ctx,
    scenario_name,
    driver_name,
    __all,
    destroy,
    parallel,
    ansible_args,
    platform_name,
):  # pragma: no cover
    """Test (dependency, cleanup, destroy, syntax, create, prepare, converge, idempotence, side_effect, verify, cleanup, destroy)."""
    args = ctx.obj.get("args")
    subcommand = base._get_subcommand(__name__)
    command_args = {
        "parallel": parallel,
        "destroy": destroy,
        "subcommand": subcommand,
        "driver_name": driver_name,
        "platform_name": platform_name,
    }

    if __all:
        scenario_name = None

    if parallel:
        util.validate_parallel_cmd_args(command_args)

    base.execute_cmdline_scenarios(scenario_name, args, command_args, ansible_args)

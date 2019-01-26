#!/usr/bin/env python3

import os
from requests import Session
from colorama import init, Fore
import click
import clipboard
from dotenv import load_dotenv, find_dotenv


def bool_input(msg, default=False):
    ans = ""
    if default:
        ans = input(f"{msg}: [Y/n]: ")
        if ans.lower() == "n":
            return False
        return True
    else:
        ans = input(f"{msg}: [y/N]: ")
        if ans.lower() == "y":
            return True
        return False


@click.command()
@click.option(
    "--token",
    "-t",
    default=lambda: os.environ.get("GITHUB_TOKEN"),
    show_default="GITHUB_TOKEN",
    help="Token to use for accessing Github",
)
@click.option("--copy", "-c", is_flag=True, default=False, help="Copy URI to clipboard")
@click.option("--html/--ssh", default=False, help="Print HTML of SSH URI")
@click.option("--private/--public", default=False, help="Make a private or public repo")
@click.argument("names", required=False, nargs=-1)
def create_repo(names, private, html, copy, token):
    if len(names) > 1 and copy:
        click.echo("URLs will be printed as multiple repo names were given")
        copy = False

    gh = Session()
    gh.headers.update({"Authorization": f"token {token}"})
    for name in names:
        resp = gh.post(
            "https://api.github.com/user/repos", json={"name": name, "private": private}
        )

        init()
        if not resp.ok:
            click.echo(Fore.RED + f"Failed to create {name}: {resp.status_code} - {resp.content.decode('utf-8')}")
        else:
            uri = resp.json()["ssh_url"]
            if html:
                uri = resp.json()["html_url"]
            if copy:
                clipboard.copy(uri)
            else:
                click.echo(uri)


if __name__ == "__main__":
    load_dotenv(find_dotenv())
    create_repo()

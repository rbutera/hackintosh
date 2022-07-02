#!/usr/bin/env python3
import os
from glob import glob
from pathlib import Path
from typing import Optional

import click

cwd = os.getcwd()
local_efi = Path(f"{cwd}/EFI")


class Log:
    def info(self, msg):
        return click.echo(click.style(msg, fg="blue"))

    def warn(self, msg):
        return click.echo(click.style(msg, fg="yellow"))

    def error(self, msg):
        return click.echo(click.style(msg, fg="red", bold="true"))

    def log(self, msg):
        return click.echo(click.style(msg))

    def success(self, msg):
        return click.secho(msg, fg="green", bold="true")

    def verbose(self, msg):
        return click.echo(click.style(msg, fg="black"))


log = Log()


def sign_local(target: Optional[Path] = None):
    target_dir = Path(target) if target is not None else local_efi
    log.info(f"Signing all binaries in '{target_dir}', recursively")
    num_signed = 0
    for file in glob(f"{target_dir}/**/*.efi", recursive=True):
        num_signed += sign_path_if_exists(file)
    if num_signed > 0:
        log.success(f"sign_local: finished signing {str(num_signed)} file(s)")
    else:
        log.warn("did not find any files to sign!")
    return num_signed


"""
    returns the number of files signed (usually 1) or 0 if no files were found
"""


def sign_path_if_exists(path: str | Path) -> int:
    target = Path(path)
    if target.exists():
        log.verbose(f"found {target}. will sign:")
        os.system(f"sudo sbctl sign {target}")
        return 1
    else:
        log.verbose(f"could not find {target}")
    return 0


def sign_linux():
    log.info("signing Linux directory")
    to_sign = [
        "/boot/vmlinuz-linux",
        "/efi/EFI/BOOT/BOOTX64.EFI",
        "/efi/EFI/BOOT/BOOTx64.efi",
        "/efi/EFI/Linux/linux-linux.efi",
        "/efi/EFI/arch/fwupdx64.efi",
        "/efi/EFI/systemd/systemd-bootx64.efi" "/boot/efi/EFI/BOOT/BOOTX64.EFI",
        "/boot/efi/EFI/BOOT/BOOTx64.efi",
        "/boot/efi/EFI/Linux/linux-linux.efi",
        "/boot/efi/EFI/arch/fwupdx64.efi",
        "/boot/efi/EFI/systemd/systemd-bootx64.efi",
    ]
    num_signed = 0
    for path in to_sign:
        num_signed += sign_path_if_exists(path)
    if num_signed > 0:
        log.success(f"sign_linux: finished signing {str(num_signed)} files")
    return num_signed


def do_import_keys():
    log.info(f"do_import: Copying {cwd}/secureboot to /usr/share")
    if Path(f"{cwd}/secureboot").exists():
        log.log("found secureboot directory, copying")
        os.system(f"sudo rsync -rvz {cwd}/secureboot /usr/share/secureboot")
        return 0
    else:
        log.error(
            "Could not find local secureboot directory. Import it from your source system using the '--import' flag"
        )
        return 1


def do_export():
    log.info("do_export: Copying /usr/share/secureboot to " + str(cwd))
    os.system(f"rm -rf {cwd}/secureboot")
    os.system(f"sudo rsync -rvz /usr/share/secureboot {cwd}/secureboot")
    log.success("finished copying /usr/share/secureboot")


@click.command()
@click.option("--local/--skip-local", default=True, help="Sign local EFI directory")
@click.option(
    "-L", "--linux/--skip-linux", default=True, help="(re)sign local linux efi files"
)
@click.option(
    "-T",
    "--target",
    type="string",
    help="Target directory to recursively search for EFI files to sign",
)
@click.option(
    "-E",
    "--export/--no-export",
    default=False,
    help="If set to true, copies /usr/share/secureboot to current working directory for backup purposes",
)
@click.option(
    "-I",
    "--import/--no-import",
    "import_keys",
    default=False,
    help="Import data from local secureboot copy to /usr/share/secureboot prior to signing",
)
def sign(
    local: bool = True,
    linux: bool = True,
    target: str = None,
    export: bool = False,
    import_keys: bool = False,
):
    click.echo(click.style("auto_sbctl starting. options selected:", bold=True))
    messages = []
    if import_keys:
        messages = messages.append(f"import keys from {cwd}/secureboot/keys")

    if linux:
        messages = messages.append("sign linux boot EFI")
    if local:
        target_dir = target if target is not None else cwd
        messages = messages.append(f"sign files in {target_dir}")
    if export_keys:
        messages = messages.append(f"export /usr/share/secureboot to {cwd}/secureboot")

    num_signed = 0
    if import_keys:
        do_import_keys()

    os.system("sudo sbctl status")

    if local:
        num_signed += sign_local(Path(target) if target is not None else None)
    if linux:
        num_signed += sign_linux()

    if num_signed > 0:
        log.success("autosbctl: finished signing " + str(num_signed) + " files.")
        os.system("sudo sbctl verify")

    if export:
        do_export()


if __name__ == "__main__":
    sign()

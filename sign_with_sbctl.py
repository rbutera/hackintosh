#!/usr/bin/env python3

from glob import glob
import os
from pathlib import Path


def sign_with_sbctl():
    cwd = os.getcwd()
    target_dir = Path(f"{cwd}/EFI_sbctl_signed")
    # os.system(f'sudo sbctl sign {target_dir}/BOOT/BOOTx64.efi')
    for file in glob(f"{target_dir}/**/*.efi", recursive=True):
        print(f"signing {file}")
        os.system(f"sudo sbctl sign {file}")
    print("finished signing!")


if __name__ == "__main__":
    sign_with_sbctl()

"""
Copyright 2017 Hermann Krumrey

This file is part of server-admin.

toktokkie is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

toktokkie is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with toktokkie.  If not, see <http://www.gnu.org/licenses/>.
"""

import os
import argparse
from typing import Dict
from subprocess import Popen
from datetime import datetime
from server_admin.sudo import quit_if_not_sudo, change_ownership

"""
This module contains functions that help manage gitlab backups
"""


def parse_backup_args() -> Dict[str, str]:
    """
    Parses the arguments for the gitlab-backup script
    :return: The arguments provided via the CLI
    """

    parser = argparse.ArgumentParser()
    parser.add_argument("--destination",
                        default="/var/opt/gitlab/backups",
                        help="Destination of the backup file")
    parser.add_argument("--backup-path",
                        default="/var/opt/gitlab/backups",
                        help="The backup directory as specified in gitlab.rb")
    parser.add_argument("--user",
                        default="root",
                        help="The user that should own the backup file. "
                             "Defaults to root.")
    args = parser.parse_args()

    return {
        "destination": args.destination,
        "backup_path": args.backup_path,
        "user": args.user
    }


def execute_gitlab_rake_backup():
    """
    Executes the gitlab-rake command that creates a backup file in the
    location specified in the gitlab.rb config file
    :return: None
    """
    Popen(["gitlab-rake", "gitlab:backup:create"]).wait()


def create_backup():
    """
    Performs the Gitlab Backup. Requires sudo permissions.
    After creating and renaming the backup, changes the ownership to the
    specified user
    :return: None
    """
    quit_if_not_sudo()
    args = parse_backup_args()

    before = os.listdir(args["backup_path"])
    execute_gitlab_rake_backup()
    after = os.listdir(args["backup_path"])

    backups = []
    for x in after:
        if x not in before:
            backups.append(x)

    if len(backups) != 1:
        print("More than one backup generated. Aborting.")

    source_path = os.path.join(args["backup_path"], backups[0])
    dest_filename = datetime.today().strftime("%Y-%M-%d-%H-%m-%S_gitlab.tar")
    dest_path = os.path.join(args["destination"], dest_filename)

    if not os.path.exists(args["destination"]):
        os.makedirs(args["destination"])

    os.rename(source_path, dest_path)
    change_ownership(dest_path, args["user"])
    print(
        "Backup completed.\n"
        "Rights transferred to " + args["user"] + ".\n"
        "Location:" + args["destination"]
    )

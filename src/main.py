#!/usr/bin/env python3

import argparse
import asyncio
import datetime
import logging

from environment import Environment
from file_updater import FileUpdater
from plants.committer import Committer
from plants.external import allow_external_calls

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")
logger: logging.Logger = logging.getLogger(__name__)


async def main() -> None:
    now = datetime.datetime.now()
    parser = argparse.ArgumentParser(description="Snapshot Spotify playlists")
    parser.add_argument(
        "--auto-register",
        help="Automatically register select playlists",
        action="store_true",
    )
    parser.add_argument(
        "--commit-and-push",
        help="Commit and push updated playlists upstream",
        action="store_true",
    )
    args = parser.parse_args()
    auto_register = bool(args.auto_register)
    commit_and_push = bool(args.commit_and_push)

    if commit_and_push:
        playlists_dir = Environment.get_prod_playlists_dir()
    else:
        playlists_dir = Environment.get_test_playlists_dir()

    await FileUpdater.update_files(
        now=now,
        playlists_dir=playlists_dir,
        auto_register=auto_register,
        update_readme=commit_and_push,
    )
    if commit_and_push:
        Committer.commit_and_push_if_github_actions()

    logger.info("Done")


if __name__ == "__main__":
    allow_external_calls()
    asyncio.run(main())

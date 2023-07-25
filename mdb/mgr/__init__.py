"""Datamase management utility."""

from mdb.mgr.argparse import get_args
from mdb.mgr.functions import find_recods


__all__ = ["main"]


def main() -> None:
    """Runs the crmgr."""

    args = get_args()

    if args.action == "find":
        for record in find_recods(args):
            print(*record.to_csv(), sep="\t")

import argparse

from scanreq.scanner import scan


def main():
    parser = argparse.ArgumentParser(description="Scan for unused Python packages.")
    parser.add_argument(
        "-r",
        "--requirements",
        type=str,
        default="requirements.txt",
        help="Path to the requirements.txt file to read packages from.",
    )
    parser.add_argument(
        "-p",
        "--path",
        type=str,
        default=".",
        help="Project path to scan for unused packages (default: current directory).",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default=None,
        help="Path to the output file where unused packages will be saved.",
    )
    parser.add_argument(
        "-i",
        "--ignored-packages",
        type=str,
        default=None,
        help="Comma separated list of package names to be ignored.",
    )
    args = parser.parse_args()

    scan(
        requirement_file=args.requirements,
        project_path=args.path,
        output_path=args.output,
        ignored_packages=(
            args.ignored_packages.split(",") if args.ignored_packages else []
        ),
    )


if __name__ == "__main__":
    main()

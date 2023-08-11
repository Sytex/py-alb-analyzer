import csv
import sys
import time
import argparse
from dataclasses import asdict

from py_alb_analyzer.albparser import parse_log_entry
from py_alb_analyzer.log_entry import LogEntry


def main():
    # Argument parsing
    parser = argparse.ArgumentParser(description="Process ALB logs.")
    parser.add_argument("--filter", type=str, help="Filter logs based on field=value")
    args = parser.parse_args()

    filter_field = None
    filter_value = None

    if args.filter:
        filter_field, filter_value = args.filter.split("=")
        if filter_field not in LogEntry.__annotations__.keys():
            print(
                f"Invalid filter field '{filter_field}', valid fields are {LogEntry.__annotations__.keys()}"
            )
            sys.exit(1)

    start_time = time.time()
    line_count = 0

    with open("output.csv", "w", newline="") as csvfile:
        fieldnames = LogEntry.__annotations__.keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for line in sys.stdin:
            log_entry = parse_log_entry(line)

            line_count += 1
            elapsed_time = time.time() - start_time
            lines_per_second = line_count / elapsed_time

            if line_count % 1000 == 0:
                print(
                    f"\rProcessed {line_count} lines at {lines_per_second:.2f} lines/sec",
                    end="",
                    file=sys.stderr,
                    flush=True,
                )

            if filter_field and str(getattr(log_entry, filter_field)) != filter_value:
                continue

            writer.writerow(asdict(log_entry))



        print(
            f"\nTotal lines processed: {line_count} in {elapsed_time:.2f} seconds",
            file=sys.stderr,
        )


if __name__ == "__main__":
    main()

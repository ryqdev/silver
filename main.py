import argparse

from src.bt import run

def main() -> None:
    parser = argparse.ArgumentParser(description='silver')
    parser.add_argument('--symbol', type=str, required=True, help='Stock symbol to fetch')
    parser.add_argument('--start', type=str, required=True, help='Start date in UTC time')
    parser.add_argument('--end', type=str, required=True, help='End date in UTC time')
    parser.add_argument('--kline', type=str, required=True, help='K line')
    args = parser.parse_args()

    run(args.symbol, args.start, args.end, args.kline)

if __name__ == "__main__":
    main()


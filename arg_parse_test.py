import argparse

def update_consul(key,value) -> None:
    #CODE TO UPDATE CONSUL
    print(f'{key} - {value:.2f}')

def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='Argument testing.')
    parser.add_argument("-k", "--consul_key", required=True,
                        help="Enter consul key after client, e.g. 'aws_mini_prod1/input'")
    parser.add_argument("-v", "--consul_value", type=int,
                        help="Leave empty for if only checking values of selected clients")
    return parser


def main() -> None:
    parser = init_argparse()
    args = parser.parse_args()
    update_consul(args.consul_key, args.consul_value)

if __name__ == "__main__":
    main()
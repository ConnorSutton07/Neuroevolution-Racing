from driver import Driver
import argparse

def main(debug: bool = False):
    driver = Driver(debug=debug)
    driver.run()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Neuroevolution Racing")
    parser.add_argument("--debug", type=bool, nargs='?',
                        const=True, default=False, 
                        help="Display racetrack generation components")
    args = parser.parse_args()
    main(debug=args.debug)
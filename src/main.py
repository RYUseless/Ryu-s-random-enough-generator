import mishmash.cpu_thread as ryuCPUpokus
import mishmash.numToAsciiConvert
from pynput.mouse import Controller


def main():
    print("Ryu's entropy-enough random string sequence generator -- in progress right now")
    ryuCPUpokus.ThreadExperiment().run()

    # result = 874741608 ** (1504175 % 1612) % 174073 ** 1612


if __name__ == '__main__':
    main()

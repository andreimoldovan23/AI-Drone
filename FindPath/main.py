from UI.UI import *


def main():
    m = Map()
    d = Drone()
    c = Controller(m, d)
    u = UI(c)
    u.run()


if __name__ == "__main__":
    main()

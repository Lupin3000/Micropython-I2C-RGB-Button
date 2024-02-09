from micropython import const
from lib.DFRobot_RGB_Button_I2C import DFRobot_RGB_Button_I2C
from time import sleep_ms


SDA_PIN = const(21)
SCL_PIN = const(22)
DELAY = const(50)


def setup(button) -> None:
    """
    Verify button available and ready to use
    :param button: instance of DFRobot_RGB_Button
    :return: None
    """
    while not button.begin():
        print('Try button initialization')
        sleep_ms(500)

    print('Button initialized')


if __name__ == '__main__':
    btn = DFRobot_RGB_Button_I2C(sda=SDA_PIN, scl=SCL_PIN)
    setup(button=btn)

    while True:
        if btn.get_button_status():
            btn.set_rgb_color(r=100, g=100, b=100)
        else:
            btn.set_rgb_color(r=0, g=0, b=0)

        sleep_ms(DELAY)

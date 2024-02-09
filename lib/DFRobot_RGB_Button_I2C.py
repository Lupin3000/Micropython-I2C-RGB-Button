from micropython import const
from machine import I2C, Pin


BUTTON_DEFAULT_I2C_ADDR = const(0x2A)
BUTTON_PART_ID = const(0x43DF)
BUTTON_PID_MSB_REG = const(0x09)
BUTTON_COLOR_REG = const(0x01)
BUTTON_BUTTON_SIGNAL_REG = const(0x04)


class DFRobot_RGB_Button_I2C:
    """
    MicroPython class for communication with the RGB LED button from DFRobot via I2C
    """

    def __init__(self, sda, scl, i2c_addr=BUTTON_DEFAULT_I2C_ADDR, i2c_bus=0):
        """
        Initialize the DFRobot_RGB_Button communication
        :param sda: I2C SDA Pin
        :param scl: I2C SCL Pin
        :param i2c_addr: I2C address
        :param i2c_bus: I2C bus number
        """
        self._addr = i2c_addr

        try:
            self._i2c = I2C(i2c_bus, sda=Pin(sda), scl=Pin(scl), freq=100000)
        except Exception as err:
            print(f'Could not initialize i2c! bus: {i2c_bus}, sda: {sda}, scl: {scl}, error: {err}')

    def _write_reg(self, reg, data) -> None:
        """
        Write data to the I2C register
        :param reg: register address
        :param data: data to write
        :return: None
        """
        if isinstance(data, int):
            data = [data]

        try:
            self._i2c.writeto_mem(self._addr, reg, bytearray(data))
        except Exception as err:
            print(f'Write issue: {err}')

    def _read_reg(self, reg, length) -> bytes:
        """
        Reads data from the I2C register
        :param reg: I2C register address
        :param length: number of bytes to read
        :return: bytes
        """
        try:
            result = self._i2c.readfrom_mem(self._addr, reg, length)
        except Exception as err:
            print(f'Read issue: {err}')
            result = [0, 0]

        return result

    def begin(self) -> bool:
        """
        Initialise the button
        :return: bool
        """
        chip_id = self._read_reg(BUTTON_PID_MSB_REG, 2)

        if BUTTON_PART_ID != ((chip_id[0] << 8) | chip_id[1]):
            return False
        else:
            return True

    def set_rgb_color(self, r: int, g: int, b: int) -> None:
        """
        Sets the RGB color of the button
        :param r: value between 0 and 255
        :param g: value between 0 and 255
        :param b: value between 0 and 255
        :return: None
        """
        rgb_buf = [0] * 3

        if 0 <= int(r) <= 255 and 0 <= int(g) <= 255 and 0 <= int():
            rgb_buf[0] = int(r)
            rgb_buf[1] = int(g)
            rgb_buf[2] = int(b)

        self._write_reg(BUTTON_COLOR_REG, rgb_buf)

    def get_button_status(self) -> bool:
        """
        Returns button status (True if pressed, False if not pressed)
        :return: bool
        """
        return bool(self._read_reg(BUTTON_BUTTON_SIGNAL_REG, 1)[0])

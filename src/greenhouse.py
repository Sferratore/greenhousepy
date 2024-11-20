
try:
    import RPi.GPIO as GPIO
    import board
    import adafruit_seesaw.seesaw as seesaw
except:
    import mock.GPIO as GPIO
    import mock.board as board
    import mock.seesaw as seesaw


class Greenhouse:

    SPRINKLER_PIN = 12
    PHOTO_PIN = 16
    LED_PIN = 18

    def __init__(self):
        i2c = board.I2C()
        self.soil_moisture_sensor = seesaw.Seesaw(i2c, addr=0x36)

        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup(self.SPRINKLER_PIN, GPIO.OUT)
        GPIO.setup(self.PHOTO_PIN, GPIO.IN)
        GPIO.setup(self.LED_PIN, GPIO.OUT)
        self.sprinkler_on = False
        self.red_light_on = False

    def measure_soil_moisture(self) -> int:
        moisture_level = self.soil_moisture_sensor.moisture_read()
        if moisture_level < 300 or moisture_level > 500:
            raise GreenhouseError("Soil moisture level is out of range!")
        return moisture_level

    def turn_on_sprinkler(self) -> None:
        GPIO.output(self.SPRINKLER_PIN, True)
        self.sprinkler_on = True

    def turn_off_sprinkler(self) -> None:
        GPIO.output(self.SPRINKLER_PIN, False)
        self.sprinkler_on = False

    def manage_sprinkler(self) -> None:
        moisture_level = self.measure_soil_moisture()
        if moisture_level < 375 and not self.sprinkler_on:
            self.turn_on_sprinkler()
        elif moisture_level > 425 and self.sprinkler_on:
            self.turn_off_sprinkler()

    def check_too_much_light(self) -> bool:
        # Return True if there is too much light, which is indicated by the photoresistor being False
        return not GPIO.input(self.PHOTO_PIN)

    def manage_lightbulb(self) -> None:
        if GPIO.input(self.PHOTO_PIN):
            GPIO.output(self.LED_PIN, True)
            self.red_light_on = True
        else:
            GPIO.output(self.LED_PIN, False)
            self.red_light_on = False


class GreenhouseError(Exception):
    pass


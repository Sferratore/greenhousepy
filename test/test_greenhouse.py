from unittest import TestCase
from unittest.mock import patch
from unittest.mock import Mock

from mock import GPIO
from mock.seesaw import Seesaw
from src.greenhouse import Greenhouse, GreenhouseError


class TestGreenhouse(TestCase):

    @patch.object(Seesaw, "moisture_read")
    def test_measure_soil_moisture(self, mock_moisture_sensor: Mock):
        mock_moisture_sensor.return_value = 300
        gh = Greenhouse()
        self.assertEqual(300, gh.measure_soil_moisture())

    @patch.object(Seesaw, "moisture_read")
    def test_measure_soil_moisture_below_range(self, mock_moisture_sensor: Mock):
        mock_moisture_sensor.return_value = 299
        gh = Greenhouse()
        self.assertRaises(GreenhouseError, gh.measure_soil_moisture)

    @patch.object(Seesaw, "moisture_read")
    def test_measure_soil_moisture_above_range(self, mock_moisture_sensor: Mock):
        mock_moisture_sensor.return_value = 501
        gh = Greenhouse()
        self.assertRaises(GreenhouseError, gh.measure_soil_moisture)

    @patch.object(GPIO, "output")
    def test_turn_on_sprinkler(self, mock_sprinkler: Mock):
        system = Greenhouse()
        system.turn_on_sprinkler()
        mock_sprinkler.assert_called_once_with(system.SPRINKLER_PIN, True)
        self.assertTrue(system.sprinkler_on)

    @patch.object(GPIO, "output")
    def test_turn_off_sprinkler(self, mock_sprinkler: Mock):
        system = Greenhouse()
        system.turn_off_sprinkler()
        mock_sprinkler.assert_called_once_with(system.SPRINKLER_PIN, False)
        self.assertTrue(not system.sprinkler_on)

    @patch.object(Seesaw, "moisture_read")
    @patch.object(GPIO, "output")
    def test_sprinkler_should_be_turned_on_when_below_375(self, mock_sprinkler: Mock, mock_moisture_sensor: Mock):
        mock_moisture_sensor.return_value = 374
        system = Greenhouse()
        system.manage_sprinkler()
        mock_sprinkler.assert_called_once_with(system.SPRINKLER_PIN, True)
        self.assertTrue(system.sprinkler_on)

    @patch.object(Seesaw, "moisture_read")
    @patch.object(GPIO, "output")
    def test_sprinkler_should_be_turned_off_when_above_425(self, mock_sprinkler: Mock, mock_moisture_sensor: Mock):
        mock_moisture_sensor.return_value = 426
        system = Greenhouse()
        system.sprinkler_on = True
        system.manage_sprinkler()
        mock_sprinkler.assert_called_once_with(system.SPRINKLER_PIN, False)
        self.assertTrue(not system.sprinkler_on)

    @patch.object(GPIO, "input")
    def test_check_too_much_light(self, mock_photoresistor: Mock):
        mock_photoresistor.return_value = False
        system = Greenhouse()
        self.assertTrue(system.check_too_much_light())

    @patch.object(GPIO, "output")
    @patch.object(GPIO, "input")
    def test_lightbulb_should_be_turned_on(self, mock_photoresistor: Mock, mock_red_light: Mock):
        mock_photoresistor.return_value = True
        system = Greenhouse()
        system.manage_lightbulb()
        mock_red_light.assert_called_once_with(system.LED_PIN, True)
        self.assertTrue(system.red_light_on)

    @patch.object(GPIO, "output")
    @patch.object(GPIO, "input")
    def test_lightbulb_should_be_turned_off(self, mock_photoresistor: Mock, mock_red_light: Mock):
        mock_photoresistor.return_value = False
        system = Greenhouse()
        system.manage_lightbulb()
        mock_red_light.assert_called_once_with(system.LED_PIN, False)
        self.assertTrue(system.red_light_on)

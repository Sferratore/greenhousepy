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
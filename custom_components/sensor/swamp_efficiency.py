import voluptuous as vol

from homeassistant.components.switch import PLATFORM_SCHEMA, SwitchDevice

from homeassistant.const import TEMP_FAHRENHEIT
from homeassistant.helpers.entity import Entity

import homeassistant.helpers.config_validation as cv

CONF_HUMIDITY_SENSOR = 'humidity_sensor'
CONF_TEMPERATURE_SENSOR = 'temperature_sensor'

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_HUMIDITY_SENSOR): cv.string,
    vol.Required(CONF_TEMPERATURE_SENSOR): cv.string
})

EFFICIENCY_HUMIDITY = [2, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80]
EFFICIENCY_TEMPERATURE = [75, 80, 85, 90, 95, 100, 105, 110, 115, 120, 125]

EFFICIENCY_CHART = [
  [54, 55, 57, 58, 59, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72],
  [57, 58, 60, 62, 63, 64, 66, 67, 68, 69, 71, 72, 73, 74, 76, 76, 77],
  [61, 62, 63, 65, 67, 68, 70, 71, 72, 73, 74, 75, 76, 77, 79, 81],
  [64, 65, 67, 69, 70, 72, 74, 76, 77, 78, 79, 81, 82, 83, 84, 86],
  [67, 68, 70, 72, 74, 76, 78, 79, 81, 82, 84, 85, 87],
  [69, 71, 73, 76, 78, 80, 82, 83, 85, 87, 88],
  [72, 74, 77, 79, 81, 84, 86, 88, 89],
  [75, 77, 80, 83, 85, 87, 90, 92],
  [78, 80, 83, 86, 89, 91, 94],
  [81, 83, 86, 90, 93, 95],
  [83, 86, 90, 93, 96]
]

def setup_platform(hass, config, add_devices, discovery_info=None):
    """Setup the sensor platform."""
    
    humidity_sensor = config.get(CONF_HUMIDITY_SENSOR)
    temperature_sensor = config.get(CONF_TEMPERATURE_SENSOR)

    add_devices([SwampEfficiencySensor(hass, humidity_sensor, temperature_sensor)])

class SwampEfficiencySensor(Entity):
    """Representation of a Sensor."""

    def __init__(self, hass, humidity_sensor, temperature_sensor):
        """Initialize the sensor."""
        self._state = None
        self._hass = hass
        self._humidity_sensor = humidity_sensor
        self._temperature_sensor = temperature_sensor

    @property
    def name(self):
        """Return the name of the sensor."""
        return 'Swamp Efficiency Temperature'

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return TEMP_FAHRENHEIT

    def update(self):
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """
        temp = float(self._hass.states.get(self._temperature_sensor).state)
        humidity = float(self._hass.states.get(self._humidity_sensor).state)

        temp_index = 0
        humidity_index = 0
        for t in range(0, len(EFFICIENCY_TEMPERATURE)):
            if temp < EFFICIENCY_TEMPERATURE[t]:
                temp_index = t
                break

        for t in range(0, len(EFFICIENCY_HUMIDITY)):                             
            if humidity < EFFICIENCY_HUMIDITY[t]:
                humidity_index = t
                break

        best_temp = EFFICIENCY_CHART[temp_index][humidity_index]

        self._state = best_temp

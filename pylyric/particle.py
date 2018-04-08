import tortilla


class Particle:
    """Reprents a Photon Particle device."""

    def __init__(self, auth_token, device_id):
        self.auth_token = auth_token
        self.api = tortilla.wrap(f'https://api.particle.io/v1/devices/{device_id}')

    @property
    def internal_temperture(self):
        result = self.api.temperature.get(params={'access_token': self.auth_token})
        return float(result['result'])

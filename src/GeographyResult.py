import logging
from dataclasses import dataclass


logger = logging.getLogger(__name__)

@dataclass
class GeographyResult:
    '''Temporary class to store geography results from API calls.
    Stored values will be used to update database's table udoZipCodes.

    Attributes:

    '''
    zip_code: str
    city: str | None=None
    state: str | None=None
    latitude: float | None=None
    longitude: float | None=None

    def __post_init__(self):
        '''Validation logic.'''
        if self.zip_code is None:
            raise ValueError('Zip code is missing (cannot be NULL)')
        elif len(self.zip_code) != 5:
            raise ValueError(f'Zip code length is invalid (should be 5):\n"{self.zip_code}"')

        if self.city is not None and len(self.city) > 100:
            raise ValueError(f'City length is too long (cannot exceed 100):\n"{self.city}"')

        if self.state is not None and len(self.state) > 2:
            raise ValueError(f'State length is too long (cannot exceed 2):\n"{self.state}"')

        if self.latitude is not None and not -90 <= self.latitude <= 90:
            raise ValueError(f'Latitude value is invalid (should be between -90 and 90):\n"{self.latitude}"')

        if self.longitude is not None and not -180 <= self.longitude <= 180:
            raise ValueError(f'Latitude value is invalid (should be between -180 and 180):\n"{self.longitude}"')

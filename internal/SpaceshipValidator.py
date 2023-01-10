from pydantic import BaseModel, validator, root_validator, Field
from internal.Spaceship import Spaceship
from typing import Optional


class SpaceshipValidator(BaseModel):
    alignment: Spaceship.Alignment
    name: str
    vessel_class: Spaceship.Vessel_class
    length: float
    size: int
    armed: Optional[bool]
    officers: list[dict[str, str]]

    @validator('length', check_fields=False)
    def length_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('Length must be positive')
        return v

    @validator('length', check_fields=False)
    def length_must_be_adjusted_to_vessel_class(cls, v, values):
        length_ranges: list[list[int]] = [[80, 250], [300, 600], [500, 1000], [800, 2000], [1000, 4000],
                                          [5000, 20000], [80, 20000]]
        if round(v) not in range(length_ranges[values['vessel_class'].value][0],
                                 length_ranges[values['vessel_class'].value][1]):
            raise ValueError('Length must be adjusted to vessel class')
        return v

    @validator('size', check_fields=False)
    def size_must_be_positive(cls, v, values):
        if v <= 0:
            raise ValueError('Size must be positive')
        return v

    @validator('size', check_fields=False)
    def size_must_be_adjusted_to_vessel_class(cls, v, values):
        size_ranges: list[list[int]] = [[4, 10], [10, 15], [15, 30], [50, 80], [120, 250], [300, 500], [4, 500]]
        if v not in range(size_ranges[values['vessel_class'].value][0], size_ranges[values['vessel_class'].value][1]):
            raise ValueError('Size must be adjusted to vessel class')
        return v

    @validator('armed', check_fields=False)
    def armed_must_be_adjusted_to_vessel_class(cls, v, values):
        armed_ranges: list[bool] = [True, True, True, True, True, False, True]
        if v is True and armed_ranges[values['vessel_class'].value] is False:
            raise ValueError('Armed must be adjusted to vessel class')
        return v

    @validator('alignment', check_fields=False)
    def alignment_must_be_adjusted_to_vessel_class(cls, v, values):
        hostile_ranges: list[bool] = [True, True, False, True, False, True, True]
        if v == 'enemy' and hostile_ranges[values['vessel_class'].value] is False:
            raise ValueError('Alignment must be adjusted to vessel class')
        return v

    # @validator('officers', check_fields=False)
    # def officers_must_be_list(cls, v):
    #     if not isinstance(v, list) and not v.empty():
    #         raise ValueError('Officers must be a list')
    #     return v

    class Config:
        validate_assignment = True
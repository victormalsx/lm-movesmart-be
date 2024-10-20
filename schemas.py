from typing import Optional, List
from enum import Enum
from pydantic import BaseModel, field_validator


class VehicleTypesEnum(str, Enum):
    SUV_AWD = "SUV_AWD"
    HATCHBACK = "HATCHBACK"
    TRUCK = "TRUCK"
    UNDEFINED = "UNDEFINED"


class FleetCompositionSchema(BaseModel):
    total_vehicles: int
    type_of_vehicle: VehicleTypesEnum = VehicleTypesEnum.UNDEFINED


class CurrentStatusSchemaIn(BaseModel):
    number_of_customers: int
    number_of_vehicles: int
    average_reservations_per_customer: Optional[float]
    average_reservations_duration: Optional[float]
    average_maintenance_hours: Optional[float]
    fleet_composition: Optional[List[FleetCompositionSchema]]

    @field_validator("average_reservations_per_customer")
    @classmethod
    def set_average_reservations_per_customer(cls, v: float):
        return 10.88 if v == 0 else v

    @field_validator("average_reservations_duration")
    @classmethod
    def set_average_reservations_duration(cls, v: float):
        return 8.99 if v == 0 else v

    @field_validator("average_maintenance_hours")
    @classmethod
    def set_average_maintenance_hours(cls, v: float):
        return 209.9 if v == 0 else v


class CurrentStatusSchemaOut(BaseModel):
    total_cost_of_operation: float
    current_utilization: float
    optimized_number_of_vehicles: int
    difference_in_total_costs: float
    fleet_composition: Optional[List[FleetCompositionSchema]]
    new_utilization: float

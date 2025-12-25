from math import floor
from typing import List, Any, Mapping


def get_utilization(
    number_of_customers: int,
    number_of_vehicles: int,
    average_reservations_per_customer: float = 10.88,
    average_reservations_duration: float = 8.99,
    average_maintenance_hours: float = 209.9,
) -> float:
    return (
        (
            number_of_customers
            * average_reservations_per_customer
            * average_reservations_duration
        )
        / (number_of_vehicles * (720 - average_maintenance_hours))
    ) * 100


def total_cost_of_operation_per_month(
    fleet_composition: List[Any] = None, number_of_vehicles: int = 0
) -> float:

    cost_mapping: Mapping[str, float] = {
        "SUV_AWD": 9626.92,
        "HATCHBACK": 7138.46,
        "TRUCK": 10936.36,
        "UNDEFINED": 11810.56,
    }

    if not fleet_composition:
        return number_of_vehicles * (11810.56 / 12)
    total_cost: float = 0
    for vehicle_type in fleet_composition:
        total_cost = total_cost + (
            (
                (
                    vehicle_type["total_vehicles"]
                    if vehicle_type["type_of_vehicle"] != "UNDEFINED"
                    else number_of_vehicles
                )
                * (cost_mapping[vehicle_type["type_of_vehicle"]] / 12)
            )
        )

    return total_cost


def maximize_utilization_by_number_of_vehicles(
    number_of_customers: int,
    average_reservations_per_customer: float = 10.88,
    average_reservations_duration: float = 8.99,
    average_maintenance_hours: float = 209.9,
    current_utilization: int = 51,
) -> int:
    vehicles = (
        100
        * (
            number_of_customers
            * average_reservations_per_customer
            * average_reservations_duration
        )
    ) / (current_utilization * (720 - average_maintenance_hours))
    return floor(vehicles)


def get_vehicle_type_ratio(
    fleet_composition: List[Any], number_of_vehicles: int
) -> List[Any]:
    fleet_composition_with_ratio: List[Any] = []
    for vehicle_type in fleet_composition:
        fleet_composition_with_ratio.append(
            {
                **vehicle_type,
                "ratio": (vehicle_type["total_vehicles"] / number_of_vehicles),
            }
        )
    return fleet_composition_with_ratio


def balance_fleet_composition(
    fleet_composition_with_ratio: List[Any], number_of_vehicles: int
) -> List[Any]:
    fleet_composition_balanced: List[Any] = []
    for vehicle_type in fleet_composition_with_ratio:
        fleet_composition_balanced.append(
            {
                "total_vehicles": round(vehicle_type["ratio"] * number_of_vehicles),
                "type_of_vehicle": vehicle_type["type_of_vehicle"],
            }
        )
    return fleet_composition_balanced

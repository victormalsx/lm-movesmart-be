from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

import calculations
import schemas

app = FastAPI(
    title="movesmart",
    openapi_url="/api/v1/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[str(origin) for origin in ["*"]],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/api/v1/utilization", response_model=schemas.CurrentStatusSchemaOut)
async def calculate_current_status(
    *, current_status: schemas.CurrentStatusSchemaIn
) -> schemas.CurrentStatusSchemaOut:

    current_utilization = calculations.get_utilization(
        **current_status.model_dump(exclude={"fleet_composition"})
    )

    fleet_composition_with_ratio = calculations.get_vehicle_type_ratio(
        **current_status.model_dump(
            include={"fleet_composition", "number_of_vehicles"},
        )
    )

    total_cost_of_operations = calculations.total_cost_of_operation_per_month(
        **current_status.model_dump(
            include={"fleet_composition", "number_of_vehicles"},
        )
    )

    optimized_number_of_vehicles = (
        calculations.maximize_utilization_by_number_of_vehicles(
            **current_status.model_dump(
                exclude={"fleet_composition", "number_of_vehicles"}
            ),
        )
    )

    fleet_composition_balanced = calculations.balance_fleet_composition(
        fleet_composition_with_ratio, optimized_number_of_vehicles
    )

    difference_in_total_costs = calculations.total_cost_of_operation_per_month(
        fleet_composition_balanced,
        number_of_vehicles=optimized_number_of_vehicles,
    )

    new_utilization = calculations.get_utilization(
        number_of_customers=current_status.number_of_customers,
        number_of_vehicles=optimized_number_of_vehicles
    )

    return schemas.CurrentStatusSchemaOut(
        total_cost_of_operation=total_cost_of_operations,
        current_utilization=current_utilization,
        optimized_number_of_vehicles=optimized_number_of_vehicles,
        difference_in_total_costs=difference_in_total_costs,
        fleet_composition=fleet_composition_balanced,
        new_utilization=new_utilization
    )

import pytest
from car_rental_rate import process_rental_fleet, check_fleet_telematics

# Example test case:
def test_single_economy_rental():
    rentals = [
        {
            "is_confirmed": True,
            "vehicle_type": "economy",
            "driver_age": 30,
            "days": 2,
            "trip_segments": [100]
        }
    ]
    result = process_rental_fleet(rentals, 10.0)
    assert result["total_revenue"] == 110.0
    assert result["status"] == "STANDARD"

# TODO: Add test cases to achieve 90-100% on both Line and Branch coverage!

# Additional tests for line coverage

def test_invalid_rental_inputs():
    with pytest.raises(ValueError):
        process_rental_fleet("invalid", 10.0)

    with pytest.raises(ValueError):
        process_rental_fleet([], -1.0)


def test_unconfirmed_and_invalid_day_rentals():
    rentals = [
        {"is_confirmed": False, "days": 2},
        {"is_confirmed": True, "days": 0},
        {"is_confirmed": True, "days": -2}
    ]

    result = process_rental_fleet(rentals, 10.0)

    assert result["total_revenue"] == 0.0
    assert result["status"] == "EMPTY_BATCH"


def test_all_vehicle_types_and_mileage_charges():
    rentals = [
        {
            "is_confirmed": True,
            "vehicle_type": "luxury",
            "driver_age": 30,
            "days": 2,
            "trip_segments": [100, 350]
        },
        {
            "is_confirmed": True,
            "vehicle_type": "suv",
            "driver_age": 24,
            "days": 1,
            "trip_segments": [301, 50]
        },
        {
            "is_confirmed": True,
            "vehicle_type": "economy",
            "driver_age": 25,
            "days": 1,
            "trip_segments": []
        }
    ]

    result = process_rental_fleet(rentals, 10.0)

    assert result["total_revenue"] == 690.4
    assert result["status"] == "STANDARD"


def test_young_luxury_driver_with_long_trip():
    rentals = [
        {
            "is_confirmed": True,
            "vehicle_type": "luxury",
            "driver_age": 20,
            "days": 2,
            "trip_segments": [350, 100]
        }
    ]

    result = process_rental_fleet(rentals, 10.0)

    assert result["total_revenue"] == 600.0
    assert result["status"] == "STANDARD"


def test_negative_mileage_segment():
    rentals = [
        {
            "is_confirmed": True,
            "vehicle_type": "economy",
            "driver_age": 25,
            "days": 1,
            "trip_segments": [-10, 50]
        }
    ]

    result = process_rental_fleet(rentals, 10.0)

    assert result["total_revenue"] == 60.0
    assert result["status"] == "STANDARD"


def test_high_risk_audit_status():
    rentals = [
        {"is_confirmed": True, "days": 0},
        {"is_confirmed": True, "days": 0},
        {"is_confirmed": True, "days": 0},
        {"is_confirmed": True, "days": 0},
        {"is_confirmed": True, "days": 0}
    ]

    result = process_rental_fleet(rentals, 10.0)

    assert result["total_revenue"] == 0.0
    assert result["status"] == "HIGH_RISK_AUDIT"


def test_telematics_no_data():
    assert check_fleet_telematics([]) == "NO_DATA"


def test_telematics_safe():
    logs = [
        [60, 80, 105, 90],
        [70, 95, 100]
    ]

    assert check_fleet_telematics(logs) == "SAFE"


def test_telematics_consecutive_speeding():
    logs = [
        [80, 105, 110, 70]
    ]

    assert check_fleet_telematics(logs) == "GROUND_VEHICLE"

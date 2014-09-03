from .healthgraph import create_healthgraph_object


def convert_tcx_to_healthgraph(tcx, notes=None, detect_pauses=False):
    path_points = map(gps_point_to_path_point, tcx.gps_points)
    healthgraph_heartrates = map(
        heartrate_measurement_to_healthgraph_heartrate,
        tcx.heartrate_measurements)

    healthgraph_object = create_healthgraph_object(
        start_time=tcx.start_time,
        duration=tcx.duration,
        activity_type=tcx.activity_type,
        activity_path=path_points,
        secondary_type=tcx.secondary_type,
        heartrates=healthgraph_heartrates,
        equipment=tcx.equipment,
        total_distance=tcx.total_distance,
        notes=notes,
        detect_pauses=detect_pauses)

    return healthgraph_object


def gps_point_to_path_point(tcx_gps_info):
    """
    timestamps are stored as absolute epoch times
    type is ommitted here and it is expected that the correct values will be
    inserted when creating the path list
    """
    return {
        'timestamp': tcx_gps_info.time,
        'latitude': tcx_gps_info.latitude,
        'longitude': tcx_gps_info.longitude,
        'altitude': tcx_gps_info.altitude,
    }


def heartrate_measurement_to_healthgraph_heartrate(tcx_heartrate_info):
    """
    timestamps are stored as absolute epoch times
    """
    return {
        'timestamp': tcx_heartrate_info.time,
        'heart_rate': tcx_heartrate_info.bpm,
    }

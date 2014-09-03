from time import (
    gmtime,
    strftime,
)

_RK_TIMESTAMP_FORMAT = '%a, %d %b %Y %H:%M:%S'


def create_healthgraph_object(start_time, duration, activity_type,
                              activity_path=None, secondary_type=None,
                              heartrates=None, equipment=None,
                              total_distance=None, notes=None,
                              detect_pauses=False):
    """
    :param start_time: Activity start time in seconds since epoch
    """
    start_time_str = strftime(_RK_TIMESTAMP_FORMAT, gmtime(start_time))

    healthgraph_object = {
        'type': activity_type,
        'start_time': start_time_str,
        'duration': duration,
        'detect_pauses': detect_pauses,
    }

    if total_distance is not None:
        healthgraph_object['total_distance'] = total_distance

    if activity_path:
        _validate_and_adjust_activity_path(activity_path, start_time)
        healthgraph_object['path'] = activity_path

    if heartrates:
        _adjust_heartrates(heartrates, start_time)
        healthgraph_object['heart_rate'] = heartrates

    if secondary_type is not None:
        healthgraph_object['secondary_type'] = secondary_type

    if equipment is not None:
        healthgraph_object['equipment'] = equipment

    if notes is not None:
        healthgraph_object['notes'] = notes

    return healthgraph_object


def _validate_and_adjust_activity_path(path, activity_start_time):
    if len(path) < 2:
        raise ValueError('The activity path must have at least two points')

    for point in path:
        point['type'] = 'manual'
        _adjust_timestamp(activity_start_time, point)
    path[0]['type'] = 'start'
    path[-1]['type'] = 'end'


def _adjust_heartrates(heartrates, activity_start_time):
    for heartrate in heartrates:
        _adjust_timestamp(activity_start_time, heartrate)


def _adjust_timestamp(activity_start_time, element):
    element['timestamp'] -= activity_start_time

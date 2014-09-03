import time
import unittest

from tcx2rk.healthgraph import create_healthgraph_object, _adjust_timestamp, _validate_and_adjust_activity_path


class TestHealthgraph(unittest.TestCase):

    def test_create_healthgraph_object(self):
        start_time = 1393881454
        offset = 3
        duration = 3600.5
        activity_path = [
            {'timestamp': start_time},
            {'timestamp': start_time + offset},
        ]
        activity_type = 'Running'

        expected_output = {
            'type': activity_type,
            'start_time': 'Mon, 03 Mar 2014 21:17:34',
            'duration': duration,
            'detect_pauses': False,
            'path': [
                {
                    'timestamp': 0,
                    'type': 'start',
                },
                {
                    'timestamp': offset,
                    'type': 'end',
                },
            ]
        }

        actual_output = create_healthgraph_object(
            start_time=start_time,
            duration=duration,
            activity_type=activity_type,
            activity_path=activity_path)

        self.assertEqual(expected_output, actual_output)

    def test_create_healthgraph_object_with_optionals(self):
        start_time = 1393881454
        offset = 3
        total_distance = 11.4
        duration = 3600.5
        notes = 'A delightful run!'
        activity_path = [
            {'timestamp': start_time},
            {'timestamp': start_time + offset},
        ]
        activity_type = 'Running'
        detect_pauses = True

        expected_output = {
            'type': activity_type,
            'start_time': 'Mon, 03 Mar 2014 21:17:34',
            'total_distance': total_distance,
            'duration': duration,
            'detect_pauses': detect_pauses,
            'notes': notes,
            'path': [
                {
                    'timestamp': 0,
                    'type': 'start',
                },
                {
                    'timestamp': offset,
                    'type': 'end',
                },
            ]
        }

        actual_output = create_healthgraph_object(
            start_time=start_time,
            duration=duration,
            activity_type=activity_type,
            activity_path=activity_path,
            notes=notes,
            total_distance=total_distance,
            detect_pauses=detect_pauses)
            
        self.assertEqual(expected_output, actual_output)

    def test_validate_and_adjust_activity_path(self):
        start_time = time.time()
        interval = 3
        path = [
            {'timestamp': start_time},
            {'timestamp': start_time + interval},
            {'timestamp': start_time + 2 * interval},
        ]
        expected_path = [
            {
                'timestamp': 0,
                'type': 'start',
            },
            {
                'timestamp': interval,
                'type': 'manual',
            },
            {
                'timestamp': interval * 2,
                'type': 'end',
            },
        ]

        _validate_and_adjust_activity_path(path, start_time)
        self.assertEqual(expected_path, path)

    def test_validate_and_adjust_activity_path_invalid(self):
        start_time = time.time()
        with self.assertRaises(ValueError):
            _validate_and_adjust_activity_path([], start_time)

    def test_adjust_timestamp(self):
        start_time = time.time()
        offset = 3
        elem = {
            'timestamp': start_time + offset,
            'foo': 'bar',
        }
        _adjust_timestamp(start_time, elem)

        self.assertEqual({
            'timestamp': offset,
            'foo': 'bar',
        }, elem)

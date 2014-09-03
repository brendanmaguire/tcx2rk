import unittest

from tcx2rk.tcx import Trackpoint, GPSInfo, TrackpointError, HeartrateInfo


class _TestTCXBase(unittest.TestCase):

    def setUp(self):
        self._latitude = 3.3
        self._longitude = -20.2
        self._altitude = 58.2

        self._bpm = 102

        self._expected_time = 1390729219.0

        self._trackpoint_dict = {
            'Time': '2014-01-26T09:40:19Z',
            'Position': {
                'LatitudeDegrees': str(self._latitude),
                'LongitudeDegrees': str(self._longitude),
            },
            'AltitudeMeters': self._altitude,
            'DistanceMeters': '0',
            'HeartRateBpm': {
                'Value': str(self._bpm),
            },
            'Extensions': {
                'TPX': {
                    'Speed': '0',
                },
            }
        }


class TestTCXTrackpoint(_TestTCXBase):

    def test_trackpoint_attributes(self):
        trackpoint = Trackpoint(self._trackpoint_dict)

        self.assertEqual(trackpoint.time, self._expected_time)

        # Just try one of each detail
        self.assertEqual(trackpoint.gps_info.latitude, self._latitude)
        self.assertEqual(trackpoint.heartrate_info.bpm, self._bpm)

    def test_trackpoint_without_gps_info(self):
        del self._trackpoint_dict['Position']
        trackpoint = Trackpoint(self._trackpoint_dict)

        self.assertIsNone(trackpoint.gps_info)
        self.assertIsNotNone(trackpoint.heartrate_info)

    def test_trackpoint_without_heartrate_info(self):
        del self._trackpoint_dict['HeartRateBpm']
        trackpoint = Trackpoint(self._trackpoint_dict)

        self.assertIsNone(trackpoint.heartrate_info)
        self.assertIsNotNone(trackpoint.gps_info)


class TestGPSInfo(_TestTCXBase):

    def test_gps_info_attributes(self):
        gps_info = GPSInfo(self._trackpoint_dict)

        self.assertEqual(gps_info.latitude, self._latitude)
        self.assertEqual(gps_info.longitude, self._longitude)
        self.assertEqual(gps_info.altitude, self._altitude)
        self.assertEqual(gps_info.time, self._expected_time)

    def test_gps_info_incomplete(self):
        del self._trackpoint_dict['Position']
        with self.assertRaises(TrackpointError):
            GPSInfo(self._trackpoint_dict)


class TestHeartrateInfo(_TestTCXBase):

    def test_heartrate_info_attributes(self):
        heartrate_info = HeartrateInfo(self._trackpoint_dict)

        self.assertEqual(heartrate_info.bpm, self._bpm)
        self.assertEqual(heartrate_info.time, self._expected_time)

    def test_heartrate_info_incomplete(self):
        del self._trackpoint_dict['HeartRateBpm']
        with self.assertRaises(TrackpointError):
            HeartrateInfo(self._trackpoint_dict)

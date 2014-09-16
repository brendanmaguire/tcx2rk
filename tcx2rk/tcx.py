import copy
import logging
import time
import xmltodict

from itertools import chain

_TCX_TIME_FORMAT = '%Y-%m-%dT%H:%M:%SZ'

logger = logging.getLogger(__name__)


class TrackpointError(ValueError):

    def __init__(self, message, tcx_element=None):
        Exception.__init__(self, message)
        self.tcx_element = tcx_element


class Activity(object):

    def __init__(self, activity_dict):
        self._activity_dict = activity_dict

        self._activity_type = activity_dict['@Sport']

        self._laps = activity_dict['Lap']
        if not isinstance(self._laps, list):
            # If there is only one lap in the activity it is not in a list. We
            # need to wrap it up in a list in that case
            self._laps = [self._laps]

        self._trackpoints = self._get_activity_trackpoints(self._laps)

        self._total_distance = sum(map(self._get_lap_distance, self._laps))
        self._duration = sum(map(self._get_lap_duration, self._laps))

    @property
    def activity_type(self):
        return self._activity_type

    @property
    def total_distance(self):
        return self._total_distance

    @property
    def secondary_type(self):
        #TODO: If this has an entry in tcx files then lets check for it
        return None
    @property
    def equipment(self):
        #TODO: If this has an entry in tcx files then lets check for it
        return None

    @property
    def start_time(self):
        return tcx_timestamp_to_epoch(self._laps[0]['@StartTime'])

    @property
    def duration(self):
        return self._duration

    @property
    def gps_points(self):
        return tuple(
            trackpoint.gps_info for trackpoint in self._trackpoints
            if trackpoint.gps_info is not None)

    @property
    def heartrate_measurements(self):
        return tuple(
            trackpoint.heartrate_info for trackpoint in self._trackpoints
            if trackpoint.heartrate_info is not None)

    @classmethod
    def _get_activity_trackpoints(cls, laps):
        trackpoint_dicts = chain.from_iterable(
            map(cls._get_lap_trackpoints, laps))
        return tuple(Trackpoint(tp) for tp in trackpoint_dicts)

    @staticmethod
    def _get_lap_trackpoints(lap):
        trackpoints = lap['Track']['Trackpoint']
        return trackpoints if isinstance(trackpoints, list) else [trackpoints]

    @staticmethod
    def _get_lap_distance(lap):
        return float(lap['DistanceMeters'])

    @staticmethod
    def _get_lap_duration(lap):
        return float(lap['TotalTimeSeconds'])


class _TrackpointBase(object):

    def __init__(self, trackpoint_dict):
        try:
            self._time = tcx_timestamp_to_epoch(trackpoint_dict['Time'])
        except KeyError as e:
            raise TrackpointError(
                'Could not extract %s from trackpoint' % e, trackpoint_dict)

    @property
    def time(self):
        """
        Returns trackpoint time in number of seconds since epoch
        """
        return self._time

    @property
    def trackpoint_dict(self):
        return copy.deepcopy(self._trackpoint_dict)


class Trackpoint(_TrackpointBase):
    """
    Immutable object to give access to trackpoint data
    """

    def __init__(self, trackpoint_dict):
        super(Trackpoint, self).__init__(trackpoint_dict)

        try:
            self._gps_info = GPSInfo(trackpoint_dict)
        except TrackpointError as e:
            logger.info('gps info skipped. %s : %s', e, e.tcx_element)
            self._gps_info = None

        try:
            self._heartrate_info = HeartrateInfo(trackpoint_dict)
        except TrackpointError as e:
            logger.debug('heartrate info skipped. %s : %s', e, e.tcx_element)
            self._heartrate_info = None

    @property
    def gps_info(self):
        return self._gps_info

    @property
    def heartrate_info(self):
        return self._heartrate_info


class GPSInfo(_TrackpointBase):

    def __init__(self, trackpoint_dict):
        super(GPSInfo, self).__init__(trackpoint_dict)
        try:
            self._altitude = float(trackpoint_dict['AltitudeMeters'])
            self._longitude = float(
                trackpoint_dict['Position']['LongitudeDegrees'])
            self._latitude = float(
                trackpoint_dict['Position']['LatitudeDegrees'])
        except KeyError as e:
            raise TrackpointError(
                'Could not extract %s from trackpoint' % e, trackpoint_dict)

    @property
    def latitude(self):
        return self._latitude

    @property
    def longitude(self):
        return self._longitude

    @property
    def altitude(self):
        return self._altitude


class HeartrateInfo(_TrackpointBase):

    def __init__(self, trackpoint_dict):
        super(HeartrateInfo, self).__init__(trackpoint_dict)
        try:
            self._bpm = int(trackpoint_dict['HeartRateBpm']['Value'])
        except KeyError as e:
            raise TrackpointError(
                'Could not extract %s from trackpoint' % e, trackpoint_dict)

    @property
    def bpm(self):
        return self._bpm


def get_tcx_activity_from_file(filepath):
    return get_activity(read_tcx_file(filepath))


def get_activity(tcx):
    return Activity(tcx['TrainingCenterDatabase']['Activities']['Activity'])


def read_tcx_file(filepath):
    """
    Reads in a tcx file and returns a dict
    """
    return xmltodict.parse(open(filepath, 'r'))


def tcx_timestamp_to_epoch(time_str):
    time_tuple = time.strptime(time_str, _TCX_TIME_FORMAT)
    return time.mktime(time_tuple)

import streamlink
<<<<<<< HEAD
import traceback
=======
>>>>>>> 8404bd861c94c828ff67ba64164dcda46d62fcb4
from streamlink import (
    StreamError,
    StreamlinkError,
    PluginError,
    NoPluginError,
    NoStreamsError,
)
<<<<<<< HEAD
=======

>>>>>>> 8404bd861c94c828ff67ba64164dcda46d62fcb4

class Fetch:
    """
    Gets data from host, filters it and returns streams
    (query: str, quality: str,list,tuple)
    """

    def __init__(self, query, quality):
        self.query = query
        if not quality:
            quality = "best"
        if "," in quality:
            self.qualities = quality.split(",")
        else:
            self.qualities = [quality]

    def get_streams(self):
        """
        Get data streams and resolutions
        Returns: (links, resolution), Error string
        """
        try:
            # FIXME has issues if a channel is hosting another on Twitch
            links = streamlink.streams(self.query)
            res = list(links.keys())
            return (links, res)
<<<<<<< HEAD
        except Exception as e:
            print('got error at getstreams')
            print(traceback.format_exec())
            return e

    def filtered_streams(self):
        stream = self.get_streams()
        print(stream)
        try:
            streams, resolutions = stream
            if not streams:
                raise ValueError
            res_str = ",".join(resolutions)
        except (ValueError, TypeError):
            print('got error at filtered')
            return stream
=======
        except Exception:
            # returnes exceptions raised by streamlink
            raise

    def filtered_streams(self):
        """
        Filter streams according to specified quality.
        Default quality: best
        Returns: {quality: stream_url}
        """
        try:
            payload = self.get_streams()
            streams, resolutions = payload
            if not streams:
                raise ValueError
            res_str = ",".join(resolutions)
        except PluginError as pe:
            return str(pe)
        except ValueError:
            return f"Could not get the link, Streamlink couldn't read {self.query}"
        except TypeError:
            return payload
>>>>>>> 8404bd861c94c828ff67ba64164dcda46d62fcb4

        # TODO: find a more elegant solution to deal with 'best' and 'worst'
        if "best" in self.qualities:
            self.qualities = [
                resolutions[-3:-2][0] if i == "best" else i for i in self.qualities
            ]
        if "worst" in self.qualities:
            self.qualities = [
                resolutions[1::-2][0] if i == "worst" else i for i in self.qualities
            ]

        for q in self.qualities:
            if q not in resolutions:
                return f"Invalid quality {q}. Available qualities are: {res_str}"
        return {quality: streams[quality].url for quality in self.qualities}

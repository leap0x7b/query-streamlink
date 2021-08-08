import streamlink
import traceback
from streamlink import (
    StreamError,
    StreamlinkError,
    PluginError,
    NoPluginError,
    NoStreamsError,
)

class Fetch:
    """
        Gets data from host, filters it and returns streams
    """
    def __init__(self, query, quality="best"):
        self.query = query
        if not quality:
            quality = "best"
        if "," in quality:
            self.qualities = quality.split(",")
        else:
            self.qualities = [quality]

    def get_streams(self):
        try:
            # FIXME has issues if a channel is hosting another on Twitch
            links = streamlink.streams(self.query)
            print(links)
            res = list(links.keys())
            return (links, res)
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

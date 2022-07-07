"""

"""
import os
import io
import numpy as np


class GDFFixer:
    """
    The class GDFFixer can parse a GDF file and check whether the Event Table is corrupted in order to fix it.
    This is specific to the GDF files recorded with OpenViBE from version 3.0.0 to 3.3.0.
    """

    HEADER_SIZE_IDX = 184
    N_DATA_RECORDS_IDX = 236
    N_CHANNEL_IDX = 252
    FIXED_HEADER_SIZE = 256
    VARIABLE_HEADING_TO_SKIP = 216  # For each channel from Label to Pre-filtering info in variable header
    EVENT_SIZE = 6

    INT32 = '<i4'
    UINT32 = '<u4'
    INT64 = '<i8'
    UINT64 = '<u8'

    # OpenViBE saves all channels as float64
    CHANNEL_TYPE_CODE = 17
    CHANNEL_TYPE_BYTES = 8

    def __init__(self):
        pass

    def process_file(self, file_name):
        """
        Processes file to check for corruption and fix if needed. Process:
        1. Check format is GDF
        2. Check version is GDF v1
        3. Check for corruption
        4. Fix if file is corrupted

        Returns True if the file was corrupted and fixed
                False if the file didn't pass any of the points 1. to 3.
        """
        print("\n -- Processing : {}".format(file_name))
        intput_file = os.path.abspath(file_name)
        path, file_name = os.path.split(intput_file)

        name, ext = os.path.splitext(file_name)
        if ext.lower() != '.gdf':
            print(" ---- Expecting GDF files only. Extension '{}' is not supported".format(ext))
            return False
        output_file = os.path.abspath(os.path.join(path, name + "-fixed" + ext))

        with open(intput_file, 'rb') as fid:
            version_number = fid.read(8).decode()[4:]  # number from version (e.g. 'GDF 1.25')

            if float(version_number) != 1.25:
                print(" ---- Expecting GDF files from version 1.25. Current file is version {}".format(version_number))
                return False

            fid.seek(self.HEADER_SIZE_IDX)
            header_size = np.fromfile(fid, self.INT64, 1)[0]

            fid.seek(self.N_DATA_RECORDS_IDX)
            n_data_records = np.fromfile(fid, self.UINT64, 1)[0]

            fid.seek(self.N_CHANNEL_IDX)
            n_channels = np.fromfile(fid, self.UINT32, 1)[0]

            fid.seek(self.FIXED_HEADER_SIZE + self.VARIABLE_HEADING_TO_SKIP * n_channels)
            n_samples = np.fromfile(fid, self.INT32, n_channels)
            channel_types = np.fromfile(fid, self.UINT32, n_channels)

            for t in channel_types:
                if t != self.CHANNEL_TYPE_CODE:
                    print("---- Expected channel type for OpenViBE records is {}, but the file contains a channel of "
                          "type {}".format(self.CHANNEL_TYPE_CODE, t))
                    return False

            # Event table start index
            etp_index = header_size + int(n_data_records * np.sum(
                [self.CHANNEL_TYPE_BYTES * n_samples[i] for i in range(n_channels)]))
            fid.seek(etp_index)

            # Skip Event table mode and Sample rate
            fid.seek(4, 1)
            n_evts = np.fromfile(fid, self.UINT32, 1)[0]

            # Beginning of events list
            evts_start = fid.tell()
            evts_size = n_evts * self.EVENT_SIZE

            fid.seek(0, io.SEEK_END)
            total_size = fid.tell()

            # The bug we expect to fix is a difference of 4 bytes in the Event Table
            if total_size - (evts_start + evts_size) == 4:
                print(" ---- File detected as corrupted.")
                print(" ---- {} extras bytes were detected in the file. Correcting into new file".format(
                    total_size - evts_start - evts_size))

                fid.seek(0)
                raw = fid.read(evts_start)
                fid.seek(4, 1)  # skip the 4 extras bytes causing trouble
                raw += fid.read()  # read until end of file
                with open(output_file, "wb") as fod:
                    print(" ---- Writing corrected file to {}".format(output_file))
                    fod.write(raw)
                return True
            else:
                print(" ---- File not corrupted.")
                return False

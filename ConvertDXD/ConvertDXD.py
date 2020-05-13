# -*- coding: utf-8 -*-
"""
created on the 05th of February 2020
@author: Xavier Bouteiller
@mail: xavier.bouteiller@mpdata.fr

Nécessite:
- un dll fournit par dewesoft 'DWDataReaderLib64.dll'
- un script py 'DWDataReaderHeader.py'

"""




# def extract_dxd(file, rootdir = 'D:\\Python\data\\transcription_test', targetdir="D:\\Python\\script\\EssaiConversion\\M1", jetlag=1):
def extract_dxd(rootdir, file, jetlag, PackageDir):
    import os
    import argparse
    import pandas as pd
    import numpy as np
    import traceback
    # from DWDataReaderHeader import *
    # from ctypes import *
    from ConvertDXD.DWDataReaderHeader import ARRAY, ArgumentError, Array, BigEndianStructure, CDLL, CFUNCTYPE, DEFAULT_MODE, DOUBLE_SIZE, DWArrayInfo, DWCANPortData, DWChannel, DWChannelProps, DWChannelType, DWComplex, DWDataType, DWEvent, DWEventType, DWFileInfo, DWRaiseError, DWReducedValue, DWStatus, DWStoreType, DllCanUnloadNow, DllGetClassObject, Enum, FormatError, GetLastError, HRESULT, INT_SIZE, LibraryLoader, LittleEndianStructure, OleDLL, POINTER, PYFUNCTYPE, PyDLL, RTLD_GLOBAL, RTLD_LOCAL, SetPointerType, Structure, Union, WINFUNCTYPE, WinDLL, WinError, __builtins__, __cached__, __doc__, __file__, __loader__, __name__, __package__, __spec__, addressof, alignment, byref, c_bool, c_buffer, c_byte, c_char, c_char_p, c_double, c_float, c_int, c_int16, c_int32, c_int64, c_int8, c_long, c_longdouble, c_longlong, c_short, c_size_t, c_ssize_t, c_ubyte, c_uint, c_uint16, c_uint32, c_uint64, c_uint8, c_ulong, c_ulonglong, c_ushort, c_void_p, c_voidp, c_wchar, c_wchar_p, cast, cdll, create_string_buffer, create_unicode_buffer, get_errno, get_last_error, memmove, memset, oledll, pointer, py_object, pydll, pythonapi, resize, set_errno, set_last_error, sizeof, string_at, sys, windll, wintypes, wstring_at
    import _ctypes
    import logging
    import datetime
    import pytz
    from datetime import datetime, timedelta
    import pytz
    from shutil import copyfile

    rootfile = rootdir + '\\' + str(file)            ;
    logging.debug('rootfile is : '+str(rootfile))

    #%% script dewesoft
    # open data file
    logging.warning("##### ENDWITH .DXD T/F " + str(rootfile.endswith('.dxd')))

    try:
        if rootfile.endswith('.dxd'):
            logging.info('file is in dxd format : ' + str(os.path.split(rootfile)[-1]))

            #création d'une dll temporaire
            dst = PackageDir+'\\'+'ConvertDXD\\DWDataReaderLib64'+str(np.random.randint(1000000))+'.dll'
            logging.warning('new dll : ' + str(dst))
            copyfile(PackageDir+'\\'+'ConvertDXD\\DWDataReaderLib64.dll', dst)
            lib = cdll.LoadLibrary(dst)

            # init data reader
            if lib.DWInit() != DWStatus.DWSTAT_OK.value:
                DWRaiseError("DWDataReader: DWInit() failed")

            # get data reader version
            logging.info("DWDataReader version: " + str(lib.DWGetVersion()))

            # add additional data reader
            if lib.DWAddReader() != DWStatus.DWSTAT_OK.value:
                DWRaiseError("DWDataReader: DWAddReader() failed")

            # get number of open data readers
            num = c_int()
            if lib.DWGetNumReaders(byref(num)) != DWStatus.DWSTAT_OK.value:
                DWRaiseError("DWDataReader: DWGetNumReaders() failed")
            logging.info("Number of data readers: " + str(num.value))




            file_name = c_char_p(rootfile.encode())
            file_info = DWFileInfo(0, 0, 0)
            if lib.DWOpenDataFile(file_name, c_void_p(addressof(file_info))) != DWStatus.DWSTAT_OK.value:
                DWRaiseError("DWDataReader: DWOpenDataFile() failed")

            logging.debug("Sample rate:" +  str(file_info.sample_rate))
            logging.debug("Start store time:" + str(file_info.start_store_time))
            logging.debug("Duration:" + str(file_info.duration))

            rate = file_info.sample_rate
            duration = file_info.duration
            start_time = file_info.start_store_time
            epoch = datetime(1899, 12, 30, tzinfo=pytz.utc)
            epoch = pd.to_datetime(epoch)
    #        print(epoch)

            # get num channels
            num = lib.DWGetChannelListCount()
            if num == -1:
                DWRaiseError("DWDataReader: DWGetChannelListCount() failed")
            logging.warning("Number of channels : " + str(num))

            # get channel list
            ch_list = (DWChannel * num)()
            if lib.DWGetChannelList(byref(ch_list)) != DWStatus.DWSTAT_OK.value:
                DWRaiseError("DWDataReader: DWGetChannelList() failed")

            print("\n")

            #----------------------------------------------------------------------------------------------------------------
            # channel loop
            #----------------------------------------------------------------------------------------------------------------
            num = 8 #problem with variables > 8
            for i in range(0, num):
            # channel_list:
                if i ==0:

                    print("Name: %s" % ch_list[i].name)
                    name = ch_list[i].name.decode("utf-8")
            #                print("Unit: %s" % ch_list[i].unit)
            #                print("Description: %s" % ch_list[i].description)

                    # channel factors
                    idx = c_int(i)
                    ch_scale = c_double()
                    ch_offset = c_double()
                    if lib.DWGetChannelFactors(idx, byref(ch_scale), byref(ch_offset)) != DWStatus.DWSTAT_OK.value:
                        DWRaiseError("DWDataReader: DWGetChannelFactors() failed")



                    # channel type
                    max_len = c_int(INT_SIZE)
                    buff = create_string_buffer(max_len.value)
                    p_buff = cast(buff, POINTER(c_void_p))
                    if lib.DWGetChannelProps(idx, c_int(DWChannelProps.DW_CH_TYPE.value), p_buff, byref(max_len)) != DWStatus.DWSTAT_OK.value:
                        DWRaiseError("DWDataReader: DWGetChannelProps() failed")
                    ch_type = cast(p_buff, POINTER(c_int)).contents

                    if ch_type.value == DWChannelType.DW_CH_TYPE_SYNC.value:
                        print("Channel type: sync")
                    elif ch_type.value == DWChannelType.DW_CH_TYPE_ASYNC.value:
                        print("Channel type: async")
                    elif ch_type.value == DWChannelType.DW_CH_TYPE_SV.value:
                        print("Channel type: single value")
                    else:
                        print("Channel type: unknown")

                    # channel data typeacti
                    if lib.DWGetChannelProps(idx, c_int(DWChannelProps.DW_DATA_TYPE.value), p_buff, byref(max_len)) != DWStatus.DWSTAT_OK.value:
                        DWRaiseError("DWDataReader: DWGetChannelProps() failed")
                    data_type = cast(p_buff, POINTER(c_int)).contents
                    logging.debug("Data type:" + str(DWDataType(data_type.value).name))

                    # number of samples
                    dw_ch_index = c_int(ch_list[i].index)
                    sample_cnt = c_int()
                    sample_cnt = lib.DWGetScaledSamplesCount(dw_ch_index)
                    if sample_cnt < 0:
                        DWRaiseError("DWDataReader: DWGetScaledSamplesCount() failed")
                    logging.debug("Num. samples:" + str(sample_cnt))

                    # get actual data
                    data = create_string_buffer(DOUBLE_SIZE * sample_cnt * ch_list[i].array_size)
                    time_stamp = create_string_buffer(DOUBLE_SIZE * sample_cnt)
                    p_data = cast(data, POINTER(c_double))
                    p_time_stamp = cast(time_stamp, POINTER(c_double))
                    if lib.DWGetScaledSamples(dw_ch_index, c_int64(0), sample_cnt, p_data, p_time_stamp) != DWStatus.DWSTAT_OK.value:
                        DWRaiseError("DWDataReader: DWGetScaledSamplesCount() failed")

                    logging.warning('converting timestamp')

                    p_time_stamp_cor = [epoch + pd.to_timedelta(start_time, unit = 'd') +
                    pd.to_timedelta(jetlag, unit = 'h') + pd.to_timedelta(t, unit = 's')
                    for t in p_time_stamp[0:sample_cnt]]
                    df = pd.DataFrame({'Time':p_time_stamp_cor, name:p_data[0:sample_cnt]})
                    #print(df.dtypes)
                    df = df.set_index('Time')

                    name_prec = name
                    name_all = [name]

                elif i>0:
                    print("Name: %s" % ch_list[i].name)
                    name = ch_list[i].name.decode("utf-8")

                    if name in name_all:
                        logging.error("Duplicated col name: " + str(name))
                        name = name+str(np.random.randint(100000))

                    # channel factors
                    idx = c_int(i)
                    ch_scale = c_double()
                    ch_offset = c_double()
                    if lib.DWGetChannelFactors(idx, byref(ch_scale), byref(ch_offset)) != DWStatus.DWSTAT_OK.value:
                        DWRaiseError("DWDataReader: DWGetChannelFactors() failed")



                    # channel type
                    max_len = c_int(INT_SIZE)
                    buff = create_string_buffer(max_len.value)
                    p_buff = cast(buff, POINTER(c_void_p))
                    if lib.DWGetChannelProps(idx, c_int(DWChannelProps.DW_CH_TYPE.value), p_buff, byref(max_len)) != DWStatus.DWSTAT_OK.value:
                        DWRaiseError("DWDataReader: DWGetChannelProps() failed")
                    ch_type = cast(p_buff, POINTER(c_int)).contents

                    if ch_type.value == DWChannelType.DW_CH_TYPE_SYNC.value:
                        print("Channel type: sync")
                    elif ch_type.value == DWChannelType.DW_CH_TYPE_ASYNC.value:
                        print("Channel type: async")
                    elif ch_type.value == DWChannelType.DW_CH_TYPE_SV.value:
                        print("Channel type: single value")
                    else:
                        print("Channel type: unknown")

                    # channel data typeacti
                    if lib.DWGetChannelProps(idx, c_int(DWChannelProps.DW_DATA_TYPE.value), p_buff, byref(max_len)) != DWStatus.DWSTAT_OK.value:
                        DWRaiseError("DWDataReader: DWGetChannelProps() failed")
                    data_type = cast(p_buff, POINTER(c_int)).contents
                    logging.debug("Data type:" + str(DWDataType(data_type.value).name))

                    # number of samples
                    dw_ch_index = c_int(ch_list[i].index)
                    sample_cnt = c_int()
                    sample_cnt = lib.DWGetScaledSamplesCount(dw_ch_index)
                    if sample_cnt < 0:
                        DWRaiseError("DWDataReader: DWGetScaledSamplesCount() failed")
                    logging.debug("Num. samples:" + str(sample_cnt))

                    # get actual data

                    data = create_string_buffer(DOUBLE_SIZE * sample_cnt * ch_list[i].array_size)
                    time_stamp = create_string_buffer(DOUBLE_SIZE * sample_cnt)
                    p_data = cast(data, POINTER(c_double))
                    p_time_stamp = cast(time_stamp, POINTER(c_double))
                    if lib.DWGetScaledSamples(dw_ch_index, c_int64(0), sample_cnt, p_data, p_time_stamp) != DWStatus.DWSTAT_OK.value:
                        DWRaiseError("DWDataReader: DWGetScaledSamplesCount() failed")



                    df[name] = p_data[0:sample_cnt]


                    name_prec = name
                    name_all.append(name)

            logging.warning('returning DF to parquet')         
            
            


            print('\n \n -------------------------------------------------------------- \n \n')

        #----------------------------------------------------------------------------------------------------------------
        # end channel loop
        #----------------------------------------------------------------------------------------------------------------

        # close data file
            if lib.DWCloseDataFile() != DWStatus.DWSTAT_OK.value:
                DWRaiseError("DWDataReader: DWCloseDataFile() failed")

            # deinit
            if lib.DWDeInit() != DWStatus.DWSTAT_OK.value:
                DWRaiseError("DWDataReader: DWDeInit() failed")

            # close DLL
            _ctypes.FreeLibrary(lib._handle)
            del lib

            # suppression de la dll temporaire
            if os.path.exists(dst):
                logging.warning("file exists :" + str(dst) )
                os.remove(str(dst))
                logging.warning("dll Removed!")
            else:
                logging.warning("The file does not exist")


        else:
            logging.warning("##### ENDWITH .DXD T/F " + str(rootfile.endswith('.dxd')))
            logging.info('file is NOT in dxd format : ' + str(os.path.split(rootfile)[-1]))
            print('\n \n -------------------------------------------------------------- \n \n')
    except:
        errorFile = open('log\\'+ str('log_') + file + str('.txt'), "w")
        errorFile.write(traceback.format_exc())
        errorFile.close()
        if lib.DWCloseDataFile() != DWStatus.DWSTAT_OK.value:
            DWRaiseError("DWDataReader: DWCloseDataFile() failed")

            # deinit
        if lib.DWDeInit() != DWStatus.DWSTAT_OK.value:
            DWRaiseError("DWDataReader: DWDeInit() failed")

        # close DLL
        _ctypes.FreeLibrary(lib._handle)
        del lib

        # suppression de la dll temporaire
        if os.path.exists(dst):
            logging.warning("file exists :" + str(dst) )
            os.remove(str(dst))
            logging.warning("dll Removed!")
        print('---- global exception -------')# continue
        
    if len(df.columns) < 7:
            logging.error('length of col mismatch < 7')
            # input('error ')

    if len(df.columns) == 8:
        logging.error('length of col is correct = 8')
        df.columns = ['moteur_g', 't_poulie_g', 't_nez_g', 'mot_x_g', 'affuteur_g', 'bv_r_g', 'bv_a_g', 'f_rot_hz']

    if len(df.columns) > 8:
        logging.error('length of col mismatch > 8' )
        lscol = df.columns.tolist()
        lscol[0:8] = ['moteur_g', 't_poulie_g', 't_nez_g', 'mot_x_g', 'affuteur_g', 'bv_r_g', 'bv_a_g', 'f_rot_hz']
        df.columns = lscol
    return df
    print(df.head())


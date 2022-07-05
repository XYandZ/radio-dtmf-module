from pyaudio import PyAudio, paInt16


def audio_config():

    def get_input_devices():

        p = PyAudio()
        info = p.get_host_api_info_by_index(0)
        num_devices = info.get('deviceCount')

        all_devices = [ p.get_device_info_by_host_api_device_index(0, i) for i in range(0, num_devices) ]
        return list(filter( lambda x  : x.get('maxInputChannels') > 0, all_devices))

    input_device = get_input_devices()[0]
    print( input_device )
    input_device_index = input_device.get('index')
    input_device_sample_rate = int(input_device.get('defaultSampleRate'))

    channels = 1
    chunk = 2**12
    input_device_format = paInt16
    input = True

    return {"format":input_device_format,
            "channels":channels,
            "input_device_index":input_device_index,
            "rate":input_device_sample_rate,
            "input":input,
            "frames_per_buffer":chunk}

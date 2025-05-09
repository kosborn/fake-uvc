from enum import IntEnum, Enum, auto
from usb_protocol.types.descriptor import DescriptorFormat, DescriptorNumber, DescriptorField

import construct

class UVC(IntEnum):
    # Video Interface Class Code
    CC_VIDEO = 0x0E

    # Video Interface Subclass Codes
    SC_UNDEFINED = 0x00
    SC_VIDEOCONTROL = 0x01
    SC_VIDEOSTREAMING = 0x02
    SC_VIDEO_INTERFACE_COLLECTION = 0x03

    # Video Interface Protocol Codes
    PC_PROTOCOL_UNDEFINED = 0x00
    PC_PROTOCOL_15 = 0x01

    # Video Class-Specific Descriptor Types
    CS_UNDEFINED = 0x20
    CS_DEVICE = 0x21
    CS_CONFIGURATION = 0x22
    CS_STRING = 0x23
    CS_INTERFACE = 0x24
    CS_ENDPOINT = 0x25

    # Video Class-Specific VC Interface Descriptor Subtypes
    VC_DESCRIPTOR_UNDEFINED = 0x00
    VC_HEADER = 0x01
    VC_INPUT_TERMINAL = 0x02
    VC_OUTPUT_TERMINAL = 0x03
    VC_SELECTOR_UNIT = 0x04
    VC_PROCESSING_UNIT = 0x05
    VC_EXTENSION_UNIT = 0x06
    VC_ENCODING_UNIT = 0x07

    # Video Class-Specific VS Interface Descriptor Subtypes
    VS_UNDEFINED = 0x00
    VS_INPUT_HEADER = 0x01
    VS_OUTPUT_HEADER = 0x02
    VS_STILL_IMAGE_FRAME = 0x03
    VS_FORMAT_UNCOMPRESSED = 0x04
    VS_FRAME_UNCOMPRESSED = 0x05
    VS_FORMAT_MJPEG = 0x06
    VS_FRAME_MJPEG = 0x07
    # Reserved = 0x08
    # Reserved = 0x09
    VS_FORMAT_MPEG2TS = 0x0A
    # Reserved = 0x0B
    VS_FORMAT_DV = 0x0C
    VS_COLORFORMAT = 0x0D
    # Reserved = 0x0E
    # Reserved = 0x0F
    VS_FORMAT_FRAME_BASED = 0x10
    VS_FRAME_FRAME_BASED = 0x11
    VS_FORMAT_STREAM_BASED = 0x12
    VS_FORMAT_H264 = 0x13
    VS_FRAME_H264 = 0x14
    VS_FORMAT_H264_SIMULCAST = 0x15
    VS_FORMAT_VP8 = 0x16
    VS_FRAME_VP8 = 0x17
    VS_FORMAT_VP8_SIMULCAST = 0x18

    # Video Class-Specific Endpoint Descriptor Subtypes
    EP_UNDEFINED = 0x00
    EP_GENERAL = 0x01
    EP_ENDPOINT = 0x02
    EP_INTERRUPT = 0x03

    # Video Class-Specific Request Codes
    RC_UNDEFINED = 0x00
    SET_CUR = 0x01
    SET_CUR_ALL = 0x11
    GET_CUR = 0x81
    GET_MIN = 0x82
    GET_MAX = 0x83
    GET_RES = 0x84
    GET_LEN = 0x85
    GET_INFO = 0x86
    GET_DEF = 0x87
    GET_CUR_ALL = 0x91
    GET_MIN_ALL = 0x92
    GET_MAX_ALL = 0x93
    GET_RES_ALL = 0x94
    GET_DEF_ALL = 0x97

    # VideoControl Interface Control Selectors
    VC_CONTROL_UNDEFINED = 0x00
    VC_VIDEO_POWER_MODE_CONTROL = 0x01
    VC_REQUEST_ERROR_CODE_CONTROL = 0x02
    # Reserved = 0x03

    # Terminal Control Selectors
    TE_CONTROL_UNDEFINED = 0x00

    # Selector Unit Control Selectors
    SU_CONTROL_UNDEFINED = 0x00
    SU_INPUT_SELECT_CONTROL = 0x01

    # Terminal Control Selectors
    CT_CONTROL_UNDEFINED = 0x00
    CT_SCANNING_MODE_CONTROL = 0x01
    CT_AE_MODE_CONTROL = 0x02
    CT_AE_PRIORITY_CONTROL = 0x03
    CT_EXPOSURE_TIME_ABSOLUTE_CONTROL = 0x04
    CT_EXPOSURE_TIME_RELATIVE_CONTROL = 0x05
    CT_FOCUS_ABSOLUTE_CONTROL = 0x06
    CT_FOCUS_RELATIVE_CONTROL = 0x07
    CT_FOCUS_AUTO_CONTROL = 0x08
    CT_IRIS_ABSOLUTE_CONTROL = 0x09
    CT_IRIS_RELATIVE_CONTROL = 0x0A
    CT_ZOOM_ABSOLUTE_CONTROL = 0x0B
    CT_ZOOM_RELATIVE_CONTROL = 0x0C
    CT_PANTILT_ABSOLUTE_CONTROL = 0x0D
    CT_PANTILT_RELATIVE_CONTROL = 0x0E
    CT_ROLL_ABSOLUTE_CONTROL = 0x0F
    CT_ROLL_RELATIVE_CONTROL = 0x10
    CT_PRIVACY_CONTROL = 0x11
    CT_FOCUS_SIMPLE_CONTROL = 0x12
    CT_WINDOW_CONTROL = 0x13
    CT_REGION_OF_INTEREST_CONTROL = 0x14

    # Processing Unit Control Selectors
    PU_CONTROL_UNDEFINED = 0x00
    PU_BACKLIGHT_COMPENSATION_CONTROL = 0x01
    PU_BRIGHTNESS_CONTROL = 0x02
    PU_CONTRAST_CONTROL = 0x03
    PU_GAIN_CONTROL = 0x04
    PU_POWER_LINE_FREQUENCY_CONTROL = 0x05
    PU_HUE_CONTROL = 0x06
    PU_SATURATION_CONTROL = 0x07
    PU_SHARPNESS_CONTROL = 0x08
    PU_GAMMA_CONTROL = 0x09
    PU_WHITE_BALANCE_TEMPERATURE_CONTROL = 0x0A
    PU_WHITE_BALANCE_TEMPERATURE_AUTO_CONTROL = 0x0B
    PU_WHITE_BALANCE_COMPONENT_CONTROL = 0x0C
    PU_WHITE_BALANCE_COMPONENT_AUTO_CONTROL = 0x0D
    PU_DIGITAL_MULTIPLIER_CONTROL = 0x0E
    PU_DIGITAL_MULTIPLIER_LIMIT_CONTROL = 0x0F
    PU_HUE_AUTO_CONTROL = 0x10
    PU_ANALOG_VIDEO_STANDARD_CONTROL = 0x11
    PU_ANALOG_LOCK_STATUS_CONTROL = 0x12
    PU_CONTRAST_AUTO_CONTROL = 0x13

    # Encoding Unit Control Selectors
    EU_CONTROL_UNDEFINED = 0x00
    EU_SELECT_LAYER_CONTROL = 0x01
    EU_PROFILE_TOOLSET_CONTROL = 0x02
    EU_VIDEO_RESOLUTION_CONTROL = 0x03
    EU_MIN_FRAME_INTERVAL_CONTROL = 0x04
    EU_SLICE_MODE_CONTROL = 0x05
    EU_RATE_CONTROL_MODE_CONTROL = 0x06
    EU_AVERAGE_BITRATE_CONTROL = 0x07
    EU_CPB_SIZE_CONTROL = 0x08
    EU_PEAK_BIT_RATE_CONTROL = 0x09
    EU_QUANTIZATION_PARAMS_CONTROL = 0x0A
    EU_SYNC_REF_FRAME_CONTROL = 0x0B
    EU_LTR_BUFFER_CONTROL = 0x0C
    EU_LTR_PICTURE_CONTROL = 0x0D
    EU_LTR_VALIDATION_CONTROL = 0x0E
    EU_LEVEL_IDC_LIMIT_CONTROL = 0x0F
    EU_SEI_PAYLOADTYPE_CONTROL = 0x10
    EU_QP_RANGE_CONTROL = 0x11
    EU_PRIORITY_CONTROL = 0x12
    EU_START_OR_STOP_LAYER_CONTROL = 0x13
    EU_ERROR_RESILIENCY_CONTROL = 0x14

    # Extension Unit Control Selectors
    XU_CONTROL_UNDEFINED = 0x00

    # VideoStreaming Interface Control Selectors
    VS_CONTROL_UNDEFINED = 0x00
    VS_PROBE_CONTROL = 0x01
    VS_COMMIT_CONTROL = 0x02
    VS_STILL_PROBE_CONTROL = 0x03
    VS_STILL_COMMIT_CONTROL = 0x04
    VS_STILL_IMAGE_TRIGGER_CONTROL = 0x05
    VS_STREAM_ERROR_CODE_CONTROL = 0x06
    VS_GENERATE_KEY_FRAME_CONTROL = 0x07
    VS_UPDATE_FRAME_SEGMENT_CONTROL = 0x08
    VS_SYNCH_DELAY_CONTROL = 0x09

class UVCError(Enum):
    SUCCESS = (0, "Success (no error)")
    ERROR_IO = (-1, "Input/output error")
    ERROR_INVALID_PARAM = (-2, "Invalid parameter")
    ERROR_ACCESS = (-3, "Access denied")
    ERROR_NO_DEVICE = (-4, "No such device")
    ERROR_NOT_FOUND = (-5, "Not found")
    ERROR_BUSY = (-6, "Resource Busy")
    ERROR_TIMEOUT = (-7, "Operation timed out")
    ERROR_OVERFLOW = (-8, "Overflow")
    ERROR_PIPE = (-9, "Pipe Error")
    ERROR_INTERRUPTED = (-10, "System call interrupted (perhaps due to signal)")
    ERROR_NO_MEM = (-11, "Insufficient memory")
    ERROR_NOT_SUPPORTED = (-12, "Not supported")
    ERROR_INVALID_DEVICE = (-50, "Invalid device")
    ERROR_INVALID_MODE = (-51, "Invalid mode")
    ERROR_CALLBACK_EXISTS = (-52, "Callback exists, cannot poll")
    ERROR_OTHER = (-99, "Unknown Error")

    def __init__(self, code, description):
        self.code = code
        self.description = description

    # Optional: allow direct comparison with integers
    def __eq__(self, other):
        if isinstance(other, int):
            return self.code == other
        return super().__eq__(other)

    @classmethod
    def _missing_(cls, value):
        if isinstance(value, int):
            for member in cls:
                if member.code == value:
                    return member
        # If no match found or value is not an int, raise ValueError
        raise ValueError(f"{cls.__name__} has no member with code {value}")


InterfaceAssociationDescriptor = DescriptorFormat(
    "bLength"                / construct.Const(8, construct.Int8ul),
    "bDescriptorType"        / DescriptorNumber(0x0B),
    "bFirstInterface"        / DescriptorField("First Interface", default=0x01),
    "bInterfaceCount"        / DescriptorField("Interface Count", default=0x01),
    "bFunctionClass"         / DescriptorField("Function Class", default=UVC.CC_VIDEO),
    "bFunctionSubClass"      / DescriptorField("Function Subclass", default=UVC.SC_VIDEO_INTERFACE_COLLECTION),
    "bFunctionProtocol"      / DescriptorField("Function Protocol", default=UVC.PC_PROTOCOL_UNDEFINED),
    "iFunction"              / DescriptorField("Function String", default=0x00),
)

ClassSpecificVCInterfaceHeader = DescriptorFormat(
    "bLength"                / construct.Const(13, construct.Int8ul),
    "bDescriptorType"        / DescriptorNumber(UVC.CS_INTERFACE),
    "bDescriptorSubType"     / DescriptorNumber(UVC.VC_HEADER),
    "bcdUVC"                 / DescriptorField("bcdUVC", default=0x0100),
    "wTotalLength"           / DescriptorField("wTotalLength", default=0x00),
    "dwClockFrequency"       / DescriptorField("dwClockFrequency", length=4),
    # TODO: bInCollection is dynamic based on length of baInterfaceNr, which is list[Byte]
    "bInCollection"          / DescriptorField("Number of VideoStreaming Interfaces", default=0x01),
    "baInterfaceNr"          / DescriptorField("baInterfaceNr", length=1, default=0x01),
)

""" Table 3-4 Input Terminal Descriptor"""
InputTerminalDescriptorComposite = DescriptorFormat(
    # TODO: length is 8+n (default +0 here)
    "bLength"                / construct.Const(8, construct.Int8ul),
    "bDescriptorType"        / DescriptorNumber(UVC.CS_INTERFACE),
    "bDescriptorSubType"     / DescriptorNumber(UVC.VC_INPUT_TERMINAL),
    "bTerminalID"            / DescriptorField("bTerminalID", default=0x01),
    "wTerminalType"            / construct.Const(0x0401, construct.Int16ul),
    "bAssocTerminal"         / DescriptorField("bAssocTerminal", default=0x00),
    "iTerminal"              / DescriptorField("iTerminal", default=0x00),
)

""" Table 3-4 Input Terminal Descriptor"""
InputTerminalCameraInputDescriptor = DescriptorFormat(
    # TODO: length is 8+n (default +10 here)
    "bLength"                  / construct.Const(18, construct.Int8ul),
    "bDescriptorType"          / DescriptorNumber(UVC.CS_INTERFACE),
    "bDescriptorSubType"       / DescriptorNumber(UVC.VC_INPUT_TERMINAL),
    "bTerminalID"              / DescriptorField("bTerminalID", default=0x01),
    "wTerminalType"            / construct.Const(0x0201, construct.Int16ul),
    "bAssocTerminal"           / DescriptorField("bAssocTerminal", default=0x00),
    "iTerminal"                / DescriptorField("iTerminal", default=0x00),
    "wObjectiveFocalLengthMin" / DescriptorField("wObjectiveFocalLengthMin", default=0x0000),
    "wObjectiveFocalLengthMax" / DescriptorField("wObjectiveFocalLengthMax", default=0x0000),
    "wOcularFocalLength"       / DescriptorField("wOcularFocalLength", default=0x0000),
    # This controls the size of bmControls, but seems it's just 3 for this descriptor sub type
    "bControlSize"            / DescriptorField("bControlSize", default=3),
    "bmControls"              / DescriptorField("bmControls", length=3, default=0x000000),
)


""" Table 3-5 Output Terminal Descriptor """
OutputTerminalDescriptor = DescriptorFormat(
    # TODO: length is 9+n (default +0 here)
    "bLength"                / construct.Const(9, construct.Int8ul),
    "bDescriptorType"        / DescriptorNumber(UVC.CS_INTERFACE),
    "bDescriptorSubType"     / DescriptorNumber(UVC.VC_OUTPUT_TERMINAL),
    "bTerminalID"            / DescriptorField("bTerminalID", default=0x02),
    "wTerminalType"          / DescriptorField("wTerminalType", default=0x0101),
    "bAssocTerminal"         / DescriptorField("bAssocTerminal", default=0x00),
    "bSourceID"              / DescriptorField("bSourceID", default=0x01),
    "iTerminal"              / DescriptorField("iTerminal", default=0x00),
)

""" Table 3-7 Selector Unit Descriptor """
SelectorUnitDescriptor = DescriptorFormat(
    # TODO: legnth is 6+n (default +1 here)
    "bLength"                / construct.Const(7, construct.Int8ul),
    "bDescriptorType"        / DescriptorNumber(UVC.CS_INTERFACE),
    "bDescriptorSubType"     / DescriptorNumber(UVC.VC_SELECTOR_UNIT),
    "bUnitID"                / DescriptorField("bUnitID", default=0x05),
    "bNrInPins"              / DescriptorField("bNrInPins", default=0x01),
    "baSourceID"             / DescriptorField("baSourceID", length=1, default=0x01),
    "iSelector"              / DescriptorField("iSelector", default=0x00),
)

""" Table 3-8 Processing Unit Descriptor """
ProcessingUnitDescriptor = DescriptorFormat(
    "bLength"                / construct.Const(13, construct.Int8ul),
    "bDescriptorType"        / DescriptorNumber(UVC.CS_INTERFACE),
    "bDescriptorSubType"     / DescriptorNumber(UVC.VC_PROCESSING_UNIT),
    "bUnitID"                / DescriptorField("bUnitID", default=0x05),
    "bSourceID"              / DescriptorField("bSourceID", default=0x04),
    "wMaxMultiplier"         / DescriptorField("wMaxMultiplier", default=0x0000),
    "bControlSize"           / DescriptorField("bControlSize", default=3),
    "bmControls"             / DescriptorField("bmControls", length=3, default=0x000000),
    "iProcessing"            / DescriptorField("iProcessing", default=0x00),
    "bmVideoStandards"       / DescriptorField("bmVideoStandards", default=0x00),
)

""" Table 3-14 Class-specific VS Interface Input Header Descriptor """
ClassSpecificVideoStreamInputHeaderDescriptor = DescriptorFormat(
    # TODO: bLength is 13+bControlSize (default +1 here)
    "bLength"                / construct.Const(14, construct.Int8ul),
    "bDescriptorType"        / DescriptorNumber(UVC.CS_INTERFACE),
    "bDescriptorSubType"     / DescriptorNumber(UVC.VS_INPUT_HEADER),
    "bNumFormats"            / DescriptorField("bNumFormats", default=0x01),
    "wTotalLength"           / DescriptorField("wTotalLength", default=0x00),
    "bEndPointAddress"       / DescriptorField("bEndPointAddress", default=0x81),
    "bmInfo"                 / DescriptorField("bmInfo", default=0x00),
    "bTerminalLink"          / DescriptorField("bTerminalLink", default=0x01),
    "bStillCaptureMethod"    / DescriptorField("bStillCaptureMethod", default=0x00),
    "bTriggerSupport"        / DescriptorField("bTriggerSupport", default=0x00),
    "bTriggerUsage"          / DescriptorField("bTriggerUsage", default=0x00),
    # TODO: bControlSize is dynamic based on bmaControls, which is list[Byte]
    "bControlSize"           / DescriptorField("bControlSize", default=0x01),
    "bmaControls"            / DescriptorField("bmaControls", length=1, default=0x00),
)


"""
Loosely based on Table 3-18 Still Image Frame Descriptor
This is more complex and dependson bDescriptorSubType
Defauling to mjpeg for this one
"""
ClassSpecificVideoStreamFormatDescriptorMJPEG = DescriptorFormat(
    # TODO: bLength is 10+(4*bNumImageSizePatterns)
    "bLength"                / construct.Const(11, construct.Int8ul),
    "bDescriptorType"        / DescriptorNumber(UVC.CS_INTERFACE),
    "bDescriptorSubType"     / DescriptorNumber(UVC.VS_FORMAT_MJPEG),
    "bFormatIndex"           / DescriptorField("bFormatIndex", default=0x01),
    "bNumFrameDescriptors"   / DescriptorField("bNumFrameDescriptors", default=0x01),
    "bmFlags"                / DescriptorField("bmFlags", default=0x00),
    "bDefaultFrameIndex"     / DescriptorField("bDefaultFrameIndex", default=0x01),
    "bAspectRatioX"          / DescriptorField("bAspectRatioX", default=0x00),
    "bAspectRatioY"          / DescriptorField("bAspectRatioY", default=0x00),
    "bmInterlaceFlags"       / DescriptorField("bmInterlaceFlags", default=0x00),
    "bCopyProtect"           / DescriptorField("bCopyProtect", default=0x00),
)


"""
Loosely based on Table 3-18 Still Image Frame Descriptor
This is more complex and dependson bDescriptorSubType
Defauling to mjpeg for this one
"""
ClassSpecificVideoStreamFrameDescriptorMJPEG = DescriptorFormat(
    "bLength"                / construct.Const(38, construct.Int8ul),
    "bDescriptorType"        / DescriptorNumber(UVC.CS_INTERFACE),
    "bDescriptorSubType"     / DescriptorNumber(UVC.VS_FRAME_MJPEG),
    "bFrameIndex"            / DescriptorField("bFrameIndex", default=0x01),
    "bmCapabilities"         / DescriptorField("bmCapabilities", default=0x03),
    "wWidth"                 / DescriptorField("wWidth", default=0x00B0),
    "wHeight"                / DescriptorField("wHeight", default=0x0090),
    "dwMinBitRate"           / DescriptorField("dwMinBitRate", default=0x000DEC00, length=4),
    "dwMaxBitRate"           / DescriptorField("dwMaxBitRate", default=0x000DEC00, length=4),
    "dwMaxVideoFrameBufSize" / DescriptorField("dwMaxVideoFrameBufSize", default=0x00009480, length=4),
    "dwDefaultFrameInterval" / DescriptorField("dwDefaultFrameInterval", default=0x000A2C2A, length=4),
    "bFrameIntervalType"     / DescriptorField("bFrameIntervalType", default=0x00),
    "dwMinFrameInterval"     / DescriptorField("dwMinFrameInterval", default=0x000A2C2A, length=4),
    "dwMaxFrameInterval"     / DescriptorField("dwMaxFrameInterval", default=0x000A2C2A, length=4),
    "dwFrameIntervalStep"    / DescriptorField("dwFrameIntervalStep", default=0x00000000, length=4),

)

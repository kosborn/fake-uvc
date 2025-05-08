import struct
from enum import Enum, auto
from dataclasses import dataclass, field, fields
from typing import ClassVar, Annotated, Literal, TypeAlias, Optional, get_type_hints, get_origin, get_args


# Type definitions with corresponding struct format characters
Byte: TypeAlias = Annotated[int, "B"]  # 1 byte unsigned (0-255)
Word: TypeAlias = Annotated[int, "H"]  # 2 bytes unsigned (0-65535)
Int24: TypeAlias = Annotated[int, "3B"]  # 3 bytes unsigned (0-16777215)
Int32: TypeAlias = Annotated[int, "I"]  # 4 bytes unsigned (0-4294967295)

class UVC:
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


@dataclass
class USBDescriptor:
    """Base class for USB descriptors with automatic packing based on field order"""

    # To be defined in subclasses
    bDescriptorType: ClassVar[Byte]

    # Mapping from type annotations to struct format characters
    FORMAT_MAP = {
        Byte: 'B',
        Word: 'H',
        Int24: '3B',
        Int32: 'I',
    }

    # Size in bytes for each format
    SIZE_MAP = {
        'B': 1,
        'H': 2,
        '3B': 3,
        'I': 4,
    }


    def __post_init__(self):
        """Calculate bLength automatically based on field types"""
        self.bLength = 2  # Start with bLength(1) + bDescriptorType(1)

        # Get annotated type information
        type_hints = get_type_hints(self.__class__, include_extras=True)

        # Calculate total length based on field types
        # for f in fields(self):
        for f in self.__dataclass_fields__.values():
            if f.name not in ['bLength', 'bDescriptorType']:
                # Get the type annotation for this field
                field_type = type_hints.get(f.name)

                # Extract format character from annotation
                format_char = self._get_format_for_type(field_type)
                if '*' in format_char:
                    # Handle list types
                    # drop * from format_char, and then format_char * len(value)
                    format_char = format_char.replace('*', '')
                    self.bLength += self.SIZE_MAP.get(format_char, 1) * len(getattr(self, f.name))
                else:
                    # Add field size to total length
                    self.bLength += self.SIZE_MAP.get(format_char, 1)  # Default to 1 byte

    def _get_format_for_type(self, type_annotation):
        """Extract format character from a type annotation"""
        # If it's an Annotated type, extract the format from metadata
        if get_origin(type_annotation) is list:
            # Handle list types
            inner_type = type_annotation.__args__[0]
            format_char = self._get_format_for_type(inner_type)
            return f'{format_char}*'

        if get_origin(type_annotation) is ClassVar:
            inner_type = type_annotation.__args__[0]
            format_char = self._get_format_for_type(inner_type)
            return format_char


        if type_annotation in self.FORMAT_MAP:
            # Return the format character for standard types
            return self.FORMAT_MAP[type_annotation]

        # For standard types, return a default format
        return 'B'  # Default to 1 byte

    def pack(self) -> bytes:
        """Convert the descriptor to its binary representation using field types"""
        values = [self.bLength, self.bDescriptorType]
        format_string = '<BB'  # Start with bLength and bDescriptorType

        # Get annotated type information
        type_hints = get_type_hints(self.__class__, include_extras=True)

        # Add values and format characters for all fields
        for f in self.__dataclass_fields__.values(): #fields(self):
            if f.name not in ['bLength', 'bDescriptorType']:
                value = getattr(self, f.name)

                # Get the type annotation for this field
                field_type = type_hints.get(f.name)

                # Extract format character from annotation
                format_char = self._get_format_for_type(field_type)
                if '*' in format_char:
                    # Handle list types
                    # drop * from format_char, and then format_char * len(value)
                    format_char = format_char.replace('*', '')
                    format_string += format_char * len(value)
                    values.extend(value)
                elif field_type is Int24:
                    format_string += format_char
                    values.extend([int(b) for b in value.to_bytes(3, 'little')])
                else:
                    values.append(value)
                    format_string += format_char

        return struct.pack(format_string, *values)

    def __str__(self) -> str:
        """Return a string representation of the descriptor"""
        result = [f"{self.__class__.__name__}:"]
        result.append(f"  bLength: {self.bLength}")
        result.append(f"  bDescriptorType: 0x{self.bDescriptorType:02X}")

        # Add all other fields
        for f in self.__dataclass_fields__.values():
            if f.name not in ['bLength', 'bDescriptorType']:
                value = getattr(self, f.name)
                if isinstance(value, int):
                    # Format integers as hex
                    field_type = get_type_hints(self.__class__, include_extras=True).get(f.name)
                    format_char = self._get_format_for_type(field_type)
                    size = self.SIZE_MAP.get(format_char, 1) * 2  # Hex digits are 2 per byte
                    result.append(f"  {f.name}: 0x{value:0{size}X}")
                else:
                    result.append(f"  {f.name}: {value}")

        return "\n".join(result)


@dataclass
class InterfaceAssociationDescriptor(USBDescriptor):
    """ Table 3-1 Standard Video Interface Collection IAD """
    bDescriptorType: ClassVar[Byte] = 0x0B

    bFirstInterface: Byte
    bInterfaceCount: Byte
    bFunctionClass: Byte = UVC.CC_VIDEO
    bFunctionSubClass: Byte = UVC.SC_VIDEO_INTERFACE_COLLECTION
    bFunctionProtocol: Byte = UVC.PC_PROTOCOL_UNDEFINED
    iFunction: Byte = 0


# Probably won't need this one
@dataclass
class StandardVCInterfaceHeader(USBDescriptor):
    """ Table 3-2 Standard VC Interface Descriptor """
    bDescriptorType: ClassVar[Byte] = UVC.CS_INTERFACE

    bInterfaceNumber: Byte
    bAlternateSetting: Byte
    bNumEndpoints: Byte
    bInterfaceClass: ClassVar[Byte] = UVC.CC_VIDEO
    bInterfaceSubClass: ClassVar[Byte] = UVC.SC_VIDEOCONTROL
    bInterfaceProtocol: ClassVar[Byte] = UVC.PC_PROTOCOL_15
    iInterface: Byte = 0

@dataclass
class ClassSpecificVCInterfaceHeader(USBDescriptor):
    """ Table 3-3 Class-specific VC Interface Header Descriptor """
    bDescriptorType: ClassVar[Byte] = UVC.CS_INTERFACE
    bDescriptorSubType: ClassVar[Byte] = UVC.VC_HEADER

    bcdUVC: Word # Video Device Class Specification
    wTotalLength: Word
    dwClockFrequency: Int32
    bInCollection: Byte
    baInterfaceNr: list[Byte] = field(default_factory=list)

@dataclass
class InputTerminalDescriptor(USBDescriptor):
    """ Table 3-4 Input Terminal Descriptor """
    bDescriptorType: ClassVar[Byte] = UVC.CS_INTERFACE
    bDescriptorSubType: ClassVar[Byte] = UVC.VC_INPUT_TERMINAL

    bTerminalID: Byte = field(default=0x00)
    wTerminalType: Word =  field(default=0x0000)
    bAssocTerminal: Byte = field (default=0x00)
    iTerminal: Byte = field(default=0x00)

@dataclass
class OutputTerminalDescriptor(USBDescriptor):
    """ Table 3-5 Output Terminal Descriptor """
    bDescriptorType: ClassVar[Byte] = UVC.CS_INTERFACE
    bDescriptorSubType: ClassVar[Byte] = UVC.VC_OUTPUT_TERMINAL

    bTerminalID: Byte
    wTerminalType: Word
    bAssocTerminal: Byte
    bSourceID: Byte
    iTerminal: Byte


@dataclass
class InputTerminalCameraInputDescriptor(InputTerminalDescriptor):
    wTerminalType: Word = field(default=0x0201)  # Camera Terminal

    wObjectiveFocalLengthMin: Word = field(default=0x0000)
    wObjectiveFocalLengthMax: Word = field(default=0x0000)
    wOcularFocalLength: Word = field(default=0x0000)

    # This controls the size of bmControls, but seems it's just 3 for this descriptor sub type
    bControlSize: ClassVar[Byte] = 3
    bmControls: Int24 = field(default=0x000000)

@dataclass
class SelectorUnitDescriptor(USBDescriptor):
    """ Table 3-7 Selector Unit Descriptor """
    bDescriptorType: ClassVar[Byte] = UVC.CS_INTERFACE
    bDescriptorSubType: ClassVar[Byte] = UVC.VC_SELECTOR_UNIT

    bUnitID: Byte
    bNrInPins: Byte
    baSourceID: list[Byte] = field(default_factory=list)
    iSelector: Byte = field(default=0x00)

@dataclass
class ProcessingUnitDescriptor(USBDescriptor):
    """ Table 3-8 Processing Unit Descriptor """
    bDescriptorType: ClassVar[Byte] = UVC.CS_INTERFACE
    bDescriptorSubType: ClassVar[Byte] = UVC.VC_PROCESSING_UNIT

    bUnitID: Byte
    bSourceID: Byte
    wMaxMultiplier: Word = field(default=0x0000)
    bControlSize: ClassVar[Byte] = 3
    bmControls: Word = field(default=0x0000)
    iProcessing: Byte = field(default=0x00)
    bmVideoStandards: Byte = field(default=0x00)

@dataclass
class StandardInterruptEndpointDescriptor(USBDescriptor):
    """ Table 3-11 Standard VC Interrupt Endpoint Descriptor """
    bDescriptorType: ClassVar[Byte] = 0x05

    bEndpointAddress: Byte
    bmAttributes: Byte
    wMaxPacketSize: Word
    bInterval: Byte

@dataclass
class ClassSpecificVideoStreamInputHeaderDescriptor(USBDescriptor):
    """ Table 3-14 Class-specific VS Interface Input Header Descriptor """
    bDescriptorType: ClassVar[Byte] = UVC.CS_INTERFACE
    bDescriptorSubType: ClassVar[Byte] = UVC.VS_INPUT_HEADER

    bNumFormats: Byte
    wTotalLength: Word
    bEndPointAddress: Byte
    bmInfo: Byte
    bTerminalLink: Byte
    bStillCaptureMethod: Byte
    bTriggerSupport: Byte
    bTriggerUsage: Byte
    bControlSize: Byte
    bmaControls: list[Byte]


@dataclass
class ClassSpecificVideoStreamFormatDescriptor(USBDescriptor):
    """
    Loosely based on Table 3-18 Still Image Frame Descriptor
    This is more complex and will require some dynamic calculations
    """
    bDescriptorType: ClassVar[Byte] = UVC.CS_INTERFACE
    bDescriptorSubType: Byte = field(default=UVC.VS_FORMAT_MJPEG)

    bFormatIndex: Byte = field(default=0x01)
    bNumFrameDescriptors: Byte = field(default=0x01)
    bmFlags: Byte = field(default=0x00)
    bDefaultFrameIndex: Byte = field(default=0x01)
    bAspectRatioX: Byte = field(default=0x00)
    bAspectRatioY: Byte = field(default=0x00)
    bmInterlaceFlags: Byte = field(default=0x00)
    bCopyProtect: Byte = field(default=0x00)

@dataclass
class ClassSpecificVideoStreamFrameDescriptor(USBDescriptor):
    """
    Loosely based on Table 3-18 Still Image Frame Descriptor
    This is more complex and will require some dynamic calculations
    """
    bDescriptorType: ClassVar[Byte] = UVC.CS_INTERFACE
    bDescriptorSubtype: Byte = field(default=UVC.VS_FRAME_MJPEG)

    bFrameIndex: Byte = field(default=0x01)
    bmCapabilities: Byte = field(default=0x03)
    wWidth: Word = field(default=0x00B0)
    wHeight: Word = field(default=0x0090)
    dwMinBitRate: Int32 = field(default=0x000DEC00)
    dwMaxBitRate: Int32 = field(default=0x000DEC00)
    dwMaxVideoFrameBufSize: Int32 = field(default=0x00009480)
    dwDefaultFrameInterval: Int32 = field(default=0x000A2C2A)
    bFrameIntervalType: Byte = field(default=0x00)
    dwMinFrameInterval: Int32 = field(default=0x000A2C2A)
    dwMaxFrameInterval: Int32 = field(default=0x000A2C2A)
    dwFrameIntervalStep: Int32 = field(default=0x00000000)

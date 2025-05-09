#!/usr/bin/env python3
# pylint: disable=unused-wildcard-import, wildcard-import
#
# This file is based off of Facedancer's minimal example
# https://github.com/greatscottgadgets/facedancer/blob/2c4b8aa27857d0d93efbcfc366db19030c17ea9e/examples/minimal.py
#

# TODO: Build a USB Descriptor class to implement a nice version of the UVC spec



# from facedancer import *
from facedancer import (
    DeviceSpeed,
    LanguageIDs,
    # USBConfiguration,
    USBControlRequest,
    USBDescriptor,
    USBDevice,
    USBDirection,
    USBEndpoint,
    USBInterface,
    USBSynchronizationType,
    USBTransferType,
    USBUsageType,
    to_device,
    use_inner_classes_automatically,
    vendor_request_handler,
    requestable,
    class_request_handler,
    to_this_interface
)
from facedancer import main
from facedancer.descriptor import USBDescribable, AutoInstantiable, StringRef, include_in_config
from facedancer.request import USBRequestHandler
from facedancer.logging import log, configure_default_logging, LOGLEVEL_TRACE

# Patching the USBConfiguration class to quickly add support for the USBAssociation type
from configuration_override import USBConfigurationOverride, USBAssociation

import logging
import binascii

from dataclasses import dataclass
from typing import List
import struct

import  uvc

configure_default_logging(level=LOGLEVEL_TRACE)


@use_inner_classes_automatically
class Webcam(USBDevice):
    # A Logitech HD Pro Webcam C920 was the source of my analysis
    product_string: StringRef = StringRef.field(string="Fake HD Pro Webcam C920")
    manufacturer_string: StringRef = StringRef.field(string="Logitek") #None
    serial_number_string: StringRef = StringRef.field(string="C0FFEEEE")
    vendor_id: int = 0x046D # Logitech
    product_id: int = 0x082D # C920 camera
    device_speed: DeviceSpeed = DeviceSpeed.SUPER
    device_revision: int = 0x11

    supported_languages: tuple = (LanguageIDs.ENGLISH_US,)

    device_class: int = 0xEF
    device_subclass: int = 0x02

    protocol_revision_number: int = 0x01
    max_packet_size: int = 64

    class Webcam(USBConfigurationOverride):


        # Not sure if USBAssociation is required
        class InterfaceAssociation(USBAssociation):
            number= 5
            alternate = 5
            include_in_config = True

        class VideoControl(USBInterface):
            number = 0x00
            class_number = 0x0E
            subclass_number = 0x01  # Video Control
            protocol_number = 0x01
            interface_string = 'idk'

            class ClassSpeicifcVideoControl(USBDescriptor):
                include_in_config: bool = True
                raw = uvc.ClassSpecificVCInterfaceHeader.build({
                    'bcdUVC': 1.0,
                    'wTotalLength': 214,
                    'dwClockFrequency': 30000000,
                    'bInCollection': 1,
                    'baInterfaceNr': 1
                })

            class InputTerminalCamera(USBDescriptor):
                include_in_config: bool = True
                raw = uvc.InputTerminalCameraInputDescriptor.build({
                    'bTerminalID':0x02,
                    'wTerminalType':0x0201,
                    'bAssocTerminal':0x00,
                    'iTerminal':0x00,
                    'bTerminalID':0x01,
                    'bAssocTerminal':0x00,
                    'iTerminal':0x00,
                    'wObjectiveFocalLengthMin':0x0000,
                    'wObjectiveFocalLengthMax':0x0000,
                    'wOcularFocalLength':0x0000,
                    'bmControls':0x0000,
                })

            class InputTerminalComposite(USBDescriptor):
                include_in_config: bool = True
                raw = uvc.InputTerminalDescriptorComposite.build({
                    'bTerminalID':0x02,
                    'bAssocTerminal':0x00,
                    'iTerminal':0x00,
                })

            class OutputTerminal(USBDescriptor):
                include_in_config: bool = True
                raw = uvc.OutputTerminalDescriptor.build({
                    'bTerminalID':0x03,
                    'wTerminalType':0x0101,
                    'bAssocTerminal':0x00,
                    'bSourceID':0x05,
                    'iTerminal':0x00,
                })

            class SelectorUnit(USBDescriptor):
                include_in_config: bool = True
                raw = uvc.SelectorUnitDescriptor.build({
                    'bUnitID':0x05,
                    'bNrInPins':1,
                    'baSourceID':0x01,
                    'iSelector':0x00
                })

            # 2.3.4.7 Processing Unit Descriptor
            class ProcessingUnit(USBDescriptor):
                include_in_config: bool = True
                raw = uvc.ProcessingUnitDescriptor.build({
                    'bUnitID':0x05,
                    'bSourceID':0x04,
                    'wMaxMultiplier':0x0000,
                    'bmControls':0x000001, # Brightness control
                    'iProcessing':0x00,
                    'bmVideoStandards':0x00
                })

            # 2.3.4.8 Standard Interrupt Endpoint Descriptor
            class StandardInterruptEndpoint(USBEndpoint):
                number = 0x81
                direction = USBDirection.IN
                interval = 0x09
                transfer_type = USBTransferType.INTERRUPT

            # 2.3.4.9 Class-specific Interrupt Endpoint Descriptor
            # class ClassSpecificInterruptEndpoint(USBDescriptor):
            #     raw: bytes = binascii.unhexlify('0505030040')
            #     include_in_config: bool = True

            # OR

            # 2.3.4.9 Class-specific Interrupt Endpoint Descriptor
            # class ClassSpecificInterruptEndpoint(USBEndpoint):
            #     number=  0x83
            #     direction = USBDirection.OUT
            #     transfer_type = USBTransferType.INTERRUPT


            @class_request_handler(number=0x81, direction=USBDirection.IN)
            @to_this_interface
            def handle_control_request_0x81(self, request: USBControlRequest):
                log.info(f"VideoControl 0x81 request direciton: {request.direction:x} type: {request.type} recipient: {request.recipient} num,value,index,length {request.number:x},{request.value:x},{request.index:x},{request.length:x} bytes: {request.data}")
                request.ack()

            @class_request_handler(number=0x86, direction=USBDirection.IN)
            @to_this_interface
            def handle_control_request_0x86(self, request: USBControlRequest):
                log.info(f"VideoControl 0x86 request direciton: {request.direction:x} type: {request.type} recipient: {request.recipient} num,value,index,length {request.number:x},{request.value:x},{request.index:x},{request.length:x} bytes: {request.data}")
                request.ack()

        # 2.3.5.1 Operational Alternate Setting 0
        # 2.3.5.1.1 Standard VS Interface Descriptor
        class VideoStreamingAlt0(USBInterface):
            number = 0x01
            alternate = 0x00
            class_number = 0x0e
            subclass_number = 0x02

            # 2.3.5.1.2 Class-specific VS Header Descriptor (Input)
            class ClassSpecificVideoStreamHeader(USBDescriptor):
                include_in_config = True
                raw = uvc.ClassSpecificVideoStreamInputHeaderDescriptor.build({
                    'bNumFormats': 0x01,
                    'wTotalLength': 0x003f,
                    'bEndPointAddress': 0x82,
                    'bmInfo': 0x00,
                    'bTerminalLink': 0x03,
                    'bStillCaptureMethod': 0x01,
                    'bTriggerSupport': 0x01,
                    'bTriggerUsage': 0x00,
                    'bControlSize': 0x01,
                    'bmaControls': 0x00
                })

            # 2.3.5.1.3 Class-specific VS Format Descriptor
            class FormatMJPEG(USBDescriptor):
                include_in_config: bool = True
                raw = uvc.ClassSpecificVideoStreamFormatDescriptorMJPEG.build({
                    'bFormatIndex':0x01,
                    'bNumFrameDescriptors':0x01,
                    'bmFlags':0x01,
                    'bDefaultFrameIndex':0x01,
                    'bAspectRatioX':0,
                    'bAspectRatioY':0,
                    'bmInterlaceFlags':0,
                    'bCopyProtect':0
                })

            # 2.3.5.1.4 Class-specific VS Frame Descriptor
            class Frame(USBDescriptor):
                include_in_config: bool = True
                raw = uvc.ClassSpecificVideoStreamFrameDescriptorMJPEG.build({
                    'bFrameIndex':0x01,
                    'bmCapabilities':0x03,
                    'wWidth':176,
                    'wHeight':144,
                    'dwMinBitRate':0x000DEC00,
                    'dwMaxBitRate':0x000DEC00,
                    'dwMaxVideoFrameBufSize':0x00009480,
                    'dwDefaultFrameInterval':0x000A2C2A,
                    'bFrameIntervalType':0,
                    'dwMinFrameInterval':0x000A2C2A,
                    'dwMaxFrameInterval':0x000A2C2A,
                    'dwFrameIntervalStep':0x00000000,
                })

            # SET VALUE
            @class_request_handler(number=1, direction=USBDirection.OUT)
            @to_this_interface
            def handle_control_request_1(self, request):
                request.ack()

            @class_request_handler(number=0x81, direction=USBDirection.IN)
            @to_this_interface
            def handle_control_request_0x81(self, request: USBControlRequest):
                log.info(f"VideoStreamingAlt0 0x81 request direciton: {request.direction:x} type: {request.type} recipient: {request.recipient} num,value,index,length {request.number:x},{request.value:x},{request.index:x},{request.length:x} bytes: {request.data}")
                request.reply(binascii.unhexlify('0100010115160500000000003d000000000000600900800a0000'))

            @class_request_handler(number=0x82, direction=USBDirection.IN)
            @to_this_interface
            def handle_control_request_0x82(self, request: USBControlRequest):
                log.info(f"VideoStreamingAlt0 0x82 request direciton: {request.direction:x} type: {request.type} recipient: {request.recipient} num,value,index,length {request.number:x},{request.value:x},{request.index:x},{request.length:x} bytes: {request.data}")
                request.ack()

            # GET_INFO
            @class_request_handler(number=0x86, direction=USBDirection.IN)
            @to_this_interface
            def handle_control_request_0x86(self, request):
                log.info(f"VideoStreamingAlt0 0x86 request direciton: {request.direction:x} type: {request.type} recipient: {request.recipient} num,value,index,length {request.number:x},{request.value:x},{request.index:x},{request.length:x} bytes: {request.data}")
                request.ack()

            # GET_DEF
            @class_request_handler(number=0x87, direction=USBDirection.IN)
            @to_this_interface
            def handle_control_request_0x87(self, request):
                log.info(f"VideoStreamingAlt0 0x87 request direciton: {request.direction:x} type: {request.type} recipient: {request.recipient} num,value,index,length {request.number:x},{request.value:x},{request.index:x},{request.length:x} bytes: {request.data}")
                request.reply(binascii.unhexlify('0100010115160500000000003d00000000000000000000000000'))


        # 2.3.5.2 Operational Alternate Setting 1
        # 2.3.5.2.1 Standard VS Interface Descriptor
        class VideoStreamingAlt1(USBInterface):
            number = 0x01
            alternate = 0x01
            class_number = 0x0e
            subclass_number = 0x02

            # 2.3.5.2.2 Standard VS Isochronous Video Data Endpoint Descriptor
            class IsochronousVideoEndpoint(USBEndpoint):
                number: int = 0x02
                direction: USBDirection = USBDirection.IN
                transfer_type: USBTransferType = USBTransferType.ISOCHRONOUS
                max_packet_size: int = 0x01fe #510 bytes
                synchronization_type: USBSynchronizationType = (
                    USBSynchronizationType.ASYNC
                )
                usage_type: USBUsageType = USBUsageType.DATA
                interval = 0x01

                # def handle_data_requested(self: USBEndpoint):
                #     logging.info("handle_data_requested")
                #     self.send(b"device on bulk endpoint")

            # INTERFACE RESPONSES
            # 0x81 GET_CUR
            # 0x82 GET_MIN
            # 0x83 GET_MAX
            # 0x84 GET_RES
            # 0x86 GET_INFO
            # 0x87 GET_DEV

            @class_request_handler(number=0x81, direction=USBDirection.IN)
            @to_this_interface
            def handle_control_request_0x81(self, request: USBControlRequest):
                log.info(f"VideoStreamingAlt1 0x81 request direciton: {request.direction:x} type: {request.type} recipient: {request.recipient} num,value,index,length {request.number:x},{request.value:x},{request.index:x},{request.length:x} bytes: {request.data}")
                request.ack()

            @class_request_handler(number=0x82, direction=USBDirection.IN)
            @to_this_interface
            def handle_control_request_0x82(self, request: USBControlRequest):
                log.info(f"VideoStreamingAlt1 0x82 request direciton: {request.direction:x} type: {request.type} recipient: {request.recipient} num,value,index,length {request.number:x},{request.value:x},{request.index:x},{request.length:x} bytes: {request.data}")
                request.ack()

            # GET_INFO
            @class_request_handler(number=0x86, direction=USBDirection.IN)
            @to_this_interface
            def handle_control_request_0x86(self, request):
                log.info(f"VideoStreamingAlt1 0x86 request direciton: {request.direction:x} type: {request.type} recipient: {request.recipient} num,value,index,length {request.number:x},{request.value:x},{request.index:x},{request.length:x} bytes: {request.data}")
                request.ack()

            # GET_DEF
            @class_request_handler(number=0x87, direction=USBDirection.IN)
            @to_this_interface
            def handle_control_request_0x87(self, request):
                log.info(f"VideoStreamingAlt1 0x87 request direciton: {request.direction:x} type: {request.type} recipient: {request.recipient} num,value,index,length {request.number:x},{request.value:x},{request.index:x},{request.length:x} bytes: {request.data}")
                # Most recent request was for 26B of data.
                # Replace me with your handler.
                #
                # request.stall()
                request.reply(binascii.unhexlify('0100010115160500000000003d00000000000000000000000000'))




if __name__ == "__main__":
    # logging.getLogger().setLevel(logging.DEBUG)
    main(Webcam)

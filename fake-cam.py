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

        class InterfaceAssociation(USBAssociation):
            number= 5
            alternate = 5
            raw: bytes = binascii.unhexlify("0b00020e030002")
            include_in_config = True

            # DESCRIPTOR_TYPE_NUMBER = 0x0B
            # class_number = 0x0E
            # subclass_number = 0x03

        class VideoControl(USBInterface):
            number = 0x00
            class_number = 0x0E
            subclass_number = 0x01  # Video Control
            protocol_number = 0x01
            interface_string = 'idk'

            class ClassSpeicifcVideoControl(USBDescriptor):
                raw: bytes = binascii.unhexlify('0d240100014200808d5b000101')
                include_in_config: bool = True


            class InputTerminalCamera(USBDescriptor):
                raw: bytes = binascii.unhexlify("1124020101020000000000000000020000")
                include_in_config: bool = True

            class InputTerminalComposite(USBDescriptor):
                raw: bytes = binascii.unhexlify("0824020201040000")
                include_in_config: bool = True

            class OutputTerminal(USBDescriptor):
                raw: bytes = binascii.unhexlify("092403030101000500")
                include_in_config: bool = True

            class SelectorUnit(USBDescriptor):
                raw: bytes = binascii.unhexlify('0824040402010200')
                include_in_config: bool = True

            # 2.3.4.7 Processing Unit Descriptor
            class ProcessingUnit(USBDescriptor):
                raw: bytes = binascii.unhexlify('0c2405050400000301000000') # real
                include_in_config: bool = True

            # 2.3.4.8 Standard Interrupt Endpoint Descriptor
            class StandardInterruptEndpoint(USBEndpoint):
                number = 0x81
                direction = USBDirection.IN
                interval = 0x20
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
                raw: bytes = binascii.unhexlify('0e2401013f008200030101000100')
                include_in_config = True

            # 2.3.5.1.3 Class-specific VS Format Descriptor
            class FormatMJPEG(USBDescriptor):
                raw: bytes = binascii.unhexlify("0b24060101010100000000")
                include_in_config: bool = True

            # 2.3.5.1.4 Class-specific VS Frame Descriptor
            class Frame(USBDescriptor):
                raw: bytes = binascii.unhexlify( # real
                    "2624070103b000900000ec0d0000ec0d00809400002a2c0a00002a2c0a002a2c0a0000000000"
                )
                include_in_config: bool = True

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

            # TODO: replace USBControlRequest with USBVideoControlRequest (they have differnet formats)

            @class_request_handler(number=0x81, direction=USBDirection.IN)
            @to_this_interface
            def handle_control_request_0x81(self, request: USBControlRequest):
                log.info(f"VideoStreamingAlt1 0x81 request direciton: {request.direction:x} type: {request.type} recipient: {request.recipient} num,value,index,length {request.number:x},{request.value:x},{request.index:x},{request.length:x} bytes: {request.data}")
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


    # SET INTERFACE
    @vendor_request_handler(request_number=0x0b, direction=USBDirection.IN)
    @to_device
    def handle_control_request_set_interface(self: USBDevice, request: USBControlRequest):
        log.info("1")
        raise Exception("1")
        request.reply(b"device sent response on control endpoint")


if __name__ == "__main__":
    # logging.getLogger().setLevel(logging.DEBUG)
    main(Webcam)

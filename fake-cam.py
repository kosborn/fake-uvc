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
    USBConfiguration,
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
    vendor_request_handler
)
from facedancer import main
from facedancer.descriptor import USBDescribable, AutoInstantiable, StringRef
from facedancer.request import USBRequestHandler
from facedancer.logging import log, configure_default_logging, LOGLEVEL_TRACE

import logging
import binascii

from dataclasses import dataclass
from typing import List
import struct

configure_default_logging(level=LOGLEVEL_TRACE)



class Association(USBDescribable, AutoInstantiable, USBRequestHandler):
    DESCRIPTOR_TYPE_NUMBER = 0x0B
    DESCRIPTOR_SIZE_BYTES = 8


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

    class Webcam(USBConfiguration):

        class InterfaceAssociation(Association):
            number = 0x00
            class_number = 0x0E
            subclass_number = 0x03

        class VideoControl(USBInterface):
            number = 0x00
            class_number = 0x0E
            subclass_number = 0x01  # Video Control

            class Header(USBDescriptor):
                # number: int = 0x0
                # type_number: int = 0x24  # USBDescriptorTypeNumber.CONFIGURATION
                # VIDEO CONTROL INTERFACE DESCRIPTOR [Header]
                #     bLength: 13
                #     bDescriptorType: 0x24 (video class interface)
                #     Subtype: Header (1)
                #     bcdUVC: 0x0150
                #     wTotalLength: 40
                #     dwClockFrequency: 27000000
                #     bInCollection: 1
                #     baInterfaceNr: 01

                raw: bytes = binascii.unhexlify("0d240150012800c0fc9b010101")
                include_in_config: bool = True

            class InputTerminalCamera(USBDescriptor):
                raw: bytes = binascii.unhexlify("1124020102010000000000000000020000")
                include_in_config: bool = True

            class InputTerminalComposite(USBDescriptor):
                raw: bytes = binascii.unhexlify("0824020204010000")
                include_in_config: bool = True

            class OutputTerminal(USBDescriptor):
                raw: bytes = binascii.unhexlify("092403030101000500")
                include_in_config: bool = True

            class SelectorUnit(USBDescriptor):
                raw: bytes = binascii.unhexlify('0824040402010201')
                include_in_config: bool = True

            class ProcessingUnit(USBDescriptor):
                raw: bytes = binascii.unhexlify('0c2405050400000300010000')
                include_in_config: bool = True

            class StandardInterruptEndpoint(USBEndpoint):
                number = 0x81
                direction = USBDirection.IN
                interval = 0x20

            # class ClassSpecificInterruptEndpoint(USBEndpoint):
            #     direction = USBDirection.IN
            #     interval = 0x20



        class VideoStreamingAlt0(USBInterface):
            number = 0x01
            alternate = 0x00
            class_number = 0x0e
            subclass_number = 0x02

            class Header(USBDescriptor):
                raw: bytes = binascii.unhexlify('0e240101003f8200030101000100') # 2.3.5.1.2
                include_in_config = True

            class FormatMJPEG(USBDescriptor):
                raw: bytes = binascii.unhexlify("0b24060101010100000000") # 2.3.5.1.3
                include_in_config: bool = True


            class Frame(USBDescriptor):
                # number = 2
                raw: bytes = binascii.unhexlify(
                    "262407010300b00090000dec00000dec0000009480000a2c2a00000a2c2a000a2c2a00000000"
                )
                include_in_config: bool = True

        class VideoStreamingAlt1(USBInterface):
            number = 0x01
            alternate = 0x01
            class_number = 0x0e
            subclass_number = 0x02

            class IsochronousVideoEndpoint(USBEndpoint):
                number: int = 0x02
                direction: USBDirection = USBDirection.IN
                transfer_type: USBTransferType = USBTransferType.ISOCHRONOUS
                max_packet_size: int = 0x01fe #510 bytes
                synchronization_type: USBSynchronizationType = (
                    USBSynchronizationType.ASYNC
                )
                usage_type: USBUsageType = USBUsageType.DATA

                def handle_data_requested(self: USBEndpoint):
                    logging.info("handle_data_requested")
                    self.send(b"device on bulk endpoint")

    # SET INTERFACE
    @vendor_request_handler(request_number=1, direction=USBDirection.IN)
    @to_device
    def handle_control_request_1(self: USBDevice, request: USBControlRequest):
        log.info("1")
        raise Exception("1")
        request.reply(b"device sent response on control endpoint")

    # @vendor_request_handler(request_number=2, direction=USBDirection.OUT)
    # @to_device
    # def my_other_vendor_request_handler(self: USBDevice, request: USBControlRequest):
    #     print("WTF")
    #     logging.info(
    #         f"device received '{request.index}' '{request.value}' '{request.data}' on control endpoint"
    #     )

    #     # acknowledge the request
    #     request.ack()

    @vendor_request_handler(number=2, direction=USBDirection.IN)
    @to_device
    def handle_control_request_2(self, request):
        log.info("2")
        raise Exception("2")
        request.reply(b'')

    @vendor_request_handler(number=3, direction=USBDirection.IN)
    @to_device
    def handle_control_request_3(self, request):
        log.info("3")
        raise Exception("3")
        request.reply(b'')

    @vendor_request_handler(number=4, direction=USBDirection.IN)
    @to_device
    def handle_control_request_4(self, request):
        log.info("4")
        raise Exception("4")
        request.reply(b'')

    @vendor_request_handler(number=5, direction=USBDirection.IN)
    @to_device
    def handle_control_request_5(self, request):
        log.info("5")
        raise Exception("5")
        request.reply(b'')

    @vendor_request_handler(number=6, direction=USBDirection.IN)
    @to_device
    def handle_control_request_6(self, request):
        log.info("6")
        raise Exception("6")
        request.reply(b'')


if __name__ == "__main__":
    # logging.getLogger().setLevel(logging.DEBUG)
    main(Webcam)

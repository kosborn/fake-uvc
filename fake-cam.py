#!/usr/bin/env python3
# pylint: disable=unused-wildcard-import, wildcard-import
#
# This file is based off of Facedancer's minimal example
# https://github.com/greatscottgadgets/facedancer/blob/2c4b8aa27857d0d93efbcfc366db19030c17ea9e/examples/minimal.py
#

import logging


from facedancer import *
from facedancer import main
from facedancer.descriptor import USBDescribable, AutoInstantiable
from facedancer.request import USBRequestHandler

import binascii

from dataclasses import dataclass
from typing import List
import struct


class Association(USBDescribable, AutoInstantiable, USBRequestHandler):
    DESCRIPTOR_TYPE_NUMBER = 0x0B
    DESCRIPTOR_SIZE_BYTES = 8


@use_inner_classes_automatically
class MyDevice(USBDevice):
    # A Logitech HD Pro Webcam C920 was the source of my analysis
    product_string: str = "Fakse HD Pro Webcam C920"
    manufacturer_string: str = None
    vendor_id: int = 0x046D # Logitech
    product_id: int = 0x082D # C920 camera
    device_speed: DeviceSpeed = DeviceSpeed.SUPER
    serial_number_string: str = "C0FFEEEE"
    device_revision = 0x11

    supported_languages: tuple = (LanguageIDs.ENGLISH_US,)

    device_class: int = 0xEF
    device_subclass: int = 0x02

    protocol_revision_number: int = 0x01
    max_packet_size: int = 64

    class MyConfiguration(USBConfiguration):

        # class VideoAssociation(Association):
        #     number = 0x00
        #     class_number = 0x0E
        #     subclass_number = 0x03

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

            class InputTerminal(USBDescriptor):
                raw: bytes = binascii.unhexlify("122402010102000000000000000003000000")
                include_in_config: bool = True

            class OutputTerminal(USBDescriptor):
                raw: bytes = binascii.unhexlify("092403020101000100")
                include_in_config: bool = True

        class VideoStreaming(USBInterface):
            number = 0x01
            class_number = 0x0E
            subclass_number = 0x02  # Video Streaming

            class Header(USBDescriptor):
                # number = 0
                raw: bytes = binascii.unhexlify("10240103ca0a81000400000001000404")
                include_in_config: bool = True

            class FormatMJPEG(USBDescriptor):
                # number = 1
                raw: bytes = binascii.unhexlify("0b24060111010100000000")
                include_in_config: bool = True

            class Frame_640x480(USBDescriptor):
                # number = 2
                raw: bytes = binascii.unhexlify(
                    "36240701008002e001000077010000ca08006009001516050007151605009a5b060020a107002a2c0a0040420f005558140080841e00"
                )
                include_in_config: bool = True

            class ColorFormat(USBDescriptor):
                # number = 3
                raw: bytes = binascii.unhexlify("06240d010104")
                include_in_config: bool = True

            class Endpoint(USBEndpoint):
                number: int = 1
                direction: USBDirection = USBDirection.IN
                max_packet_size: int = 64
                # transfer_type: USBTransferType = USBTransferType.ISOCHRONOUS
                # synchronization_type: USBSynchronizationType = (
                #     USBSynchronizationType.ASYNC
                # )
                # usage_type: USBUsageType = USBUsageType.DATA

                # def handle_data_requested(self: USBEndpoint):
                #     logging.info("handle_data_requested")
                #     self.send(b"device on bulk endpoint")

        class VideoSubClass1_1(USBInterface):
            number = 0x01
            alternate = 0x01
            class_number = 0x0E
            subclass_number = 0x02  # Video Streaming

            class Endpoint(USBEndpoint):
                number: int = 2
                direction: USBDirection = USBDirection.IN
                max_packet_size: int = 192
                transfer_type: USBTransferType = USBTransferType.ISOCHRONOUS
                synchronization_type: USBSynchronizationType = (
                    USBSynchronizationType.ASYNC
                )
                usage_type: USBUsageType = USBUsageType.DATA

                def handle_data_requested(self: USBEndpoint):
                    logging.info("handle_data_requested")
                    self.send(b"device on bulk endpoint")

        # class MyInEndpoint(USBEndpoint):
        #     number: int = 1
        #     direction: USBDirection = USBDirection.IN
        #     max_packet_size: int = 64

        #     def handle_data_requested(self: USBEndpoint):
        #         logging.info("handle_data_requested")
        #         self.send(b"device on bulk endpoint")

        # class MyOutEndpoint(USBEndpoint):
        #     number: int = 1
        #     direction: USBDirection = USBDirection.OUT
        #     max_packet_size: int = 64

        #     def handle_data_received(self: USBEndpoint, data):
        #         logging.info(f"device received {data} on bulk endpoint")

    @vendor_request_handler(request_number=1, direction=USBDirection.IN)
    @to_device
    def my_vendor_request_handler(self: USBDevice, request: USBControlRequest):
        print("WTF")
        request.reply(b"device sent response on control endpoint")

    @vendor_request_handler(request_number=2, direction=USBDirection.OUT)
    @to_device
    def my_other_vendor_request_handler(self: USBDevice, request: USBControlRequest):
        print("WTF")
        logging.info(
            f"device received '{request.index}' '{request.value}' '{request.data}' on control endpoint"
        )

        # acknowledge the request
        request.ack()


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.DEBUG)
    main(MyDevice)

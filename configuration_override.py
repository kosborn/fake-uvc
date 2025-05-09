# This is 100% a hack!
# USBConfiguration doesn't currently support an association descriptor before interfaces
# We're just overriding the class and hacking in a USBAssociation class

from facedancer.configuration import USBConfiguration
from facedancer.descriptor    import USBDescribable, USBDescriptor, StringRef
from facedancer.magic         import instantiate_subordinates, AutoInstantiable
from facedancer.request       import USBRequestHandler
from facedancer.interface     import USBInterface

from dataclasses  import field


class USBAssociation(USBDescribable, AutoInstantiable, USBRequestHandler):
    DESCRIPTOR_TYPE_NUMBER  = 0x0b
    DESCRIPTOR_SIZE_BYTES   = 8
    parent: USBDescribable = None

    def get_descriptor(self) -> bytes:
        return bytes([
           8,
           0x0b,
           0,
           2,
           0x0e,
           0x03,
           0,
           0 ])

    def get_identifier(self):
        return (5,5) # Not really relevant, just need to satisfy the interface class hack

    def get_endpoints(self):
        return []

    def _request_handlers(self):
        return ()


class USBConfigurationOverride(USBConfiguration):
    associations: USBAssociation = field(default_factory=dict)

    def __post_init__(self):

        self.configuration_string = StringRef.ensure(self.configuration_string)

        # Gather any interfaces attached to the configuration.
        for association in instantiate_subordinates(self, USBAssociation):
            self.add_interface(association)

        # Gather any interfaces attached to the configuration.
        for interface in instantiate_subordinates(self, USBInterface):
            self.add_interface(interface)

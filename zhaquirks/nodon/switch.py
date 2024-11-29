"""NodOn on/off switch two channels."""

from zigpy.quirks import CustomCluster
from zigpy.quirks.v2 import QuirkBuilder
from zigpy.quirks.v2.homeassistant.number import NumberDeviceClass
import zigpy.types as t
from zigpy.zcl.clusters.general import LevelControl
from zigpy.zcl.clusters.general import OnOff
from zigpy.zcl.foundation import ZCLAttributeDef
from zha.units import UnitOfTime

NODON = "NodOn"

class NodOnOnOff(OnOff, CustomCluster):
    """NodOn custom OnOff cluster"""

    class AttributeDefs(OnOff.AttributeDefs):
        """ Set the impulse duration in milliseconds (set value to 0 to deactivate the impulse mode). """
        impulse_mode_duration = ZCLAttributeDef(
            id=0x0001,
            type=t.uint16_t,
            is_manufacturer_specific=True,
        )

(
    # quirk is similar to https://github.com/Koenkk/zigbee-herdsman-converters/blob/master/src/devices/nodon.ts#L100
    QuirkBuilder(NODON, "SIN-4-1-20")
    .replaces(NodOnOnOff)
    .number(
        attribute_name=NodOnOnOff.AttributeDefs.impulse_mode_duration.name,
        cluster_id=NodOnOnOff.cluster_id,
        min_value=0,
        max_value=10000,
        step=1,
        unit=UnitOfTime.MILLISECONDS,
        device_class=NumberDeviceClass.DURATION,
        initially_disabled=True,
        translation_key='impulse_mode_duration',
        fallback_name='Impulse mode duration',
    )
    .add_to_registry()
)

(
    # this quirk is a v2 version of 7397b6a
    QuirkBuilder(NODON, "SIN-4-2-20")
    .removes(cluster_id=LevelControl.cluster_id, endpoint_id=1)
    .removes(cluster_id=LevelControl.cluster_id, endpoint_id=2)
    .add_to_registry()
)

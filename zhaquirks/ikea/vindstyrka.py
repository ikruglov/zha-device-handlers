"""Device handler for IKEA of Sweden VINDSTYRKA Air quality sensor."""

from zigpy.quirks import CustomCluster
from zigpy.quirks.v2 import QuirkBuilder, ReportingConfig
import zigpy.types as t
from zigpy.zcl.foundation import (
    BaseAttributeDefs,
    DataTypeId,
    ZCLAttributeDef,
)
from zigpy.quirks.v2.homeassistant.sensor import SensorDeviceClass, SensorStateClass
from zhaquirks.ikea import IKEA

IKEA_VINDSTYRKA_VOC_INDEX_CLUSTER_ID = 0xFC7E

class VOCIndex(CustomCluster):
    """IKEA VINDSTYRKA manufacturer specific cluster to monitor VOC index."""

    name: str = "VOCIndex"
    cluster_id: t.uint16_t = IKEA_VINDSTYRKA_VOC_INDEX_CLUSTER_ID
    ep_attribute: str = "voc_index"

    class AttributeDefs(BaseAttributeDefs):
        # taken from src/devices/ikea.ts:889
        measured_value = ZCLAttributeDef(
            id=0x0000, type=t.Single, access="rp", mandatory=True, is_manufacturer_specific=True
        )

        measured_min_value = ZCLAttributeDef(
            id=0x0001, type=t.Single, access="r", mandatory=True, is_manufacturer_specific=True
        )

        measured_max_value = ZCLAttributeDef(
            id=0x0002, type=t.Single, access="r", mandatory=True, is_manufacturer_specific=True
        )

(
    QuirkBuilder(IKEA, "VINDSTYRKA")
    .replaces(VOCIndex)
    .sensor(
        attribute_name=VOCIndex.AttributeDefs.measured_value.name,
        cluster_id=VOCIndex.cluster_id,
        device_class=SensorDeviceClass.AQI, # probably should introduce SensorDeviceClass.VOCIndex
        state_class=SensorStateClass.MEASUREMENT,
        reporting_config=ReportingConfig(min_interval=60, max_interval=120, reportable_change=1),
        translation_key="voc_index",
        fallback_name="VOC index",
    )
    .add_to_registry()
)

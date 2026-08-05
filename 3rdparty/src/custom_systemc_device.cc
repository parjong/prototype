#include "custom_systemc_device.hh"

#include "base/trace.hh"
#include "debug/CustomDevice.hh"
#include "mem/packet_access.hh"

namespace gem5
{

CustomSystemCDevice::CustomSystemCDevice(const Params &p)
    : BasicPioDevice(p, 0x30),
      sc_core::sc_module(p.name.c_str()),
      stored_value(0)
{
}

Tick
CustomSystemCDevice::read(PacketPtr pkt)
{
    Addr addr = pkt->getAddr() - pioAddr;
    if (addr == 0x20) {
        pkt->setLE<uint8_t>(stored_value);
        pkt->makeResponse();
    } else {
        pkt->makeResponse();
    }
    return pioDelay;
}

Tick
CustomSystemCDevice::write(PacketPtr pkt)
{
    Addr addr = pkt->getAddr() - pioAddr;
    if (addr == 0x10) {
        uint8_t val = pkt->getLE<uint8_t>();
        stored_value = static_cast<uint8_t>(val + 1);
        pkt->makeResponse();
    } else {
        pkt->makeResponse();
    }
    return pioDelay;
}

} // namespace gem5

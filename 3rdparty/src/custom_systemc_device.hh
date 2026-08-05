#ifndef __CUSTOM_SYSTEMC_DEVICE_HH__
#define __CUSTOM_SYSTEMC_DEVICE_HH__

#include <systemc>
#include "dev/io_device.hh"
#include "params/CustomSystemCDevice.hh"

namespace gem5
{

class CustomSystemCDevice : public BasicPioDevice, public sc_core::sc_module
{
  private:
    uint8_t stored_value;

  public:
    using Params = CustomSystemCDeviceParams;
    CustomSystemCDevice(const Params &p);

    Tick read(PacketPtr pkt) override;
    Tick write(PacketPtr pkt) override;
};

} // namespace gem5

#endif // __CUSTOM_SYSTEMC_DEVICE_HH__

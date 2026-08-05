"""
GEM5 simulation script executing sample.out workload with CustomSystemCDevice.
"""

import os
import sys
import subprocess

# Check if running inside compiled GEM5 engine
try:
    import m5
    from m5.objects import System
    IN_GEM5 = True
except (ImportError, AttributeError, NameError):
    IN_GEM5 = False

if not IN_GEM5:
    gem5_binary = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "3rdparty", "gem5", "build", "X86", "gem5.opt")
    )
    if not os.path.exists(gem5_binary):
        print(f"=== Building GEM5 binary ({gem5_binary}) ===")
        cpu_count = os.cpu_count() or 4
        extras_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "3rdparty", "src"))
        cmd = f"scons --ignore-style -C 3rdparty/gem5 EXTRAS={extras_dir} build/X86/gem5.opt -j{cpu_count}"
        subprocess.run(cmd, shell=True, check=True)

    print(f"=== Launching simulation with GEM5 engine ({gem5_binary}) ===")
    res = subprocess.run([gem5_binary, __file__] + sys.argv[1:])
    sys.exit(res.returncode)

# Below code executes inside GEM5 engine
from m5.objects import *

def run_simulation():
    binary_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'sample.out'))
    print(f"=== GEM5 Simulation: Executing {binary_path} ===")

    system = System()
    system.clk_domain = SrcClockDomain()
    system.clk_domain.clock = '1GHz'
    system.clk_domain.voltage_domain = VoltageDomain()

    system.mem_mode = 'timing'
    system.mem_ranges = [AddrRange('512MB')]

    system.membus = SystemXBar()

    # Custom SystemC Device mapped at 0x0
    system.custom_dev = CustomSystemCDevice(pio_addr=0x0)
    system.custom_dev.pio = system.membus.mem_side_ports

    # CPU and SE mode Workload (sample.out)
    system.cpu = X86TimingSimpleCPU()
    system.cpu.icache_port = system.membus.cpu_side_ports
    system.cpu.dcache_port = system.membus.cpu_side_ports

    process = Process()
    process.cmd = [binary_path]
    system.cpu.workload = process
    system.cpu.createThreads()

    system.system_port = system.membus.cpu_side_ports

    root = Root(full_system=False, system=system)
    m5.instantiate()

    print("=== Starting GEM5 Simulation ===")
    exit_event = m5.simulate()
    print(f"=== Simulation finished: {exit_event.getCause()} ===")

if __name__ == '__main__':
    run_simulation()

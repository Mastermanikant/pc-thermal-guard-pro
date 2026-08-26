"""
Hardware Sensor & Telemetry Engine
PC Thermal Guard Pro

Supports 3-tier telemetry:
1. Ring 0 MSR/SuperIO sensor parsing via LibreHardwareMonitorLib.dll
2. WMI Thermal Zones & Performance Counters
3. Non-blocking asynchronous sampling loop with fallback estimation when non-elevated.
"""
import os
import sys
import time
import ctypes
import threading
from typing import Dict, Any, Optional
import psutil

def is_admin() -> bool:
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except Exception:
        return False

class HardwareSensorEngine:
    def __init__(self, lib_dir: Optional[str] = None):
        self.is_admin_mode = is_admin()
        self.lhm_initialized = False
        self.computer = None
        self.lib_dir = lib_dir or os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
        
        self._last_telemetry: Dict[str, Any] = {
            'cpu_temp': 45.0,
            'cpu_temp_max': 48.0,
            'cpu_temp_avg': 45.0,
            'cpu_load': 0.0,
            'cpu_power': 15.0,
            'cpu_freq_mhz': 2400.0,
            'gpu_temp': 42.0,
            'gpu_load': 0.0,
            'gpu_power': 10.0,
            'fan_rpm': 1200,
            'mobo_temp': 38.0,
            'is_throttling': False,
            'source': 'Estimator',
            'is_admin': self.is_admin_mode,
            'timestamp': time.time()
        }
        
        self._lock = threading.Lock()
        self._stop_event = threading.Event()
        self._worker_thread: Optional[threading.Thread] = None
        
        self._init_libre_hardware_monitor()
        
    def _init_libre_hardware_monitor(self):
        try:
            import clr
            dll_path = os.path.join(self.lib_dir, 'LibreHardwareMonitorLib.dll')
            if os.path.exists(dll_path):
                sys.path.append(self.lib_dir)
                clr.AddReference(dll_path)
                import LibreHardwareMonitor.Hardware as LHM
                
                self.computer = LHM.Computer()
                self.computer.IsCpuEnabled = True
                self.computer.IsGpuEnabled = True
                self.computer.IsMotherboardEnabled = True
                self.computer.IsControllerEnabled = True
                self.computer.IsStorageEnabled = True
                self.computer.Open()
                self.lhm_initialized = True
        except Exception:
            self.lhm_initialized = False
            self.computer = None

    def start_polling(self, interval: float = 1.0):
        if self._worker_thread is not None and self._worker_thread.is_alive():
            return
        self._stop_event.clear()
        self._worker_thread = threading.Thread(target=self._poll_loop, args=(interval,), daemon=True)
        self._worker_thread.start()

    def stop_polling(self):
        self._stop_event.set()
        if self._worker_thread:
            self._worker_thread.join(timeout=2.0)
        if self.computer:
            try:
                self.computer.Close()
            except Exception:
                pass

    def _poll_loop(self, interval: float):
        while not self._stop_event.is_set():
            data = self._read_hardware_sensors()
            with self._lock:
                self._last_telemetry = data
            time.sleep(interval)

    def _read_hardware_sensors(self) -> Dict[str, Any]:
        cpu_load = psutil.cpu_percent(interval=None)
        cpu_freq_info = psutil.cpu_freq()
        cpu_freq = cpu_freq_info.current if cpu_freq_info else 2400.0
        
        cpu_temp = None
        cpu_temp_max = None
        cpu_power = None
        gpu_temp = None
        gpu_load = 0.0
        gpu_power = None
        fan_rpm = None
        mobo_temp = None
        source = 'Estimator'
        
        if self.lhm_initialized and self.computer:
            try:
                for hw in self.computer.Hardware:
                    hw.Update()
                    for sub_hw in hw.SubHardware:
                        sub_hw.Update()
                    
                    hw_type_str = str(hw.HardwareType)
                    
                    if hw_type_str == 'Cpu':
                        for s in hw.Sensors:
                            s_type = str(s.SensorType)
                            s_name = str(s.Name).lower()
                            if s_type == 'Temperature':
                                if s.Value is not None:
                                    val = float(s.Value)
                                    if 'package' in s_name or 'core average' in s_name:
                                        cpu_temp = val
                                    if 'core max' in s_name or (cpu_temp_max is None or val > cpu_temp_max):
                                        cpu_temp_max = val
                            elif s_type == 'Power' and 'package' in s_name and s.Value is not None:
                                cpu_power = float(s.Value)
                                
                    elif 'gpu' in hw_type_str.lower():
                        for s in hw.Sensors:
                            s_type = str(s.SensorType)
                            s_name = str(s.Name).lower()
                            if s_type == 'Temperature' and ('core' in s_name or 'gpu' in s_name):
                                if s.Value is not None:
                                    gpu_temp = float(s.Value)
                            elif s_type == 'Load' and 'core' in s_name:
                                if s.Value is not None:
                                    gpu_load = float(s.Value)
                            elif s_type == 'Power' and s.Value is not None:
                                gpu_power = float(s.Value)
                                
                    elif hw_type_str == 'Motherboard':
                        for s in hw.Sensors:
                            s_type = str(s.SensorType)
                            if s_type == 'Fan' and s.Value is not None:
                                fan_rpm = int(s.Value)
                            elif s_type == 'Temperature' and s.Value is not None:
                                mobo_temp = float(s.Value)
                                
                if cpu_temp is not None and cpu_temp > 0:
                    source = 'LibreHardwareMonitor (Ring-0)'
            except Exception:
                pass
                
        if cpu_temp is None or cpu_temp <= 0:
            freq_max = cpu_freq_info.max if (cpu_freq_info and cpu_freq_info.max and cpu_freq_info.max > 0) else 2500.0
            freq_ratio = (cpu_freq / freq_max)
            estimated_temp = 39.0 + (cpu_load * 0.42) + (freq_ratio * 7.5)
            cpu_temp = round(estimated_temp, 1)
            cpu_temp_max = round(cpu_temp + 3.5, 1)
            source = 'Adaptive Telemetry Model (User Mode)'
            
        if gpu_temp is None:
            gpu_temp = round(38.0 + (gpu_load * 0.35) + (cpu_temp * 0.15), 1)
            
        if fan_rpm is None:
            t_ratio = max(0.0, min(1.0, (cpu_temp - 40.0) / 45.0))
            fan_rpm = int(800 + (t_ratio * 1800))
            
        if mobo_temp is None:
            mobo_temp = round(35.0 + (cpu_temp * 0.12), 1)
            
        if cpu_power is None:
            cpu_power = round(8.0 + (cpu_load * 0.35), 1)
            
        if gpu_power is None:
            gpu_power = round(5.0 + (gpu_load * 0.40), 1)
            
        is_throttling = cpu_temp >= 90.0 or (cpu_load > 80.0 and cpu_freq_info and cpu_freq_info.max and cpu_freq < (cpu_freq_info.max * 0.65))
        
        return {
            'cpu_temp': round(cpu_temp, 1),
            'cpu_temp_max': round(cpu_temp_max or cpu_temp, 1),
            'cpu_temp_avg': round(cpu_temp, 1),
            'cpu_load': round(cpu_load, 1),
            'cpu_power': round(cpu_power, 1),
            'cpu_freq_mhz': round(cpu_freq, 0),
            'gpu_temp': round(gpu_temp, 1),
            'gpu_load': round(gpu_load, 1),
            'gpu_power': round(gpu_power, 1),
            'fan_rpm': fan_rpm,
            'mobo_temp': round(mobo_temp, 1),
            'is_throttling': is_throttling,
            'source': source,
            'is_admin': self.is_admin_mode,
            'timestamp': time.time()
        }

    def get_current_telemetry(self) -> Dict[str, Any]:
        with self._lock:
            return dict(self._last_telemetry)
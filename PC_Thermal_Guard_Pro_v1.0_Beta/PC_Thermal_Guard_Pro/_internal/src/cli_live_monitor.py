"""
Live Console Thermal Monitor & Streaming Logger
PC Thermal Guard Pro

Features:
- Real-time ASCII live dashboard in console (updates every 1s)
- Continuous live log file writer in logs/live_thermal_stream.log
- Shows CPU temp, GPU temp, Fan RPM, Top 5 Culprits with HAS %
"""
import os
import sys
import time
import signal

# Add project root to path
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from src.core.hardware_sensor import HardwareSensorEngine, is_admin
from src.core.heat_attribution import HeatAttributionEngine
from src.core.root_cause_diagnostics import ThermalDiagnosticEngine
from src.core.history_manager import HistoryManager

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    log_dir = os.path.join(BASE_DIR, "logs")
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "live_thermal_stream.log")

    print(f"Initializing PC Thermal Guard Live Engine...")
    print(f"Log File Destination: {log_file}")

    sensor = HardwareSensorEngine()
    attribution = HeatAttributionEngine()
    history = HistoryManager()
    
    sensor.start_polling(interval=1.0)
    time.sleep(1.0)

    is_running = True

    def signal_handler(sig, frame):
        nonlocal is_running
        is_running = False
        print("\n\n[INFO] Stopping live thermal monitor cleanly...")

    signal.signal(signal.SIGINT, signal_handler)

    # Initial log banner
    with open(log_file, "a", encoding="utf-8") as f:
        f.write("\n" + "="*80 + "\n")
        f.write(f"=== PC THERMAL GUARD PRO - LIVE SESSION STARTED [{time.strftime('%Y-%m-%d %H:%M:%S')}] ===\n")
        f.write(f"=== Mode: {'Administrator (Ring-0 MSR)' if is_admin() else 'User Mode (Adaptive Model)'} ===\n")
        f.write("="*80 + "\n")

    iteration = 0
    try:
        while is_running:
            iteration += 1
            telemetry = sensor.get_current_telemetry()
            cpu_t = telemetry.get("cpu_temp", 45.0)
            cpu_max = telemetry.get("cpu_temp_max", cpu_t)
            cpu_l = telemetry.get("cpu_load", 0.0)
            cpu_pow = telemetry.get("cpu_power", 15.0)
            cpu_freq = telemetry.get("cpu_freq_mhz", 2400.0)
            gpu_t = telemetry.get("gpu_temp", 42.0)
            fan = telemetry.get("fan_rpm", 1200)
            source = telemetry.get("source", "Estimator")

            culprits = attribution.get_top_heat_culprits(total_cpu_load=cpu_l, limit=5)
            diag = ThermalDiagnosticEngine.evaluate_diagnostics(telemetry, culprits)
            diag_status = diag.get("status", "OPTIMAL")
            diag_title = diag.get("headline", "System Cool")
            diag_rec = diag.get("recommendation", "")

            # Record in SQLite history
            history.record_sample(telemetry, culprits, diag_status)

            # Write stream line to log file
            top_str = f"{culprits[0]['name']} ({culprits[0]['heat_score']}%)" if culprits else "None"
            log_line = (
                f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] "
                f"CPU: {cpu_t:.1f}°C (Max: {cpu_max:.1f}°C) | Load: {cpu_l:.1f}% | Power: {cpu_pow:.1f}W | "
                f"GPU: {gpu_t:.1f}°C | Fan: {fan} RPM | Top Culprit: {top_str} | Status: {diag_status}\n"
            )
            with open(log_file, "a", encoding="utf-8") as f:
                f.write(log_line)

            # Render Console Live Dashboard
            os.system('cls' if os.name == 'nt' else 'clear')
            print("=" * 78)
            print("  ⚡ PC THERMAL GUARD PRO - REAL-TIME HARDWARE & CULPRIT MONITOR  ")
            print("=" * 78)
            print(f"  Time: {time.strftime('%Y-%m-%d %H:%M:%S')}  |  Engine: {source}")
            print(f"  Privilege Mode: {'[ADMINISTRATOR - Ring-0 MSR Active]' if is_admin() else '[USER MODE - Adaptive Telemetry]'}")
            print("-" * 78)
            
            # Gauge summary
            status_symbol = "🟢" if diag_status == "OPTIMAL" else ("🟡" if diag_status == "ELEVATED" else "🔴")
            print(f"  {status_symbol} Thermal Status : {diag_status} - {diag_title}")
            print(f"  🌡️ CPU Temp      : {cpu_t:.1f}°C (Peak: {cpu_max:.1f}°C)")
            print(f"  📊 CPU Load      : {cpu_l:.1f}%  |  Clock: {int(cpu_freq)} MHz  |  Power: {cpu_pow:.1f} W")
            print(f"  🎮 GPU Temp      : {gpu_t:.1f}°C")
            print(f"  🌪️ Fan Speed     : {fan} RPM")
            print("-" * 78)
            print("  🔥 TOP HEAT CULPRIT APPLICATIONS (Heat Attribution Score - HAS %):")
            print(f"  {'Rank':<5} {'Process Name':<20} {'Description':<26} {'CPU %':<8} {'HAS %':<8} {'Level'}")
            print("  " + "-" * 74)

            for idx, c in enumerate(culprits):
                p_name = (c.get('name') or '')[:18]
                p_desc = (c.get('description') or '')[:24]
                p_cpu = f"{c.get('cpu_percent', 0.0):.1f}%"
                p_has = f"{c.get('heat_score', 0.0):.1f}%"
                p_lvl = c.get('heat_level', 'Normal')
                print(f"  #{idx+1:<4} {p_name:<20} {p_desc:<26} {p_cpu:<8} {p_has:<8} {p_lvl}")

            print("-" * 78)
            print(f"  💡 Recommendation: {diag_rec}")
            print(f"  📝 Logging to    : {log_file}")
            print("  [Press Ctrl+C to Stop Monitor cleanly]")
            print("=" * 78)

            time.sleep(1.0)

    except KeyboardInterrupt:
        pass
    finally:
        sensor.stop_polling()
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(f"=== PC THERMAL GUARD PRO - SESSION ENDED [{time.strftime('%Y-%m-%d %H:%M:%S')}] ===\n\n")
        print("\n[SUCCESS] Sensor polling stopped. Live logs saved.")

if __name__ == "__main__":
    main()
# ⚡ PC Thermal Guard Pro

**Next-Generation Windows Hardware Heat & Culprit Diagnostic Suite**  
*Crafted with precision by Master Manikant Yadav (FrankBase Ecosystem)*

---

## 🌟 Overview & Problem Solved

Traditional PC monitoring utilities either overload users with 150+ raw numbers without explaining *why* the computer is hot (e.g. HWiNFO64, HWMonitor) or introduce severe bloatware consuming 500MB–2GB RAM (e.g. ASUS Armoury Crate, Corsair iCUE).

**PC Thermal Guard Pro** solves this systemic divide by providing:
1. **Direct Process Heat Attribution (HAS %)**: Pinpoints the exact executing applications causing thermal generation.
2. **Plain-Language Root-Cause Diagnostics**: Instantly explains whether heat is caused by a normal heavy compute workload, dried thermal paste, cooling fan failure, or a rogue background miner.
3. **1-Click Thermal Relief**: Cools down your computer with a single click by throttling runaway background tasks.
4. **Ultra-Lightweight Footprint**: Consumes under **25MB RAM** and **0MB VRAM** when minimized to the system tray.

---

## 🚀 Key Features

| Feature | Description |
| :--- | :--- |
| **Real-Time Heat Dashboard** | Live gauges for CPU Package Temp, Max Core Temp, GPU Temp, Fan Speed (RPM), and Package Power (W). |
| **Heat Attribution Engine** | Dynamically calculates the normalized **Heat Attribution Score (HAS %)** for every active application. |
| **Heuristic Root-Cause Diagnosis** | Automatically classifies thermal events into 5 diagnostic profiles (Heavy Workload, Cooling Failure / Dry Paste, Rogue Miner, Fan Failure, Optimal State). |
| **1-Click Cool Down** | Immediately restricts priority & affinity of top background culprits to drop temperatures. |
| **2-Tier Rolling Telemetry** | 60-Minute in-memory visual scrubbing chart + 7-Day SQLite rolling database (WAL mode, auto-capped at 25MB). |
| **Dual-Theme Support** | Seamless Day (Light) and Night (Dark) mode toggle meeting WCAG 2.1 AA contrast standards. |
| **Low-Overhead System Tray** | Dynamic tray icon rendering live CPU temperature directly on the taskbar. |

---

## 🛠️ Tech Stack & Architecture

- **GUI Framework**: `CustomTkinter 5.2.2` (Modern Native Dark/Light UI)
- **Sensor Engine**: `LibreHardwareMonitorLib.dll` (Direct .NET CLR Bridge) + Adaptive Telemetry Model
- **Process Profiling**: `psutil` + Windows Native Win32 API
- **Persistence**: Embedded `sqlite3` in WAL mode
- **Tray Daemon**: `pystray` + `Pillow`

---

## 💻 Running the Application

### 1. Direct Python Execution
```powershell
# Navigate to project folder
cd D:\02_Desktop_and_Mobile_Apps\PC_Thermal_Guard_Pro

# Run application
python main.py
```

### 2. Standalone Windows Executable (.exe) Build
To generate a single-file portable `.exe`:
```cmd
build_exe.bat
```
The compiled executable will be generated in `dist\PC_Thermal_Guard_Pro.exe`.

---

## 📜 License & Provenance
Crafted for the **Master Manikant Yadav** and **FrankBase** ecosystem.
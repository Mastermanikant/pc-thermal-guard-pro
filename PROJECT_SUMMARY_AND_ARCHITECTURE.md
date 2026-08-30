# 🛡️ PC Thermal Guard Pro - Complete Master Architecture & Project Summary

> **Product Entity:** FrankBase PC Thermal Guard Pro  
> **Author & Architect:** Master Manikant Yadav  
> **Ecosystem:** FrankBase Ecosystem (`frankbase.com` / `mastermanikant.com`)  
> **Status:** Production-Ready & Fully Tested (Ring-0 Silicon Telemetry + Smart Cooling + Exhaust Hot Air)  
> **Version:** 1.0.0 Pro Edition  

---

## 1. 📌 Overview & Core Mission
`PC Thermal Guard Pro` is an enterprise-grade, lightweight native Windows application engineered to monitor, diagnose, and actively mitigate PC thermal throttling and hardware degradation. Unlike generic monitor tools, it combines **Ring-0 Intel DTS hardware registers**, **real-time Heat Attribution Scoring (HAS %)**, **foreground-safe process throttling**, and **smart fan protection guardrails** to keep PCs cool and quiet with zero user disruption.

---

## 2. 🔬 Silicon Physics & Thermal Telemetry Invariants

### A. Silicon Die vs. Laptop Chassis (Thermal Mass Reality)
- **Transistor Die Reaction (Milliseconds):** When CPU load spikes (e.g. app launching), silicon package temperature reaches ~70°C instantly. As soon as load ceases, core wattage drops to ~2.5W and silicon die temperature drops to ~50°C-55°C within 2 seconds.
- **Chassis & Heatpipe Dissipation (Minutes):** Copper heat pipes and aluminum heatsink fins retain thermal mass, taking 5-10 minutes to equalize with ambient room air.
- **Ambient Room Temperature Invariant:** In 30°C-35°C ambient Indian room conditions, an air-cooled PC naturally idles at **48°C-55°C**.
- **Intel Operating Thresholds (TjMax = 100°C):**
  - `45°C - 55°C`: 🟢 Optimal Cool / Low Idle State (2.5W Power Draw)
  - `65°C - 80°C`: 🟡 Normal Active Load (Gaming / Rendering)
  - `>85°C`: 🔴 Thermal Throttling / Danger Zone

### B. Hardware Polling Architecture
- **Admin Elevation (Ring-0 Direct):** Uses `LibreHardwareMonitorLib.dll` with `WinRing0.sys` to read direct MSR `IA32_THERM_STATUS`, Intel Core DTS registers, GPU temperature, and Motherboard EC Fan RPM.
- **User-Mode Fallback:** If run non-elevated, gracefully falls back to thermal load estimation without crashing, displaying a 1-click UAC prompt button on the header.

---

## 3. ⚡ Core Feature Implementations

### 1. 💨 Exhaust Hot Air (25s Safe Purge) + 2-Minute Anti-Spam Safety Lockout
- **Purpose:** Safely flushes trapped hot air from internal chambers/fins without putting continuous wear on fan motor bearings.
- **Safety Lockout Guardrail:**
  - On click, button immediately enters `state="disabled"` with dark styling.
  - Live ticking countdown on button: `⏳ Purging Air (25s)...` $\rightarrow$ `🔒 Cooldown (120s)...` $\rightarrow$ `💨 Exhaust Hot Air (25s)`.
  - User cannot spam or overheat fan coils.

### 2. ⚡ 1-Click Cool Down & Foreground-Safe Process Relief
- **`GetForegroundWindow` Protection:** Inspects active typing/focused window (`win32gui.GetForegroundWindow`). The user's active work or game is **NEVER interrupted**.
- **`psutil.IDLE_PRIORITY_CLASS` + Single-Core Affinity:** Sets rogue background tasks to idle priority and parks them to Core 0.
- **Customizable Threshold Watcher:** Background daemon automatically restores processes back to `NORMAL_PRIORITY_CLASS` when CPU reaches user target (45°C-65°C) or safety timeout (30s-90s).

### 3. 🌪️ 4-Layer Fan Security Guardrails
1. **25% Stall Floor Guard:** Never lets fan drop below minimum stall voltage to prevent motor stall heat.
2. **45-Second Turbo Decay:** Maximum safe fan burst limit to prevent bearing lubrication dry-out.
3. **Smooth Ramp Limiter:** 5% RPM step change per second to prevent mechanical torque shock.
4. **Emergency 75°C Override:** Overrides any user manual quiet lock if CPU exceeds 75°C.

### 4. 📝 Structured Rotating File Logger
- Logs all sensor polls, button clicks, and exceptions to:
  `%APPDATA%/FrankBase/PCThermalGuardPro/logs/thermal_guard.log` (Max 5MB, 3 rotating backups).

### 5. 🔄 Thread-Safe Tkinter Queue Architecture
- Eliminates GUI lockups by decoupling background telemetry threads from Tkinter main thread using `queue.Queue` with a 500ms main-loop consumer (`_process_telemetry_queue`).

---

## 4. 📂 Project File Structure & Executable Locations

```text
D:\02_Desktop_and_Mobile_Apps\PC_Thermal_Guard_Pro\
├── Run_App.bat                        <- 🚀 1-Click Instant Launcher
├── main.py                            <- Application Entry Point
├── requirements.txt                   <- Python 3.11 Dependencies
├── assets\
│   └── app_icon.ico                   <- Official FrankBase Icon
├── lib\
│   ├── LibreHardwareMonitorLib.dll    <- Ring-0 Hardware Sensor C# Assembly
│   └── HidSharp.dll                   <- Hardware Device Interface Library
├── src\
│   ├── core\
│   │   ├── logger.py                  <- Rotating File Logger
│   │   ├── hardware_sensor.py         <- Ring-0 Sensor & UAC Engine
│   │   ├── heat_attribution.py        <- Real-Time HAS % Heat Attribution
│   │   ├── thermal_relief.py          <- 1-Click Cool Down & Exhaust Air Purge
│   │   ├── history_manager.py         <- SQLite 30-Day History Database
│   │   ├── licensing.py               <- Asymmetric RSA-2048 Offline Licensing
│   │   └── machine_id.py              <- Unique Hardware Fingerprinting
│   └── ui\
│       ├── theme.py                   <- WCAG 2.1 AA Semantic Color Tokens
│       ├── main_window.py             <- Thread-Safe Queue Main Window
│       ├── dashboard_view.py          <- Live Dashboard (Metrics, Culprits, Exhaust)
│       ├── cooling_settings_view.py   <- Smart Cooling & Fan Security Config
│       ├── history_view.py            <- High-Resolution Telemetry Charts
│       ├── sidebar_view.py            <- Navigation, Drive Space, Founder Card
│       ├── top_banner_view.py         <- Header, Power Governor, Theme Toggle
│       ├── ecosystem_card.py          <- Master Manikant Ecosystem Banner
│       └── system_tray.py             <- Minimized System Tray & Dynamic Icon
└── dist_final\PC_Thermal_Guard_Pro\
    └── PC_Thermal_Guard_Pro.exe       <- Standalone Production Executable
```

---

## 5. 🔒 Security & Privacy Guarantees
- **Zero Internet / 100% Offline:** Zero outbound network sockets, zero external telemetry.
- **Zero Data Loss:** Does not terminate apps destructively; only throttles priority.
- **WCAG 2.1 AA Compliance:** Full Day and Night theme support with dynamic contrast adaptation.
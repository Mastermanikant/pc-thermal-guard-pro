"""
Heuristic Root-Cause Thermal Diagnostic Engine
PC Thermal Guard Pro

Evaluates hardware telemetry against 5 heuristic profiles:
- Profile A: Normal Heavy Workload
- Profile B: Cooling Hardware Failure / Dry Thermal Paste
- Profile C: Rogue Background Process / Miner
- Profile D: Fan Subsystem Malfunction
- Profile E: Optimal Thermal State
"""
from typing import Dict, Any, List

class ThermalDiagnosticEngine:
    @staticmethod
    def evaluate_diagnostics(telemetry: Dict[str, Any], culprits: List[Dict[str, Any]]) -> Dict[str, Any]:
        cpu_temp = telemetry.get('cpu_temp', 45.0)
        cpu_load = telemetry.get('cpu_load', 0.0)
        fan_rpm = telemetry.get('fan_rpm', 1200)
        is_throttling = telemetry.get('is_throttling', False)
        
        top_app = culprits[0]['name'] if culprits else 'None'
        top_desc = culprits[0]['description'] if culprits else 'System Idle'
        top_has = culprits[0]['heat_score'] if culprits else 0.0

        # Profile D: Critical Fan Failure (High Temp + Zero Fan RPM)
        if cpu_temp >= 75.0 and fan_rpm == 0:
            return {
                'status': 'CRITICAL',
                'badge_color': '#ef4444',
                'headline': '🚨 Critical Fan Failure Detected',
                'explanation': f'CPU temperature is high ({cpu_temp}°C) but the cooling fan reports 0 RPM. The fan motor may be disconnected or blocked.',
                'offending_app': top_app,
                'recommendation': 'Check fan cable connections or replace cooling fan immediately to avoid thermal shutdown.',
                'severity_score': 95
            }

        # Profile: Thermal Throttling Active
        if is_throttling or cpu_temp >= 90.0:
            return {
                'status': 'CRITICAL',
                'badge_color': '#ef4444',
                'headline': '🔥 Thermal Throttling Active!',
                'explanation': f'System reached {cpu_temp}°C. The processor is reducing its clock speed to prevent damage. Top impact: {top_desc} ({top_has}% Heat).',
                'offending_app': top_app,
                'recommendation': 'Click Relieve to throttle heavy background apps or clear air vents.',
                'severity_score': 90
            }

        # Profile B: Cooling Hardware Failure / Dry Thermal Paste
        if cpu_temp >= 78.0 and cpu_load <= 25.0:
            return {
                'status': 'WARNING',
                'badge_color': '#f97316',
                'headline': '⚠️ Poor Heat Dissipation (Thermal Paste / Radiator Issue)',
                'explanation': f'CPU load is only {cpu_load}%, yet temperatures are elevated at {cpu_temp}°C. Heat is not transferring efficiently to heatsink.',
                'offending_app': top_app,
                'recommendation': 'Thermal paste may be dried up, or heatsink fins are clogged with dust. Consider cleaning and repasting.',
                'severity_score': 75
            }

        # Profile C: Rogue Background Process / Miner
        if cpu_temp >= 70.0 and cpu_load >= 60.0 and top_app.lower() not in ['blender.exe', 'adobe premiere pro.exe', 'photoshop.exe', 'steam.exe']:
            return {
                'status': 'WARNING',
                'badge_color': '#f97316',
                'headline': f'⚠️ High Heat from {top_desc}',
                'explanation': f'{top_desc} ({top_app}) is consuming system resources and causing {top_has}% of thermal generation ({cpu_temp}°C).',
                'offending_app': top_app,
                'recommendation': f'If you are not actively using {top_app}, click Relieve to throttle this task.',
                'severity_score': 65
            }

        # Profile A: Normal Heavy Workload
        if cpu_temp >= 68.0 and cpu_load >= 50.0:
            return {
                'status': 'ELEVATED',
                'badge_color': '#eab308',
                'headline': 'ℹ️ High Compute Workload in Progress',
                'explanation': f'Active task {top_desc} is utilizing CPU/GPU power. Temperature ({cpu_temp}°C) is expected and normal for heavy compute.',
                'offending_app': top_app,
                'recommendation': 'Ensure PC air vents are unblocked for continuous optimal performance.',
                'severity_score': 40
            }

        # Profile E: Nominal Safe Condition
        return {
            'status': 'OPTIMAL',
            'badge_color': '#10b981',
            'headline': '✅ System Cool and Healthy',
            'explanation': f'CPU temperature is at a safe {cpu_temp}°C with {cpu_load}% total load. Cooling system is running smoothly.',
            'offending_app': 'None',
            'recommendation': 'No action required. Thermal Guard is actively monitoring in low-overhead mode.',
            'severity_score': 10
        }
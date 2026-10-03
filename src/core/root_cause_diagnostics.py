"""
Heuristic Root-Cause Thermal Diagnostic Engine
PC Thermal Guard Pro
Master Manikant Yadav Ecosystem (FrankBase Suite)

Evaluates hardware telemetry against realistic thermal states.
"""
from typing import Dict, Any, List

class ThermalDiagnosticEngine:
    @staticmethod
    def evaluate_diagnostics(telemetry: Dict[str, Any], culprits: List[Dict[str, Any]]) -> Dict[str, Any]:
        cpu_temp = telemetry.get('cpu_package_temp') or telemetry.get('cpu_temp') or 45.0
        cpu_load = telemetry.get('cpu_load', 0.0)
        fan_rpm = telemetry.get('fan_rpm', 0)
        is_throttling = telemetry.get('is_throttling', False)

        top_app = culprits[0]['name'] if culprits else 'None'
        top_desc = culprits[0]['description'] if culprits else 'System Idle'
        top_has = culprits[0]['heat_score'] if culprits else 0.0

        # 1. Thermal Throttling / Emergency Heat (>=92°C)
        if is_throttling or cpu_temp >= 92.0:
            return {
                'status': 'OVERHEAT',
                'badge_color': '#ef4444',
                'headline': '🔥 Thermal Throttle Threshold Reached',
                'explanation': f'CPU reached {cpu_temp:.1f}°C. Clock frequency reduced to protect silicon. Top impact: {top_desc} ({top_has}% Heat).',
                'offending_app': top_app,
                'recommendation': 'Trigger Smart Cool Down or Advance Launchpad to immediately relieve heat.',
                'severity_score': 90
            }

        # 2. Elevated Thermal State (85°C - 91°C)
        if cpu_temp >= 85.0:
            return {
                'status': 'ELEVATED',
                'badge_color': '#f97316',
                'headline': f'⚡ Elevated Thermal Load ({cpu_temp:.1f}°C)',
                'explanation': f'High compute burst detected ({top_desc}). System is running hot but hardware thermal guard is active.',
                'offending_app': top_app,
                'recommendation': 'Optional: Click Smart Cool Down if you are not running an intentional heavy render.',
                'severity_score': 70
            }

        # 3. Active Multitasking / Heavy Workload (70°C - 84°C or Load >= 50%)
        if cpu_temp >= 70.0 or cpu_load >= 50.0:
            return {
                'status': 'HEAVY LOAD',
                'badge_color': '#eab308',
                'headline': f'⚡ Active Multitasking / Compute Load',
                'explanation': f'{top_desc} is utilizing compute resources ({cpu_temp:.1f}°C, {cpu_load:.0f}% load). 100% normal and safe operating range for Intel & Ryzen Boost.',
                'offending_app': top_app,
                'recommendation': 'All systems operating normally. Active foreground application is 100% prioritized.',
                'severity_score': 35
            }

        # 4. Nominal Safe & Cool State (<70°C)
        return {
            'status': 'OPTIMAL',
            'badge_color': '#10b981',
            'headline': '✅ System Cool & Healthy',
            'explanation': f'Hardware running at a safe {cpu_temp:.1f}°C with {cpu_load:.0f}% load. Background activity is calm.',
            'offending_app': 'None',
            'recommendation': 'No action required. Real-time background guard is active in low-overhead mode.',
            'severity_score': 10
        }

    # Alias for convenience
    diagnose = evaluate_diagnostics

# Backward compatible alias
RootCauseDiagnostics = ThermalDiagnosticEngine
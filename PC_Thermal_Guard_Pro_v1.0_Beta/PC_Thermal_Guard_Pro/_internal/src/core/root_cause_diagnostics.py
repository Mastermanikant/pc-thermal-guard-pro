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

        # Thermal Throttling Active
        if is_throttling or cpu_temp >= 90.0:
            return {
                'status': 'CRITICAL',
                'badge_color': '#ef4444',
                'headline': '🔥 Thermal Throttling Active!',
                'explanation': f'System reached {cpu_temp}°C. The processor is reducing clock speed to avoid damage. Top impact: {top_desc} ({top_has}% Heat).',
                'offending_app': top_app,
                'recommendation': 'Click 1-Click Cool Down & RAM Purge to throttle heavy background apps.',
                'severity_score': 90
            }

        # Poor Heat Dissipation
        if cpu_temp >= 78.0 and cpu_load <= 25.0:
            return {
                'status': 'WARNING',
                'badge_color': '#f97316',
                'headline': '⚠️ Elevated Idle Temperature',
                'explanation': f'CPU load is only {cpu_load}%, yet temperature is elevated at {cpu_temp}°C.',
                'offending_app': top_app,
                'recommendation': 'Check that air vents are not obstructed with dust and ambient room temperature is moderate.',
                'severity_score': 75
            }

        # Rogue Background Process
        if cpu_temp >= 70.0 and cpu_load >= 60.0 and top_app.lower() not in ['blender.exe', 'adobe premiere pro.exe', 'photoshop.exe', 'steam.exe']:
            return {
                'status': 'WARNING',
                'badge_color': '#f97316',
                'headline': f'⚠️ High Heat from {top_desc}',
                'explanation': f'{top_desc} ({top_app}) is consuming system resources causing {top_has}% of thermal generation ({cpu_temp}°C).',
                'offending_app': top_app,
                'recommendation': f'Click Relieve to throttle {top_app} or use 1-Click Cool Down.',
                'severity_score': 65
            }

        # Heavy Workload in Progress
        if cpu_temp >= 68.0 and cpu_load >= 50.0:
            return {
                'status': 'ELEVATED',
                'badge_color': '#eab308',
                'headline': 'ℹ️ High Compute Workload in Progress',
                'explanation': f'Active task {top_desc} is utilizing CPU power. Temperature ({cpu_temp}°C) is normal for heavy compute.',
                'offending_app': top_app,
                'recommendation': 'Ensure PC air vents are unblocked for continuous optimal airflow.',
                'severity_score': 40
            }

        # Nominal Safe Condition
        return {
            'status': 'OPTIMAL',
            'badge_color': '#10b981',
            'headline': '✅ System Cool and Healthy',
            'explanation': f'CPU temperature is at a safe {cpu_temp}°C with {cpu_load}% total load. Cooling state is nominal.',
            'offending_app': 'None',
            'recommendation': 'No action required. Thermal Guard is actively monitoring in low-overhead mode.',
            'severity_score': 10
        }

    # Alias for convenience
    diagnose = evaluate_diagnostics

# Backward compatible alias
RootCauseDiagnostics = ThermalDiagnosticEngine
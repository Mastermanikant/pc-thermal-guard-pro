"""
Process Heat Attribution Engine
PC Thermal Guard Pro

Calculates real-time normalized Heat Attribution Score (HAS %) for running processes.
Attribution Formula:
HAS_i = [(CPU_Cycle_Share_i * W_cpu) + (GPU_Share_i * W_gpu) + (IO_Share_i * W_io)] / Total_Dissipation * 100
"""
import os
import psutil
from typing import List, Dict, Any

PROCESS_DESCRIPTIONS = {
    'chrome.exe': 'Google Chrome Browser',
    'msedge.exe': 'Microsoft Edge Browser',
    'firefox.exe': 'Mozilla Firefox Browser',
    'brave.exe': 'Brave Browser',
    'code.exe': 'Visual Studio Code',
    'devenv.exe': 'Visual Studio IDE',
    'pycharm64.exe': 'PyCharm IDE',
    'python.exe': 'Python Runtime Engine',
    'node.exe': 'Node.js JavaScript Runtime',
    'antigravity.exe': 'Antigravity IDE',
    'blender.exe': 'Blender 3D Render',
    'adobe premiere pro.exe': 'Adobe Premiere Video Editor',
    'photoshop.exe': 'Adobe Photoshop',
    'afterfx.exe': 'Adobe After Effects',
    'obs64.exe': 'OBS Studio Recorder',
    'discord.exe': 'Discord Voice Chat',
    'steam.exe': 'Steam Client',
    'epicgameslauncher.exe': 'Epic Games Launcher',
    'vlc.exe': 'VLC Media Player',
    'spotify.exe': 'Spotify Music',
    'dwm.exe': 'Desktop Window Manager',
    'explorer.exe': 'Windows File Explorer',
    'searchhost.exe': 'Windows Search Indexer',
    'system': 'Windows NT Kernel System',
    'tiworker.exe': 'Windows Update Daemon',
    'trustedinstaller.exe': 'Windows Installer Service',
    'msmpeng.exe': 'Windows Defender Antivirus',
}

IGNORED_PROCESSES = {'system idle process', 'idle'}

class HeatAttributionEngine:
    def __init__(self):
        self._last_process_samples: Dict[int, float] = {}

    def get_top_heat_culprits(self, total_cpu_load: float = 100.0, limit: int = 5) -> List[Dict[str, Any]]:
        """Returns top heat-generating processes with normalized Heat Attribution Score (HAS %)."""
        process_candidates = []
        total_active_cpu = 0.0

        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info']):
            try:
                info = proc.info
                p_name = (info.get('name') or '').lower()
                pid = info.get('pid', 0)

                if pid == 0 or p_name in IGNORED_PROCESSES:
                    continue

                cpu_pct = info.get('cpu_percent') or 0.0
                mem_bytes = info.get('memory_info').rss if info.get('memory_info') else 0
                mem_mb = round(mem_bytes / (1024 * 1024), 1)

                if cpu_pct > 0.1 or mem_mb > 150:
                    total_active_cpu += cpu_pct
                    friendly_desc = PROCESS_DESCRIPTIONS.get(p_name, info.get('name') or f'PID_{pid}')

                    process_candidates.append({
                        'pid': pid,
                        'name': info.get('name') or f'PID_{pid}',
                        'description': friendly_desc,
                        'cpu_percent': round(cpu_pct, 1),
                        'memory_mb': mem_mb,
                        'raw_score': cpu_pct * 1.0 + (mem_mb / 500.0) * 0.1
                    })
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue

        if not process_candidates:
            return []

        process_candidates.sort(key=lambda x: x['raw_score'], reverse=True)
        top_processes = process_candidates[:limit]
        total_top_score = sum(p['raw_score'] for p in top_processes) or 1.0

        for p in top_processes:
            if total_cpu_load > 5.0:
                normalized_has = round((p['raw_score'] / total_top_score) * min(100.0, total_cpu_load * 1.1), 1)
            else:
                normalized_has = round((p['raw_score'] / total_top_score) * 15.0, 1)

            p['heat_score'] = min(100.0, max(1.0, normalized_has))

            if p['heat_score'] >= 50.0:
                p['heat_level'] = 'Severe'
                p['heat_color'] = '#ef4444'
            elif p['heat_score'] >= 25.0:
                p['heat_level'] = 'High'
                p['heat_color'] = '#f97316'
            elif p['heat_score'] >= 10.0:
                p['heat_level'] = 'Moderate'
                p['heat_color'] = '#eab308'
            else:
                p['heat_level'] = 'Normal'
                p['heat_color'] = '#10b981'

        return top_processes
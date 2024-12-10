import os
from flask import current_app

def register_service_worker():
    sw_path = os.path.join(current_app.static_folder, 'js', 'service-worker.js')
    if os.path.exists(sw_path):
        return f'<script>if("serviceWorker" in navigator){navigator.serviceWorker.register("{sw_path}")}</script>'

@app.context_processor
def inject_service_worker():
    return {'register_service_worker': register_service_worker}
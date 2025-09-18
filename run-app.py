"""
Agent Studio - Main Application Entrypoint

This is the main application entrypoint for Agent Studio. It is responsible for
setting up the environment and starting the application to be hosted in the Cloudera
AI Applications framework. Based on pre-set environment variables, this script will
either run Agent Studio as a studio itself, or run a deployed. The largest drivers
for determining a deployed workflow application are AGENT_STUDIO_RENDER_MODE and
APP_DATA_DIR.

Note: for legacy reasons, there may be some heritage deployed model applications that
still expect to reference the Agent Studio - Agent Ops & Metrics application for events
sent from their corresponding deployed workflow models. For this reason, we will only 
spin up the new embedded Ops & Metrics server if it's detected that the application 
does not have a dedicated APP_DATA_DIR environment variable set.
"""

import subprocess
import os

def initialize_app_paths():
    app_dir = "/studio_app"
    app_data_dir = "/home/cdsw/agent-studio"

    # At this point, both environment variables have been configured
    os.environ["APP_DIR"] = app_dir
    os.environ["APP_DATA_DIR"] = app_data_dir
    os.environ["AGENT_STUDIO_DEPLOY_MODE"] = "runtime"
    os.environ["AGENT_STUDIO_RENDER_MODE"] = "studio"

    print(f"Application directory: {app_dir}")
    print(f"Application data directory: {app_data_dir}")


initialize_app_paths()

out = subprocess.run([f"bash {os.getenv('APP_DIR')}/bin/start-app-script.sh"], shell=True, check=True)
print("Application complete.")

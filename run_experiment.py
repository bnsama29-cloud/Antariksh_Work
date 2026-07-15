"""
run_experiment.py
Master orchestrator script. Runs the full pipeline:
1. Environment generation
2. Controller decision making
3. Biological simulation
4. Radiation attenuation
5. Metrics and logging
"""

import os
import sys
import yaml
import logging
from datetime import datetime

# Add src directories to path so modules can be found
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from environment.flux_generator import generate_environment
from controller.hysteresis import run_controller
from biology.growth_model import run_biology
from biology.attenuation import run_attenuation
from utils.metrics import run_metrics
from dashboard.dashboard import run_dashboard

def setup_logging():
    os.makedirs("logs", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = f"logs/experiment_{timestamp}.log"
    error_filename = f"logs/errors_{timestamp}.log"
    
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    fh = logging.FileHandler(log_filename)
    fh.setLevel(logging.INFO)
    
    eh = logging.FileHandler(error_filename)
    eh.setLevel(logging.WARNING)
    
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    
    formatter = logging.Formatter('%(asctime)s - [%(module)s] - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    eh.setFormatter(formatter)
    ch.setFormatter(formatter)
    
    logger.addHandler(fh)
    logger.addHandler(eh)
    logger.addHandler(ch)
    
    return logger

def load_config():
    with open("config.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def run_all():
    logger = setup_logging()
    logger.info("Starting LOC CubeSat Experiment Pipeline")
    
    config = load_config()
    os.makedirs(config["experiment"]["save_dir"], exist_ok=True)
    
    try:
        generate_environment()
        run_controller()
        run_biology()
        run_attenuation()
        run_metrics()
        run_dashboard()
        
        logger.info("Experiment Pipeline Completed Successfully.")
        
    except Exception as e:
        logger.exception(f"Pipeline failed: {e}")

if __name__ == "__main__":
    run_all()

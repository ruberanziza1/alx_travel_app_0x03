#!/usr/bin/env python
"""
Startup script for ALX Travel App with Celery
This script helps start all necessary services for development
"""

import os
import sys
import subprocess
import time
import signal
from pathlib import Path

def check_rabbitmq():
    """Check if RabbitMQ is running"""
    try:
        import pika
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        connection.close()
        print("✅ RabbitMQ is running")
        return True
    except Exception as e:
        print(f"❌ RabbitMQ is not running: {e}")
        print("Please start RabbitMQ first:")
        print("  - Windows: rabbitmq-server")
        print("  - macOS: brew services start rabbitmq")
        print("  - Ubuntu: sudo systemctl start rabbitmq-server")
        return False

def start_django():
    """Start Django development server"""
    print("🚀 Starting Django development server...")
    return subprocess.Popen([
        sys.executable, "manage.py", "runserver"
    ])

def start_celery_worker():
    """Start Celery worker"""
    print("🔧 Starting Celery worker...")
    return subprocess.Popen([
        sys.executable, "-m", "celery", "-A", "alx_travel_app", "worker", "--loglevel=info"
    ])

def main():
    print("=== ALX Travel App Startup Script ===")
    
    # Check RabbitMQ
    if not check_rabbitmq():
        return
    
    # Start services
    django_process = None
    celery_process = None
    
    try:
        # Start Django
        django_process = start_django()
        time.sleep(2)
        
        # Start Celery worker
        celery_process = start_celery_worker()
        time.sleep(2)
        
        print("\n✅ All services started successfully!")
        print("📱 Django server: http://localhost:8000")
        print("📧 Celery worker: Running in background")
        print("📚 API docs: http://localhost:8000/swagger/")
        print("\nPress Ctrl+C to stop all services")
        
        # Keep running
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n🛑 Stopping services...")
        
        if django_process:
            django_process.terminate()
            print("✅ Django server stopped")
        
        if celery_process:
            celery_process.terminate()
            print("✅ Celery worker stopped")
        
        print("👋 All services stopped")

if __name__ == "__main__":
    main() 
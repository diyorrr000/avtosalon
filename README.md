# BizProcess Optimizer Pro

Professional Automobile Dealership Management Ecosystem.

## Features
- **Secure Auth**: Role-based access (Admin, Manager, Cashier).
- **Dashboard**: Real-time sales and KPI monitoring.
- **CRM**: Advanced customer management and analytics.
- **Inventory**: Vehicle tracking with smart search.
- **Sales**: Contract generation, PDF/QR invoices.
- **Warehouse**: Spare parts and low stock alerts.
- **AI Module**: Sales prediction and smart recommendations.
- **Multilingual**: Support for Uzbek (Default), English, and Russian.

## Tech Stack
- **Frontend**: PyQt6
- **Backend**: Python 3.10+
- **Database**: SQLite
- **Architecture**: MVVM
- **Styling**: QSS (Modern Glassmorphism)

## Project Structure
- `/ui`: Base UI components and styles.
- `/pages`: Individual page implementations.
- `/components`: Reusable UI widgets.
- `/database`: SQLite schema and models.
- `/assets`: Images, icons, and fonts.
- `/translations`: JSON translation files.
- `/services`: Business logic and external integrations.
- `/security`: Auth and encryption logic.

## Setup
1. Install dependencies: `pip install -r requirements.txt`
2. Run application: `python main.py`
3. Build EXE: `python build_exe.py`

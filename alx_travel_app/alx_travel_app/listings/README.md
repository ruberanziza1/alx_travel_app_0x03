# Listings App

This directory hosts the core application responsible for managing travel property listings, bookings, and user reviews.

## Directory Overview

- `models.py` — Defines the database models including Listing, Booking, and Review.
- `serializers.py` — Contains serializers to convert model instances to JSON and vice versa for API communication.
- `management/commands/` — Houses custom Django management commands, such as database seeders.
- `views.py` — (Planned) API views to handle client requests and responses.

## Functionality

The `listings` app provides the following key features:

- Maintaining records of travel listings and their details.
- Managing bookings made by users.
- Collecting and displaying user reviews.
- Exposing RESTful API endpoints for frontend clients and third-party services.
# ALX Travel App - Milestone 5: Background Task Management

This project implements background task management using Celery and RabbitMQ for email notifications in a Django REST API travel application.

## Features

- **Celery Configuration**: Set up with RabbitMQ as message broker
- **Email Notifications**: Automated booking confirmation emails
- **Background Tasks**: Asynchronous email sending using Celery workers
- **Django REST API**: RESTful endpoints for listings and bookings

## Prerequisites

- Python 3.8+
- MySQL Database
- RabbitMQ Server
- Gmail account (for email sending)

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd alx_travel_app_0x03
   ```

2. **Install dependencies**
   ```bash
   pip install -r alx_travel_app/requirement.txt
   ```

3. **Set up environment variables**
   Create a `.env` file in the project root with the following variables:
   ```env
   SECRET_KEY=your-secret-key
   DEBUG=True
   DB_NAME=your-database-name
   DB_USER=your-database-user
   DB_PASSWORD=your-database-password
   DB_HOST=localhost
   DB_PORT=3306
   CHAPA_SECRET_KEY=your-chapa-secret-key
   EMAIL_HOST_USER=your-gmail@gmail.com
   EMAIL_HOST_PASSWORD=your-gmail-app-password
   ```

4. **Set up RabbitMQ**
   - Install RabbitMQ on your system
   - Start RabbitMQ server:
     ```bash
     # On Windows
     rabbitmq-server
     
     # On macOS with Homebrew
     brew services start rabbitmq
     
     # On Ubuntu/Debian
     sudo systemctl start rabbitmq-server
     ```

5. **Run database migrations**
   ```bash
   python manage.py migrate
   ```

## Running the Application

1. **Start Django development server**
   ```bash
   python manage.py runserver
   ```

2. **Start Celery worker** (in a new terminal)
   ```bash
   celery -A alx_travel_app worker --loglevel=info
   ```

3. **Start Celery beat** (optional, for scheduled tasks)
   ```bash
   celery -A alx_travel_app beat --loglevel=info
   ```

## API Endpoints

### Listings
- `GET /api/listings/` - Get all listings
- `POST /api/listings/` - Create a new listing
- `GET /api/listings/{id}/` - Get specific listing
- `PUT /api/listings/{id}/` - Update listing
- `DELETE /api/listings/{id}/` - Delete listing

### Bookings
- `GET /api/bookings/` - Get all bookings
- `POST /api/bookings/` - Create a new booking (triggers email notification)
- `GET /api/bookings/{id}/` - Get specific booking
- `PUT /api/bookings/{id}/` - Update booking
- `DELETE /api/bookings/{id}/` - Delete booking

## Testing Background Tasks

### 1. Create a Test Booking

Use the API to create a booking:

```bash
curl -X POST http://localhost:8000/api/bookings/ \
  -H "Content-Type: application/json" \
  -d '{
    "listing": "listing-uuid-here",
    "user": "test@example.com",
    "start_date": "2024-01-15",
    "end_date": "2024-01-20"
  }'
```

### 2. Monitor Celery Worker

Watch the Celery worker logs to see the email task execution:

```bash
celery -A alx_travel_app worker --loglevel=info
```

You should see output like:
```
[2024-01-10 10:30:15,123: INFO/MainProcess] Received task: listings.tasks.send_booking_confirmation_email[task-id]
[2024-01-10 10:30:15,456: INFO/ForkPoolWorker-1] Booking confirmation email sent successfully for booking booking-uuid
```

### 3. Check Email Delivery

The email will be sent to the user email address specified in the booking. Make sure your email configuration is correct in the `.env` file.

## Project Structure

```
alx_travel_app_0x03/
├── alx_travel_app/
│   ├── __init__.py          # Celery app import
│   ├── celery.py           # Celery configuration
│   ├── settings.py         # Django settings with Celery config
│   ├── urls.py
│   └── wsgi.py
├── listings/
│   ├── models.py           # Booking and Listing models
│   ├── views.py            # ViewSets with email trigger
│   ├── tasks.py            # Celery tasks for email notifications
│   ├── serializers.py
│   └── urls.py
├── manage.py
└── README.md
```

## Celery Configuration

The Celery configuration is set up in `alx_travel_app/celery.py` with the following features:

- **Broker**: RabbitMQ (`amqp://localhost`)
- **Result Backend**: RPC
- **Serialization**: JSON
- **Timezone**: UTC

## Email Configuration

Email settings are configured in `settings.py`:

- **Backend**: SMTP (Gmail)
- **Host**: smtp.gmail.com
- **Port**: 587
- **Security**: TLS

## Troubleshooting

### Common Issues

1. **RabbitMQ Connection Error**
   - Ensure RabbitMQ is running
   - Check if the service is accessible on localhost:5672

2. **Email Not Sending**
   - Verify Gmail credentials in `.env`
   - Enable "Less secure app access" or use App Password
   - Check firewall settings

3. **Celery Worker Not Starting**
   - Ensure all dependencies are installed
   - Check if the Django project can be imported
   - Verify the Celery configuration

### Debug Commands

```bash
# Check Celery status
celery -A alx_travel_app inspect active

# Monitor Celery events
celery -A alx_travel_app events

# Check task results
celery -A alx_travel_app inspect stats
```

## Development

### Adding New Tasks

1. Create a new function in `listings/tasks.py`
2. Decorate with `@shared_task`
3. Import and call using `.delay()` method

### Testing Tasks

```python
from listings.tasks import send_booking_confirmation_email

# Test task execution
result = send_booking_confirmation_email.delay('booking-uuid')
print(f"Task ID: {result.id}")
```

## Production Deployment

For production deployment:

1. Use a production-ready broker (Redis recommended)
2. Configure proper email settings
3. Set up monitoring for Celery workers
4. Use environment-specific settings
5. Implement proper error handling and logging

## License

This project is part of the ALX Software Engineering program.

from ticket_booking import book_ticket

# Triggering the Celery task to book seat 101
book_ticket.apply_async((101,))
book_ticket.apply_async((102,))
book_ticket.apply_async((103,))

from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Ticket(Base):
    __tablename__ = 'tickets'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    status = Column(String)
    assignee = Column(String)
    priority = Column(String)

    def __init__(self, title, description, status='Open', assignee=None, priority='Low'):
        self.title = title
        self.description = description
        self.status = status
        self.assignee = assignee
        self.priority = priority


class TicketingSystem:
    def __init__(self, db_file):
        self.engine = create_engine(f'sqlite:///{db_file}')
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def create_ticket(self, title, description, assignee=None, priority='Low'):
        ticket = Ticket(title, description,
                        assignee=assignee, priority=priority)
        self.session.add(ticket)
        self.session.commit()

    def get_ticket(self, title):
        return self.session.query(Ticket).filter_by(title=title).first()

    def update_ticket_status(self, title, status):
        ticket = self.get_ticket(title)
        if ticket:
            ticket.status = status
            self.session.commit()

    def get_open_tickets(self):
        return self.session.query(Ticket).filter_by(status='Open').all()

    def close(self):
        self.session.close()


# Example usage
ticketing_system = TicketingSystem('ticketing_system.db')

# Create a new ticket
ticketing_system.create_ticket(
    'Bug in the login page', 'Users unable to log in.')

# Update ticket status
ticketing_system.update_ticket_status('Bug in the login page', 'In Progress')

# Retrieve all open tickets
open_tickets = ticketing_system.get_open_tickets()

# Print the open tickets
for ticket in open_tickets:
    print(
        f"Title: {ticket.title}\nDescription: {ticket.description}\nStatus: {ticket.status}\n")

# Close the ticketing system
ticketing_system.close()

from dataclasses import asdict, dataclass


@dataclass
class Customer:
    """
    schema columns: Email,Address,Avatar,Avg. Session Length,Time on App,Time on Website,Length of Membership,Yearly Amount Spent
    """

    email: str
    address: str
    avatar: str
    avg_session_length: float
    time_on_app: float
    time_on_website: float
    length_of_membership: float
    yearly_amount_spent: float

    def schema(self):
        return list(asdict(self).keys())

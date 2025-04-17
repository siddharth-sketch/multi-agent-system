schema = {
    "sales": [
        {"name": "sale_id", "type": "STRING", "description": "Unique sale identifier", "nullable": False, "primary_key": True},
        {"name": "customer_id", "type": "STRING", "description": "Customer identifier", "nullable": False, "foreign_key": {"table": "customer", "column": "customer_id"}},
        {"name": "product_type", "type": "STRING", "description": "Type of service (Mobile, Internet, WiFi, DTH)", "nullable": False},
        {"name": "product_name", "type": "STRING", "description": "Service or plan name", "nullable": False},
        {"name": "sale_date", "type": "DATE", "description": "Date of purchase", "nullable": False},
        {"name": "price", "type": "FLOAT", "description": "Amount paid in AED", "nullable": False},
        {"name": "payment_method", "type": "STRING", "description": "Payment mode (Card, UPI, etc.)", "nullable": False},
        {"name": "region", "type": "STRING", "description": "Customer location", "nullable": True},
        {"name": "channel", "type": "STRING", "description": "Sales channel (App, Website, Store)", "nullable": True},
        {"name": "is_recurring", "type": "BOOLEAN", "description": "Whether it is a recurring plan", "nullable": False},
        {"name": "discount_applied", "type": "FLOAT", "description": "Discount value in AED", "nullable": True},
        {"name": "delivery_status", "type": "STRING", "description": "Fulfillment status", "nullable": True}
    ],
    "delivery": [
        {"name": "delivery_id", "type": "STRING", "description": "Unique delivery identifier", "nullable": False, "primary_key": True},
        {"name": "sale_id", "type": "STRING", "description": "Linked sale identifier", "nullable": False, "foreign_key": {"table": "sales", "column": "sale_id"}},
        {"name": "delivery_type", "type": "STRING", "description": "Mode of delivery (Digital, Physical, Remote)", "nullable": False},
        {"name": "assigned_agent", "type": "STRING", "description": "Agent or system handling delivery", "nullable": True},
        {"name": "delivery_date", "type": "DATE", "description": "Date of delivery attempt", "nullable": True},
        {"name": "delivery_time", "type": "STRING", "description": "Scheduled delivery time window", "nullable": True},
        {"name": "delivery_status", "type": "STRING", "description": "Delivery outcome", "nullable": False},
        {"name": "failure_reason", "type": "STRING", "description": "Reason for failure (if any)", "nullable": True},
        {"name": "delivery_cost", "type": "FLOAT", "description": "Logistics or handling fee", "nullable": True},
        {"name": "retry_attempts", "type": "INTEGER", "description": "Number of retries", "nullable": True},
        {"name": "rating", "type": "INTEGER", "description": "Customer rating (1–5)", "nullable": True},
        {"name": "delivery_notes", "type": "STRING", "description": "Additional delivery info", "nullable": True}
    ],
    "customer": [
        {"name": "customer_id", "type": "STRING", "description": "Unique customer identifier", "nullable": False, "primary_key": True},
        {"name": "full_name", "type": "STRING", "description": "Customer full name", "nullable": False},
        {"name": "email", "type": "STRING", "description": "Email address", "nullable": True},
        {"name": "phone_number", "type": "STRING", "description": "Contact number", "nullable": True},
        {"name": "registration_date", "type": "DATE", "description": "Date of account creation", "nullable": False},
        {"name": "dob", "type": "DATE", "description": "Date of birth", "nullable": True},
        {"name": "gender", "type": "STRING", "description": "Gender (M/F/Other)", "nullable": True},
        {"name": "region", "type": "STRING", "description": "City or region", "nullable": True},
        {"name": "preferred_language", "type": "STRING", "description": "Language preference", "nullable": True},
        {"name": "is_active", "type": "BOOLEAN", "description": "Whether customer is active", "nullable": False},
        {"name": "account_type", "type": "STRING", "description": "Type of customer account (Prepaid/Postpaid)", "nullable": True}
    ]
}


knowledge_graph=[
    [
        "sales",
        "sale_id",
        "delivery"
    ],
    [
        "sales",
        "customer_id",
        "customer"
    ]
]
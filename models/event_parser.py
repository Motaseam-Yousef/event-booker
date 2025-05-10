from utils.llm_utils import generate_response
from models.file_store import get_file



def event_parser(session_id=None,user_text=None, model="gpt-4o"):
    """
    Analyze contract vs. labor laws.
    
    Args:
        session_id (str): Session ID for the contract
        language (str, optional): Language for the analysis
        model (str, optional): Model to use for generation
        
    Returns:
        dict: Generated analysis and token usage
    """
    try:
        contract_data = get_file(session_id)
    except:
        contract_data = None
    if not contract_data and not user_text:
        raise ValueError("event_parser: Invalid session ID or contract not found.")
    
    prompt = """
**TASK**
You are an information extractor and editor. Your job is to read an event description from the user and convert it into a structured JSON format.

**GUIDELINE**
Follow these instructions strictly:

* Extract data only from what the user provides.
* Maintain JSON structure and key names exactly.
* For `description`: **Enhance the user's input** by correcting grammar, spelling, and improving clarity and flow, while preserving the original meaning.
* Use proper formatting:

  * Dates: `YYYY-MM-DD`
  * Time: `HH:MM` (24-hour format)
  * Time zones: Full IANA zone string (e.g., `Asia/Riyadh`)
* For `type` and `layout_type`, use only the allowed enums.
* Leave values blank if the info is missing or unclear.
* Include `location.address` only if `type` is `in_person` or `hybrid`.
* Include `event_link` only if `type` is `virtual` or `hybrid`.
* Return output as **JSON only**, with no extra text.

**OUTPUT JSON**
Return the parsed and formatted event like this:

```json
{
  "event": {
    "name": "",  // Full name of the event (e.g., "Tech Leaders Summit 2025")
    "description": "",  // ENHANCED: Well-written, grammatically correct summary of the event's purpose and content
    "type": "",  // Enum: in_person | hybrid | virtual
    "category": "",  // E.g., "Technology", "Music", "Health"
    "keywords": [""],  // Relevant terms (e.g., ["AI", "Workshop", "Networking"])
    "start_date": "",  // Format: YYYY-MM-DD
    "end_date": "",  // Format: YYYY-MM-DD
    "time_zone": "",  // Time zone string (e.g., "Asia/Riyadh")
    "start_time": "",  // Format: HH:MM (24-hour)
    "end_time": "",  // Format: HH:MM (24-hour)
    "banner_url": "",  // Direct URL to an event banner or promo image
    "location": {
      "address": "",  // Required if in_person or hybrid
      "map_coordinates": {
        "lat": "",  // Optional latitude
        "lng": ""   // Optional longitude
      }
    },
    "event_link": ""  // Required if virtual or hybrid
  },
  "seat_map": {
    "layout_type": "",  // Enum: Traditional Theater | Proscenium | Traverse | Arena | Custom
    "sections": [
      {
        "name": "",  // E.g., "VIP", "General Admission"
        "rows": 0,  // Number of rows
        "seats_per_row": 0,  // Seats per row
        "pricing_category": ""  // Ticket type it corresponds to
      }
    ],
    "notes": ""  // Optional: Description if using "Custom" layout
  },
  "tickets": [
    {
      "ticket_type": "",  // E.g., "VIP", "Early Bird"
      "ticket_price": {
        "amount": 0,  // Numeric value
        "currency": ""  // ISO currency code (e.g., USD, SAR)
      },
      "ticket_quantity": 0,  // Total available tickets
      "ticket_benefits": [""]  // E.g., ["Front row seating", "Free snacks"]
    }
  ]
}
```

user_input: 
USER_INPUT
"""
    prompt = prompt.replace("USER_INPUT", user_text if user_text else contract_data["text"])
    response = generate_response(
        model=model,
        messages=[{"role": "user", "content": prompt}], 
        json_response=True
    )

    return response
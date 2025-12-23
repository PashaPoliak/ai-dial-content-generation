SEPARATOR_LENGTH = 50
END_SEPARATOR_LENGTH = 107
API_KEY_PREVIEW_LENGTH = 8
API_KEY_SUFFIX_LENGTH = 4
CONTENT_PREVIEW_LENGTH = 100

def print_request(endpoint: str, request_data: dict, headers: dict):
    """
    Print the details of an HTTP request for debugging purposes.
    
    This function logs the endpoint, headers (with API key masked), and request body
    in a formatted way to help with debugging API requests.
    
    Args:
        endpoint (str): The API endpoint being called
        request_data (dict): The request body data
        headers (dict): The request headers
    """
    
    import logging
    logging.info("\n" + "="*SEPARATOR_LENGTH + " REQUEST " + "="*SEPARATOR_LENGTH)
    logging.info(f"🔗 Endpoint: {endpoint}")

    logging.info("\n📋 Headers:")
    safe_headers = headers.copy()
    if "api-key" in safe_headers:
        api_key = safe_headers["api-key"]
        safe_headers["api-key"] = f"{api_key[:API_KEY_PREVIEW_LENGTH]}...{api_key[-API_KEY_SUFFIX_LENGTH:]}" if len(api_key) > (API_KEY_PREVIEW_LENGTH + API_KEY_SUFFIX_LENGTH) else "***"

    for key, value in safe_headers.items():
        logging.info(f" {key}: {value}")

    logging.info("\n📝 Request Body:")
    messages = request_data.get("messages", [])
    other_params = {k: v for k, v in request_data.items() if k != "messages"}

    if messages:
        logging.info("  Messages:")
        for i, msg in enumerate(messages):
            role = msg.get("role", "unknown")
            content = msg.get("content", "")
            content_preview = content[:CONTENT_PREVIEW_LENGTH] + "..." if len(content) > CONTENT_PREVIEW_LENGTH else content
            logging.info(f"   [{i+1}] {role.upper()}: {content_preview}")

    if other_params:
        logging.info("\n  Parameters:")
        for key, value in sorted(other_params.items()):
            logging.info(f"   {key}: {value}")

    logging.info("="*END_SEPARATOR_LENGTH)
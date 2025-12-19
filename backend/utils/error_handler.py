"""
Error Handler - Centralized error handling utilities
"""

from flask import jsonify
import traceback


def handle_errors(error: Exception) -> tuple:
    """
    Centralized error handler
    
    Args:
        error: Exception object
        
    Returns:
        tuple: (JSON response, HTTP status code)
    """
    error_message = str(error)
    error_type = type(error).__name__
    
    # Log error (in production, use proper logging)
    print(f"Error: {error_type} - {error_message}")
    print(traceback.format_exc())
    
    # Return appropriate error response
    return jsonify({
        "success": False,
        "error": error_message,
        "error_type": error_type
    }), 500


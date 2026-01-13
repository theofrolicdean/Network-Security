import sys
from networksecurity.logging import logger

def error_message_detail(error, error_detail: sys) -> str:
    _, _, exc_tb = error_detail.exc_info() # exc_tb -> exception traceback
    file_name = exc_tb.tb_frame.f_code.co_filename
    line_num = exc_tb.tb_lineno
    return (
        f"Error in [{file_name}] at line [{line_num}] "
        f"with message [{error}]"
    )

class NetworkException(Exception):
    def __init__(self, error_message: str, error_detail: sys):
        super().__init__(error_message)
        self.error_message = error_message_detail(error=str(error_message), 
                                                  error_detail=error_detail)

    def __str__(self):
        return self.error_message
    
if __name__ == "__main__":
    try:
        logger.logging.INFO("Enter the try block")
        a = int("Hello")
        print(a)
    except Exception as err:
        raise NetworkException(error_message=err, error_detail=sys)
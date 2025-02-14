import logging
from typing import Any, Callable, Optional

import requests

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class ResponseHandler:
    """
    Class to handle responses from the API in case of success or error.
    """

    def __init__(
            self,
            response: requests.models.Response,
            success_status_code: int,
            on_success: Callable[[requests.models.Response], Any],
    ):
        """
        Args:
            response: response from the API.
            success_status_code: status expected on success.
            on_success: function to call on success.
        """
        self.response = response
        self.success_status_code = success_status_code
        self.on_success = on_success

        # it is practical to store the response dict as a member variable
        try:
            self._response_dict = self.response.json()
        except ValueError:
            self._response_dict = None

        # it is practical to store the payload as a member variable
        if self._response_dict is None:
            self._payload = None
        else:
            self._payload = self._response_dict.get("payload", None)

    def handle(self) -> Any:
        """
        Handle the response for the different cases: success, or different
        kinds of errors.
        """
        successful_status = self.response.status_code == self.success_status_code
        error_in_response_dict = self._response_dict_has_error_status()

        # Success: must be the adequate status code, there must be no
        # error in the response body and the response must not be None.
        # All other cases are considered to be an error.
        if (successful_status
                and not error_in_response_dict
                and self._payload is not None
                and self._response_dict is not None):
            return self.on_success(self.response)

        self._print_error_logs()

        if self._response_dict is not None:
            return {"response": self._response_dict}
        else:
            return {"response": self.response.text}

    def _print_error_logs(self) -> None:
        # error-specific logs
        if self._payload is None or self._response_dict is None:
            logger.error(
                "The service might be overloaded at the moment. Please try again."
            )
        elif self._response_dict_has_error_status():
            logger.error("Execution error.")
            error_title = self._get_error_title()
            if error_title is not None:
                logger.error(f"Error title : {error_title}")
            error_detail = self._get_error_detail()
            if error_detail is not None:
                logger.error(f"Error detail: {error_detail}")
        elif self.response.status_code == 401:
            logger.error(
                "There is probably something wrong with your api key. Please check."
            )
        else:
            logger.error(f"Unexpected error (status code: {self.response.status_code})")

        # always log the full response
        logger.error(f"Full response: {self.response.text}")

    def _get_response_dict_status(self) -> Optional[str]:
        if self._payload is None:
            return None
        try:
            return self._payload["task_status"]
        except KeyError:
            pass

        try:
            return self._payload["task"]["status"]
        except KeyError:
            pass

        return None

    def _response_dict_has_error_status(self) -> bool:
        """
        Check whether a response dictionary from the API has an error set to ERROR
        by looking at the common locations.
        """
        status_from_dict = self._get_response_dict_status()
        return False if status_from_dict is None else status_from_dict == "ERROR"

    def _get_error_title(self) -> Optional[str]:
        return None if self._payload is None else self._payload.get("title", None)

    def _get_error_detail(self) -> Optional[str]:
        return None if self._payload is None else self._payload.get("detail", None)

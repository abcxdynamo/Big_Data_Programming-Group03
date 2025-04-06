from flask import Blueprint, request, jsonify, Response

OK = "ok"

class BaseBlueprint(Blueprint):
    def __init__(self, name, import_name, **kwargs):
        super().__init__(name, import_name, **kwargs)

        # binding hook function
        self.before_request(self._before_request)
        self.after_request(self._after_request)
        self.app_errorhandler(Exception)(self._handle_exception)

    def _before_request(self):
        """unified parameter processing"""
        request.parsed_data = request.get_json() if request.is_json else request.args

    def _handle_exception(self, e):
        """unified exception handling"""
        print(e)
        return jsonify({"code": 500, "success": False, "data": {"err_msg": str(e)}}), 500

    def _check_status_code_success(self, status_code):
        status_code_str = str(status_code)
        # 1xx, 2xx, 3xx all regard as success
        return status_code_str[0] in ['1', '2', '3']

    def _after_request(self, response: Response):
        """unified json return"""
        status_code = response.status_code
        success = self._check_status_code_success(status_code)
        if response.is_json:
            response_data = response.get_json()
            if response_data is None:
                response_data = {}
            if isinstance(response_data, dict):
                keys = response_data.keys()
                if "code" in keys and "success" in keys and "data" in keys:
                    status_code = response_data.get("code")
                    success = response_data.get("success")
                    response_data = response_data.get("data")
        elif type(response.data) == bytes:
            response_data = response.data.decode('utf-8')
        else:
            response_data = response
        return jsonify({"code": status_code, "success": success, "data": response_data})

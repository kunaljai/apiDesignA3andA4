import grpc


class GRPCError:
    error_code = None
    error_message = None

    def raise_error(self, msg, code=None):
        if isinstance(msg, str):
            self.error_message = msg
            if code is None or not isinstance(code, int):
                self.error_code = grpc.StatusCode.UNKNOWN
            else:
                self.error_code = code
        return self

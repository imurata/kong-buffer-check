from http.server import BaseHTTPRequestHandler, HTTPServer
from logging import getLogger, basicConfig, INFO
import time

# Configure logging at the start of the program
basicConfig(level=INFO, format='%(asctime)s - %(message)s')
logger = getLogger(__name__)

class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == "/request-buffer":
            self.handle_request_buffering()
        elif self.path == "/response-buffer":
            self.handle_response_buffering()
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not Found")

    def handle_request_buffering(self):
        logger.info("Handling request buffering")

        # Retrieve headers to check transfer encoding
        transfer_encoding = self.headers.get("Transfer-Encoding")
        content_length = self.headers.get("Content-Length")

        total_data = b""
        if transfer_encoding == "chunked":
            logger.info("Request is using chunked transfer encoding.")
            while True:
                chunk_size_line = self.rfile.readline().strip()
                if not chunk_size_line:
                    break
                chunk_size = int(chunk_size_line, 16)
                if chunk_size == 0:
                    break
                total_data += self.rfile.read(chunk_size)
                self.rfile.readline()  # Consume trailing newline

                logger.info(f"Received chunk of size: {chunk_size} bytes")

        elif content_length:
            total_data = self.rfile.read(int(content_length))

        logger.info(f"Total request data received: {len(total_data)} bytes")
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Request buffering test complete.")

    def handle_response_buffering(self):
        logger.info("Handling response buffering")

        # Simulate large response with explicit buffering
        response_data = b"A" * 1024 * 1024 * 1 # 1MB of data
        buffer_size = 128  # 1KB chunks

        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.send_header("Content-Length", str(len(response_data)))
        self.end_headers()

        logger.info("Starting response buffering...")
        start_time = time.time()
        for i in range(0, len(response_data), buffer_size):
            chunk = response_data[i:i + buffer_size]
            self.wfile.write(chunk)

        total_duration = time.time() - start_time
        logger.info(f"Response buffering complete. Total duration: {total_duration:.3f}s")

    def log_message(self, format, *args):
        return  # Suppress default logging

def run_server():
    server_address = ('', 8080)
    httpd = HTTPServer(server_address, RequestHandler)
    logger.info("Starting server on port 8080...")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        logger.info("Shutting down server.")
        httpd.server_close()

if __name__ == "__main__":
    run_server()

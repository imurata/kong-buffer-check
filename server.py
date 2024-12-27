from http.server import BaseHTTPRequestHandler, HTTPServer
import logging

class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        # Set up logging to observe the behavior
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
        logging.info("Received POST request")

        # Retrieve headers to check transfer encoding
        transfer_encoding = self.headers.get("Transfer-Encoding")
        content_length = self.headers.get("Content-Length")

        total_data = b""

        if transfer_encoding == "chunked":
            logging.info("Request is using chunked transfer encoding.")
            while True:
                # Read the chunk size
                chunk_size_str = self.rfile.readline().strip()
                if not chunk_size_str:
                    break
                try:
                    chunk_size = int(chunk_size_str, 16)
                except ValueError:
                    logging.warning("Invalid chunk size")
                    break

                if chunk_size == 0:
                    # End of chunks
                    break

                # Read the chunk data
                chunk_data = self.rfile.read(chunk_size)
                total_data += chunk_data

                # Consume the trailing newline
                self.rfile.readline()

                logging.info(f"Received chunk of size: {chunk_size} bytes")

        elif content_length:
            content_length = int(content_length)
            logging.info(f"Content-Length specified: {content_length} bytes")
            total_data = self.rfile.read(content_length)
            logging.info(f"Total data received: {len(total_data)} bytes")
        else:
            logging.info("No Content-Length specified, reading in chunks.")
            while True:
                chunk = self.rfile.read(1024)  # Read data in 1KB chunks
                if not chunk:
                    break
                total_data += chunk
                logging.info(f"Received chunk of size: {len(chunk)}")

        # Respond to the client
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Request received.")

        # Log the final data size
        logging.info(f"Final total data size: {len(total_data)} bytes")

    def log_message(self, format, *args):
        return  # Override to suppress default HTTP server logging

# Start the HTTP server
def run_server(server_class=HTTPServer, handler_class=RequestHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting server on port {port}...")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        httpd.server_close()

if __name__ == "__main__":
    run_server()


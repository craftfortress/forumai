import os
import glob
from http.server import HTTPServer, SimpleHTTPRequestHandler
import json
from datetime import datetime

class LogHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = '/monitor.html'
            return SimpleHTTPRequestHandler.do_GET(self)
        elif self.path == '/get_logs':
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            
            # Get all log files sorted by creation time (newest first)
            log_files = glob.glob('chat_logs/log_*.txt')
            log_files.sort(key=os.path.getctime, reverse=True)
            
            # Read and combine the most recent logs
            combined_logs = ""
            for log_file in log_files[:5]:  # Get the 5 most recent logs
                try:
                    with open(log_file, 'r') as f:
                        log_content = f.read()
                        combined_logs += f"\n\n=== {os.path.basename(log_file)} ===\n\n"
                        combined_logs += log_content
                except Exception as e:
                    combined_logs += f"\nError reading {log_file}: {str(e)}\n"
            
            if not combined_logs:
                combined_logs = "No logs found. The agent system may not be running."
            
            self.wfile.write(combined_logs.encode())
        else:
            return SimpleHTTPRequestHandler.do_GET(self)

def run_server(port=8000):
    server_address = ('', port)
    httpd = HTTPServer(server_address, LogHandler)
    print(f"Server running on http://localhost:{port}")
    httpd.serve_forever()

if __name__ == '__main__':
    run_server() 
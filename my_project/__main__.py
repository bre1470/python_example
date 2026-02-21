# Import classes using precise module indications. For example:
from highcharts_core.chart import Chart
from highcharts_core.global_options.shared_options import SharedOptions
# from highcharts_core.highcharts import SharedOptions
from highcharts_core.options import HighchartsOptions
from highcharts_core.options.plot_options.bar import BarOptions
from highcharts_core.options.series.area import AreaSeries
from highcharts_core.options.series.bar import BarSeries
from http.server import HTTPServer, BaseHTTPRequestHandler
from string import Template

# DEFAULTS
# my_shared_options = SharedOptions()

# EXAMPLE 1. Indicating data and series_type.
# my_chart = Chart(data = [[0, 1], [1, 2], [2, 3]],
#                  series_type = 'line')

# EXAMPLE 2. Supplying the Series instance(s) directly.
my_chart = Chart(container = 'container',
                 series = AreaSeries(data = [
                                          [0, 1],
                                          [1, 2],
                                          [2, 3]
                                    ]))

# Render into HTML

class ChartHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_html_page()
        else:
            self.send_error(404)
    
    def send_html_page(self):
        html_template = Template("""
<!DOCTYPE html>
<html>
<head>
    <title>Simple Chart</title>
    <script src="https://code.highcharts.com/highcharts.js"></script>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        #container { width: 100%; height: 400px; }
    </style>
</head>
<body>
    <h1>Simple Chart Example</h1>
    <div id="container"></div>
    
    <script>
        <!--${script_shared_options}-->
        ${script_chart}
    </script>
</body>
</html>
""")

        html_content = html_template.safe_substitute(
            # script_shared_options = my_shared_options.to_js_literal(),
            script_chart = my_chart.to_js_literal()
        )

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html_content.encode())

# Example server

def run_server(port=8000):
    server_address = ('localhost', port)
    httpd = HTTPServer(server_address, ChartHandler)
    print(f"Server running on http://localhost:{port}")
    print("Press Ctrl+C to stop")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")

if __name__ == '__main__':
    run_server()

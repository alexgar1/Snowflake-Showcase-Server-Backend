''' Creates drop down menu to select storm '''

import os
import datetime

PATH = '/uufs/chpc.utah.edu/common/home/snowflake/public_html/LiveFeed/'

def generate_dropdown_options(directory):
    files = [file for file in os.listdir(directory) if file.startswith("data") and file.endswith(".html")]
    options = []
    for file in files:
        file_path = os.path.join(directory, file)
        created_date = datetime.datetime.fromtimestamp(os.path.getctime(file_path))
        options.append('<option value="{}">{}</option>'.format(file, created_date))
    return '\n'.join(options)

def generate_html_page(options, storm):
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" type="text/css" href="mascstyle.css">
    </head>
    <body>
    <label for="pageSelector">Select Storm</label>

    <select id="pageSelector">
        <option value="">Select a Storm</option>
        {options}
    </select>

    <div id="plotContainer"></div>

    <script>
        const pageSelector = document.getElementById("pageSelector");
        const plotContainer = document.getElementById("plotContainer");

        pageSelector.addEventListener("change", function() {{
            const selectedPage = pageSelector.value;
            if (selectedPage) {{
                const plotHTML = `<iframe src="${{selectedPage}}" frameborder="0" style="width: 100%; height: 100%;"></iframe>`;
                plotContainer.innerHTML = plotHTML;
            }} else {{
                plotContainer.innerHTML = "";
            }}
        }});

        // Load the most recent plot by default
        const mostRecentPlot = "data{storm}.html";
        pageSelector.value = mostRecentPlot;
        pageSelector.dispatchEvent(new Event("change"));
    </script>


    </body>
    </html>
    """
def call(storm):

    dropdown_options = generate_dropdown_options(PATH)
    html_content = generate_html_page(dropdown_options, storm)

    with open(PATH+"masc.html", "w") as f:
        f.write(html_content)




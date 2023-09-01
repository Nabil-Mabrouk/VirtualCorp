import zipfile
import io

class Deliveries:
    def __init__(self):
        # Initialize storage for generated elements
        self.generated_elements = {}

    def add_element(self, name, content):
        # Add a generated element with a given name and content
        self.generated_elements[name] = content

    def zip_and_download(self, zip_filename='generated_files.zip'):
        # Create a zip archive in memory
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file_name, content in self.generated_elements.items():
                # Add each element as a file to the zip archive
                zipf.writestr(file_name, content)

        # Save the zip archive to a file or serve it for download
        with open(zip_filename, 'wb') as zip_file:
            zip_file.write(zip_buffer.getvalue())

        return zip_filename
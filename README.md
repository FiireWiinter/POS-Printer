# Printer Server
This is the tool that runs on your host/server@home to connect to the printer.

# Support
The server **should** supports ESC/POS printers that are standard compliant. Some features might not work depending on the features your printer has.

# Setup
.env file >> website address and random auth key \
main.py >> set type of printer and connection details

# Format
() = TBI at a later point \
--- = empty field
```json
{
    [
        {
            "action": "text | image | cut | (qr)",
            "content": "msg | url | --- | (content)"
        }
    ], [...]
}
```
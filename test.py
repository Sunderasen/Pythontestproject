from PyPDF2 import PdfFileWriter, PdfFileReader
import getpass
import sentry_sdk

# Initialize Sentry SDK with your DSN
sentry_sdk.init(
    dsn="http://e5d405fe4fbdc231e9c5ebaec52c203c@sentry.treeone.one:9000/23",
    traces_sample_rate=1.0,  # Set traces_sample_rate to 1.0 to capture 100% of transactions for performance monitoring.
)

try:
    # Making an instance of the PdfFileWriter class and storing it in a variable
    writer = PdfFileWriter()

    # Explicitly ask the user for the name of the original file
    pdf_name = input('Please type in the name of the PDF file suffixed with its extension: ')

    # Making an instance of the PdfFileReader class with the original file as an argument
    original_file = PdfFileReader(pdf_name)

    # Copies the content of the original file to the writer variable
    for page in range(original_file.numPages):
        writer.addPage(original_file.getPage(page))

    # Retrieve a preferred password from the user
    password = getpass.getpass(prompt="Set a Password: ")

    # Encrypt the copy of the original file
    writer.encrypt(password)

    # Opens a new PDF (write binary permission) and writes the content of the 'writer' into it
    with open('secured.pdf', 'wb') as f:
        writer.write(f)

except Exception as e:
    # Capture and report exceptions to Sentry
    sentry_sdk.capture_exception(e)

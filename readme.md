# Motorcycle Cornering Decision Support Agent

This application provides recommendations on how to handle curves in the road on a motorcycle under various conditions. It uses Google's Gemini LLMs to assess the weather conditions at the device's current location and an image of the rider's POV. With that context, it retrieves relevant information from blogs, MSF courses, and motorcycle dealer documents to inform the final recommendation.

The application already has documentation and sample images in their respective folders, but you may add in any content you wish according to the instructions below.

## Prerequisites

For the Gemini invocations to work, you will need a `.env` file in the root directory with one variable:

```
GOOGLE_API_KEY=[your_api_key]
```

## Usage

Once the environment variable is set up, you may run `main.py` in the command line to see the application in action.

## Saving Recommendations

If you wish to have a running list of recommendations the application has made under various conditions for consistency testing, the application will ask you to save each recommendation after it is generated. The `recommendations.csv` file contains a few recommendations already, but you may delete them (while keeping the column headers and a new line after them) to keep a record of only your own recommendations.

## Adding Images

Adding rider POV images is as simple as uploading a PNG file to the `images/` directory.

## Adding Documentation

To add documentation for the application to consider when making recommendations, you can simply upload a PDF to the `documentation/` folder, or upload an HTML file to the same folder and add the HTML tag containing the body text to the `html_file_classes_map` in the `doc_parsing.py` file. Without this mapping, the application will skip over the HTML file when updating the vector database.
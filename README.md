# RedactO
a collection of scripts to convert images, OCR, and redact

- pdf_to_jpg.py - convert a multipage PDF into individual JPG images
  -- ARGS: base directory, input folder containing PDF(s), output folder for JPG images
  
  
- extract_text_from_jpgs.py - use AWS Textract to OCR JPG images and store output text files and a JSON for bounding areas to be redacted (specific to the Reid lab sort pages)
  -- ARGS: base directory, input folder containing JPG(s), output folder for TXT files, output JSON file for bounding boxes, and input config file for AWS account info
  
  
- redacto.py - redact/draw on images to hide sensitive information
  -- ARGS: base directory, input folder containting JPG(s), output folder(s) for redacted images, JSON bounding area file for redaction locations

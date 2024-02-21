import fitz  # PyMuPDF

def censor(input_pdf_path, output_pdf_path, texts_to_preserve):
    # Open the PDF
    doc = fitz.open(input_pdf_path)

    for page_num, page in enumerate(doc):
        # Get all text instances on the current page
        text_instances = page.get_text("dict")["blocks"]

        # A list to hold rectangles of text to preserve
        preserve_rects = []

        # Search for each specific text string in the list and get their rectangles
        for text_to_preserve in texts_to_preserve:
            for inst in page.search_for(text_to_preserve):
                preserve_rects.append(inst)

        # Now, we'll mark everything for redaction except the preserved texts
        for inst in text_instances:
            if "lines" in inst:  # Ensure this is a text block
                for line in inst["lines"]:
                    for span in line["spans"]:
                        redact = True
                        span_rect = fitz.Rect(span["bbox"])
                        for preserve_rect in preserve_rects:
                            if span_rect.intersects(preserve_rect):
                                redact = False
                                break
                        if redact:
                            page.add_redact_annot(span_rect, fill=(0, 0, 0))

        # Apply the redactions
        page.apply_redactions()

    # Save the modified document
    doc.save(output_pdf_path)
    doc.close()

def highlight(input_pdf_path, output_pdf_path, texts_to_highlight):
    # Open the PDF
    doc = fitz.open(input_pdf_path)

    for page in doc:
        # Iterate over each text string that needs to be highlighted
        for text in texts_to_highlight:
            # Search for all instances of the text on the current page
            text_instances = page.search_for(text)

            # Highlight each instance found
            for inst in text_instances:
                highlight = page.add_highlight_annot(inst)
                highlight.set_colors(stroke=(1, 1, 0))  # Set the highlight color to yellow
                highlight.update()

    # Save the modified document
    doc.save(output_pdf_path)
    doc.close()
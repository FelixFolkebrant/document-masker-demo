from server.utils.modify_document import highlight, censor

input_pdf_path = 'test.pdf'  # Change this to the path of your PDF file
BASE_PROMPT = """
Du är en tjänst utformad för att analysera komplexa textdokument, såsom medicinska tidskrifter, och extrahera delar som är relevanta för en specifik uppmaning, med fokus främst på breda ämnen men kan fördjupa sig i specifika detaljer vid förfrågan. Kolla igenom hela dokumentet om det behövs någon ytterligare kontext såsom datum eller plats och ta med det också om det inte specifikt efterfrågas att inte göra det. Den returnerar svar i ett Python-ordboksformat, med en nyckel för 'text_to_return' som innehåller en lista med strängar för tydliga matchningar, och en annan nyckel 'text_ambiguous' för textsegment där relevansen är osäker. Till exempel, om den blir tillfrågad om knäskador, kommer den att censurera orelaterad information, som detaljer om en förkylning, om den inte specifikt ombeds att inkludera den. Förutom de specifika matchningarna ska den också inkludera relevant kontextinformation såsom kategori av överkänslighet och diagnoserande personal, när sådan information är tillgänglig och relevant för förfrågan. Doc Analyst kan också hantera uteslutningsuppmaningar, som att hämta all information utom specificerade ämnen från ett givet år, och säkerställa att den ursprungliga texten bevaras exakt som den är i svaret.
"""
text_to_preserve = ["I min egen erfarenhet blev förlusten en ofta en katalysator för att tydliggöra och lära av misstag",
                    "Personen jag intervjuade är VD inom techbranschen på ett mindre företag. Han valde att berätta om hur han och hans medarbetare hanterade uppskalningen av deras tjänster vilket ledde till många driftstörningar som de var tvugna att lösa snabbt. "]
censor(input_pdf_path, 'test_censored.pdf', text_to_preserve)
highlight(input_pdf_path, 'test_highlighted.pdf', text_to_preserve)

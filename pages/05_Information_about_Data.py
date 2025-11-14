import streamlit as st

st.set_page_config(page_title="Data", layout="wide")

st.title("Information about Data")

st.markdown("""## Election data

Source: http://www.german-elections.com/        
Heddesheimer, Vincent, Hanno Hilbig, Florian Sichart, & Andreas Wiedemann. 2025. GERDA: German Election Database. Nature: Scientific Data, 12: 618.         
            
## Unemployment data
Source: https://discord.com/channels/689122077504176142/1438091518232756264/1438808812562677860

## Income data

Source: https://www.regionalstatistik.de/genesis//online?operation=table&code=73111-01-01-4&bypass=true&levelindex=1&levelid=1763043942228#abreadcrumb          

**Notes**:   
Der dargestellte Gebietsstand entspricht dem Zeitpunkt nach Ende des Veranlagungszeitraumes von bis zu 2 ¾ Jahren. Für den Berichtszeitpunkt t liegt daher der Gebietsstand t+3 Jahre zugrunde.

Abweichungen in den Summen (Spalte 2 und 3) sind auf das Runden der Zahlen zurückzuführen.

zu "gesamter Tabelle":
Methodischer Hinweis zum Vergleich der Einkommensteuerstatistiken bis 2007: Die Ergebnisse der Lohn- und Einkommensteuerstatistiken sind ab 2004 mit den Ergebnissen früherer Jahre (2001, 1998 usw.) nur eingeschränkt vergleichbar, da bis 2001 lohnsteuer-
pflichtige Personen, die keine Einkommensteuerveranlagung durchführen ließen, nur insoweit in die Statistik einbezo- gen werden konnten, als deren Lohnsteuerkarten den Statistischen Landesämtern zur Auswertung zur Verfügung gestellt wurden. So waren im Ergebnisnachweis bis einschl. 2001 die Angaben von bundesweit lediglich etwa 1,87 Millionen sogenannten Nichtveranlagten enthalten. Nach der sukzessiven Einführung der vom Arbeitgeber an die Finanzverwaltung zu übermittelnden elektronischen Lohnsteuerbescheinigungen ab 2002 standen diese erstmals für das Statistikjahr 2004 zur Verfügung. Im Ergebnisnachweis der Lohn- und Einkommen-steuerstatistik 2004 sind so ca. 9,03 Millionen Lohnsteuer-pflichtige ohne Einkommensteuerveranlagung enthalten.
Nach dem Wegfall einiger Ausnahmetatbestände zur Übermittlungspflicht der elektronischen Lohnsteuerbescheinigungen werden ab dem Berichtsjahr 2007 nunmehr alle Nichtveranlagten in der Statistik berücksichtigt. Damit werden in der Lohn- und Einkommensteuerstatistik ab 2007 die veranlagten und nichtveranlagten Steuerpflichtigen vollständig nachgewiesen.           
 
Baden-Württemberg (Berichtsjahr 1995-2010): Gebietsstand 01.01.1979     
Baden-Württemberg (ab Berichtsjahr 2011): Gebietsstand 01.01.2011       
Brandenburg (1995): einschl. nachträglicher Korrekturen durch die Finanzämter des Landes Brandenburg""")
from OpenOrchestrator.orchestrator_connection.connection import OrchestratorConnection
from OpenOrchestrator.database.queues import QueueElement
import os
from datetime import datetime, timedelta
import locale
import pandas as pd
import pyodbc
import smtplib
from email.message import EmailMessage
import locale

# pylint: disable-next=unused-argument
def process(orchestrator_connection: OrchestratorConnection) -> None:
    orchestrator_connection.log_info('Starting process BBR-tal-bot ')

    # Sæt dansk lokalitet (virker kun hvis den er installeret i systemet)
    locale.setlocale(locale.LC_TIME, "da_DK.UTF-8")

    today = datetime.today()

    # Gå til første dag i denne måned og træk én dag fra → sidste dag i forrige måned
    first_of_this_month = today.replace(day=1)
    last_day_of_prev_month = first_of_this_month - timedelta(days=1)

    # Forrige måned som to-cifret streng (fx "04")
    måned = last_day_of_prev_month.strftime("%m")
    år = last_day_of_prev_month.strftime("%Y")
    forrige_maaned_navn = last_day_of_prev_month.strftime("%B")

    # Read the SQL query from file
    sql_file_path_bunken = "1. BBR - bunken.sql"
    sql_file_path_færdigbehandlede = "2. BBR - færdigbehandlede i perioden.sql"
    with open(sql_file_path_bunken, "r", encoding="utf-8") as file:
        query_bunken = file.read()
    with open(sql_file_path_færdigbehandlede, "r", encoding="utf-8") as file:
        query_færdigbehandlede = file.read()

    # Replace placeholders with actual date values, ensuring they are formatted correctly
    query_færdigbehandlede = query_færdigbehandlede.replace("@år", f"{år}").replace("@måned", f"{måned}")  # Add single quotes

    # Database connection setup
    sql_server = orchestrator_connection.get_constant("SqlServer").value
    conn_str = 'DRIVER={ODBC Driver 17 for SQL Server};' + f'SERVER={sql_server};DATABASE=LOIS;Trusted_Connection=yes'
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    #Getting bunken
    cursor.execute(query_bunken)
    rows_bunken = cursor.fetchall()
    data_bunken = pd.read_sql(query_bunken, conn)

    #Getting færdigbehandlede
    cursor.execute(query_færdigbehandlede)
    rows_færdigbehandlede = cursor.fetchall()
    data_færdigbehandlede = pd.read_sql(query_færdigbehandlede, conn)

    # Step 5: Close database connection
    cursor.close()
    conn.close() 

    bunke_tilladelser = data_bunken['Tilladelsessager'][0]
    bunke_afslutninger = data_bunken['Afslutningssager'][0]
    færdige_tilladelser = data_færdigbehandlede['Tilladelsessager'][0]
    færdige_afslutninger = data_færdigbehandlede['Afslutningssager'][0]

    # SMTP Configuration (from your provided details)
    SMTP_SERVER = "smtp.adm.aarhuskommune.dk"
    SMTP_PORT = 25
    SCREENSHOT_SENDER = "bbr-tal-bot@aarhus.dk"
    subject = "Nye tal fra BBR"

    html = f"""
    <html>
    <body>
        <p style="margin-bottom: 20px;">Hej Karina 👋</p>
        <p>Her kommer månedens BBR-tal:</p>

        <div style="margin-top: 20px;">
        <strong>Bunken</strong><br>
        Tilladelsessager: <strong>{bunke_tilladelser}</strong><br>
        Afslutningssager: <strong>{bunke_afslutninger}</strong>
        </div>

        <div style="margin-top: 20px;">
        <strong>Færdigbehandlet i {forrige_maaned_navn}</strong><br>
        Tilladelsessager: <strong>{færdige_tilladelser}</strong><br>
        Afslutningssager: <strong>{færdige_afslutninger}</strong>
        </div>

        <p style="margin-top: 40px;">Med venlig hilsen</p>
        <p> Laura </p>
    </body>
    </html>
    """


    # Create the email message
    UdviklerMail = orchestrator_connection.get_constant('balas').value
    ModtagerMail = orchestrator_connection.get_constant('bbrtalbotmails').value
    mail1 = ModtagerMail.split(', ')[0]
    mail2 = ModtagerMail.split(', ')[1]
    msg = EmailMessage()
    msg['To'] = mail1
    # msg['To'] = UdviklerMail
    msg['From'] = SCREENSHOT_SENDER
    msg['Subject'] = subject
    msg.set_content("Please enable HTML to view this message.")
    msg.add_alternative(html, subtype='html')
    msg['Reply-To'] = UdviklerMail
    msg['Cc'] = mail2
    msg['Bcc'] = UdviklerMail

    # Send the email using SMTP
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as smtp:
            smtp.send_message(msg)
    except Exception as e:
        orchestrator_connection.log_info(f"Failed to send success email: {e}")

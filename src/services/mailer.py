import win32com.client
import os

class Mailer:
    def __init__(self):
        pass

    def send_report(self, report_data, attachments):
        outlook = win32com.client.Dispatch("Outlook.Application")
        mail = outlook.CreateItem(0)  # 0: olMailItem
        
        # Displaying the mail first is the most reliable way to preserve 
        # the user's default signature in Outlook COM.
        mail.Display()
        
        mail.To = report_data.get('supervisor_email', '')
        mail.Subject = f"Reporte de Actividades - {report_data['employee_name']} - {report_data['date']}"
        
        # We use HTMLBody to keep formatting and the signature
        # We append our text BEFORE the existing body (which contains the signature)
        intro_text = f"""
        <p>Hola,</p>
        <p>Adjunto env&iacute;o mi reporte de actividades correspondiente al d&iacute;a {report_data['date']}.</p>
        <p><b>Resumen:</b><br>
        - Periodo de Pago: {report_data['pay_period']}<br>
        - Total de Horas: {report_data['total_hours']}</p>
        <p>Saludos cordiales,</p>
        """
        
        mail.HTMLBody = intro_text + mail.HTMLBody
        
        # Filter attachments: Only PDF
        for path in attachments:
            if os.path.exists(path) and path.lower().endswith('.pdf'):
                mail.Attachments.Add(path)
        
        # Send it automatically after displaying and composing
        mail.Send()

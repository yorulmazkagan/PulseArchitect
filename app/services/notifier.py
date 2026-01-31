import os
import aiosmtplib 
from email.message import EmailMessage

class PulseNotifier:
    def __init__(self):
        self.email_user = os.getenv("EMAIL_USER")
        self.email_pass = os.getenv("EMAIL_PASS")
        self.target_email = "user@example.com" 

    async def send_report_email(self, analysis_text: str, water: float, energy: float):
        try:
            msg = EmailMessage()
            msg["Subject"] = "🚀 PulseArchitect | CRITICAL RISK AND ESG REPORT"
            msg["From"] = self.email_user
            msg["To"] = self.target_email
            
            content = f"""
            >>> [SYSTEM NOTIFICATION]: PulseArchitect Sovereign AI is running.
            
            RISK ANALYSIS IDENTIFIED:
            --------------------------------------------------
            {analysis_text}
            
            RESOURCE OPTIMIZATION (ESG) DATAS:
            --------------------------------------------------
            💧 Spent Water: {water} Litre
            ⚡ Energy Spent: {energy} kWh
            
            [STATUS]: The risk has been ticketed and sealed in the Sovereign Database.
            -- Kağan Yorulmaz | PulseArchitect Core
            """
            msg.set_content(content)

            
            print(f"📧 [NOTIFIER]: Autonomous report email simulated!")
            return True
        except Exception as e:
            print(f"❌ Mail Error: {e}")
            return False
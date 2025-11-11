"""
Servicio para envío de emails con templates HTML estéticos.
Usa SMTP (Gmail, SendGrid, etc.)
"""
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class EmailService:
    
    @staticmethod
    def send_reservation_confirmation(reservation_data: dict, user_email: str) -> bool:
        """
        Envía email de confirmación de reserva con diseño estético.
        
        Args:
            reservation_data: Datos de la reserva
            user_email: Email del usuario
            
        Returns:
            bool: True si se envió correctamente
        """
        try:
            # Configuración SMTP desde variables de entorno
            smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
            smtp_port = int(os.getenv('SMTP_PORT', '587'))
            smtp_user = os.getenv('SMTP_USER')
            smtp_password = os.getenv('SMTP_PASSWORD')
            from_email = os.getenv('FROM_EMAIL', smtp_user)
            
            if not smtp_user or not smtp_password:
                logger.error("Credenciales SMTP no configuradas")
                return False
            
            # Crear mensaje
            msg = MIMEMultipart('alternative')
            msg['Subject'] = f"🎉 Confirmación de Reserva - {reservation_data['bar_name']}"
            msg['From'] = from_email
            msg['To'] = user_email
            
            # HTML del email
            html_content = EmailService._create_confirmation_html(reservation_data)
            
            # Adjuntar HTML
            html_part = MIMEText(html_content, 'html')
            msg.attach(html_part)
            
            # Enviar email
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(smtp_user, smtp_password)
                server.send_message(msg)
            
            logger.info(f"Email enviado a {user_email} para reserva {reservation_data['id']}")
            return True
            
        except Exception as e:
            logger.error(f"Error al enviar email: {str(e)}")
            return False
    
    @staticmethod
    def _create_confirmation_html(data: dict) -> str:
        """Crea el HTML estético para el email de confirmación."""
        
        return f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Confirmación de Reserva</title>
</head>
<body style="margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh;">
    <table width="100%" cellpadding="0" cellspacing="0" style="max-width: 600px; margin: 40px auto; background: white; border-radius: 20px; overflow: hidden; box-shadow: 0 20px 60px rgba(0,0,0,0.3);">
        <!-- Header con gradiente -->
        <tr>
            <td style="background: linear-gradient(135deg, #185ADB 0%, #0A2342 100%); padding: 40px 30px; text-align: center;">
                <h1 style="color: white; margin: 0; font-size: 32px; font-weight: bold; text-shadow: 0 2px 10px rgba(0,0,0,0.3);">
                    🎉 ¡Reserva Confirmada!
                </h1>
                <p style="color: #FFD93D; margin: 10px 0 0 0; font-size: 16px; font-weight: 500;">
                    Tu noche perfecta está lista
                </p>
            </td>
        </tr>
        
        <!-- Información del bar -->
        <tr>
            <td style="padding: 30px;">
                <div style="background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); border-radius: 15px; padding: 25px; margin-bottom: 25px;">
                    <h2 style="color: #0A2342; margin: 0 0 15px 0; font-size: 24px; font-weight: bold;">
                        {data['bar_name']}
                    </h2>
                    <p style="color: #555; margin: 5px 0; font-size: 15px;">
                        📍 {data['bar_address']}
                    </p>
                </div>
                
                <!-- Detalles de la reserva -->
                <table width="100%" cellpadding="0" cellspacing="0">
                    <tr>
                        <td style="padding: 12px 0; border-bottom: 1px solid #e0e0e0;">
                            <span style="color: #666; font-size: 14px;">👤 Nombre:</span>
                        </td>
                        <td style="padding: 12px 0; border-bottom: 1px solid #e0e0e0; text-align: right;">
                            <strong style="color: #0A2342; font-size: 15px;">{data['full_name']}</strong>
                        </td>
                    </tr>
                    <tr>
                        <td style="padding: 12px 0; border-bottom: 1px solid #e0e0e0;">
                            <span style="color: #666; font-size: 14px;">📅 Fecha:</span>
                        </td>
                        <td style="padding: 12px 0; border-bottom: 1px solid #e0e0e0; text-align: right;">
                            <strong style="color: #0A2342; font-size: 15px;">{data['reservation_date']}</strong>
                        </td>
                    </tr>
                    <tr>
                        <td style="padding: 12px 0; border-bottom: 1px solid #e0e0e0;">
                            <span style="color: #666; font-size: 14px;">🕐 Hora:</span>
                        </td>
                        <td style="padding: 12px 0; border-bottom: 1px solid #e0e0e0; text-align: right;">
                            <strong style="color: #0A2342; font-size: 15px;">{data['reservation_time']}</strong>
                        </td>
                    </tr>
                    <tr>
                        <td style="padding: 12px 0; border-bottom: 1px solid #e0e0e0;">
                            <span style="color: #666; font-size: 14px;">👥 Personas:</span>
                        </td>
                        <td style="padding: 12px 0; border-bottom: 1px solid #e0e0e0; text-align: right;">
                            <strong style="color: #0A2342; font-size: 15px;">{data['num_people']}</strong>
                        </td>
                    </tr>
                    <tr>
                        <td style="padding: 12px 0;">
                            <span style="color: #666; font-size: 14px;">📱 Teléfono:</span>
                        </td>
                        <td style="padding: 12px 0; text-align: right;">
                            <strong style="color: #0A2342; font-size: 15px;">{data['phone']}</strong>
                        </td>
                    </tr>
                </table>
                
                <!-- Código de reserva -->
                <div style="background: linear-gradient(135deg, #FFD93D 0%, #FFA500 100%); border-radius: 12px; padding: 20px; margin: 25px 0; text-align: center;">
                    <p style="color: #0A2342; margin: 0 0 8px 0; font-size: 13px; font-weight: 600; text-transform: uppercase; letter-spacing: 1px;">
                        Código de Reserva
                    </p>
                    <p style="color: #0A2342; margin: 0; font-size: 28px; font-weight: bold; letter-spacing: 2px;">
                        #{data['id']:06d}
                    </p>
                </div>
                
                <!-- Instrucciones -->
                <div style="background: #f8f9fa; border-left: 4px solid #185ADB; border-radius: 8px; padding: 15px; margin: 20px 0;">
                    <p style="color: #0A2342; margin: 0 0 10px 0; font-size: 14px; font-weight: 600;">
                        📋 Instrucciones:
                    </p>
                    <ul style="color: #555; margin: 0; padding-left: 20px; font-size: 13px; line-height: 1.6;">
                        <li>Llega 10 minutos antes de tu hora de reserva</li>
                        <li>Presenta este código al personal del bar</li>
                        <li>Si necesitas cancelar, hazlo con 24h de anticipación</li>
                    </ul>
                </div>
            </td>
        </tr>
        
        <!-- Footer -->
        <tr>
            <td style="background: #f8f9fa; padding: 25px 30px; text-align: center; border-top: 1px solid #e0e0e0;">
                <p style="color: #999; margin: 0 0 10px 0; font-size: 12px;">
                    ¿Necesitas ayuda? Contáctanos
                </p>
                <p style="color: #185ADB; margin: 0; font-size: 14px; font-weight: 600;">
                    support@partyfinder.com
                </p>
                <p style="color: #ccc; margin: 15px 0 0 0; font-size: 11px;">
                    © 2024 PartyFinder. Todos los derechos reservados.
                </p>
            </td>
        </tr>
    </table>
</body>
</html>
        """